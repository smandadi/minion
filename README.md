## Synopsis

   - Minion is a simple tool which can be used for configuration management, and it    drives inspiration from salt stack/Anisible.
   - Minion can be used to setup a light weight webserver and run php files.

## Logic
   - setup.py will package "resource" directory into a setup.zip file.
   - setup.zip file is deployed to minion clients, which is then unzipped.
   - setup.zip has a setup.sh, php and nginx conf file(s).
   - setup.sh is a small script, that runs and installs nginx, php5-fpm and configures nginx to use new config file.

## Run

	## Step:1 (Set config.yml)
		- Under "config.yml" add server name, username and password (optional).
	## Step:2 (Add php files to resources)
		- Add all the php files which you wanna upload to resources folder.
	## Step:3 (Run ./setup.py)
		- Then thats it run "python setup.py" --> This should install stuff

## Tests

	curl -sv [hostname] -- should return 200 ok
	Example:
	$ curl -sv 52.23.171.74
	* Rebuilt URL to: 52.23.171.74/
	*   Trying 52.23.171.74...
	* Connected to 52.23.171.74 (52.23.171.74) port 80 (#0)
	> GET / HTTP/1.1
	> Host: 52.23.171.74
	> User-Agent: curl/7.43.0
	> Accept: */*
	>
	< HTTP/1.1 200 OK
	< Server: nginx/1.4.6 (Ubuntu)
	< Date: Mon, 09 May 2016 05:14:19 GMT
	< Content-Type: text/plain
	< Transfer-Encoding: chunked
	< Connection: keep-alive
	< X-Powered-By: PHP/5.5.9-1ubuntu4.16
	<
	Hello, world!
	* Connection #0 to host 52.23.171.74 left intact


## Limitations/Pre-requisites

	- Can only run on ubuntu
	- Can only setup php files (Can be extended for more.)

## REFERENCE
- https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-12-04
- https://github.com/paramiko/paramiko