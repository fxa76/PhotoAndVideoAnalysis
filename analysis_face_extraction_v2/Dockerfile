from analysis_engine:v1

RUN apt-get update && apt-get install -y libgl1-mesa-dev

ADD ./app/specific_requirements.txt /app
ADD ./app/fx_analyzer.py /app

WORKDIR /app

RUN pip install cmake
#install python modules
RUN pip install -r specific_requirements.txt


RUN chmod 664 analyzer_engine.py
CMD [ "python", "analyzer_engine.py" ]