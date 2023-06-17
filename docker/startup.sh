cd /
randpass MND -o /usr/enable_mkuser
python /usr/local/bin/frame.py

for f in passwd shadow
do
    if [ -r /home/${f} ]
    then
        cp /home/${f} /etc/${f}
    fi
done
bash /usr/local/sbin/sssd.conf.sh
service sssd start

echo -n $LDAP_ADMIN_PASSWORD > /etc/ldap-admin-pw.txt
chmod 600 /etc/ldap-admin-pw.txt
echo -n $LDAP_READONLY_USER_PASSWORD > /etc/ldap-pw.txt
chmod 600 /etc/ldap-pw.txt
unset LDAP_READONLY_USER_PASSWORD
unset LDAP_ADMIN_PASSWORD

export PYTHONPATH=/usr/local/lib/python$(python3 -c 'import sys; print("%d.%d" % (sys.version_info.major, sys.version_info.minor))')/dist-packages/cyolauthenticator

PORT=443
echo jupyterhub --ip 0.0.0.0 --port $PORT -f jup-config.py
jupyterhub --ip 0.0.0.0 --port $PORT -f jup-config.py
echo jupyterhub exited
sleep infinity
