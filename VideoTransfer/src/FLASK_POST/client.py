"""
The transition of data (frames) is as follows:

Import an image as a Pillow Image 
⇒ Convert to bytes 
⇒ Encode with base64 (still bytes) 
⇒ Convert data that was bytes to str 
⇒ json .dumps to json 
⇒ You can safely POST with json
"""

from flask import request
import requests
from PIL import Image
import json
import base64
from io import BytesIO
import cv2
import os


"""
Video is taken as input and the frames are extracted
"""
def video_to_frames(video, path_output_dir):
    print("[CLIENT] Began cutting the video into frames")
    # extract frames from a video and save to directory as 'x.png' where 
    # x is the frame index
    vidcap = cv2.VideoCapture(video)
    count = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()
    print("[CLIENT] Finished cutting the video into frames")
    return count

count = video_to_frames('./VideoInput/test.mp4', './Frames') # count is the number of frames
print("[CLIENT] Read " + str(count) + " frames")      
      
"""
Send the frames to the server
""" 
for frame in range(count):
    # Read frame
    img = Image.open('./Frames/' + str(frame) + '.png')

    #Convert Pillow Image to bytes and then to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_byte = buffered.getvalue() # bytes
    img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes * not str

    #It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
    img_str = img_base64.decode('utf-8') # str

    files = {
        "text":"hogehoge",
        "img":img_str
        }

    #LOCALLY
    #r = requests.post("http://127.0.0.1:5000", json=json.dumps(files)) #POST to server as json
    
    #OPENFAAS
    r = requests.post("http://127.0.0.1:8080/function/flask-service", json=json.dumps(files)) #POST to server as json
    dict_data = r.json() #Convert json to dictionary
    img = dict_data["img"] #Take out base64# str
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img) 
    img.show() #Show the image
    print("[CLIENT] Received frame from the server")
    break

print("[CLIENT] >>>>>>>>>>>>> All frames were posted to the server <<<<<<<<<<<<<<<<")

"""
Get the frames from the server.
The client sends the GET request to the server and the server returns the frame.
The client receives the frame and saves it as a .png file.
"""
""" request = requests.get("http://127.0.0.1:8080/function/flask-service/recieve") #POST to server as json
#print(request.text)
dict_data = request.json() #Convert json to dictionary
img = dict_data["img"] #Take out base64# str
img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
img = Image.open(img) 
print("[CLIENT] Received frame from the server")
img.show() """