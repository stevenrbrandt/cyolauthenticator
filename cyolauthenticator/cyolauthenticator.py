from traitlets import Unicode

from jupyterhub.auth import Authenticator

from subprocess import call, Popen, PIPE, STDOUT, check_output
from tornado.httpclient import HTTPError
from tornado import gen
from os import stat
import os
import sys
import re
import pwd
import PAM

pam_passwd = None

service = 'passwd'
auth = PAM.pam()
auth.start(service)

def call_with_output(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    rtn = p.wait()
    msg = p.stdout.read()
    return rtn, msg

# Attempt to authenticate using PAM
def authuser(user, passw):
    def pam_conv(auth, query_list, userData):
        return [(passw, 0)]
    if user != None:
        auth.set_item(PAM.PAM_USER, user)
    auth.set_item(PAM.PAM_CONV, pam_conv)
    try:
        auth.authenticate()
        auth.acct_mgmt()
        return True
    except PAM.error as resp:
        e = HTTPError(403)
        e.my_message = "Incorrect password"
        raise e
    e = HTTPError(403)
    e.my_message = "Login failure"

def mkuser(user, passw, passw2, code_check):
    if user == None or len(user.strip())=="":
        e = HTTPError(403)
        e.my_message = "Username is missing"
        raise e

    if len(user) < 5:
        e = HTTPError(403)
        e.my_message = "Your user name is too short"
        raise e

    if len(user) > 15:
        e = HTTPError(403)
        e.my_message = "Your user name is too long"
        raise e

    if len(passw) < 7:
        e = HTTPError(403)
        e.my_message = "Your password is too short"
        raise e

    if len(passw) > 50:
        e = HTTPError(403)
        e.my_message = "Your password is too long"
        raise e

    if passw in [user, "abc123", "abcd1234", "abc1234", "abcd123"]:
        e = HTTPError(403)
        e.my_message = "Choose a better password"
        raise e

    if re.search(r'\W',user):
        e = HTTPError(403)
        e.my_message = "Illegal character in user nmame. Only letters, numbers and the underscore are allowed."
        raise e

    if re.search(r'\W',passw):
        e = HTTPError(403)
        e.my_message = "Illegal character in password. Only letters, numbers and the underscore are allowed."
        raise e

    homebase = '/nfs/home'
    homedir = os.path.join(homebase, user)

    create_uid = None
    create_homedir = False

    #cmd = ['useradd',user,"-s","/bin/bash",'-b',homebase'-g','users']
    check_pass2 = False

    # Check if username is an existing user
    try:
        p = pwd.getpwnam(user)
        if not os.path.exists(homedir):
            # Not a regular user
            e = HTTPError(403)
            e.my_message = "User name '%s' not allowed (conflicts with system user)" % user
            raise e
        return authuser(user, passw)
    except KeyError:
        # No such user
        # If homedir exists from a previous instance of the server,
        # use that uid.
        if os.path.exists(homedir):
            uid = stat(homedir).st_uid
            create_uid = str(uid)
        else:
            create_homedir = True
        check_pass2 = True

    # Create a new user...
    if not os.path.exists("/usr/enable_mkuser"):
        e = HTTPError(403)
        e.my_message = "MkUser disabled"
        raise e
    if not code_check:
        e = HTTPError(403)
        e.my_message = "Code check failed"
        raise e
    check_pass2 = True
    if passw != passw2:
        e = HTTPError(403)
        e.my_message = "Password and Password2 do not match."
        raise e

    # Find an unused UID for this new user
    uids = set()
    for path in os.listdir(homebase):
        u = stat(os.path.join(homebase, path)).st_uid
        uids.add(u)
    for u in range(10000,100000):
        if u in uids:
            continue
        try:
            pwd.getpwuid(u)
        except KeyError:
            create_uid = str(u)
            break

    if check_pass2:
        if passw != passw2:
            e = HTTPError(403)
            e.my_message = "Password and Password2 do not match."
            raise e

    # cmd = ['useradd',user,"-s","/bin/bash",'-b',homebase'-g','users']
    # if create_homedir is not None:
    #   cmd += ['-m']
    # if create_uid is not None:
    #   cmd += ['-u',create_uid]
    #call(cmd)

    cmds = []

    cmd = ['ldapadduser', user, 'users']
    if create_uid is not None:
        cmd += [create_uid]

    cmds.append(cmd)

    if create_homedir:
        cmds.append(['mkdir', homedir])
        cmds.append(['chown','%s:users' % user, homedir])

    for cmd in cmds:
        print('Calling:', cmd)
        rtn,msg = call_with_output(cmd)
        print('->', rtn, msg)
        if rtn != 0:
            e = HTTPError(500)
            e.my_message = ("Failed to create user: '%s', error '%s'" %
                            (cmd, msg))
            raise e

    if create_homedir:
        pipe = Popen(['ldapmodifyuser',user], stdin=PIPE, universal_newlines=True)
        pipe.stdin.write('replace: homeDirectory\nhomeDirectory: %s\n' % homedir)
        pipe.stdin.close()
        pipe.wait()

    pipe = Popen(['ldapsetpasswd', user], stdin=PIPE, universal_newlines=True)
    pipe.stdin.write('%s\n%s\n' % (passw, passw))
    pipe.stdin.close()
    pipe.wait()

    call(["su","-",user,"-c","bash /inituser.sh"])

    # pipe = Popen(["chpasswd"],stdin=PIPE,universal_newlines=True)
    # pipe.stdin.write("%s:%s\n" % (user, passw))
    # pipe.stdin.close()
    # pipe.wait()
    # print("Chpasswd called with %s:%s" % (user, passw))
    return True

class CYOLAuthenticator(Authenticator):
    password = Unicode(
        None,
        allow_none=True,
        config=True,
        help="""
        Set a global password for all users wanting to log in.

        This allows users with any username to log in with the same static password.
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):

        # Retrieve form data
        username = data['username'].lower()
        password = data['password']
        password2 = data['password2']
        code = data['code']

        # If the /usr/enable_mkuser is present, read it.
        # This file must be present for users to create
        # new accounts.
        try:
          with open("/usr/enable_mkuser","r") as fd:
            code_check = fd.read().strip()
        except:
          # Ensure code check doesn't happen
          code_check = "disabled"
          code = ""

        print('Code check: user entered "%s", right answer is "%s"' % (code, code_check))
        if mkuser(username, password, password2, code == code_check):
            return username
        else:
            return None
