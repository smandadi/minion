import yaml
import zipfile
import os
import paramiko
from getpass import getpass


def create_zipfile():
    """Create a package of all the files to be exported."""
    zf = zipfile.ZipFile("setup.zip", "w")
    for d, sd, f in os.walk("resource"):
        zf.write(d)
        for filename in f:
            zf.write(os.path.join(d, filename))
    zf.close()


def connect_to_server(host, user, passd):
    """Connect to the server, deploy the package and install the package"""
    paramiko.util.log_to_file('setup.log')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=passd)
    sftp = client.open_sftp()
    sftp.put("setup.zip", "setup.zip")
    sftp.close()
    stdin, stdout, stderr = client.exec_command('unzip setup.zip')
    stdin, stdout, stderr = client.exec_command('bash resource/setup.sh 2>&1 | tee install.log')
    client.close()


def run(host, user, passd):
    """Execute the functions in order"""
    if len(passd) == 0:
        passd = getpass('Please enter the password for server: ')
    connect_to_server(host, user,passd)


if __name__ == "__main__":

    create_zipfile()
    with open('config.yml') as data:
        data = yaml.load(data)
        for i in data['instances']:
            run(i['name'], i['user'], i['passd'])
