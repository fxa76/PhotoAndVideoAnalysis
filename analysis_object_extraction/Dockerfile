FROM python:3.6-stretch
RUN mkdir /pictures

RUN apt-get update && apt-get install -y libgl1-mesa-dev

EXPOSE 6000

#add yolo config files. to avoid long dowload at first analysis
ADD ./yolo_cfg /root/.cvlib/object_detection/yolo/yolov3

ADD ./app /app
WORKDIR /app

#RUN pip install
RUN pip install cmake
RUN pip install --default-timeout=100 -r requirements.txt



RUN chmod 664 extract_objects.py
CMD [ "python", "extract_objects.py" ]
