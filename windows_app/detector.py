import os
import numpy as np
import time
import cv2
import math
from PyQt5.QtCore import QThread, pyqtSignal
from benchmark import Benchmark
import gatilhos

class SSDDetector(QThread):
    def __init__(self, frame, onFrameProcessed):
        super(SSDDetector, self).__init__()
        self.blobSize = 400
        self.frame = frame
        self.bDetect = True
        self.detections = None
        self.onFrameProcessed = onFrameProcessed # Evento chamado após o término de uma detecção
        self.resizeStartPoint = None
        self.resizeEndPoint = None
        self.croppedFrame = self.frame
        # self.finishDetectionSignal = pyqtSignal(str)
        # self.finishDetectionSignal.connect(utils.printLog)
        self.aspectRatio = self.croppedFrame.shape[1] / self.croppedFrame.shape[0]

        self.updateDetectionArea()

        # Get root folder
        rootFolder = __file__[:-len(os.path.basename(__file__))]
        PROTOTXT = rootFolder + "/neural_networks/MobileNetSSD_deploy.prototxt"
        MODEL = rootFolder + "/neural_networks/MobileNetSSD_deploy.caffemodel"
        GPU_SUPPORT = 0

        self.net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
        if GPU_SUPPORT:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def run(self):
        benchmark = Benchmark('Detector')

        while(True):
            if self.bDetect:
                benchmark.startTimer()
                if len(gatilhos.listaGatilhos) != 0:
                    detections = self.detect(self.croppedFrame)

                    self.detections = self.convertCoordsCroppedToOriginal(detections)

                    # Ao terminar uma detecção, chama função
                    self.onFrameProcessed(self.detections)
                    # self.finishDetectionSignal.emit(benchmark.stopTimer(bPrint=False))

                benchmark.stopTimer(True)
                time.sleep(.01)
            else:
                time.sleep(0.5)

    def detect(self, frame):
        blobSize = (int(self.blobSize * self.aspectRatio), self.blobSize)
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, blobSize, 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        return detections

    def convertCoordsCroppedToOriginal(self, detections):
        '''
        Converte coordenadas (normalizadas) das bounding boxes de croppedFrame para o frame em tamanho normal
        '''
        croppedFrameHeight, croppedFrameWidth = self.croppedFrame.shape[:2]
        frameHeight, frameWidth = self.frame.shape[:2]
        for i in np.arange(0, detections.shape[2]):
            idx = int(detections[0, 0, i, 1])
            if idx != 15: continue

            detections[0, 0, i, 3] = (detections[0, 0, i, 3] * croppedFrameWidth + self.resizeStartPoint[1]) / frameWidth
            detections[0, 0, i, 4] = (detections[0, 0, i, 4] * croppedFrameHeight + self.resizeStartPoint[0]) / frameHeight
            detections[0, 0, i, 5] = (detections[0, 0, i, 5] * croppedFrameWidth + self.resizeStartPoint[1]) / frameWidth
            detections[0, 0, i, 6] = (detections[0, 0, i, 6] * croppedFrameHeight + self.resizeStartPoint[0]) / frameHeight

        return detections

    
    def updateDetectionArea(self):
        '''
        Calcula a área em que deve ser realizada detecções
        '''
        if len(gatilhos.listaGatilhos) == 0: return

        startPoint = [math.inf, math.inf]
        endPoint = [-math.inf, -math.inf]

        for gatilho in gatilhos.listaGatilhos:
            if gatilho.areaStartY < startPoint[0]:
                startPoint[0] = gatilho.areaStartY
            if gatilho.areaEndY > endPoint[0]:
                endPoint[0] = gatilho.areaEndY
            if gatilho.areaStartX < startPoint[1]:
                startPoint[1] = gatilho.areaStartX
            if gatilho.areaEndX > endPoint[1]:
                endPoint[1] = gatilho.areaEndX
        
        h, w = self.frame.shape[:2]

        # Transforma pontos normalizados para pixels
        self.resizeStartPoint = (int(startPoint[0] * h), int(startPoint[1] * w))
        self.resizeEndPoint = (int(endPoint[0] * h), int(endPoint[1] * w))

        self.croppedFrame = self.frame[
            self.resizeStartPoint[0]:self.resizeEndPoint[0],
            self.resizeStartPoint[1]:self.resizeEndPoint[1],
            :
        ]
        self.aspectRatio = self.croppedFrame.shape[1] / self.croppedFrame.shape[0]
