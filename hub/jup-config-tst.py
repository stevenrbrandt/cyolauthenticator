#import os

c.JupyterHub.authenticator_class = 'cyolauthenticator.CYOLAuthenticator'
c.JupyterHub.template_paths = ['/jinja/templates']

# eg from https://github.com/GoogleCloudPlatform/gke-jupyter-classroom/blob/master/jupyterhub/jupyterhub_config.py
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 9001

c.ConfigurableHTTPProxy.pid_file = '/proxy-tst.pid'
c.ConfigurableHTTPProxy.api_url = 'http://0.0.0.0:5432'

import kubespawner
c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.debug = True
c.KubeSpawner.start_timeout = 300
#c.KubeSpawner.http_timeout = 90

import pwd
def get_kube_uid(spawner):
    print('Hello, I am get_kube_uid() with spawner', spawner)
    print('spawner.user is', spawner.user)
    print('spawner.user.name is', spawner.user.name)
    print('spawner.user.id is', spawner.user.id)
    uid = pwd.getpwnam(spawner.user.name).pw_uid
    print('pwd uid:', uid)
    return uid

def get_kube_gid(spawner):
    return pwd.getpwnam(spawner.user.name).pw_gid

c.KubeSpawner.uid = get_kube_uid
c.KubeSpawner.gid = get_kube_gid

c.KubeSpawner.image_pull_policy = 'Always'
c.KubeSpawner.volumes = [
    dict(name='nfs2', persistentVolumeClaim=dict(claimName='nfs2')),
]
c.KubeSpawner.volume_mounts = [
    dict(name='nfs2', mountPath='/nfs/home'),
]

# c.KubeSpawner.uid = int, callable -- user to run container as.
#     callable: takes KubeSpawner, returns int.
# c.KubeSpawner.gid = int, callable
# c.KubeSpawner.volumes?
#c.KubeSpawner.volume_mounts, etc

c.KubeSpawner.profile_list = [
    {
        'display_name': 'my singleuser container',
        'default': True,
        'kubespawner_override': {
            'image': 'dstndstn/cyol-singleuser',
        }
    },
    {
        'display_name': 'jupyterhub singleuser 1.0',
        'default': True,
        'kubespawner_override': {
            'image': 'jupyterhub/singleuser:1.0',
        }
    }
]

# https://github.com/nteract/hydrogen/issues/922
c.NotebookApp.token = 'super$ecret'

#'cpu_limit': 1,
#'mem_limit': '512M',
    

# openssl genrsa -out rootCA.key 2048
# openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem

import os
if os.path.exists('/etc/pki/tls/certs/tutorial.cer'):
  c.JupyterHub.ssl_cert = '/etc/pki/tls/certs/tutorial.cer'
  c.JupyterHub.ssl_key =  '/etc/pki/tls/private/tutorial.key'

# Uncomment if needed
#c.JupyterHub.base_url = '/somename/'
