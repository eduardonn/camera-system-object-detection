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
import math
import os
from playsound import playsound
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import database as db
import layout

triggerList = []

class Trigger:
    soundThread = None
    triggersWindow = None
    shouldPlaySound = False
    isAlarmSilenced = False
    MAX_SOUNDING_TIME = 10

    def __init__(
            self,
            id,
            nome,
            initialTime,
            finalTime,
            tempoPermanencia,
            acao,
            areaStartX,
            areaStartY,
            areaEndX,
            areaEndY):
        self.id = id
        self.nome = nome
        self.initialTime = initialTime
        self.finalTime = finalTime
        self.tempoPermanencia = tempoPermanencia
        self.acao = acao
        self.areaStartX = areaStartX
        self.areaStartY = areaStartY
        self.areaEndX = areaEndX
        self.areaEndY = areaEndY
        self.labelTempoPermaneceu = 0
        self.tempoPermaneceu = .0
        self.acionado = False
        self.detectionLastTime = -math.inf
        self.timeSinceLastUpdate = time.time()
        self.incrementLastTime = -math.inf
        self.bDetectionInside = False
        self.widget = None
        self.lTempoPermaneceu = None
        self.camera = 0

    def remove(self):
        print("removendo id:", self.id)

        db.deleteGatilho(self.id)
        self.triggersWindow.vBoxGatilhos.removeWidget(self.widget)
        triggerList.remove(self)
        sip.delete(self.widget)
        self.widget = None
        db.printDB()

    def reset(self):
        self.tempoPermaneceu = 0.
        self.timeSinceLastUpdate = 0.
        self.acionado = False
        Trigger.shouldPlaySound = False

        if self.widget is not None:
            self.triggersWindow.resetTriggerUI.emit(self)

        if self.lTempoPermaneceu is not None:
            self.lTempoPermaneceu.setText(str(round(self.tempoPermaneceu, 3)))

    def print(self):
        print('GATILHO:',
                self.id,
                self.nome,
                self.initialTime,
                self.finalTime,
                self.tempoPermanencia,
                self.acao,
                self.areaStartX,
                self.areaStartY,
                self.areaEndX,
                self.areaEndY)

    def startAlarmSound():
        Trigger.soundThread = QThread()
        Trigger.soundThread.run = Trigger.playAlarmSound
        Trigger.soundThread.start()

    def playAlarmSound():
        Trigger.shouldPlaySound = True
        filePath = __file__[:-len(os.path.basename(__file__))]
        initTime = time.time()

        while Trigger.shouldPlaySound:
            playsound(filePath + '/sounds/mixkit-warning-alarm-buzzer.wav')
            time.sleep(0.5)
            if time.time() - initTime > Trigger.MAX_SOUNDING_TIME:
                print('alarm stopped')
                break

        Trigger.shouldPlaySound = False

class UpdateGatilhosPeriodicallyThread(QThread):
    '''Atualiza gatilhos a cada THREAD_TIME_SLEEP segundos'''
    changeGatilhoStateSignal = pyqtSignal(Trigger, bool) # Necessário pois mudanças na UI devem ocorrer na thread principal
    isPlayingSound = False

    def run(self):
        THREAD_TIME_SLEEP = 0.1 # Tempo (em segundos) que a thread irá dormir e incrementar o tempo que detecções permaneceram
        MAX_TIME_INC_LAST_DETECTION = 1.0 # Continuar incrementando o tempo que permaneceu até esse tempo (em segundos)
        TIME_LIMIT_TO_RESET = 10 # Se passar esse tempo (em segundos) sem detecção no gatilho, ele resetará

        while True:
            for trigger in triggerList:
                timeSinceLastDetection = time.time() - trigger.detectionLastTime
                timeSinceLastIncrement = time.time() - trigger.incrementLastTime
                trigger.incrementLastTime = time.time()

                if timeSinceLastDetection > MAX_TIME_INC_LAST_DETECTION:
                    if not trigger.bDetectionInside:
                        if timeSinceLastDetection > TIME_LIMIT_TO_RESET:
                            trigger.reset()

                    continue

                trigger.tempoPermaneceu += timeSinceLastIncrement

                if trigger.lTempoPermaneceu is not None:
                    trigger.lTempoPermaneceu.setText(str(round(trigger.tempoPermaneceu, 3)))
                
                if trigger.acionado: continue

                if trigger.tempoPermaneceu > trigger.tempoPermanencia and not trigger.acionado:
                    trigger.acionado = True
                    print(f'GATILHO [{trigger.nome}] DISPAROU')

                    if not Trigger.isAlarmSilenced:
                        Trigger.startAlarmSound()

                    self.changeGatilhoStateSignal.emit(trigger, True)

            time.sleep(THREAD_TIME_SLEEP)

def updateGatilhosAfterDetection(detections):
    anyDetection = False
    for i in np.arange(0, detections.shape[2]):
        idx = int(detections[0, 0, i, 1])
        if idx != 15: continue # Se não for pessoa, vai para a próxima detecção
        anyDetection = True

        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            boundingBox = detections[0, 0, i, 3:7]

            timeNow = datetime.now()
            
            global triggerList
            for trigger in triggerList:
                if testHorario(trigger, timeNow) and testBoundingBox(trigger, *boundingBox):
                    trigger.tempoPermaneceuBeforeDetection = trigger.tempoPermaneceu
                    trigger.detectionLastTime = time.time()
                    trigger.bDetectionInside = True
                else:
                    trigger.bDetectionInside = False
    if not anyDetection:
        for trigger in triggerList:
            trigger.bDetectionInside = False

def initGatilhos(updateGatilhoState):
    global triggerList
    triggerList.clear()

    for gatilho in db.selectGatilhos():
        gatilhoClass = Trigger(*gatilho)
        triggerList.append(gatilhoClass)

    thread = UpdateGatilhosPeriodicallyThread()
    thread.changeGatilhoStateSignal.connect(updateGatilhoState)
    thread.start()

    return thread

def createGatilho(*args):
    gatilho = Trigger(-1, *args)
    db.createGatilho(gatilho)
    layout.addTriggerOnViewList(Trigger.triggersWindow, gatilho)
    triggerList.append(gatilho)

def testHorario(trigger: Trigger, timeNow: datetime) -> bool:
    '''Testa se o horário de agora está dentro do horário do gatilho'''

    iniHour = int(trigger.initialTime[:2])
    iniMinute = int(trigger.initialTime[3:])
    finalHour = int(trigger.finalTime[:2])
    finalMinute = int(trigger.finalTime[3:])

    if iniHour < timeNow.hour and finalHour > timeNow.hour:
        return True
    if iniHour == timeNow.hour:
        return iniMinute <= timeNow.minute
    if finalHour == timeNow.hour:
        return finalMinute >= timeNow.minute

    return False

def testBoundingBox(trigger: Trigger, boxStartX: float, boxStartY: float, boxEndX: float, boxEndY: float) -> bool:
    '''Testa se a detecção está dentro da área do gatilho'''
    xThreshold = 0.01041
    yThreshold = 0.0185

    return (boxStartX >= trigger.areaStartX - xThreshold
            and boxEndX   <= trigger.areaEndX + xThreshold
            and boxStartY >= trigger.areaStartY - yThreshold
            and boxEndY   <= trigger.areaEndY + yThreshold)
