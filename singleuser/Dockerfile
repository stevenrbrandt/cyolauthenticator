# OR https://github.com/jupyter/docker-stacks
#FROM jupyter/base-notebook
#RUN pip3 install --no-cache jupyterhub notebook

FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \   #apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    run-one \
    python3 python3-pip \
    openssh-client libssl-dev npm \
    gnupg policycoreutils python3-pam imagemagick curl vim \
    iputils-ping git less
#python3-numpy \
#&& rm -rf /var/lib/apt/lists/*

# Make python3 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install --upgrade pip==19.0.3

RUN pip install --no-cache-dir oauthenticator==0.9.0 jupyter==1.0.0 jupyterhub==1.0.0 tornado==5.1.1 python-oauth2==1.1.1 jupyterhub-dummyauthenticator

RUN pip install matplotlib numpy scipy scikit-learn astropy pandas fitsio pyephem asdf h5py emcee corner cython

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

EXPOSE 8888
CMD ["start-notebook.sh"]

# From https://github.com/jupyter/docker-stacks
#COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/

