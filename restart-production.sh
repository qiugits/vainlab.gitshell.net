git pull &

uwsgi --ini uwsgi.ini &

nginx -s reload
