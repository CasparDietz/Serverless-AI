This folder contains the video reciever and sender.
To run the two, first run reciever.py in one terminal window and the run sender.py in another terminal window.

Frames are saved on the reciever side in the folder frames.

# Dockerizing the reciever
```bash
   docker build -t babakuranavideo . 
```

```bash
   docker run -p 8089:8089 babakuranavideo 
```

... Now you can send the video by running sender.py locally
```bash
python3 sender.py
```