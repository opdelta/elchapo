FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install -y git
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install ffmpeg-python
RUN pip3 install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
COPY . .


CMD [ "python3", "main.py"]
