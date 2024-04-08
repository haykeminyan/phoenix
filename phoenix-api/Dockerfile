# Pull base image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Install dependencies
RUN pip install --upgrade pip
COPY phoenix-api/requirements.txt .
RUN pip install psycopg2-binary && pip install -r requirements.txt

COPY . .

EXPOSE 8000
