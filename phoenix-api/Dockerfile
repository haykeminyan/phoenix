# Pull base image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /phoenix/

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install psycopg2-binary && pip install -r requirements.txt

COPY . /phoenix/

EXPOSE 8000
