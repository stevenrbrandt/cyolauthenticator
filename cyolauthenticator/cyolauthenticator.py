from traitlets import Unicode

from jupyterhub.auth import Authenticator

from subprocess import call, Popen, PIPE
from tornado.httpclient import HTTPError
from tornado import gen
from os import stat
import os
import sys
import re
import pwd
from hmac import compare_digest
from crypt import crypt

# Attempt to authenticate using PAM
def authuser(user, passw):
    with open("/etc/shadow", "r") as fd:
        for line in fd.readlines():
            cols = line.split(':')
            if cols[0] == user:
                if compare_digest(crypt(passw, cols[1]), cols[1]):
                  return True
                else:
                  break
    e = HTTPError(403)
    e.my_message = "Incorrect password"
    raise e

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

    home = "/home/%s" % user
    cmd = ["useradd",user,"-s","/bin/bash"]
    check_pass2 = False
    if os.path.exists(home):
      uid = stat(home).st_uid
      try:
        pwd.getpwuid(uid)
        return authuser(user, passw)
        # The user already exists, nothing to do
        #return uid
      except KeyError:
        check_pass2 = True
      cmd += ["-u",str(uid)]
    else:

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
      cmd += ["-m"]
      uids = set()
      for path in os.listdir("/home"):
        u = stat("/home/%s" % path).st_uid
        uids.add(u)
      for u in range(1000,100000):
        if u in uids:
          continue
        try:
          pwd.getpwuid(u)
        except KeyError:
          uid = u
          cmd += ["-u",str(uid)]
          break

    if check_pass2:
      if passw != passw2:
        e = HTTPError(403)
        e.my_message = "Password and Password2 do not match."
        raise e
    call(cmd)
    call(["su","-",user,"-c","bash /inituser.sh"])

    pipe = Popen(["chpasswd"],stdin=PIPE,universal_newlines=True)
    pipe.stdin.write("%s:%s\n" % (user, passw))
    pipe.stdin.close()
    pipe.wait()
    print("Chpasswd called with %s:%s" % (user, passw))
    call(["cp","/etc/shadow","/home/shadow"])
    call(["cp","/etc/passwd","/home/passwd"])
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

        if mkuser(username, password, password2, code == code_check):
            return username
        else:
            return None
