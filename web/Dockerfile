# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.6

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# change the pip source
ADD pip.conf /etc/pip.conf

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

RUN mkdir app
WORKDIR /app
ADD . /app


