import cv2
import pickle
import socket
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 9501
server_address = (TCP_IP, TCP_PORT)
i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP,TCP_PORT))
data = ''
payload_size = struct.calcsize("I")

while True:
	while len(data) < payload_size:
		data += sock.recv(4096)
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("I", packed_msg_size)[0]
	while len(data) < msg_size:
		data += sock.recv(4096)
	frame_data = data[:msg_size]
	data = data[msg_size:]
	if frame_data=='':
		break
	frame=pickle.loads(frame_data)
	print(i)
	i += 1
	
sock.close()
	