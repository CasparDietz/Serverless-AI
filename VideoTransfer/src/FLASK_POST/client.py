"""
The transition of data (frames) is as follows:

Import an image as a Pillow Image 
⇒ Convert to bytes 
⇒ Encode with base64 (still bytes) 
⇒ Convert data that was bytes to str 
⇒ json .dumps to json 
⇒ You can safely POST with json
"""

from fileinput import filename
import re
from flask import request
import requests
from PIL import Image
import json
import base64
from io import BytesIO
import cv2
import os
import time

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
            #img_rotate_180 = cv2.rotate(image, cv2.ROTATE_180)
            #cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, img_rotate_180)
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
        "text":"client",
        "img":img_str
        }

    #LOCALLY
    #r = requests.post("http://127.0.0.1:5000", json=json.dumps(files)) #POST to server as json
    
    #OPENFAAS
    #r = requests.post("http://127.0.0.1:8080/function/flask-service", json=json.dumps(files)) #POST to server as json
    #r = requests.post("http://127.0.0.1:8080/function/slblur", json=json.dumps(files)) #POST to server as json
    r = requests.post("http://127.0.0.1:8080/function/slblur", data = img_str) 
    
    # Extract the image string after "'img': " and before "}" => This has tobe done because the watchdog returns every warning and print
    for line in r.text.splitlines():
        if "img" in line:
            img_str = re.search("'img': '(.*)'}", line).group(1)
            break
    
    img = base64.b64decode(img_str) 
    img = BytesIO(img) 
    img = Image.open(img) 
    img.show() #Show the image
    filename = "./BlurredFrames/" + str(frame) + ".png"
    img.save(filename) #Save the image)   
    print("[CLIENT] Received frame from the server")
    #break

print("[CLIENT] All frames were posted to the server")
ts = time.time()
print("[CLIENT] Finished at " + str(ts))