FROM python:3.10-buster
RUN apt-get update && apt-get install -y libgl1-mesa-dev

EXPOSE 6000

ADD ./app /app
WORKDIR /app

RUN pip install cmake
RUN pip install dlib==19.23.1
RUN pip install opencv-python-headless==4.10.0.84
RUN pip install face_recognition
RUN pip install pika
RUN pip install flask

RUN chmod 664 start.py
CMD [ "python", "start.py" ]