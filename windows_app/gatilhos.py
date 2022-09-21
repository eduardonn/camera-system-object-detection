"""
Gatilhos
========

1. Define classe Gatilho
2. Mantém lista de gatilhos
3. Atualiza gatilhos periodicamente
"""

import numpy as np
import time
import sip
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import database as db
import css
import layout

listaGatilhos = []

class Gatilho:
    gatilhosWindow = None

    def __init__(
            self,
            id,
            nome,
            horarioInicial,
            horarioFinal,
            tempoPermanencia,
            acao,
            areaStartX,
            areaStartY,
            areaEndX,
            areaEndY):
        self.id = id
        self.nome = nome
        self.horarioInicial = horarioInicial
        self.horarioFinal = horarioFinal
        self.tempoPermanencia = tempoPermanencia
        self.acao = acao
        self.areaStartX = areaStartX
        self.areaStartY = areaStartY
        self.areaEndX = areaEndX
        self.areaEndY = areaEndY
        self.labelTempoPermaneceu = 0
        self.tempoPermaneceu = .0
        self.acionado = False
        self.detectionLastTime = time.time()
        self.bDetectionInside = False
        self.widget = None
        self.lTempoPermaneceu = None
        self.camera = 0

    def remove(self):
        print("removendo id:", self.id)

        db.deleteGatilho(self.id)
        Gatilho.gatilhosWindow.vBoxGatilhos.removeWidget(self.widget)
        listaGatilhos.remove(self)
        sip.delete(self.widget)
        self.widget = None
        db.printDB()

    def reset(self):
        self.tempoPermaneceu = .0
        self.acionado = False

        if self.widget is not None:
            self.widget.setStyleSheet(css.gatilhoPadrao)

        if self.lTempoPermaneceu is not None:
            self.lTempoPermaneceu.setText(str(round(self.tempoPermaneceu, 3)))

    def print(self):
        print('GATILHO:',
                self.id,
                self.nome,
                self.horarioInicial,
                self.horarioFinal,
                self.tempoPermanencia,
                self.acao,
                self.areaStartX,
                self.areaStartY,
                self.areaEndX,
                self.areaEndY)
    
class UpdateGatilhosThread(QThread):
    changeGatilhoStateSignal = pyqtSignal(Gatilho, bool) # Necessário pois mudanças na UI devem ocorrer na thread principal

    def run(self):
        '''Atualiza gatilhos a cada THREAD_TIME_SLEEP segundos'''
        
        THREAD_TIME_SLEEP = 0.1 # Tempo (em segundos) que a thread irá dormir e incrementar o tempo que detecções permaneceram
        TIME_INC_LAST_DETECTION = 0.5 # Continuar incrementando o tempo que permaneceu até esse tempo (em segundos)
        TIME_LIMIT_TO_RESET = 10 # Se passar esse tempo (em segundos), o gatilho resetará

        while(True):
            for gatilho in listaGatilhos:
                if not gatilho.bDetectionInside: continue
                timeSinceLastDetection = time.time() - gatilho.detectionLastTime
                if timeSinceLastDetection > TIME_INC_LAST_DETECTION: continue

                gatilho.tempoPermaneceu += THREAD_TIME_SLEEP

                if gatilho.lTempoPermaneceu is not None:
                    gatilho.lTempoPermaneceu.setText(str(round(gatilho.tempoPermaneceu, 3)))
                
                if gatilho.acionado: continue
                if timeSinceLastDetection > TIME_LIMIT_TO_RESET:
                    gatilho.reset()

                # Testa se disparou
                if gatilho.tempoPermaneceu > gatilho.tempoPermanencia and not gatilho.acionado:
                    gatilho.acionado = True
                    print(f'GATILHO [{gatilho.nome}] DISPAROU')

                    self.changeGatilhoStateSignal.emit(gatilho, True)

            time.sleep(THREAD_TIME_SLEEP)

def initGatilhos(updateGatilhoState):
    global listaGatilhos
    listaGatilhos.clear()

    for gatilho in db.selectGatilhos():
        gatilhoClass = Gatilho(*gatilho)
        listaGatilhos.append(gatilhoClass)
        # layout.addGatilho(gatilhosWindow, gatilhoClass)

    thread = UpdateGatilhosThread()
    thread.changeGatilhoStateSignal.connect(updateGatilhoState)
    thread.start()

    return thread

def createGatilho(*args):
    gatilho = Gatilho(-1, *args)
    db.createGatilho(gatilho)
    layout.addGatilho(Gatilho.gatilhosWindow, gatilho)
    listaGatilhos.append(gatilho)

def updateGatilhosDetection(detections):
    '''Deve ser chamada para atualizar gatilhos após uma detecção'''

    for i in np.arange(0, detections.shape[2]):
        idx = int(detections[0, 0, i, 1])
        if idx != 15: continue # Se não for pessoa, vai para a próxima detecção

        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            boundingBox = detections[0, 0, i, 3:7]

            timeNow = datetime.now()
            
            global listaGatilhos
            for gatilho in listaGatilhos:
                if testHorario(gatilho, timeNow) and testBoundingBox(gatilho, *boundingBox):
                    gatilho.detectionLastTime = time.time()
                    gatilho.bDetectionInside = True
                else:
                    gatilho.bDetectionInside = False
        if idx == 15: break

def testHorario(gatilho: Gatilho, timeNow: datetime) -> bool:
    '''Testa se o horário de agora está dentro do horário do gatilho'''

    iniHour = int(gatilho.horarioInicial[:2])
    iniMinute = int(gatilho.horarioInicial[3:])
    finalHour = int(gatilho.horarioFinal[:2])
    finalMinute = int(gatilho.horarioFinal[3:])

    if iniHour < timeNow.hour and finalHour > timeNow.hour:
        return True
    if iniHour == timeNow.hour:
        return iniMinute <= timeNow.minute
    if finalHour == timeNow.hour:
        return finalMinute >= timeNow.minute

    return False

def testBoundingBox(gatilho: Gatilho, boxStartX: float, boxStartY: float, boxEndX: float, boxEndY: float) -> bool:
    '''Testa se a detecção está dentro da área do gatilho'''

    return (boxStartX >= gatilho.areaStartX
            and boxEndX <= gatilho.areaEndX
            and boxStartY >= gatilho.areaStartY
            and boxEndY <= gatilho.areaEndY)

# def testBoxes(startX, startY, endX, endY, gatilhoStartX, gatilhoStartY, gatilhoEndX, gatilhoEndY):
#     if (startX >= gatilho.areaStartX) & (endX <= gatilho.areaEndX) & (startY >= gatilho.areaStartY) & (endY <= gatilho.areaEndY):
