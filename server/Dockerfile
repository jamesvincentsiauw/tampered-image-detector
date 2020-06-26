FROM centos:centos7

# System dependencies
# System dependencies
RUN yum install -y \
        epel-release \
    && yum install -y \
        python3 python3-pip \
        python-dev build-essential \
        libsm6 libxext6 \
        curl unzip wget bzip2 \
        xvfb \
        python3-devel \
    && yum clean all

ADD requirements.txt /apps/tampered-image-detector/requirements.txt
RUN pip3 install -r /apps/tampered-image-detector/requirements.txt

RUN yum install gcc -y

RUN yum install make -y

RUN yum install automake libtool -y

RUN yum install gcc-c++ -y

RUN pip3 install opencv-python-headless
RUN pip3 install tensorflow

RUN yum -y install libpng-devel libtiff-devel libjpeg-devel

# Source code
COPY . /apps/tampered-image-detector
WORKDIR /apps/tampered-image-detector

# Network interfaces
EXPOSE 5000

RUN pip3 install tensorflow --user && pip3 install -r requirements.txt

#allow folder app-root
RUN chown -R 3000:3000 /opt/

#allow folder /apps/
RUN chown -R 3000:3000 /apps/

USER 3000

CMD python3 -u api.py