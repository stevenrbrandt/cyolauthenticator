cd /
randpass MND -o /usr/enable_mkuser
python /usr/local/bin/frame.py

#cp --update /home/passwd /home/group /home/shadow /etc/

PORT=443
jupyterhub --ip 0.0.0.0 --port $PORT -f jup-config.py
