import cv2
import numpy as np
import socket
#import sys
import pickle
import struct

cap=cv2.VideoCapture('../videos/sample2.mp4')
#cap=cv2.VideoCapture('videos/sample-video.mp4')
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))


if (cap.isOpened() == False):
	print("Error opening the video file")
# Read fps and frame count
else:
	# Get frame rate information
	fps = cap.get(5)
	print('Frames per second : ', fps,'FPS')

	# Get frame count
	frame_count = cap.get(7)
	print('Frame count : ', frame_count)
    
while cap.isOpened():
    ret,frame=cap.read()
    if ret == True:
        # Serialize frame
        data = pickle.dumps(frame)

        # Send message length first
        message_size = struct.pack("L", len(data))

        # Then data
        clientsocket.sendall(message_size + data)
        print('Frame sent')
    else:
        # When the last frame is reached, send a message to the server to close the connection
        data = pickle.dumps(int(0))
        message_size = struct.pack("L", len(data))
        clientsocket.sendall(message_size + data)
        break

cap.release()