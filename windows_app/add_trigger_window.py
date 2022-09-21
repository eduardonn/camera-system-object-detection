import os
import sys
import cv2 as cv
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont
from PyQt5.QtCore import Qt
import gatilhos
import layout
from image_manager import ImageManager
from area_painter import AreaPainter

class AddTriggerWindow(QWidget):
    def __init__(self, gatilhosWindow):
        super().__init__()
        self.gatilhosWindow = gatilhosWindow
        
        self.setGeometry(200, 50, 700, 440)
        self.setWindowTitle('Adicionar Gatilho')
        self.setFont(QFont("Times", 10))
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.setWindowIcon(QIcon(filePath + '/Assets/GatilhosIcone.png'))
        # self.setStyleSheet("background-color: lightgrey")

        self.bDrawing = False

        layout.addTriggerWindowLayout(self)

        h, w = ImageManager.frame.shape[:2]
        self.scaleFactor = .4
        self.camImgShape = (int(w * self.scaleFactor), int(h * self.scaleFactor))
        self.camImg.setMaximumSize(self.camImgShape[0], self.camImgShape[1])

        self.areaPainter = AreaPainter()
        # self.areaPainter = AreaPainter((int(h * self.scaleFactor), int(w * self.scaleFactor), 3))

        ImageManager.updateFrameEvent.append(self.updateFrame)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()
        if e.key() == Qt.Key_Z:
            self.areaPainter.deleteLastArea()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.areaPainter.startArea(self.camImg)
            self.bDrawing = True

    def mouseMoveEvent(self, e):
        if self.bDrawing:
            self.areaPainter.updateArea()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.bDrawing = False
            self.areaPainter.saveArea()

    def updateFrame(self, frame):
        h, w = ImageManager.frame.shape[:2]
        frameResized = cv.resize(frame, (int(w * self.scaleFactor), int(h * self.scaleFactor)))
        self.areaPainter.paintAreasAddGatilho(frameResized)

        height, width, _ = frameResized.shape
        bytesPerLine = 3 * width
        qImg = QImage(frameResized.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        image = QPixmap(qImg)
        self.camImg.setPixmap(image)

    def salvarGatilhoESair(self):
        try:
            float(self.timePermanencia.text())
        except:
            print('Tempo de permanência inválido:', self.timePermanencia.text())
            return

        if self.timePermanencia.text() == '':
            print('Tempo de permanência obrigatório')
            return

        if len(self.areaPainter.areas) == 0:
            print("Não há áreas desenhadas")
            return

        h, w = ImageManager.frame.shape[:2]
        h *=  self.scaleFactor
        w *=  self.scaleFactor
        print('h, w', h, w, '| type:', type(w))

        # Normaliza areas
        areaStartX = self.areaPainter.areas[0][0][0] / w
        areaStartY = self.areaPainter.areas[0][0][1] / h
        areaEndX = self.areaPainter.areas[0][1][0] / w
        areaEndY = self.areaPainter.areas[0][1][1] / h

        gatilhos.createGatilho(
            self.nomeGatilho.text(),
            self.timeFrom.time().toString()[:-3],
            self.timeTo.time().toString()[:-3],
            float(self.timePermanencia.text()),
            self.tipoAlarme.currentText(),
            areaStartX,
            areaStartY,
            areaEndX,
            areaEndY)

        ImageManager.instance.detector.updateDetectionArea()

        self.close()