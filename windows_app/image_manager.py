import os
import time
import cv2
from queue import Queue
from PyQt5.QtCore import QThread
from blob_size_tester import BlobSizeTester as dt
from benchmark import Benchmark

class ImageManager:
    onUpdateFrame = []
    onVideoEnd = []
    frameResolution = (300, 300)

    def __init__(self, maxBufferSize):
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.isVideo = True
        if self.isVideo:
            self.cap = cv2.VideoCapture(filePath + '/recordings/tests/Estabelecimento Dia.mp4')
            self.playRange = (0, 999999) # Video start-end in ms
            self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
        else:
            self.cap = cv2.VideoCapture(0)
        self.isVideoPaused = False
        self.bVideoEnded = False
        self.imageBuffer = Queue(maxsize=maxBufferSize)
        ret, self.lastFrameRead = self.cap.read()
        if not ret:
            raise Exception('Reading image failed')
        ImageManager.frameResolution = self.lastFrameRead.shape[:2]
        self.frametime = 1 / 30 # 1 / FPS
        self.showPersonTester = False
        self.personTesterSize = 2
        dt.addTesterToList((.5, .5))

        self.readFrameThread = QThread()
        self.readFrameThread.run = self.readFrame
        self.readFrameThread.start()

        self.feedFrameThread = QThread()
        self.feedFrameThread.run = self.feedFrame
        self.feedFrameThread.start()

    def readFrame(self) -> None:
        """
        1. Read images from cameras
        2. Put in the buffer
        """
        while True:
            if self.imageBuffer.full():
                time.sleep(0.05)
                continue

            ret, frame = self.cap.read()
            
            if self.isVideo and (not ret or self.cap.get(cv2.CAP_PROP_POS_MSEC) > self.playRange[1]):
                self.bVideoEnded = True
                self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
                time.sleep(0.1)
                continue
                
            self.imageBuffer.put(frame)

    def feedFrame(self) -> None:
        '''
        Deliver frames to subscribed functions
        '''
        lastFrameTime = time.time()

        while True:
            initTime = time.time()

            if self.showPersonTester:
                self.lastFrameRead = dt.drawPeople(self.lastFrameRead, self.personTesterSize)

            for function in self.onUpdateFrame:
                function(self.lastFrameRead)

            if self.isVideoPaused:
                time.sleep(0.2)
                continue
                    
            self.lastFrameRead = self.imageBuffer.get()

            while self.lastFrameRead is None:
                time.sleep(0.05)
                self.lastFrameRead = self.imageBuffer.get()

                if self.bVideoEnded:
                    for function in self.onVideoEnd:
                        function()
                    # os._exit(0)

            # time.sleep(0.005)
            # print('DeltaTime:', time.time() - lastFrameTime)
            # lastFrameTime = time.time()
            
            sleepTime = self.frametime - (time.time() - initTime)
            if sleepTime > 0.011:
                time.sleep(sleepTime - 0.011)

    def setShowPersonTester(self, value):
        self.showPersonTester = value

    def setPersonTesterSize(self, value):
        self.personTesterSize = value

    def togglePauseVideo(self):
        self.isVideoPaused = not self.isVideoPaused
    
    # def terminateDetectors(self):
    #     for p in self.detectorProcesses:
    #         p.terminate()
