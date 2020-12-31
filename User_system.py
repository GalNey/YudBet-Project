__author__ = "Gal Neystadt"



import socket
from graphic_part import *
import tcp_by_size as tbs
import os
import pygame
import threading
import cv2
import pickle
import time
import datetime
import func_timeout
from func_timeout import func_set_timeout

window_width = 720
window_height = 540

chunk = 9  # length of list of picture which is presented in one page

threads = []
show_video = False

log_path = "user_log.txt"

log = False
def log_data(data):
    global log_path
    if log:
        with open(log_path, "a") as f:
            f.write("at: " + str(datetime.datetime.now()) + " | " + data + "\n")


def get_online_cameras(sock):  # gets list of connected cameras by asking the manager_system

    tbs.send_with_size(sock, "UGLCC".encode("utf8"))  # get list of connected cameras

    '''
    logic: frame decode = crash, normal msg decode = data
    will keep crash until answer sent
    '''
    data = tbs.recv_by_size(sock)  # will get camera list as needed

    if data != "" and data != None:
        data = data.decode("utf8")
    else:
        return "err"

    if data[1:5] == "LOCC":
        to_return = data[5:].replace("[", "").replace("]", "").replace("\\","").replace("'","").split(",")  # gets list containing names as strings
        if to_return == ['']:
            to_return = []
        return to_return
    else:
        return "err"


def get_list_of_photos_from_manager(which, sock):  # gets different lists of photos from the manager system via socket

    if which == "BM":
        tbs.send_with_size(sock, "UGLMP".encode("UTF8"))

        data = tbs.recv_by_size(sock)
        if not data:
            return -1
        else:
            data = data.decode("utf8")

        if data[1:5] == "LOMP":
            return data[5:]
    else:
        tbs.send_with_size(sock, "UGLIP".encode("UTF8"))

        data = tbs.recv_by_size(sock)
        if not data:
            return -1
        else:
            data = data.decode("utf8")

        if data[1:5] == "LOIP":
            return data[5:]
        elif data[1:5] == "NODB":
            return "NODB"

    return -1


def photos_by_mark(sock, mark, which="all", give_sorted=False):  # gives partial list from list of all photos by part number (gets full list by asking of manager_system
    global chunk

    lst = get_list_of_photos_from_manager(which, sock)

    if lst == "NODB":
        return "NODB"

    sorted_data = lst[1:].replace("\\", "").replace("'", "").replace(",", "").replace(")", "").split("(")

    if give_sorted:
        return sorted_data

    #if mark

    return sorted_data[chunk * (mark - 1) : chunk * (mark - 1) + chunk], get_len_round_up(sorted_data, chunk)


def get_len_round_up(lst, part):  # returns the amount of parts for the slicing of the list by the part length
    num = len(lst) / part
    if num > int(num):
        num = int(num + 1)

    return num


def get_bigger_if_can(lst, num, changing_num):  # gets number and raise it if not above the amount of parts
    if changing_num < get_len_round_up(lst, num):
        return changing_num + 1
    return changing_num


def delete_picture_by_id(sock, id):  # deletes photo by id
    tbs.send_with_size(sock, ("UDELX"+id).encode("utf8"))

    ans = tbs.recv_by_size(sock)
    if not ans:
        return -1
    else:
        ans = ans.decode("utf8")

    if ans[1:5] == "DSCD":
        return ans[5:]
    elif ans[1:5] == "NODB":
        return "No database connected"


def bookmark_picture_by_id(sock, id):  # bookmarks photo by id
    tbs.send_with_size(sock, ("UBKMX"+id).encode("utf8"))

    ans = tbs.recv_by_size(sock)
    if not ans:
        return -1
    else:
        ans = ans.decode("utf8")

    if ans[1:5] == "DSCD":
        return ans[5:]
    elif ans[1:5] == "NODB":
        return "No database connected"


def unbookmark_picture_by_id(sock, id):  # unbookmarks photo by id
    tbs.send_with_size(sock, ("UUBMX" + id).encode("utf8"))

    ans = tbs.recv_by_size(sock)
    if not ans:
        return -1
    else:
        ans = ans.decode("utf8")

    if ans[1:5] == "DSCD":
        return ans[5:]
    elif ans[1:5] == "NODB":
        return "No database connected"


def get_txt_by_id(sock, id):  # gets text of photo by id
    tbs.send_with_size(sock, ("USTOX" + id).encode("utf8"))

    ans = tbs.recv_by_size(sock)
    if not ans:
        return -1
    else:
        ans = ans.decode("utf8")

    if ans[1:5] == "TOFX":
        return ans[5:]
    elif ans[1:5] == "NODB":
        return "No database connected"


def set_txt_by_id(sock, id, text):  # sets text of photo by id
    tbs.send_with_size(sock, ("UCTPX" + id + "|" + text).encode("utf8"))

    ans = tbs.recv_by_size(sock)
    if not ans:
        return -1
    else:
        ans = ans.decode("utf8")

    if ans[1:5] == "DSCD":
        return ans[5:]
    elif ans[1:5] == "NODB":
        return "No database connected"


def get_picture_by_id(sock, id):  # gets picture object after pickle from manager
    tbs.send_with_size(sock, ("UGPHX" + id).encode("utf8"))

    ans = tbs.recv_by_size(sock)
    if not ans:
        return -1
    else:
        ans = ans.decode("utf8")

    if ans[1:5] == "PHTX":
        ans = tbs.recv_by_size(sock)
        return ans

    return -1


@func_set_timeout(4)  # should be 4
def get_one_frame(sock):  # receive one frame part from manager with timeout

    frame = tbs.recv_by_size(sock)

    if not frame:
        return -1

    return frame

def live_video_manage(camera_name):  # thread that will manage the communication while in live video
    global port
    global show_video
    global location

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip = "192.168.99.49"  # local host
    ip = "127.0.0.1"
    port = 9000
    time.sleep(1)
    sock.connect((ip, port))

    no_frame_recieved = 0

    while show_video:

        try:
            frame = get_one_frame(sock)

            no_frame_recieved = 0


            try:
                cv2.imshow(camera_name, pickle.loads(frame))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except TypeError:
                break
            except:

                print("Error with showing frame")

        except func_timeout.exceptions.FunctionTimedOut:
            print("no frame received")

            if no_frame_recieved > 0:
                location = "mid_video_camera_dc"
                break
            else:
                no_frame_recieved += 1


    cv2.destroyAllWindows()
    sock.close()

location = "main"
def main():
    global threads
    global show_video
    global location

    sock = socket.socket()
    #ip = "192.168.99.49"  # local host
    ip = "127.0.0.1"
    port = 8000
    sock.connect((ip, port))
    log_data("Connected to manager")

    tbs.send_with_size(sock, "im_user".encode('utf8'))

    os.environ['SDL_VIDEO_CENTERED'] = "True"
    pygame.init()
    size = (window_width, window_height)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Security Agent")
    icon = pygame.image.load('detective.png')
    pygame.display.set_icon(icon)

    """
    locations meanings :

    1.  main: choose watch live or see picture
    2.  choose_live_camera: user chooses which camera to see live 
    3.  choosing_live_camera: currently user is looking at connected camera list  
    4.  live_video: live video of one of the cameras is currently presented
    5.  mid_video_camera_dc: while in live video camera is disconnected
    6.  build_choose_photo: building the screen in which photo can be chosen
    7.  no_database: no database connected to manager hence o photos can be observed 
    8.  choose_photo: user chooses which photo to see
    9.  choosing_photo: currently user is looking at photos list  
    10. on_picture: currently showing data on certain picture
    11. on_picture_full: full screen of a picture
    12. see_text: free text of a photo is shown to the user
    13. edit_text: user can edit the free text

    """

    try:
        location = "main"
        finish = False
        while not finish:
            time.sleep(0.02)  # not too fast hovering of the loop (as the sleep gets longer- longer delay on pressing on buttons until action

            pygame.display.flip()

            if location == "main":
                watch_live, see_picture, _exit = build_main_screen(screen)
                location = "main_"
            elif location == "choose_live_camera":
                back, cameras, refresh = build_watch_live(screen, get_online_cameras(sock))
                location = "choosing_live_camera"
            elif location == "no_database":
                back = no_database(screen)
            elif location == "build_choose_photo":
                photos_location_mark = 1
                which_lst_now = "all"
                pbm = photos_by_mark(sock, photos_location_mark)
                if pbm == "NODB":
                    location = "no_database"
                else:
                    photos, back, next_, previous, see_bm, see_all = build_photo_list(screen, pbm, photos_location_mark)
                    see_all.set_bg_color((160,0,0))
                    location = "choosing_photo"
            elif location == "mid_video_camera_dc":
                back = mid_video_camera_dc(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                    break
                elif event.type == pygame.MOUSEBUTTONUP:

                    press = pygame.mouse.get_pos()

                    if location == "main_":
                        if watch_live.is_clicked(press):
                            location = "choose_live_camera"
                            log_data("Watch live camera was pressed while in: %s" % (location))
                        elif see_picture.is_clicked(press):
                            location = "build_choose_photo"
                            log_data("See photos was pressed while in: %s" % (location))
                        elif _exit.is_clicked(press):
                            finish = True
                            log_data("Exit was pressed while in: %s" % (location))
                            break

                    elif location == "no_database":
                        if back.is_clicked(press):
                            log_data("Back was pressed while in: %s" % (location))

                            location = "main"

                    elif location == "choosing_live_camera":
                        if back.is_clicked(press):
                            log_data("back was pressed while in: %s" % (location))

                            location = "main"
                        elif refresh.is_clicked(press):
                            location = "choose_live_camera"
                            log_data("Refresh was pressed while in: %s" % (location))
                        else:
                            for i in cameras:
                                if i.is_clicked(press):
                                    show_video = True
                                    name = i.get_text()

                                    tbs.send_with_size(sock, ("UGSOC" + name).encode("utf8"))

                                    t = threading.Thread(target=live_video_manage, args=(name,))
                                    t.start()
                                    threads.append(t)

                                    back = build_back_screen(screen)
                                    # start video broadcast of camera i

                                    location = "live_video"
                                    log_data("Camera with name of: %s, Was chosen to watch live video" % (name))

                                    break

                    elif location == "live_video" or location == "mid_video_camera_dc":
                        if back.is_clicked(press):
                            show_video = False
                            tbs.send_with_size(sock, ("USTSX").encode("utf8"))

                            log_data("Back was pressed while in: %s" % (location))

                            location = "choose_live_camera"

                    elif location == "choosing_photo":
                        if back.is_clicked(press):
                            log_data("Back was pressed while in: %s" % (location))

                            location = "main"
                        elif next_.is_clicked(press):
                            log_data("Next was pressed while in: %s" % (location))

                            global chunk

                            pbm = photos_by_mark(sock, photos_location_mark, which_lst_now, give_sorted=True)
                            if pbm == "NODB":
                                location = "no_database"
                                log_data("Seems that no database is connected from manager")
                            else:
                                photos_location_mark_tmp = get_bigger_if_can(pbm, chunk, photos_location_mark)
                                if photos_location_mark < photos_location_mark_tmp:
                                    photos_location_mark = photos_location_mark_tmp
                                    if which_lst_now == "all":
                                        pbm = photos_by_mark(sock, photos_location_mark)
                                        if pbm == "NODB":
                                            location = "no_database"
                                        else:
                                            photos, back, next_, previous, see_bm, see_all = build_photo_list(screen, pbm, photos_location_mark)
                                            see_all.set_bg_color((160, 0, 0))
                                            see_bm.set_bg_color((0, 0, 0))

                                    else:
                                        pbm =  photos_by_mark(sock, photos_location_mark, which="BM")
                                        if pbm == "NODB":
                                            location = "no_database"
                                        else:
                                            photos, back, next_, previous, see_bm, see_all = build_photo_list(screen,pbm, photos_location_mark)
                                            see_all.set_bg_color((0, 0, 0))
                                            see_bm.set_bg_color((160, 0, 0))

                        elif previous.is_clicked(press):
                            log_data("Previous was pressed while in: %s" % (location))
                            if photos_location_mark > 1:
                                photos_location_mark -= 1
                                if which_lst_now == "all":
                                    pbm = photos_by_mark(sock, photos_location_mark)
                                    if pbm == "NODB":
                                        location = "no_database"
                                    else:
                                        photos, back, next_, previous, see_bm, see_all = build_photo_list(screen, pbm, photos_location_mark)
                                        see_all.set_bg_color((160, 0, 0))
                                        see_bm.set_bg_color((0, 0, 0))

                                else:
                                    pbm = photos_by_mark(sock, photos_location_mark, which="BM")
                                    if pbm == "NODB":
                                        location = "no_database"
                                    else:
                                        photos, back, next_, previous, see_bm, see_all = build_photo_list(screen, pbm, photos_location_mark)
                                        see_all.set_bg_color((0, 0, 0))
                                        see_bm.set_bg_color((160, 0, 0))

                        elif see_bm.is_clicked(press):
                            log_data("See bookmarked was pressed while in: %s" % (location))

                            which_lst_now = "BM"
                            photos_location_mark = 1

                            pbm = photos_by_mark(sock, photos_location_mark, which="BM")
                            if pbm == "NODB":
                                location = "no_database"
                            else:
                                photos, back, next_, previous, see_bm, see_all = build_photo_list(screen, pbm, photos_location_mark)
                                see_all.set_bg_color((0, 0, 0))
                                see_bm.set_bg_color((160, 0, 0))
                        elif see_all.is_clicked(press):
                            log_data("See all was pressed while in: %s" % (location))

                            which_lst_now = "all"
                            photos_location_mark = 1

                            pbm = photos_by_mark(sock, photos_location_mark)
                            if pbm == "NODB":
                                location = "no_database"
                            else:
                                photos, back, next_, previous, see_bm, see_all = build_photo_list(screen, pbm, photos_location_mark)
                                see_all.set_bg_color((160, 0, 0))
                                see_bm.set_bg_color((0, 0, 0))

                        else:
                            for i in photos:
                                if i.is_clicked(press):
                                    id_tmp = i.get_text().split(" ")[0]

                                    log_data("Photo with id: %s was chosen" % (id_tmp))

                                    seeP, dele, bookMark, unbookMark, gtxt, stxt, back = build_options_for_photo(screen, i.get_text(), get_picture_by_id(sock, id_tmp))

                                    location = "on_picture"

                    elif location == "on_picture":
                        if seeP.is_clicked(press):
                            back = build_back_screen_with_photo(screen, get_picture_by_id(sock, id_tmp))
                            location = "on_picture_full"
                            log_data("See in full screen was pressed while in: %s" % (location))
                        elif dele.is_clicked(press):
                            delete_picture_by_id(sock,id_tmp)
                            location = "build_choose_photo"
                            log_data("Delete was pressed while in: %s" % (location))
                        elif bookMark.is_clicked(press):
                            bookmark_picture_by_id(sock,id_tmp)
                            log_data("Bookmark was pressed while in: %s" % (location))
                        elif unbookMark.is_clicked(press):
                            unbookmark_picture_by_id(sock,id_tmp)
                            log_data("Unbookamek was pressed while in: %s" % (location))
                        elif gtxt.is_clicked(press):
                            txt = get_txt_by_id(sock,id_tmp)[2:-3]  # deletes opening and closer of how the text get delivered
                            back = build_show_text(screen,txt)
                            location = "see_text"
                            log_data("Get text was pressed while in: %s" % (location))
                        elif stxt.is_clicked(press):
                            txt = (get_txt_by_id(sock, id_tmp))[2:-3]
                            if txt == "":
                                txt = "No Current Text"
                            writer, back = build_get_text(screen, txt)
                            location = "edit_text"
                            log_data("Edit text was pressed while in: %s" % (location))
                        elif back.is_clicked(press):
                            log_data("Back was pressed while in: %s" % (location))

                            location = "build_choose_photo"

                    elif location == "on_picture_full" or location == "edit_text" or location == "see_text":
                        if back.is_clicked(press):
                            seeP, dele, bookMark, unbookMark, gtxt, stxt, back = build_options_for_photo(screen,i.get_text(),get_picture_by_id(sock, id_tmp))
                            log_data("Back was pressed while in: %s" % (location))
                            location = "on_picture"

                elif event.type == pygame.KEYDOWN:
                    if location == "edit_text":
                        if event.key == pygame.K_BACKSPACE:
                            writer.set_text(writer.get_text()[:len(writer.get_text()) - 1])  # deletes last char in string
                        elif event.key == pygame.K_SPACE:
                            writer.set_text(writer.get_text() + " ")
                        elif pygame.key.name(event.key) in "0123456789.,abcdefghijklmnopqrstuvwxyz":  # "abcdefghijklmnopqrstuvwxyz":
                            writer.set_text(writer.get_text() + pygame.key.name(event.key))

                        writer.draw_button()

                        if event.key == pygame.K_RETURN:
                            new_txt = writer.get_text()
                            set_txt_by_id(sock, id_tmp, new_txt)
                            log_data("Set the text of photo %s to be: %s" % (id_tmp, new_txt))

                            seeP, dele, bookMark, unbookMark, gtxt, stxt, back = build_options_for_photo(screen,i.get_text(),get_picture_by_id(sock, id_tmp))

                            location = "on_picture"


        reset_bg(screen)


    except ConnectionResetError:
        print("seems to be disconnected from manager")
        log_data("Disconnected manager")

        dc_from_manager(screen)
        pygame.display.flip()

        while not finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                    break
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN:
                    finish = True
                    break
            time.sleep(0.02)

    except TypeError as e:
    #except Exception as e:
        print("Error seems to accure:")
        print(str(e))


if __name__ == "__main__":
    main()





