#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static
sudo apt-get update -y
sudo apt-get install nginx -y
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "test your Nginx configuration Airbnb_v2" > /data/web_static/releases/test/index.html
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data

printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root   /var/www/html;
    index  index.html index.htm;
    add_header X-Served-By $HOSTNAME;
    location /redirect_me {
        return 301 https://www.youtube.com;
    }
    error_page 404 /page404.html;
    location = /page404.html {
        root /usr/share/nginx/html;
        internal;
    }
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}" > /etc/nginx/sites-enabled/default
sudo service nginx restart
