'''
import cv2
import socket
import pickle
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                   socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    cv2.imshow("test", pickle.loads(data))


'''


'''
import socket
import numpy
import time
import cv2

UDP_IP="127.0.0.1"
UDP_PORT = 999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s=b""

while True:
      data, addr = sock.recvfrom(46080)
      s+= data
      #s = b''.join([s, data])
      if len(s) == (46080*20):
          frame = numpy.fromstring (s, dtype=numpy.uint8)
          frame = frame.reshape(480,640,3)
          cv2.imshow("frame",frame)

          s=""
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
'''

'''
import socket
import numpy
import time
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


s=b''

while True:

  data, addr = sock.recvfrom(46080)

  s += data

  if len(s) == (46080*20):

    frame = numpy.fromstring (s,dtype=numpy.uint8)
    frame = frame.reshape (480,640,3)

    cv2.imshow('frame',frame)

    s=b''

  if cv2.waitKey(1) & 0xFF == ord ('q'):
    break
    
'''

import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 1233)
buf = 512
width = 640
height = 480
code = b'start'
num_of_chunks = width * height * 3 / buf

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk, _ = s.recvfrom(buf)
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)

        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(height, width, 3)

        cv.imshow('recv', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()