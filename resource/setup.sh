#!/bin/bash

### functions:
function update_nginx_files()
{
 mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.old
 host_name=`hostname -i`
 sed -i.bak s/myipaddress/$host_name/ resource/default
 cp resource/default /etc/nginx/sites-available/default

}

function copy_php_files()
{
    cp resource/*.php /usr/share/nginx/html/
}

function check_for_nginx()
{
    if [[ ! -z /etc/nginx ]]; then
        apt-get install -y nginx
    else
        echo "Nginx already installed on the server."
    fi
    update_nginx_files
    copy_php_files
}

function check_for_php()
{
    if [[ ! -z /etc/php5 ]]; then
        apt-get install -y php5-fpm
    else
        echo "php5 already installed on the server."
    fi
}


function open_ports()
{
    iptables -I INPUT -p tcp --dport 80 --syn -j ACCEPT
}

function start()
{
    sudo service php5-fpm restart
    sudo service nginx restart
}


### Main
check_for_nginx
check_for_php
open_ports
start

