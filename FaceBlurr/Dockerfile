FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN apt-get install -y --upgrade python3 python3-dev python3-pip libpcap-dev libpq-dev
RUN pip3 install --upgrade pip
ENV server .
WORKDIR /server/
ADD requirements.txt /server/
ADD ./src/ /server/
ADD ./face_model/ /server/ 
RUN pip3 install -r requirements.txt
RUN pip3 install -U flask-cors
RUN pip3 install --upgrade setuptools
WORKDIR /server/
#CMD ["python3", "auto_blur_image.py"]
CMD ["python3", "handler.py"]
# Can we use the follwing here?: python3 auto_blur_image.py --input_image ../inputs/input.jpg --output_image ../outputs/out.jpg  --model_path ../face_model/face.pb --threshold 0.4