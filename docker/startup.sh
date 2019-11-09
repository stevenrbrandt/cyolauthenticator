cd /
#echo jtest789 > /usr/enable_mkuser

#krb5kdc
#kadmind


#slappasswd -s $(cat /tmp/slappasswd) > /tmp/hashpass
#echo -e "dn: olcDatabase={1}mdb,cn=config\nchangetype: modify\nadd: olcRootPW\nolcRootPW: $(cat /tmp/hashpass)\n" | ldapmodify -Q -Y EXTERNAL -H ldapi:///
slappasswd -g > /tmp/slappasswd
chmod 400 /tmp/slappasswd
slappasswd -T /tmp/slappasswd > /tmp/hashpass

service slapd start

echo -e "dn: olcDatabase={1}mdb,cn=config\nchangetype: modify\nreplace: olcRootPW\nolcRootPW: $(cat /tmp/hashpass)" | ldapmodify -Y EXTERNAL -H ldapi:///
#echo -e "dn: olcDatabase={1}mdb,cn=config\nchangetype: modify\nreplace: olcRootDN\nolcRootDN: cn=admin,dc=hub" | ldapmodify -Y EXTERNAL -H ldapi:///

#service slapd stop
#service slapd start

# ldapsearch -H ldapi:// -LLL -Q -Y EXTERNAL -b "cn=config" "(olcRootDN=*)" dn olcRootDN olcRootPW

# ldapsearch -H ldapi:// -LLL -Q -Y EXTERNAL -b "dc=hub"

# https://www.digitalocean.com/community/tutorials/how-to-change-account-passwords-on-an-openldap-server

echo -e "dn: cn=admin,dc=hub\nchangetype: modify\nreplace: userPassword\nuserPassword: $(cat /tmp/hashpass)" | ldapmodify -H ldap:// -x -D "cn=admin,dc=hub" -y /tmp/slappasswd

ldapadd -y /tmp/slappasswd -x -D cn=admin,dc=hub -f /tmp/add_content.ldif
#ldapadd -y /tmp/slappasswd -x -D cn=admin,dc=hub -f /tmp/george.ldif

cp /tmp/slappasswd /etc/ldapscripts/ldapscripts.passwd
chmod 600 /etc/ldapscripts/ldapscripts.passwd
ldapaddgroup users
ldapadduser george users



# # from https://github.com/GoogleCloudPlatform/nfs-server-docker/blob/master/1/debian9/1.3/docker-entrypoint.sh
# rpcbind -w
# mount -t nfsd nfds /proc/fs/nfsd
# /usr/sbin/rpc.mountd -N 2 -V 3
# /usr/sbin/exportfs -r
# # -G 10 to reduce grace time to 10 seconds (the lowest allowed)
# /usr/sbin/rpc.nfsd -G 10 -N 2 -V 3
# /sbin/rpc.statd --no-notify

# Need to run in a "privileged" container for this!!
mount -t nfsd nfds /proc/fs/nfsd

service rpcbind start
service nfs-kernel-server start


#cp --update /home/passwd /home/group /home/shadow /etc/

# Set my local IP address -- passed to spawned notebook servers (?)
#export HUB_CONNECT_IP=$(ip route ls | tail -n 1 | awk '{print $NF}')

# If we have a certificate directory...
if [ -d /etc/pki/tls/certs/tutorial.cer ]
then
  PORT=443
else
  PORT=80
fi
jupyterhub --ip 0.0.0.0 --port $PORT -f jup-config.py
