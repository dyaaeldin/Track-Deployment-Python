FROM python:3.9
MAINTAINER Dyaa
WORKDIR /dtracker
COPY dtracker.py requirements.yml ./
RUN pip install -r requirements.yml
CMD python dtracker.py