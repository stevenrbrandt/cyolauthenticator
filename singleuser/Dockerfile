FROM ubuntu:18.04

RUN apt update && apt -yq dist-upgrade \
 && DEBIAN_FRONTEND=noninteractive apt install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    run-one \
    python3 python3-pip python3-dev \
    openssh-client libssl-dev \
    gnupg policycoreutils imagemagick curl vim \
    iputils-ping git less \
    patch gcc make libc6-dev \
    nfs-common rpcbind libnss-ldap ldap-utils ldap-auth-config \
    libpam-ldap \
    && rm -rf /var/lib/apt/lists/*
 # strace \
# Make python3 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir oauthenticator==0.9.0 jupyter==1.0.0 \
    python-oauth2==1.1.1 notebook==6.0.2 \
    matplotlib numpy scipy scikit-learn astropy pandas fitsio pyephem \
    asdf h5py emcee corner cython && echo 1

RUN wget -nv https://julialang-s3.julialang.org/bin/linux/x64/1.2/julia-1.2.0-linux-x86_64.tar.gz && \
     tar xvz -C /usr/local --strip-components 1 -f julia-1.2.0-linux-x86_64.tar.gz && \
     rm julia-1.2.0-linux-x86_64.tar.gz

COPY nsswitch.conf /etc
COPY etcldap.conf /etc/ldap.conf

RUN echo "libpam-runtime libpam-runtime/profiles multiselect unix, ldap" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure libpam-runtime

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

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

