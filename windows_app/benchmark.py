import time
import math

class Benchmark:
    def __init__(self, name):
        self.name = name
        self.initTime = None
        self.listTimes = []

    def startTimer(self):
        self.initTime = time.time()

    def stopTimer(self, bPrint=False):
        if self.initTime is None:
            raise Exception('(Benchmark) stopTimer was called before startTimer')

        timeElapsed = time.time() - self.initTime
        
        self.listTimes.append(timeElapsed)
        self.initTime = None

        if bPrint:
            print(f'BENCHMARK [{self.name}] | Time elapsed: {round(timeElapsed, 5)}s')

        return timeElapsed

    # def __del__(self):
    #     self.print()

    def print(self):
        print('deleted')
        if len(self.listTimes) == 0: return

        sum = 0
        maxValue = 0
        minValue = math.inf
        for val in self.listTimes:
            maxValue = val if val > maxValue else maxValue
            minValue = val if val < minValue else minValue
            sum += val

        print(f'----------BENCHMARK [{self.name}]----------')
        print(f'Average time: {round(sum / len(self.listTimes), 5)}s')
        print(f'Max time: {round(maxValue, 5)}s')
        print(f'Min time: {round(minValue, 5)}s')