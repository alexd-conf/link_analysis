# FROM python:3.8
FROM debian:buster

WORKDIR /backend

# update
RUN apt-get -y update

# install python
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# copy project files
COPY ./browser /browser
COPY ./config /config
COPY ./endpoints /endpoints
COPY ./logs /logs
COPY ./temp_downloads /temp_downloads
COPY ./webdrivers /webdrivers
COPY ./__init__.py .
COPY ./app.py .
COPY ./requirements.txt .

# install dependencies
RUN pip3 install -r ./requirements.txt

# install browser
RUN apt-get install -y chromium-common=83.0.4103.116-1~deb10u3
RUN apt-get install -y ./browser/chromium_83.0.4103.116-1_deb10u3_amd64.deb

# run with uwsgi application server
RUN pip3 install uwsgi
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "backend.app:app"]
