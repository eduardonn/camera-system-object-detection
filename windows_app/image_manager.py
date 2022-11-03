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
    instance = None
    frameResolution = (300, 300)

    def __init__(self, onVideoEnd, maxBufferSize):
        ImageManager.instance = self
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.onVideoEnd.append(onVideoEnd)
        self.cap = cv2.VideoCapture(filePath + '/recordings/Estabelecimento Dia.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Estabelecimento Noite.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Residencia Noite.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Top.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Top 2.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Bottom.mp4')
        self.playRange = (2000, 30000) # Estabelecimento Dia
        # self.playRange = (24000, 40000)
        # self.playRange = (70000, 75000)
        # self.playRange = (272000, 290000)
        # self.playRange = (19000, 50000) # Top 2 - 300
        # self.playRange = (000, 50000) # Bottom
        # self.playRange = (0, 9999999)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
        self.isVideoPaused = False
        self.imageBuffer = Queue(maxsize=maxBufferSize)
        ret, self.lastFrame = self.cap.read()
        if not ret:
            raise Exception('Read image failed')
        ImageManager.frameResolution = self.lastFrame.shape[:2]
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
                time.sleep(0.02)
                continue

            ret, frame = self.cap.read()
            
            # Loop video
            if not ret or self.cap.get(cv2.CAP_PROP_POS_MSEC) > self.playRange[1]:
                self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
                for function in self.onVideoEnd:
                    function()
                continue
                
            self.imageBuffer.put(frame)
            # print('queue size:', self.imageBuffer._qsize())

            # time.sleep(0.3)

    def feedFrame(self) -> None:
        '''
        Deliver frames to subscribed functions
        '''
        # lastFrame = 

        while True:
            if self.isVideoPaused:
                for function in self.onUpdateFrame:
                    if self.showPersonTester:
                        self.lastFrame = dt.drawPeople(self.lastFrame, self.personTesterSize)
                    else:
                        self.lastFrame = self.lastFrame
                    function(self.lastFrame)

                time.sleep(0.2)
                continue

            if self.showPersonTester:
                self.lastFrame = dt.drawPeople(self.lastFrame, self.personTesterSize)

            for function in self.onUpdateFrame:
                function(self.lastFrame)

            self.lastFrame = self.imageBuffer.get()

            # time.sleep(0.005)
            # time.sleep(self.frametime)

    def setShowPersonTester(self, value):
        self.showPersonTester = value

    def setPersonTesterSize(self, value):
        self.personTesterSize = value

    def togglePauseVideo(self):
        self.isVideoPaused = not self.isVideoPaused
    
    # def terminateDetectors(self):
    #     for p in self.detectorProcesses:
    #         p.terminate()
