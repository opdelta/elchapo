FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install ffmpeg-python

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD [ "python3", "main.py"]
