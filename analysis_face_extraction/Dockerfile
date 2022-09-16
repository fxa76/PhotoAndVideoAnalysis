FROM python:3.6-stretch
RUN mkdir /pictures
RUN mkdir /pictures_work
RUN apt-get update && apt-get install -y libgl1-mesa-dev

EXPOSE 6000

ADD ./app /app
WORKDIR /app

RUN pip install cmake
RUN pip install -r requirements.txt

RUN chmod 664 extract_face_v2.py
CMD [ "python", "extract_face_v2.py" ]
