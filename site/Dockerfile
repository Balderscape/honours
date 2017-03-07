FROM ubuntu:xenial

RUN apt-get update -yqq \
	&& apt-get upgrade -yqq \
	&& apt-get install -yqq --no-install-recommends build-essential python-pip python-dev git \
	&& rm -fr /var/lib/apt/lists

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install markdown pelican jupyter ipython nbconvert beautifulsoup4 ghp-import matplotlib

WORKDIR /site


