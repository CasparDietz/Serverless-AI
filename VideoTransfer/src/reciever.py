# https://learnopencv.com/reading-and-writing-videos-using-opencv/#read-video-from-file
# https://github.com/abhikesare9/live-streaming-with-opencv/blob/main/client.py
# https://medium.com/nerd-for-tech/live-streaming-using-opencv-c0ef28a5e497

import pickle
import socket
import struct
import cv2

HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen()
print('Socket now listening')

conn, addr = s.accept()
print('Connected with ' + addr[0] + ':' + str(addr[1]))

data = b'' # a bytes object
payload_size = struct.calcsize("L") # payload size is 4 bytes 

i = 0
while True:
    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096) # 4096 is the buffer size

    packed_msg_size = data[:payload_size]
    data = data[payload_size:] 
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    if data == b'':
        break

    # Extract frame
    frame = pickle.loads(frame_data)

    # Display
    #cv2.imshow('frame', frame)
    print('Frame ' + str(i))
    #cv2.waitKey(1)
    
    # Save frames in the frames folder
    cv2.imwrite('../frames/frame{}.jpg'.format(i), frame)
    i += 1
 
conn.close()
print('Revied ' + str(i) + ' frames')
print('Connection closed') 