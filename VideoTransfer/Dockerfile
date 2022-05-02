FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN apt-get install -y --upgrade python3 python3-dev python3-pip libpcap-dev libpq-dev
RUN pip3 install --upgrade pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
ENV server .
WORKDIR /server/
ADD requirements.txt /server/
ADD ./src/ /server/
#ADD ./frames/ /server/
RUN pip3 install -r requirements.txt
RUN pip3 install -U flask-cors
RUN pip3 install --upgrade setuptools
WORKDIR /server/
CMD ["python3", "reciever.py"]