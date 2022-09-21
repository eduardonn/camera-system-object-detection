import os
import time
import numpy as np
import cv2
from PyQt5.QtCore import QThread
from detector import SSDDetector
import gatilhos

class ImageManager:
    updateFrameEvent = []
    frame = None
    instance = None

    def __init__(self):
        ImageManager.instance = self
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.cap = cv2.VideoCapture(filePath + '/recordings/Estabelecimento1.mp4')
        self.cap.set(cv2.CAP_PROP_POS_MSEC, 9000)
        # self.detectorProcesses = []
        self.frametime = 1 / 30 # 1 / FPS
        self.bDrawDetections = True
        self.filePath = __file__[:-len(os.path.basename(__file__))]
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
                        "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike",
                        "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
        self.detectionColor = (0, 0, 200)
        self.confidenceDrawDetection = .4

        ret, ImageManager.frame = self.cap.read()

        if ret:
            self.detector = SSDDetector(ImageManager.frame, gatilhos.updateGatilhosDetection)
            self.detector.start()

            self.updateFrameThread = QThread()
            self.updateFrameThread.run = self.updateFrame
            self.updateFrameThread.start()
        else:
            print("[ERROR] Detector creation failed")

    def updateFrame(self) -> None:
        """
        1. Capta imagem das câmeras
        2. Desenha detecções
        3. Chama funções inscritas no evento updateFrameEvent
        """
        while (True):
            initTime = time.time()
            ret, frame = self.cap.read()

            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_MSEC, 0)
                continue

            ImageManager.frame[:] = frame

            for func in self.updateFrameEvent:
                if self.bDrawDetections & self.detector.bDetect:
                    func(self.drawDetections())
                else:
                    func(ImageManager.frame)

            # Calcula o tempo de sleep necessário para manter 30 fps
            sleepTime = self.frametime - (time.time() - initTime)
            # print(f"frametime: {time.time() - initTime} | sleepTime: {sleepTime}")
            time.sleep(sleepTime if sleepTime > 0 else 0.005)

    def drawDetections(self):
        if self.detector.detections is None: return ImageManager.frame

        frame = np.array(ImageManager.frame, dtype=np.uint8)

        h, w = frame.shape[:2]
        for i in np.arange(0, self.detector.detections.shape[2]):
            idx = int(self.detector.detections[0, 0, i, 1])
            if idx != 15: continue # Se não for pessoa

            confidence = self.detector.detections[0, 0, i, 2]
            if confidence > self.confidenceDrawDetection:
                box = self.detector.detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), self.detectionColor, 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.detectionColor, 2)
        
        return frame
    
    # def terminateDetectors(self):
    #     for p in self.detectorProcesses:
    #         p.terminate()
