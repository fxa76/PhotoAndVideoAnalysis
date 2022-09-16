FROM python:3.6-stretch

EXPOSE 6000

ADD ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod 664 insert_obj.py
CMD [ "python", "insert_obj.py" ]
