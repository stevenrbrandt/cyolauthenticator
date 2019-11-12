# CYOLAuthenticator: Create Your Own Login Authenticator
A Jupyterhub authenticator that allows users to pick a name and password if they know a code.

This branch is a heavily modified version that runs in the Google Compute Platform environment.

The front-end web service runs on a Google Compute Engine VM in a
docker container (`dstndstn/cyol`), described in the `docker/`
directory.  This includes a persistent disk mounted in `/nfs`, which
holds user home directories as well as persistent state for the
service. It also runs an LDAP server, and exports the home directories
via NFS.

The notebook servers are started on Kubernetes pods, which run the
`dstndstn/cyol-singleuser` container (in the `singleuser/` directory).
The notebooks are run as the logged-in user, and the home directory is
mounted over NFS.

To enable users to create a login, place a code word in /usr/enable_mkuser. If the users provide this code word when attempting to create a login, they will succeed.

To disable creation of logins, remove /usr/enable_mkuser.

Note that you will also need a custom login.html page. See the docker directory for how to do this.
