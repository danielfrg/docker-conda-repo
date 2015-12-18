nohup /opt/conda/bin/python /opt/watch.py /channel >> /var/log/watch.py.log 2>&1 &
nginx -g "daemon off;"
