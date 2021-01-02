# FROM python:3.8
FROM debian:buster

# update
RUN apt-get -y update

# install python
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# copy project files
COPY . /backend

# install dependencies
RUN pip3 install -r ./backend/requirements.txt

# set environment variables
# ENV FLASK_ENV=PRODUCTION
# for webdriver
# ENV PATH=$PATH:/backend/webdrivers

# install browser
RUN apt-get install -y ./backend/browser/chromium_83.0.4103.116-1_deb10u3_amd64.deb

# expose port
# EXPOSE 5000

# run with uwsgi application server
RUN pip3 install uwsgi
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "backend.app:app"]
