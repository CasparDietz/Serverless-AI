"""
This script is used to send the frames (jpg) from one docker container to another docker container.
The recieving container will then use the frames to blur the faces.
"""
import cv2
import numpy as np
import socket
import pickle
import struct
import os

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))

for i in range(0,10):
    print('Frame ' + str(i))
    img = cv2.imread('../frames/frame{}.jpg'.format(i))
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    img_encode = cv2.imencode('.jpg', img)[1]
    data = pickle.dumps(img_encode)
    size = len(data)
    clientsocket.sendall(struct.pack("L", size) + data)
    
