FROM python:3.8.5

WORKDIR /foodgram
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn foodgram.wsgi:application --bind 0:8000 
