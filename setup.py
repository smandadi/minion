#!/usr/bin/python

import zipfile
import os
import paramiko
from time import sleep
from getpass import getpass
from yaml import load


def create_zipfile():
    """Create a package of all the files to be exported."""
    zf = zipfile.ZipFile("setup.zip", "w")
    for d, sd, f in os.walk("resource"):
        zf.write(d)
        for filename in f:
            zf.write(os.path.join(d, filename))
    zf.close()


def restart_server(host, user, passd):
    """Restart the minion client server."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=passd)
    client.exec_command('reboot -h')
    sleep(120)


def connect_to_server(host, user, passd):
    """Connect to the server, deploy the package and install the package"""
    print "#" * 100
    print "Updating server: ", host
    print "#" * 100
    paramiko.util.log_to_file('setup.log')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=passd)
    stdin, stdout, stderr = client.exec_command("df -H / | awk {'print $5'} | tail -1 | cut -d'%' -f1")
    result = stdout.readline()
    if int(result) > 95:
        print "Restarting %r, disk is almost full" % host
        restart_server(host, user, passd)
        client.connect(host, username=user, password=passd)
    sftp = client.open_sftp()
    sftp.put("setup.zip", "setup.zip")
    sftp.close()
    stdin, stdout, stderr = client.exec_command('unzip setup.zip')
    #result = stdout.channel.recv_exit_status
    #if int(result) != 0:
    #   print "Unable to execute the script, Please manually check the server for errors."
    print stdout.readline()
    stdin, stdout, stderr = client.exec_command('bash resource/setup.sh 2>&1 | tee install.log')
    print "output:", stdout.readline()
    client.close()


def run(host, user, passd):
    """Execute the functions in order"""
    if len(passd) == 0:
        passd = getpass('Please enter the password for server: ')
    connect_to_server(host, user,passd)


if __name__ == "__main__":

    create_zipfile()
    with open('config.yml') as data:
        data = load(data)
        for i in data['instances']:
            run(i['name'], i['user'], i['passd'])