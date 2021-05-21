FROM python:3.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PRODUCTION 1

RUN apk update && apk add postgresql-dev gcc python3-dev
RUN apk add musl-dev freetype libpng libjpeg-turbo freetype-dev libpng-dev libjpeg-turbo-dev
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "src.wsgi:application"]
