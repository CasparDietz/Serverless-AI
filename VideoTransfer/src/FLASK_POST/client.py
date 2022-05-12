"""
The transition of data (frames) is as follows:

Import an image as a Pillow Image 
⇒ Convert to bytes 
⇒ Encode with base64 (still bytes) 
⇒ Convert data that was bytes to str 
⇒ json .dumps to json 
⇒ You can safely POST with json
"""

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
    return count

count = video_to_frames('./VideoInput/test.mp4', './Frames') # count is the number of frames

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

    r = requests.post("http://127.0.0.1:5000", json=json.dumps(files)) #POST to server as json

    print(r.json())
