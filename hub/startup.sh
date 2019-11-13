#! /bin/bash

cd /

service ssh start

# Authorize to use kubernetes using service account,
# assumed to be stored in /nfs/sys/svc.json
gcloud auth activate-service-account --key-file /nfs/sys/svc.json
gcloud container clusters get-credentials --zone us-central1-a \
       --project research-technologies-testbed \
       your-first-cluster-1

# Reset the LDAP passwords
slappasswd -g > /tmp/slappasswd
chmod 400 /tmp/slappasswd
slappasswd -T /tmp/slappasswd > /tmp/hashpass
# Copy password for ldapscripts
cp /tmp/slappasswd /etc/ldapscripts/ldapscripts.passwd
chmod 600 /etc/ldapscripts/ldapscripts.passwd

if [ -f /nfs/sys/ldap/data.mdb ]; then
    echo "/nfs/sys/ldap/data.mdb exists -- symlinking!"
    mv /var/lib/ldap /var/lib/ldap.orig
    ln -s /nfs/sys/ldap /var/lib/
    service slapd start

    echo -e "dn: olcDatabase={1}mdb,cn=config\nchangetype: modify\nreplace: olcRootPW\nolcRootPW: $(cat /tmp/hashpass)" | ldapmodify -Y EXTERNAL -H ldapi:///
    echo -e "dn: cn=admin,dc=hub\nchangetype: modify\nreplace: userPassword\nuserPassword: $(cat /tmp/hashpass)" | ldapmodify -H ldap:// -x -D "cn=admin,dc=hub" -y /tmp/slappasswd

else
    service slapd start

    echo -e "dn: olcDatabase={1}mdb,cn=config\nchangetype: modify\nreplace: olcRootPW\nolcRootPW: $(cat /tmp/hashpass)" | ldapmodify -Y EXTERNAL -H ldapi:///
    # https://www.digitalocean.com/community/tutorials/how-to-change-account-passwords-on-an-openldap-server
    echo -e "dn: cn=admin,dc=hub\nchangetype: modify\nreplace: userPassword\nuserPassword: $(cat /tmp/hashpass)" | ldapmodify -H ldap:// -x -D "cn=admin,dc=hub" -y /tmp/slappasswd
    ldapadd -y /tmp/slappasswd -x -D cn=admin,dc=hub -f /tmp/add_content.ldif
    ldapaddgroup users
fi
rm /tmp/slappasswd

# Need to run in a "privileged" container for this!!
mount -t nfsd nfds /proc/fs/nfsd

service rpcbind start
service nfs-common start
service nfs-kernel-server start

# If we have a certificate directory...
if [ -d /etc/pki/tls/certs/tutorial.cer ]
then
  PORT=443
else
  PORT=80
fi
jupyterhub --port $PORT -f jup-config.py | tee jupyterhub.log
