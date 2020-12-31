'''
import cv2
import socket
import pickle
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

cap = cv2.VideoCapture(0)
while 1:
    ret, frame = cap.read()

    message_size = struct.pack("L", len(frame))

    sock.sendto(message_size + frame, (UDP_IP, UDP_PORT))


'''

'''
import socket
import numpy as np
import cv2
UDP_IP = '127.0.0.1'
UDP_PORT = 999
cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #cv2.imshow('frame',frame)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    d = frame.flatten ()
    s = d.tostring ()
    for i in range(20):
        sock.sendto (s[i*46080:(i+1)*46080],(UDP_IP, UDP_PORT))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
'''


'''
import socket
import numpy as np
import cv2

UDP_IP = '127.0.0.1'
UDP_PORT = 9999
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
def xrange(x):

  return iter(range(x))
while (True):
  ret, frame = cap.read()
  #cv2.imshow('frame', frame)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  d = frame.flatten()
  s = d.tostring()
  for i in xrange(20):
    sock.sendto(s[i * 46080:(i + 1) * 46080], (UDP_IP, UDP_PORT))
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()


'''

import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 1233)
buf = 512
width = 640
height = 480
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            s.sendto(code, addr)
            data = frame.tostring()
            for i in range(0, len(data), buf):
                s.sendto(data[i:i+buf], addr)
            # cv.imshow('send', frame)
            # if cv.waitKey(1) & 0xFF == ord('q'):
                # break
        else:
            break

