FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /ruleit_backend
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt