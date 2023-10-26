FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /app

#copying requirements.txt
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV FLASK_APP = app.py

#RUn Flask app

CMD ["flask","run", "--host", "0.0.0.0"]