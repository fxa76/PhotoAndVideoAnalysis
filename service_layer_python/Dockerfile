FROM python:3.6
RUN mkdir /pictures
COPY ./app /app
WORKDIR /app
RUN rm -rf /var/lib/apt/lists
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
RUN pip install -r requirements.txt
RUN chmod 664 server_api_python.py
CMD ["python" , "-u","server_api_python.py"]
