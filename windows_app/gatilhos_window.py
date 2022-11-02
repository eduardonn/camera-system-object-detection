import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from add_trigger_window import AddTriggerWindow
import layout
import gatilhos
import css

class TriggersWindow(QWidget):
    resetTriggerUI = pyqtSignal(gatilhos.Trigger)

    def __init__(self, mainWindow):
        super().__init__()
        self.resetTriggerUI.connect(resetTriggerStyle)
        self.mainWindow = mainWindow
        
        self.setGeometry(300, 200, 700, 440)
        self.setWindowTitle('Gatilhos')
        filePath = __file__[:-len(os.path.basename(__file__))]
        self.setWindowIcon(QIcon(filePath + '/Assets/GatilhosIcone.png'))

        layout.gatilhosWindowLayout(self)

        gatilhos.Trigger.triggersWindow = self # Cria uma variável estática referenciando esta instância
        
        for gatilho in gatilhos.triggerList:
            layout.addTrigger(self, gatilho)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()
    
    def openDrawAreaWindow(self):
        self.drawAreaWindow = AddTriggerWindow(self)

def resetTriggerStyle(trigger):
    if trigger.widget is not None:
        trigger.widget.setStyleSheet(css.gatilhoPadrao)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TriggersWindow()
    sys.exit(app.exec_())