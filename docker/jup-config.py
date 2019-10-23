#import os

c.JupyterHub.authenticator_class = 'cyolauthenticator.CYOLAuthenticator'
c.JupyterHub.template_paths = ['/jinja/templates']

# openssl genrsa -out rootCA.key 2048
# openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem

import os
if os.path.exists('/etc/pki/tls/certs/tutorial.cer'):
  c.JupyterHub.ssl_cert = '/etc/pki/tls/certs/tutorial.cer'
  c.JupyterHub.ssl_key =  '/etc/pki/tls/private/tutorial.key'

# Uncomment if needed
#c.JupyterHub.base_url = '/somename/'
