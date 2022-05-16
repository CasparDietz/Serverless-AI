# https://linuxtut.com/en/bd6c5c486b31e87db44b/
"""
Receive with json: 
⇒ Extract the desired data (base64-encoded text data) from json 
⇒ Decode base64-encoded text data and convert it to bytes 
⇒ Convert to _io.BytesIO so that it can be handled by Pillow 
⇒ You can get the original Pillow Image safely
"""
from flask import Flask, jsonify, request
from PIL import Image
import json
import base64
from io import BytesIO
import os
from waitress import serve

app = Flask(__name__)

@app.before_request
def before_request():
    return "[SERVER]"

@app.route("/", methods=["GET", "POST"])
def index():    
    json_data = request.get_json() #Get the POSTed json
    dict_data = json.loads(json_data) #Convert json to dictionary

    img = dict_data["img"] #Take out base64# str
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img) 
    #img.show()
    
    # Count the number of files in the folder 
    #count = len(os.listdir('src/FLASK_POST/RecievedFrames'))
    count = len(os.listdir('RecievedFrames'))
    
    # Save the image to the folder with the name of the number of files as the name
    img.save('RecievedFrames/' + str(count) + '.png')      
    img_shape = img.size #Appropriately process the acquired image
    
    text = dict_data["text"] + "fuga" #Properly process with the acquired text

    #Return the processing result to the client
    response = {
        "text":text,
        "img_shape":img_shape        
        }
    return jsonify(response)


"""
app.rout that allows the client to make GET requests to the server and receive the .png files from the RecievedFrames folder
"""
# @app.route("/recieve", methods=["GET", "POST"])
# def recieve():
#     img = Image.open('src/FLASK_POST/RecievedFrames/' + str(0) + '.png')
#     #Convert Pillow Image to bytes and then to base64
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     img_byte = buffered.getvalue() # bytes
#     img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes * not str

#     #It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
#     img_str = img_base64.decode('utf-8') # str

#     files = {
#         "text":"hogehoge",
#         "img":img_str
#         }
    
#     return json.dumps(files)



if __name__ == "__main__":
    app.debug = True
    #LOCALLY
    #app.run()
    #OPENFAAS
    #serve(app, host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port = 5000)