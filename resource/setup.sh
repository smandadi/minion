#!/bin/bash

set -e

echo "Check/Install nginx..."
if [[ -z /etc/nginx ]]; then
   echo "Installing nginx"
   apt-get install -y nginx
else
   echo "Nginx already installed on the server."
fi
if [[ -z /etc/nginx/sites-available/default ]]; then
    mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.old
fi
host_name=`hostname -i`
sed -i.bak s/myipaddress/$host_name/ resource/default
echo "Setting up nginx conf."
cp resource/default /etc/nginx/sites-available/default
echo "Copying index.php files...:"
cp resource/*.php /usr/share/nginx/html/

echo "Check/Install php5-fpm..."
if [[ -z /etc/php5 ]]; then
   echo "Installing php5..."
   apt-get install -y php5-fpm
else
   echo "php5 already installed on the server."
fi

echo "Opening the ports...."
iptables -I INPUT -p tcp --dport 80 --syn -j ACCEPT


echo "Restarting Nginx and php5 services....."
sudo service php5-fpm restart
sudo service nginx restart

