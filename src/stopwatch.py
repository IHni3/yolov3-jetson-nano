import time

# class for time measurement
class Stopwatch:
    def __init__(self):
        self.start_time = time.time()
    def start(self):
        self.start_time = time.time()
    def diffInMs(self, decimals=2):
        return round(self.diffInSec() * 1000 * pow(10,decimals)) / pow(10,decimals)
    def diffInSec(self):
        return time.time() - self.start_time
    def message(self, message):
        return message + ": " + str(self.diffInMs()) + " ms"