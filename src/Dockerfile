FROM python:3.12.3
WORKDIR /code
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD which gunicorn
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate
CMD gunicorn quicklycheck.wsgi:application --bind 0.0.0.0:8000
EXPOSE 8000