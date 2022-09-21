import sys
import os
import layout
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from add_trigger_window import AddTriggerWindow
import gatilhos

class GatilhosWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(300, 200, 700, 440)
        self.setWindowTitle('Gatilhos')
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.setWindowIcon(QIcon(filePath + '/Assets/GatilhosIcone.png'))

        layout.gatilhosWindowLayout(self)

        gatilhos.Gatilho.gatilhosWindow = self # Cria uma variável estática referenciando esta instância
        
        for gatilho in gatilhos.listaGatilhos:
            layout.addGatilho(self, gatilho)
        # self.openDrawAreaWindow()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()
    
    def openDrawAreaWindow(self):
        self.drawAreaWindow = AddTriggerWindow(self)

    # def addGatilho(self, *args):
    #     gatilho = Gatilho(0, *args[:5], args[5][0][0], args[5][0][1], args[5][1][0], args[5][1][1])
    #     db.createGatilho(gatilho)
    #     lm.addGatilho(self, gatilho)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GatilhosWindow()
    sys.exit(app.exec_())