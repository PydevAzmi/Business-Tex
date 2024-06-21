# Strat Docker : Python + Kernal
FROM python:3.12-slim-bullseye

# ENV: Show Logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update Kernal + Install Dep
RUN apt-get update && apt-get -y install gcc libpq-dev

# Create Project Folder 
WORKDIR /code

# Copy Requirements
COPY requirements.txt /code/

# Install Requirements
RUN pip install -r requirements.txt

# Copy Project Code > Docker
COPY . /code/