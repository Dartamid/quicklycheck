FROM python:3.12.3
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn quicklycheck.wsgi:application --bind 0.0.0.0:8000