import time
import sys

class ProgressBar:
    def __init__(self, title, maximum, sign):
        self.title = title
        self.maximum = maximum
        self.sign = sign
        self.LENGTH = 50
        self.i = 0

    def start(self):
        self.start = time.time()
        self.printBar(0)

    def update(self):
        self.i += 1
        progress = (50 * self.i) / self.maximum
        self.printBar(progress)

    def printBar(self, progress):
        percentage = (self.i * 100) / self.maximum
        bar = "\r%s: %.2f %% [%s%s] Time Left: %s" % (
            self.title,
            percentage,
            (self.sign * progress),
            (" " * (self.LENGTH - progress)),
            self.timeLeft()
        )
        print bar,
        sys.stdout.flush()

    def timeLeft(self):
        duration = time.time() - self.start
        eta = 0
        if self.i != 0:
            eta = (duration * self.maximum) / self.i
        left = eta - duration
        return self.convertTime(left)

    @staticmethod
    def convertTime(number):
        hours = number / 3600
        minutes = (number % 3600) / 60
        seconds = number % 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
