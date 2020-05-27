#### Use latest Ubuntu LTS release as the base
FROM ubuntu:eoan

#fix for tzdata
ARG DEBIAN_FRONTEND=noninteractive

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

# Install GDAL dependencies

RUN apt-get install -y python3 python-dev python3-dev \
    build-essential libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    python3-pip  libgdal-dev locales \
    libsqlite3-mod-spatialite

# Ensure locales configured correctly
RUN locale-gen en_US.UTF-8
ENV LC_ALL='en_US.utf8'

#Time zone
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set python aliases for python3
RUN echo 'alias python=python3' >> ~/.bashrc
RUN echo 'alias pip=pip3' >> ~/.bashrc

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
 
# This will install latest version of GDAL
RUN pip3 install GDAL==2.2.3

# # set work directory
 WORKDIR /usr/src/app

# # # set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONHASHSEED=random


# # # install dependencies
RUN pip3 install --upgrade pip
# RUN pip install pipenv virtualenv

COPY requirements.txt /usr/src/app/requirements.txt
# # #RUN pipenv install --skip-lock --system --dev
RUN  pip3 install  --no-cache-dir -r requirements.txt



# RUN add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update \
# RUN apt-get install gdal-bin libgdal-dev\
# RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal\
# RUN export C_INCLUDE_PATH=/usr/include/gdal\
# RUN pip install GDAL 


# copy project
COPY . /usr/src/app/




