FROM python:3.7.9-buster
RUN mkdir /pictures
RUN mkdir /pictures_work
RUN apt-get update && apt-get -y install tesseract-ocr
RUN apt-get update && apt-get install -y libgl1-mesa-dev

EXPOSE 6000


ADD ./app /app
WORKDIR /app

RUN pip install cmake
RUN pip install -r requirements.txt

RUN chmod 664 extract_text.py
CMD [ "python","-u", "extract_text.py" ]
