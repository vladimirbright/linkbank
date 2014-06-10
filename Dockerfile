FROM ubuntu:14.04
MAINTAINER Vladimir Prokhoda <vladimirbright@gmail.com>
USER root
RUN apt-get -qq update
RUN apt-get -qq upgrade
RUN locale-gen ru_RU.UTF-8
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=ru_RU.UTF-8 LC_ALL=ru_RU.UTF-8

RUN apt-get install -qqy python2.7 python2.7-dev \
			 	python2.7-psycopg2 \
			 	subversion ipython \
			 	python-pip \
				python-lxml
# Pillow dependencies
RUN apt-get install -qqy libjpeg-dev libpng12-dev libtiff5-dev libfreetype6-dev \
				libwebp-dev liblcms2-dev
# Python unverified dependencies
RUN pip install --allow-external=elementtree --allow-unverified=elementtree elementtree

ADD . /opt/src/

RUN pip install -r /opt/src/pip.recv.txt

ENV PYTHONPATH /opt/src/
ENV DJANGO_SETTINGS_MODULE settings_docker

CMD ["help"]
ENTRYPOINT ["django-admin.py"]
