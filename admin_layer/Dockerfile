FROM python:3.10-buster

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install -y ffmpeg

RUN mkdir /pictures
RUN mkdir /pictures_work
RUN mkdir /pictures_inbox
ADD ./app /app

WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod 664 server_admin.py
CMD [ "python", "-u", "server_admin.py" ]
