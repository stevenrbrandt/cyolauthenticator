# It is possible to use a later version of Ubuntu,
# however, if one does that then a Singularity version
# of the image will not run on clusters with older
# linux kernels.
FROM ubuntu:20.04
USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
# python3-pam is needed for authuser.py
RUN apt-get install -y python3 python3-pip openssh-client libssl-dev npm \
  gnupg policycoreutils python3-pam imagemagick curl vim git \
  ldap-utils vim sssd-ldap perl-modules-5.30 libpam-ldapd apt-file dialog ca-certificates libnss-ldap libpam-modules libpam-sss

COPY sssd.conf.sh /usr/local/sbin/sssd.conf.sh
RUN  bash /usr/local/sbin/sssd.conf.sh

# Make python3 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install --upgrade pip

RUN pip install oauthenticator==14.1.0 jupyter==1.0.0 jupyterhub==1.4.2 tornado==6.1 python-oauth2==1.1.1 jupyterhub-dummyauthenticator

RUN apt-get -y install nodejs 

RUN npm install -g configurable-http-proxy@4.5.0

# Edit the message in the h1 tags to customize your tutorial
COPY login.html /usr/local/share/jupyterhub/templates/login.html
COPY error.html /usr/local/share/jupyterhub/templates/error.html

# Replace logo.png with whatever logo you wish to use to brand the server
COPY logo.png /usr/local/share/jupyterhub/static/images/logo.png

#RUN mkdir -p /usr/local/lib/python3.5/dist-packages/cyolauthenticator
#COPY cyol.py /usr/local/lib/python3.5/dist-packages/cyolauthenticator/__init__.py
#COPY cyolauthenticator.py /usr/local/lib/python3.5/dist-packages/cyolauthenticator/cyolauthenticator.py

RUN pip install randpass
RUN pip install git+https://github.com/stevenrbrandt/cyolauthenticator
COPY cyol.tgz ./
#RUN tar xzf cyol.tgz 
RUN python3 setup.py install


COPY startup.sh /
COPY jup-config.py /
COPY info.txt /
COPY frame.py /usr/local/bin/
COPY test.sh /
CMD bash ./startup.sh
