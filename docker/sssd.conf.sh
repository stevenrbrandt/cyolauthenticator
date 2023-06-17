mkdir -p /etc/sssd

# Don't reinstall
if [ -d /etc/sssd/sssd.conf ]
then return
fi

cat > /etc/sssd/sssd.conf << EOF
[sssd]
config_file_version = 2
domains = ${LDAP_DOMAIN}
services = nss, pam

[pam]

[domain/${LDAP_DOMAIN}]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://${LDAP_HOST}
cache_credentials = True
ldap_search_base = ${LDAP_BASE_DN}
ldap_group_search_base = ${LDAP_BASE_DN}
ldap_user_search_base = ${LDAP_BASE_DN}
ldap_default_bind_dn = cn=admin,${LDAP_BASE_DN}
ldap_default_authtok = ${LDAP_ADMIN_PASSWORD}

[nss]
filter_groups = root
filter_users = root
entry_cache_nowait_percentage = 75
EOF
chmod 600 /etc/sssd/sssd.conf
