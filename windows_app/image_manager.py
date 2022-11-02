import os
import time
import cv2
from PyQt5.QtCore import QThread
from blob_size_tester import BlobSizeTester as dt

class ImageManager:
    onUpdateFrame = []
    onVideoEnd = []
    instance = None
    frameResolution = (300, 300)

    def __init__(self, onVideoEnd):
        ImageManager.instance = self
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.cap = cv2.VideoCapture(filePath + '/recordings/Estabelecimento Dia.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Estabelecimento Noite.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Residencia Noite.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Top.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Top 2.mp4')
        # self.cap = cv2.VideoCapture(filePath + '/recordings/Bottom.mp4')
        # self.playRange = (2000, 30000)
        self.playRange = (24000, 40000)
        # self.playRange = (70000, 75000)
        # self.playRange = (272000, 290000)
        self.playRange = (8000, 10000)
        # self.playRange = (0, 9999999)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
        self.isVideoPaused = False
        self.onVideoEnd.append(onVideoEnd)
        ret, self.frame = self.cap.read()
        if not ret:
            raise Exception('Read image failed')
        ImageManager.frameResolution = self.frame.shape[:2]
        self.frametime = 1 / 30 # 1 / FPS
        self.showPersonTester = False
        self.personTesterSize = 150

        self.updateFrameThread = QThread()
        self.updateFrameThread.run = self.updateFrame
        self.updateFrameThread.start()

    def updateFrame(self) -> None:
        """
        1. Capta imagem das câmeras
        2. Desenha detecções
        3. Chama funções inscritas no evento onUpdateFrame
        """
        while True:
            if self.isVideoPaused:
                for func in self.onUpdateFrame:
                    func(self.frame)

                time.sleep(0.2)
                continue

            initTime = time.time()
            ret, self.frame = self.cap.read()
            
            # Loop video
            if not ret or self.cap.get(cv2.CAP_PROP_POS_MSEC) > self.playRange[1]:
                self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
                for function in self.onVideoEnd:
                    function()
                continue

            if self.showPersonTester:
                self.frame = dt.drawPerson(self.frame, self.personTesterSize)

            for func in self.onUpdateFrame:
                func(self.frame)

            # Calcula o tempo de sleep necessário para manter 30 fps
            sleepTime = self.frametime - (time.time() - initTime)
            # print(f"frametime: {time.time() - initTime} | sleepTime: {sleepTime}")
            time.sleep(sleepTime if sleepTime > 0.005 else 0.005)

    def setShowPersonTester(self, value):
        self.showPersonTester = value

    def setPersonTesterSize(self, value):
        self.personTesterSize = value

    def togglePauseVideo(self):
        self.isVideoPaused = not self.isVideoPaused
    
    # def terminateDetectors(self):
    #     for p in self.detectorProcesses:
    #         p.terminate()
