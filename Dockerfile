FROM bamos/ubuntu-opencv-dlib-torch:ubuntu_14.04-opencv_2.4.11-dlib_19.0-torch_2016.07.12
MAINTAINER kimsup10 <kss5662@gmail.com>
LABEL description="Ajou Univ > Spring 2017 > Capstone Design > Team Helloworld"

# TODO: Should be added to opencv-dlib-torch image.
RUN ln -s /root/torch/install/bin/* /usr/local/bin

RUN apt-get update && apt-get install -y \
    curl \
    git \
    graphicsmagick \
    libssl-dev \
    libffi-dev \
    python-dev \
    python-pip \
    python-numpy \
    python-nose \
    python-scipy \
    python-pandas \
    python-protobuf \
    python-openssl \
    nginx \
    wget \
    zip \
    redis-server \
    postgresql \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /root/openface

ADD ./requirements.txt /root/openface/requirements.txt
RUN python -m pip install --upgrade --force pip
RUN pip2 install -r requirements.txt

ADD . /root/openface
RUN cd ~/openface && \
    ./models/get-models.sh && \
    python2 setup.py install

RUN adduser --disabled-password --gecos '' cumera
