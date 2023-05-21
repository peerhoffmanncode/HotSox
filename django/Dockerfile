FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
# Install psycopg2 dependencies.
RUN apt-get update -y && apt-get install -y libpq-dev build-essential
# Install python dependencies.
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8000
