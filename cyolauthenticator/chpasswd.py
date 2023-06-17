#!/usr/bin/env python3
from random import randint
import sys, os, re
from subprocess import Popen, PIPE

LDAP_BASE_DN=os.environ["LDAP_BASE_DN"]
LDAP_HOST=os.environ["LDAP_HOST"]

def change_passwd(user, passwd):
    cmd=["ldapmodify","-x","-H",f"ldap://{LDAP_HOST}","-D", f"cn=admin,{LDAP_BASE_DN}","-y","/etc/ldap-admin-pw.txt"]
    p = Popen(cmd,universal_newlines=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
    msg=f"""
dn: uid={user},{LDAP_BASE_DN}
changetype: modify
replace: userPassword
userPassword: {passwd}
"""
    o, e = p.communicate(msg)
    if p.returncode != 0:
        print(o,e)
        print(f"Error: ret={p.returncode}")
        return p.returncode

if __name__ == "__main__":
    for line in sys.stdin.readlines():
        g = re.match(r'(.*?):(.*)', line)
        assert g, f"Bad data '{line}'"
        user, passwd = g.group(1), g.group(2)
        r = change_passwd(user, passwd)
        if r != 0:
            exit(r)
