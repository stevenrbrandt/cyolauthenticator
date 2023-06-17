from subprocess import Popen, PIPE, call
import sys, re, os
from tempfile import NamedTemporaryFile

LDAP_BASE_DN=os.environ["LDAP_BASE_DN"]
LDAP_HOST=os.environ["LDAP_HOST"]

def check_passwd(user, passwd):
    n = NamedTemporaryFile(mode='w')
    n.write(passwd)
    n.flush()

    cmd=["ldapwhoami","-x","-y",n.name,f"-D",f"uid={user},{LDAP_BASE_DN}","-H",f"ldap://{LDAP_HOST}"]
    p = Popen(cmd, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    o,e = p.communicate(passwd)
    print(e,end='')
    return p.returncode

if __name__ == "__main__":
    for line in sys.stdin.readlines():
        g = re.match(r'(.*?):(.*)', line)
        assert g, f"Bad data '{line}'"
        user, passwd = g.group(1), g.group(2)
        r = check_passwd(user, passwd)
        if r != 0:
            exit(r)
