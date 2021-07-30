cd /
randpass MND -o /usr/enable_mkuser
python /usr/local/bin/frame.py

#cp --update /home/passwd /home/group /home/shadow /etc/

# If we have a certificate directory...
if [ -d /etc/pki/tls/certs/tutorial.cer ]
then
  PORT=443
else
  PORT=80
fi
jupyterhub --ip 0.0.0.0 --port $PORT -f jup-config.py
