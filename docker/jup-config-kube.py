#import os

c.JupyterHub.authenticator_class = 'cyolauthenticator.CYOLAuthenticator'
c.JupyterHub.template_paths = ['/jinja/templates']

# eg from https://github.com/GoogleCloudPlatform/gke-jupyter-classroom/blob/master/jupyterhub/jupyterhub_config.py
c.JupyterHub.hub_ip = '0.0.0.0'

import kubespawner
c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.debug = True

c.KubeSpawner.profile_list = [
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
