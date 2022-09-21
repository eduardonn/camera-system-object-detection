import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont
from PyQt5.QtCore import Qt
from add_trigger_window import AddTriggerWindow
from image_manager import ImageManager
from gatilhos_window import GatilhosWindow
from detection_tester import DetectionTester
from area_painter import AreaPainter
from server import ServerConnection
import layout
import gatilhos
import css

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.filePath = __file__[:-len(os.path.basename(__file__))]
        self.initMainWindow()
        self.bVisualizarAreas = True
        self.gatilhosThread = gatilhos.initGatilhos(self.updateGatilhoState)
        self.imgManager = ImageManager()
        self.areaPainter = AreaPainter()
        self.server = ServerConnection(self.updateClientStatus)
        self.server.start()

        # Configurar imagem "sem sinal"
        frame = cv2.imread(self.filePath + "/Assets/sem_sinal.jpg")
        frameResized = cv2.resize(frame, (300, 300))
        height, width, _ = frameResized.shape
        bytesPerLine = 3 * width
        qImg = QImage(frameResized.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        image = QPixmap(qImg)
        self.camImg.setPixmap(image)

        self.initImgWidget()
        ImageManager.updateFrameEvent.append(self.updateFrame)

    def initMainWindow(self):
        self.setGeometry(50, 50, 1000, 440)
        self.setWindowTitle('Camera Surveillance System')
        self.setWindowIcon(QIcon(self.filePath + '/Assets/icone.png'))
        # self.setFont(QFont('Times', 10))
        # self.setStyleSheet("background-color: lightgrey")

        layout.initMainWindowLayout(self)

        # self.openGatilhosWindow()
        # self.openDrawAreaWindow()

    def initImgWidget(self):
        h, w = ImageManager.frame.shape[:2]

        maxImgHeight = 345
        newWidth = int(w * (float(maxImgHeight) / h))
        self.camImgShape = (newWidth, maxImgHeight)
        # self.camImg.setMaximumSize(self.camImgShape[0], self.camImgShape[1])

        # scaleFactor = .32
        # self.camImgShape = (int(w * scaleFactor), int(h * scaleFactor))
        # self.camImg.setMaximumSize(self.camImgShape[0], self.camImgShape[1])

        width, height = self.camImgShape
        bytesPerLine = 3 * width
        frameResized = cv2.resize(ImageManager.frame, self.camImgShape)
        # frameResized = cv.resize(ImageManager.frameBuffer[:], self.camImgShape)

        self.camImgQImage = QImage(frameResized.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.camImgPixmap = QPixmap(self.camImgQImage)
        self.camImg.setPixmap(self.camImgPixmap)

    def updateFrame(self, frame):
        frameResized = cv2.resize(frame, self.camImgShape)
        
        frameResized2 = cv2.resize(self.imgManager.detector.croppedFrame, self.camImgShape)
        self.camImg2.setMaximumSize(self.camImgShape[0], self.camImgShape[1])

        if self.btnViewGatilhos.isChecked():
            self.areaPainter.paintAreasMainImg(frameResized)

        width, height = self.camImgShape
        bytesPerLine = 3 * width
        self.camImgQImage = QImage(frameResized.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.camImgPixmap = QPixmap(self.camImgQImage)
        self.camImg.setPixmap(self.camImgPixmap)
        
        frameResized2 = np.array(frameResized2, dtype=np.uint8)
        height, width = frameResized2.shape[:2]
        bytesPerLine = 3 * width
        self.camImgQImage = QImage(frameResized2, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.camImgPixmap = QPixmap(self.camImgQImage)
        self.camImg2.setPixmap(self.camImgPixmap)

    def updateGatilhoState(self, gatilho: gatilhos.Gatilho, state):
        if gatilho.widget is not None:
            gatilho.widget.setStyleSheet(css.gatilhoAcionado if state else css.gatilhoPadrao)

        self.server.sendTrigger(gatilho)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_2:
            self.server.sendNotification()
        elif e.key() == Qt.Key_3:
            self.server.sendAlarm()
        elif e.key() == Qt.Key_Q:
            self.close()

    # def closeEvent(self, e):
        # self.imgManager.terminateDetectors() # Se for usado multiprocessing
        # pass

    def updateClientStatus(self, status):
        if status:
            self.lClientConnectedValue.setText('Connected')
            self.lClientConnectedValue.setStyleSheet(css.textGreen)
        else:
            self.lClientConnectedValue.setText('Disconnected')
            self.lClientConnectedValue.setStyleSheet(css.textRed)

    def openGatilhosWindow(self):
        self.gatilhosWindow = GatilhosWindow()
    
    def openDrawAreaWindow(self):
        self.drawAreaWindow = AddTriggerWindow()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())