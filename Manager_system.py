__author__ = "Gal Neystadt"

import cv2
import pickle
import socket
import tcp_by_size as tbs
import os
import datetime
import pygame
import threading
import SQL_ORM
import predict
import shutil  # for free space checking
import ConvolutionalNN



threads = []
cameras = {}
acceptor_stop = False

client_video = False
client_conn = None
client_sock_to_send_frames = None
camera_to_send_conn = None

#start prediction part
LR = 1e-3 # Learning Rate 0.001
MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match
#end prediction part

ofhm = 2  # one of how many frames captured from each camera should go to recognition

space_amount_to_delete_old = 50  # how much free space should be when start to delete old photos (mega bytes)

path_of_database = 'Identified_photos.db'

srv_sock = socket.socket()
ip = "0.0.0.0"  # means local
port = 8000  # 0 means get random free port
srv_sock.bind((ip,port))
srv_sock.listen(20)  # the length of the TCP/IP stack but not yet accepted by the server

db_lock = threading.Lock()

log_path = "manager_log.txt"

log = False
def log_data(data):
    global log_path
    if log:

        with open(log_path, "a") as f:
            f.write("at: " + str(datetime.datetime.now()) + " | " + data + "\n")


def user_manager(conn, db):
    global acceptor_stop
    global client_video
    global camera_to_send_conn
    global client_conn
    global client_sock_to_send_frames

    global db_lock

    try:
        while not acceptor_stop:
            try:
                data = tbs.recv_by_size(conn).decode("utf8")
                if data == "" or data == None:
                    break
            except:
                print("client disconnected")
                break

            log_data("Message from user: %s" % (data[1:5]))

            if data[1:5] == "GPHX":  # get photo x
                if db:
                    path = db.get_photo_path_by_id(data[5:])
                    try:
                        picture = pygame.image.load(path[2:-3].replace("\\\\", "\\").replace(":", "-"))
                    except:
                        picture = pygame.image.load("path_problem.png")

                    data = pygame.image.tostring(picture, "RGB")

                    tbs.send_with_size(conn, ("MPHTX".encode("utf8")))
                    tbs.send_with_size(conn, (data))
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "CTPX":  # change text of photo x by id
                if db:
                    parts = data[5:].split("|")
                    data = ("MDSCD" + db.set_text_of_photo_by_id(parts[0], parts[1])).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "STOX":  # get text of photo x by id
                if db:
                    data = ("MTOFX" + db.get_photo_text_by_id(data[5:])).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "BKMX":  # bookmark photo x by id
                if db:
                    data = ("MDSCD" + db.bookmark_photo_by_id(data[5:])).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "UBMX":  # unbookmark photo x by id
                if db:
                    data = ("MDSCD" + db.unbookmark_photo_by_id(data[5:])).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "DELX":  # delete photo x by id
                if db:
                    data = ("MDSCD" + db.delete_photo_by_id(data[5:])).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "GLIP":  # get list of all identified photos
                if db:
                    data = ("MLOIP" + db.get_list_of_photos()).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "GLMP":  # get list of marked identified photos
                if db:
                    data = ("MLOMP" + db.get_list_of_bookmark_photos()).encode("utf8")
                    tbs.send_with_size(conn, data)
                else:
                    tbs.send_with_size(conn, "MNODB".encode("utf8"))

            elif data[1:5] == "GLCC":  # get list of connected cameras
                tbs.send_with_size(conn, ("MLOCC" + str(get_online_cameras())).encode('utf8'))

            elif data[1:5] == "GSOC":  # get video stream of camera x
                try:
                    camera_to_send_conn = cameras[(data[5:]).replace(" ", "")][1]

                    vid_sock = socket.socket()
                    ip = "0.0.0.0"  # means local
                    port = 9000  # 0 means get random free port
                    vid_sock.bind((ip, port))
                    vid_sock.listen(1)  # the length of the TCP/IP stack but not yet accepted by the server
                    (connection_, (client_ip, port)) = vid_sock.accept()

                    db_lock = threading.Lock()

                    client_sock_to_send_frames = connection_

                    client_video = True

                except KeyError:
                    print("Error with video stream")


            elif data[1:5] == "STSX":  # stop video stream
                client_video = False
                client_sock_to_send_frames.close()

    finally:
        log_data("User has disconnected")
        client_conn = None
        client_video = False


def is_enough_space(where_to_check):  # is there enough place on disk to save new image or need to delete the oldest one
    global space_amount_to_delete_old

    #total, used, free = shutil.disk_usage("/")  # for current folder

    #print("Total: %d MB" % (total // (2 ** 20)))
    #print("Used: %d MB" % (used // (2 ** 20)))
    #print("Free: %d MB" % (free // (2 ** 20)))

    total, used, free = shutil.disk_usage(where_to_check)

    free_space = free // (2 ** 20)

    if free_space > space_amount_to_delete_old:
        return True
    else:
        log_data("Free disk space seems missing")
        return False

save_image = True  # for debug purpose
def image_recognizer(frame, model, db, id, name):
    if not is_enough_space("ident_phts"):
        path_to_delete = (db.get_photo_lowest_id())[2:-3]

        os.remove(path_to_delete)


    cv2.imwrite("tmp.jpg", frame)

    img = cv2.imread("tmp.jpg", cv2.IMREAD_GRAYSCALE)
    sized_frame = (cv2.resize(img, (50,50)))

    reco = False  # for debug
    if reco:
        if predict.predict(sized_frame, model=model) == "Cat":
            reco_time = str(datetime.datetime.now())[:-3]

            path = "ident_phts\\" + reco_time + ".jpg"

            if save_image and db != None:
                cv2.imwrite(path.replace(":", "-"), frame)
                with db_lock:
                    db.add_photo(path, reco_time.replace(":", "-"), id, name, False, reco_time)

            log_data("A cat was recognized in a picture")
            print("cat photo saved \n")


def camera_client_manager(conn,id,name,db):  # thread which will manage single camera client connection to manager system
    global acceptor_stop

    global client_video
    global client_conn
    global camera_to_send_conn

    global threads
    global cameras

    global client_sock_to_send_frames

    cameras[name] = (id, conn)  # add camera to online cameras list

    will_go_to_reco = 1  # not every frame should go to recognition

    #reco_model = predict.CreateModel()
    reco_model = ConvolutionalNN.CreateModel()
    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        reco_model.load(MODEL_NAME)

    try:

        while not acceptor_stop:
            try:
                data = tbs.recv_by_size(conn)
            except:
                print("camera disconnected")
                break
            if data != "":
                will_go_to_reco = (will_go_to_reco + 1) % ofhm  # one of how many

                if will_go_to_reco:
                    #send for recognition

                    try:
                        frame = pickle.loads(data)
                    except TypeError:
                        break

                    t = threading.Thread(target=image_recognizer, args=(frame,reco_model,db, id, name))
                    t.start()
                    threads.append(t)

                #send if needed to client
                if client_video:
                    if camera_to_send_conn == conn and data and client_conn:
                        tbs.send_with_size(client_sock_to_send_frames, data)

            else:
                break
        print ("acceptor_stop")
    finally:
        log_data("Camera client with the name: '%s' has disconnected" % (name))
        del cameras[name]

def acceptor(srv_sock): # a thread that will be accepting all new connections
    global acceptor_stop
    global threads
    global client_conn

    if os.path.isfile(path_of_database):
        db = SQL_ORM.Identified_ObjectsORM(path_of_database)
    else:
        db = None

    while not acceptor_stop:
        (conn, (client_ip, port)) = srv_sock.accept()

        msg = tbs.recv_by_size(conn).decode("utf8")
        if msg == "im_camera_client":
            with open("approved_cameras.txt", 'r') as f:
                data = f.read().split("\n")
            is_found = False
            for i in data:
                parts = i.split("_")
                if client_ip in parts:
                    t = threading.Thread(target=camera_client_manager, args=(conn,parts[1],parts[2],db))  # socket, id, name
                    t.start()
                    threads.append(t)
                    log_data("Camera client with ip '%s' has connected" % (str(client_ip)))
                    is_found = True
            if not is_found:
                log_data("Unauthorised Camera client with ip '%s' has tried to connect" % (str(client_ip)))
                print("Not approved camera ip")

        elif msg == "im_user":
            if not client_conn:  # only one client connected at all times
                with open("approved_user.txt", 'r') as f:
                    data = f.readlines()
                if client_ip in data:
                    client_conn = conn
                    t = threading.Thread(target=user_manager, args=(conn,db))
                    t.start()
                    threads.append(t)
                    log_data("User with ip '%s' has connected" % (str(client_ip)))
                else:
                    log_data("Unauthorised user with ip '%s' has tried to connect" % (str(client_ip)))
                    print("Not approved user ip")
        else:
            log_data("Unknown entity with ip '%s' has tried to connect" % (str(client_ip)))


def get_online_cameras():  # will give list of connected cameras
    global cameras

    return list(cameras.keys())


def main():
    try:
        global threads

        accepter_thread = threading.Thread(target=acceptor, args=(srv_sock,))
        accepter_thread.start()
        threads.append(accepter_thread)

        for i in threads:
            i.join()

    except:
        print("Error accured")


if __name__ == "__main__":
    main()

