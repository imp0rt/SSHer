#!usr/bin/python2.7
import optparse


class getInput:
    def __init__(self):
        self.config = {
            "machines": [],
            "username": [],
            "password": [],
            "output": "cracked_ips.txt",
            "threads": 10,
            "verbose": False,
            "port": 22
        }

    @staticmethod
    def checkFile(filename):
        if filename.endswith(".txt"):
            return True
        return False

    def checkInput(self):
        parser = optparse.OptionParser("%prog -u <username> -p <password> -M <machines> [-t <threads>]")
        parser.add_option("-M", dest="machines", help="specify machines file")
        parser.add_option("-u", dest="username", help="username to test")
        parser.add_option("-p", dest="password", help="password to test")
        parser.add_option("-o", dest="output", help="specify successful credentials filename")
        parser.add_option("-t", dest="threads", help="number of threads [10]")
        parser.add_option("--port", dest="port", help="specify SSH port [22]")
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                          help="get status of every connection attempt [False]")
        (options, args) = parser.parse_args()
        self.saveInput(parser, options)
        self.printInformation()
        return self.config

    def saveInput(self, parser, options):
        if not (options.machines and options.username and options.password):
            parser.print_help()
            exit(0)

        self.readFile(options.machines, "machines")
        self.addOption(options.username, "username")
        self.addOption(options.password, "password")

        self.config["output"] = "cracked_ips.txt"
        self.config["threads"] = 25

        if options.output:
            if self.checkFile(options.output):
                self.config["output"] = options.output
            else:
                print("[-] File format is not valid, outputting to default %s" % (self.config["machines"]))
        if options.threads:
            self.config["threads"] = int(options.threads)
        if options.verbose:
            self.config["verbose"] = True
        if options.port:
            self.config["port"] = int(options.port)

    # Convert filename to array of lines
    def addOption(self, option, parameter):
        if self.checkFile(option):
            self.readFile(option, parameter)
        else:
            self.config[parameter].append(option.replace("None", " "))

    # Read file and save its contents to the proper parameter
    def readFile(self, filename, parameter):
        realfile = open(filename, "r")
        values = realfile.read().splitlines()
        self.config[parameter] = filter(None, [v.replace("None", " ") for v in values])
        realfile.close()

    # Print configuration
    def printInformation(self):
        print("Attacking with configuration:")
        print("\tMachines: %s" % (len(self.config["machines"])))
        print("\tThreads: %s" % (self.config["threads"]))
        print("\tOutput: %s" % self.config["output"])
        print("\n")
