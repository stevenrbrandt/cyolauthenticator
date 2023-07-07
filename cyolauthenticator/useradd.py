#!/usr/bin/env python3
from random import randint
import sys, os
from subprocess import Popen, PIPE, call
from time import sleep
from pwd import getpwnam
from grp import getgrgid

UIDNUMBER_NOT_UNIQUE = 19
USER_EXISTS = 68
LDAP_BASE_DN=os.environ["LDAP_BASE_DN"]
LDAP_HOST=os.environ["LDAP_HOST"]

user_data = {}

def get_user_data(user):
    if user in user_data:
        return user_data[user]
    try:
        return getpwnam(user)
    except:
        return None

def user_add(user):
    uid_number = randint(1000,100000)
    while True:
        ldap_cmd=["ldapadd","-x","-H",f"ldap://{LDAP_HOST}","-D", f"cn=admin,{LDAP_BASE_DN}","-y","/etc/ldap-admin-pw.txt"]
        p = Popen(ldap_cmd,universal_newlines=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        login_shell = "/bin/bash"
        home_directory = f"/home/{user}"
        gid_number = 100
        email = 'sbrandt@cct.lsu.edu'
        gecos = user

        ldap_txt=f"""
# define ldif file with record arrtributes
# file saved with bassa.lfip
dn: uid={user},{LDAP_BASE_DN}
uid: {user}
cn: {user}
sn: 3
objectClass: top
objectClass: posixAccount
objectClass: inetOrgPerson
loginShell: {login_shell}
homeDirectory: {home_directory}
uidNumber: {uid_number}
gidNumber: {gid_number}
mail: {email}
gecos: {gecos}
"""
        o, e = p.communicate(ldap_txt)
        if e.strip() != "":
            print("error:",e)

        # Create a fake pwd entry because getpwnam()
        # doesn't see updates immedately.
        class _user:
            def __init__(self):
                self.pw_name = user
                self.pw_dir = home_directory
                self.pw_gid = gid_number
                self.pw_uid = uid_number
                self.pw_gecos = gecos
                self.pw_shell = login_shell
                self.pw_passwd = '*'

        if p.returncode == 0:
            uinfo = _user()
            user_data[user] = uinfo
            os.makedirs(uinfo.pw_dir, exist_ok=True)
            ginfo = getgrgid(uinfo.pw_gid)
            while True:
                sleep(1)
                r = call(["id",user])
                if r == 0:
                    break
            call(["chown",f"{user}:{ginfo.gr_name}",uinfo.pw_dir])
            call(["su","-",user,"-c","cp -TRn /etc/skel/ ~/"])
            break
        
            uid_number = randint(1000,100000)
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
