from python:3.6-stretch

RUN mkdir /pictures
RUN mkdir /pictures_work

EXPOSE 6000

ADD ./app /app
WORKDIR /app

#install python modules
RUN pip install -r requirements.txt
RUN chmod 664 analyzer_engine.py
CMD [ "python", "analyzer_engine.py" ]