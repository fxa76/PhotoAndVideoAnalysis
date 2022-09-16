from python:3.6-stretch
#install ffmpeg
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN apt-get install -y frei0r-plugins


RUN mkdir /tmp/data

EXPOSE 6000

ADD ./app /app
WORKDIR /app

#install python modules
RUN pip install -r requirements.txt
RUN chmod 664 extract_speech_to_text.py
CMD [ "python", "extract_speech_to_text.py" ]