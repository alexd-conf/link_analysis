# FROM python:3.8
FROM debian:buster

WORKDIR /backend

# update
RUN apt-get -y update

# install python
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# copy project files
COPY ./backend/browser ./browser
COPY ./backend/config ./config
COPY ./backend/endpoints ./endpoints
COPY ./backend/logs ./logs
COPY ./backend/temp_downloads ./temp_downloads
COPY ./backend/webdrivers ./webdrivers
COPY ./backend/__init__.py .
COPY ./backend/app.py .
COPY ./backend/requirements.txt .

# install dependencies
RUN pip3 install -r ./requirements.txt

# install browser
RUN apt-get install -y chromium-common=83.0.4103.116-1~deb10u3
RUN apt-get install -y ./browser/chromium_83.0.4103.116-1_deb10u3_amd64.deb

# run with uwsgi application server
RUN pip3 install uwsgi
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "backend.app:app"]
