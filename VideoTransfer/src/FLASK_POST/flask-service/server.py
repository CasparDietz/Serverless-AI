# https://linuxtut.com/en/bd6c5c486b31e87db44b/

#Forward ports with: kubectl port-forward -n openfaas svc/gateway 8080:8080
"""
Receive with json: 
⇒ Extract the desired data (base64-encoded text data) from json 
⇒ Decode base64-encoded text data and convert it to bytes 
⇒ Convert to _io.BytesIO so that it can be handled by Pillow 
⇒ You can get the original Pillow Image safely
"""
#from urllib import response
import cv2
from flask import Flask, jsonify, request
from PIL import Image
import json
import base64
from io import BytesIO
#import os
#from waitress import serve
#from pathlib import Path
from auto_blur_image import blurBoxes
from DetectorAPI import Detector

app = Flask(__name__)

"""
app.rout that receives the base64-encoded text data from the client.
The frames are blurred and the resulting image is sent back to the client.
"""
@app.route("/", methods=["GET", "POST"])
def main():    
    json_data = request.get_json() #Get the POSTed json
    dict_data = json.loads(json_data) #Convert json to dictionary

    img = dict_data["img"] #Take out base64# str
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img) 
    
    # Count the number of files in the folder 
    #count = len(os.listdir('src/FLASK_POST/RecievedFrames'))
    #count = len(os.listdir('RecievedFrames'))
    
    # Save the image to the folder with the name of the number of files as the name
    img.save('unblurred.png')   
    
    """
    Blur the image
    """
    # create detection object
    detector = Detector('face.pb', name="detection")
    # open image
    image = cv2.imread('unblurred.png')
    # real face detection
    faces = detector.detect_objects(image, threshold=0.4)
    print("Faces detected")
    # apply blurring
    image = blurBoxes(image, faces)
    print("Faces blurred")
    # Save the image
    cv2.imwrite('./blurred.png', image)

    """
    Prepare the image to be sent back to the client
    """
    img = Image.open('blurred.png')
    #Convert Pillow Image to bytes and then to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_byte = buffered.getvalue() # bytes
    img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes * not str

    #It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
    img_str = img_base64.decode('utf-8') # str

    response = {
        "text":"hogehoge",
        "img":img_str
        }
    return jsonify(response)

"""
app.rout that allows the client to make GET requests to the server and receive the .png files from the RecievedFrames folder
"""
@app.route("/recieve", methods=["GET", "POST"])
def recieve():
    img = Image.open('RecievedFrames/' + str(0) + '.png')
    #Convert Pillow Image to bytes and then to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_byte = buffered.getvalue() # bytes
    img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes * not str

    #It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
    img_str = img_base64.decode('utf-8') # str

    files = {
        "text":"This goes back to the client",
        "img":img_str
        }
    
    return json.dumps(files)



if __name__ == "__main__":
    app.debug = True
    #LOCALLY
    #app.run()
    #OPENFAAS
    #serve(app, host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port = 5000)