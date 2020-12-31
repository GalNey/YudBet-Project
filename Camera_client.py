__author__ = "Gal Neystadt"

import cv2
import pickle
import socket
import tcp_by_size as tbs
import time
import datetime

fps = 20  # frames per second

sock = socket.socket()
ip = "127.0.0.1" # local host
port = 8000

log_path = "camera_client_log.txt"

log = False
def log_data(data):
    global log_path
    if log:

        with open(log_path, "a") as f:
            f.write("at: " + str(datetime.datetime.now()) + " | " + data + "\n")

sock.connect((ip, port))
log_data("Connected to manager")

tbs.send_with_size(sock, "im_camera_client".encode("utf8"))

cap = cv2.VideoCapture(0)

def main():
    cnt = 1

    while True:  # will continue to send frames until disconnect
        ret, frame = cap.read()

        if cv2.waitKey(1) == 27:
            break  # esc to quit

        if frame is None:
            print("Connect camera and restart the client")
            log_data("camera was disconnected")
            break

        try:
            tbs.send_with_size(sock, pickle.dumps(frame))
        except:
            print("Seems to be disconnected from manager")
            log_data("disconnected from manager")
            break

        #time.sleep(1 / fps)
        time.sleep(0.5)

        print (cnt)
        cnt += 1


    cap.release()

if __name__ == "__main__":
    main()