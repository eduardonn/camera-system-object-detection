import os
import time
import numpy as np
import cv2
from PyQt5.QtCore import QThread
import gatilhos

class ImageManager:
    onUpdateFrame = []
    instance = None
    frameResolution = (300, 300)

    def __init__(self):
        ImageManager.instance = self
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.cap = cv2.VideoCapture(filePath + '/recordings/Estabelecimento1.mp4')
        self.cap.set(cv2.CAP_PROP_POS_MSEC, 9000)
        ret, frame = self.cap.read()
        if not ret:
            raise Exception('Read image failed')
        ImageManager.frameResolution = frame.shape[:2]
        self.frametime = 1 / 30 # 1 / FPS

        self.updateFrameThread = QThread()
        self.updateFrameThread.run = self.updateFrame
        self.updateFrameThread.start()

    def updateFrame(self) -> None:
        """
        1. Capta imagem das câmeras
        2. Desenha detecções
        3. Chama funções inscritas no evento onUpdateFrame
        """
        while (True):
            initTime = time.time()
            ret, frame = self.cap.read()

            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_MSEC, 0)
                continue

            for func in self.onUpdateFrame:
                # if self.bDrawDetections & self.detector.bDetect:
                #     # func.emit(self.drawDetections())
                #     func(self.drawDetections(frame))
                # else:
                #     # func.emit(frame)
                func(frame)

            # Calcula o tempo de sleep necessário para manter 30 fps
            # sleepTime = self.frametime - (time.time() - initTime)
            # print(f"frametime: {time.time() - initTime} | sleepTime: {sleepTime}")
            # time.sleep(sleepTime if sleepTime > 0.005 else 0.005)
    
    # def terminateDetectors(self):
    #     for p in self.detectorProcesses:
    #         p.terminate()
