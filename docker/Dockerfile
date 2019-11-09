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
COPY pi-logo.png /usr/local/share/jupyterhub/static/images/logo.png

# Install packages for the Jupyter notebooks!
RUN pip install matplotlib numpy scipy scikit-learn astropy pandas fitsio pyephem asdf h5py emcee corner cython

RUN apt install wget
RUN wget -nv https://julialang-s3.julialang.org/bin/linux/x64/1.2/julia-1.2.0-linux-x86_64.tar.gz
RUN tar xvz -C /usr/local --strip-components 1 -f julia-1.2.0-linux-x86_64.tar.gz

# docker run -it -p 8802:80 cyol


### Dustin -- try adding gcloud for launching notebook servers in gcloud kubernetes!

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt install apt-transport-https ca-certificates
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt update && apt install -y google-cloud-sdk kubectl

RUN pip install kubernetes==9.0.1 # && pip install jupyterhub-kubespawner
RUN apt install -y --no-install-recommends git less

# Copy service account credentials!
COPY research-technologies-testbed-a786f12c5112.json /svc.json

RUN gcloud config configurations create testbed-config \
    && gcloud config configurations activate testbed-config \
    && gcloud auth activate-service-account --key-file /svc.json \
    && gcloud container clusters get-credentials your-first-cluster-1 --zone us-central1-a --project research-technologies-testbed
#    && rm /svc.json \
#    && gcloud config set project research-technologies-testbed \

RUN git clone https://github.com/jupyterhub/kubespawner.git
RUN cd kubespawner && python setup.py install

# Google Container Registry:
# > docker tag dstndstn/cyol gcr.io/research-technologies-testbed/cyol
# > docker push gcr.io/research-technologies-testbed/cyol

# Getting logs from service running in GKE
# gcloud container clusters get-credentials your-first-cluster-1 --zone us-central1-a --project research-technologies-testbed
# kubectl logs jupyterhub-cyol-6b6f84b5f6-6mp2h

# Runs container:
# jupyterhub/singleuser:latest

# kubectl cluster-info
# kubectl get nodes
# kubectl run hello-server --image gcr.io/google-samples/hello-app:1.0 --port 8080

# PER https://cloud.google.com/kubernetes-engine/docs/troubleshooting#autofirewall
# $ gcloud container clusters describe your-first-cluster-1 --format=get"(network)" --zone us-central1-a
# default
# $ gcloud container clusters describe your-first-cluster-1 --format=get"(clusterIpv4Cidr)" --zone us-central1-a
# 10.4.0.0/14
# $ gcloud compute firewall-rules create "your-first-cluster-1-to-all-vms-on-network" --network="default" --source-ranges="10.4.0.0/14" --allow=tcp,udp,icmp,esp,ah,sctp
# Creating firewall...⠧Created [https://www.googleapis.com/compute/v1/projects/research-technologies-testbed/global/firewalls/your-first-cluster-1-to-all-vms-on-network].
# Creating firewall...done.
# NAME                                        NETWORK  DIRECTION  PRIORITY  ALLOW                     DENY  DISABLED
# your-first-cluster-1-to-all-vms-on-network  default  INGRESS    1000      tcp,udp,icmp,esp,ah,sctp        False


# hub.c.research-technologies-testbed.internal

RUN DEBIAN_FRONTEND=noninteractive \
    apt install -y --no-install-recommends nfs-server iputils-ping emacs-nox



#COPY slappasswd /tmp
#slappasswd -g > /tmp/slappasswd && \
#slappasswd -s $(cat /tmp/slappasswd) > /tmp/hashpass && \
#RUN sed -i 's/nodomain/hub/g' /etc/ldap/slapd.d/cn=config/olcDatabase={1}mdb.ldif

RUN echo "BASE dc=hub\nURI ldap://hub\n" >> /etc/ldap/ldap.conf

RUN git config --global user.email x && \
    git config --global user.name x

ARG LDAP_PW=XXX333

RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    debconf-utils


### Do we need ldapscripts??

#    echo "slapd slapd/password1 password ${LDAP_PW}" | debconf-set-selections && \
#    echo "slapd slapd/password2 password ${LDAP_PW}" | debconf-set-selections && \

RUN echo "slapd slapd/domain string hub" | debconf-set-selections && \
    echo "slapd slapd/purge_database boolean true" | debconf-set-selections && \
    echo "slapd slapd/move_old_database boolean true" | debconf-set-selections && \
    echo "slapd shared/organization string PI" | debconf-set-selections && \
    echo "slapd slapd/allow_ldap_v2 boolean false" | debconf-set-selections && \
    echo "slapd slapd/no_configuration boolean false" | debconf-set-selections && \
    echo "slapd slapd/backend string MDB" | debconf-set-selections && \
    echo "slapd slapd/password1 password XXX" | debconf-set-selections && \
    echo "slapd slapd/password2 password XXX" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive   apt install -y --no-install-recommends \
        slapd ldap-utils ldapscripts libnss-ldap && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure slapd

COPY nsswitch.conf /etc
# required for 'getent passwd'
COPY etcldap.conf /etc/ldap.conf
COPY ldapscripts.conf /etc/ldapscripts

RUN echo "libpam-runtime  libpam-runtime/profiles multiselect     unix, ldap" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive   apt install -y --no-install-recommends \
        libpam-ldap && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure libpam-runtime

# pam-auth-update

#COPY slap.db /etc/ldap/slapd.d/cn=config/olcDatabase={1}mdb.ldif

# ldapsearch -b 'dc=hub' -s base '(objectclass=*)'
# ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config dn
# ldapsearch -x -LLL -H ldap:/// -b dc=hub dn

### docker run --hostname hub -it dstndstn/cyol bash

#slappasswd -g > /tmp/slappasswd && \
#slappasswd -s $(cat /tmp/slappasswd) > /tmp/hashpass && \
#sed -i "s/olcRootPW.*/olcRootPW: $(cat /tmp/hashpass)/" /etc/ldap/slapd.d/cn=config/olcDatabase={1}mdb.ldif
#sed -i "s/olcRootPW: .*/olcRootPW: $(cat /tmp/hashpass)/" /etc/ldap/slapd.d/cn=config/olcDatabase={1}mdb.ldif

COPY add_content.ldif /tmp
COPY george.ldif /tmp

#echo -e "dn: olcDatabase={1}mdb,cn=config\nchangetype: modify\nadd: olcRootPW\nolcRootPW: $(cat /tmp/hashpass)\n" |
# ldapmodify -Q -Y EXTERNAL -H ldapi:///

# kubectl apply -f ../config/nfs-pv.yaml
# kubectl apply -f ../config/nfs-pvc.yaml

# In workload -> deployment details, add to YAML under spec: containers:

#        volumeMounts:
#        - name: my-pvc-nfs
#          mountPath: "/home"
#      volumes:
#      - name: my-pvc-nfs
#        persistentVolumeClaim:
#          claimName: nfs

# https://medium.com/platformer-blog/nfs-persistent-volumes-with-kubernetes-a-case-study-ce1ed6e2c266

#COPY libnss-ldap.conf /etc/

# ldapadd -x -D cn=admin,dc=hub -W -f /tmp/add_content.ldif

# Test:
# # ldapsearch -x -LLL -b dc=hub 'uid=test' cn gidNumber
#dn: uid=test,ou=People,dc=hub
#cn: Test Guy
#gidNumber: 5000

# On instance-1:
# # ldapsearch -x -LLL -H ldap://hub -b dc=hub 'uid=test' cn gidNumber
# dn: uid=test,ou=People,dc=hub
# cn: Test Guy
# gidNumber: 5000

# ldapsearch -x -LLL -H ldap://hub -b dc=hub 'uid=george'

# ldapsearch -x

# !! lsldap

# https://help.ubuntu.com/lts/serverguide/openldap-server.html
#  apt install 
#  apt install ldap-auth-config
#  dpkg-reconfigure ldap-auth-config
#  python2 /usr/sbin/auth-client-config -t nss -p lac_ldap
#  pam-auth-update
#  edit /etc/ldapscripts/ldapscripts.conf

# /usr/share/doc/libpam-krb5/README.Debian.gz
# https://wiki.debian.org/LDAP/Kerberos#PAM


#ADD slapd-conf.tgz /etc/ldap/

RUN mkdir -p /usr/local/lib/python3.5/dist-packages/cyolauthenticator
COPY __init__.py /usr/local/lib/python3.5/dist-packages/cyolauthenticator/__init__.py
COPY cyolauthenticator.py /usr/local/lib/python3.5/dist-packages/cyolauthenticator/cyolauthenticator.py
#RUN pip install cyolauthenticator

COPY startup.sh /
CMD bash startup.sh
COPY inituser.sh /
COPY jup-config-kube.py /jup-config.py
COPY codeword.txt /usr/enable_mkuser
ENV GOOGLE_APPLICATION_CREDENTIALS /svc.json
EXPOSE 80
EXPOSE 8081

#RUN echo "/home 10.0.0.0/8(rw)" > /etc/exports
RUN echo "/nfs/home 10.0.0.0/8(rw)" > /etc/exports
# per https://github.com/GoogleCloudPlatform/nfs-server-docker/blob/master/1/debian9/1.3/Dockerfile
EXPOSE 2049/tcp
EXPOSE 20048/tcp



# gcloud beta compute --project=research-technologies-testbed instances create-with-container hub \
#  --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM \
#  --metadata=google-logging-enabled=true --maintenance-policy=MIGRATE \
#  --service-account=310980440256-compute@developer.gserviceaccount.com \
#  --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
#  --tags=hub,http-server --image=cos-stable-77-12371-114-0 --image-project=cos-cloud --boot-disk-size=10GB \
#  --boot-disk-type=pd-standard --boot-disk-device-name=hub --disk=name=nfs-home,device-name=nfs-home,mode=rw,boot=no \
#  --container-image=gcr.io/research-technologies-testbed/cyol --container-restart-policy=always --container-privileged \
#  --container-mount-disk=mount-path=/nfs/home,name=nfs-home,mode=rw --labels=container-vm=cos-stable-77-12371-114-0 --reservation-affinity=any

