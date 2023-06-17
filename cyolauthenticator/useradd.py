#!/usr/bin/env python3
from random import randint
import sys, os
from subprocess import Popen, PIPE

UIDNUMBER_NOT_UNIQUE = 19
USER_EXISTS = 68
LDAP_BASE_DN=os.environ["LDAP_BASE_DN"]
LDAP_HOST=os.environ["LDAP_HOST"]

def user_add(user):
    uidNumber = randint(1000,100000)
    while True:
        print(user, uidNumber)
        p = Popen(["ldapadd","-x","-H",f"ldap://{LDAP_HOST}","-D", f"cn=admin,{LDAP_BASE_DN}","-y","/etc/ldap-admin-pw.txt"],universal_newlines=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        o, e = p.communicate(f"""
# define ldif file with record arrtributes
# file saved with bassa.lfip
dn: uid={user},{LDAP_BASE_DN}
uid: {user}
cn: {user}
sn: 3
objectClass: top
objectClass: posixAccount
objectClass: inetOrgPerson
loginShell: /bin/bash
homeDirectory: /home/{user}
uidNumber: {uidNumber}
gidNumber: 100
mail: sbrandt@cct.lsu.edu
gecos: {user}
""")
        if p.returncode == 0:
            break
        elif p.returncode == UIDNUMBER_NOT_UNIQUE:
            uidNumber = randint(1000,100000)
        elif p.returncode == USER_EXISTS:
            print(f"USER exists {user}")
            break
        else:
            print(f"Error: ret={p.returncode}")
            break
    return p.returncode

if __name__ == "__main__":
    user = sys.argv[1]
    r = user_add(user)
    exit(r)
