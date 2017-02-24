import time
import sys

class ProgressBar():
    i = 0

    def __init__(self, title, maximum, sign):
        self.title = title
        self.maximum = maximum
        self.sign = sign
        self.LENGTH = 50

    def start(self):
        self.start = time.time()
        self.printBar(0)

    def update(self):
        self.i += 1
        progress = (50 * self.i) / self.maximum
        self.printBar(progress)

    def printBar(self, progress):
        percentage = (self.i * 100) / self.maximum
        print "\r" + self.title + ": " + str(percentage)  + "%  [" + (self.sign * progress) + (" " * (self.LENGTH - progress)) + "] Time Left: " + self.timeLeft(),
        sys.stdout.flush()

    def timeLeft(self):
        duration = time.time() - self.start
        eta = 0
        if self.i != 0:
            eta = (duration * self.maximum) / self.i
        left = eta - duration
        return self.convertTime(left)

    def convertTime(self, number):
        hours = number / 3600;
        minutes = (number % 3600) / 60;
        seconds = number % 60;
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

