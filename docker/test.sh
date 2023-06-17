echo -n $LDAP_ADMIN_PASSWORD > /etc/ldap-admin-pw.txt
chmod 600 /etc/ldap-admin-pw.txt
echo -n $LDAP_READONLY_USER_PASSWORD > /etc/ldap-pw.txt
chmod 600 /etc/ldap-pw.txt

cat > user.ldif << EOF
# define ldif file with record arrtributes
# file saved with ${LDAP_READONLY_USER_USERNAME}.lfip
dn: uid=${LDAP_READONLY_USER_USERNAME},${LDAP_BASE_DN}
uid: ${LDAP_READONLY_USER_USERNAME}
cn: ${LDAP_READONLY_USER_USERNAME}
sn: 3
objectClass: top
objectClass: posixAccount
objectClass: inetOrgPerson
loginShell: /bin/bash
homeDirectory: /home/${LDAP_READONLY_USER_USERNAME}
uidNumber: 1234
gidNumber: 100
userPassword: ${LDAP_READONLY_USER_PASSWORD}
mail: ${LDAP_READONLY_USER_USERNAME}@rahasak.com
gecos: ${LDAP_READONLY_USER_USERNAME} User
EOF

set -x
ldapadd -x -H ldap://${LDAP_HOST} -D cn=admin,${LDAP_BASE_DN}  -f user.ldif -y /etc/ldap-admin-pw.txt
ldapsearch -x -H ldap://${LDAP_HOST} -b ${LDAP_BASE_DN} -D cn=admin,${LDAP_BASE_DN} -y /etc/ldap-admin-pw.txt
