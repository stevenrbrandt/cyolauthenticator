# It is possible to use a later version of Ubuntu,
# however, if one does that then a Singularity version
# of the image will not run on clusters with older
# linux kernels.
FROM ubuntu:16.04
USER root

RUN apt-get update
# python3-pam is needed for authuser.py
RUN apt-get install -y python3 python3-pip openssh-client libssl-dev npm \
  gnupg policycoreutils python3-pam imagemagick curl vim

# Make python3 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install --upgrade pip==19.0.3

RUN pip install oauthenticator==0.9.0 jupyter==1.0.0 jupyterhub==1.0.0 tornado==5.1.1 python-oauth2==1.1.1 jupyterhub-dummyauthenticator

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get -y install nodejs 

RUN npm install -g configurable-http-proxy

# Edit the message in the h1 tags to customize your tutorial
COPY login.html /usr/local/share/jupyterhub/templates/login.html
COPY error.html /usr/local/share/jupyterhub/templates/error.html

# Replace logo.png with whatever logo you wish to use to brand the server
COPY logo.png /usr/local/share/jupyterhub/static/images/logo.png

#RUN mkdir -p /usr/local/lib/python3.5/dist-packages/cyolauthenticator
#COPY cyol.py /usr/local/lib/python3.5/dist-packages/cyolauthenticator/__init__.py
#COPY cyolauthenticator.py /usr/local/lib/python3.5/dist-packages/cyolauthenticator/cyolauthenticator.py
RUN pip install cyolauthenticator

COPY startup.sh /
COPY jup-config.py /
CMD bash startup.sh
