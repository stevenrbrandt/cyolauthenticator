# CYOLAuthenticator: Create Your Own Login Authenticator
A Jupyterhub authenticator that allows users to pick a name and password if they know a code.

To enable users to create a login, place a code word in /usr/enable_mkuser. If the users provide this code word when attempting to create a login, they will succeed.

To disable creation of logins, remove /usr/enable_mkuser.

Note that you will also need a custom login.html page. See the docker directory for how to do this.
