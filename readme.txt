SSHer

This program has been developed by import as a substitution to Hydra for easiness of use.

It uses threading to bruteforce SSH connection of machines that used default credentials. It is NOT RECOMMENDED to use this program to bruteforce multiple usernames and passwords, it is prepared to handle mostly short lists while being really fast.
It relies on paramiko to attempt to connect to port [default 22] and bruteforce the SSH connection.

Dependencies:
	- paramiko

Default settings:
	- Port: 22
	- Threads: 25
	- Output: cracked_ips.txt
	- Verbose: False

Samples:
	python -u root -p toor -M ips.txt -t 20
	python -u usernames.txt -p passwords.txt -M ips.txt -o kaliMachines.txt
	python -u admin -p admin -M ips.txt --verbose --port=1000


