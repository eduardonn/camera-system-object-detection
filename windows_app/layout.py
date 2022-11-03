import os
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QSlider
from PyQt5.QtWidgets import QWidget, QComboBox, QTimeEdit, QLineEdit, QScrollArea, QCheckBox, QLayout
from PyQt5.QtGui import QCursor, QIcon, QIntValidator
from PyQt5.QtCore import Qt
from image_widget import ImageWidget
import css

filePath = __file__[:-len(os.path.basename(__file__))]

def initMainWindowLayout(UI):
    UI.setGeometry(50, 50, 1250, 660)
    # UI.setFixedSize(1150, 620)
    UI.setObjectName('window')
    UI.setStyleSheet(css.windowStyle)

    # Button gatilhos
    btnGatilhos = QPushButton("Gatilhos")
    btnGatilhos.setStyleSheet(css.btnStyle)
    btnGatilhos.setMaximumWidth(200)
    btnGatilhos.clicked.connect(UI.openGatilhosWindow)

    # CheckBox visualizar detecções
    UI.checkboxViewGatilhos = QCheckBox('Visualizar Gatilhos')
    UI.checkboxViewGatilhos.setStyleSheet(css.checkBoxStyle)
    checkboxBlobSize = QCheckBox('Ajustar Blob Size')
    checkboxBlobSize.setStyleSheet(css.checkBoxStyle)
    checkboxBlobSize.clicked.connect(UI.onCheckboxAjustarBlobSizeClick)
    # UI.checkboxViewGatilhos.setChecked(True)

    # Image
    UI.camImgs.append(ImageWidget(UI.handleImageClick))
    UI.camImgs[0].setStyleSheet(css.imageStyle)
    # UI.camImgs[0].setScaledContents(True)
    # UI.camImgs[0].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    UI.camImgs.append(ImageWidget(UI.handleImageClick))
    UI.camImgs[1].setStyleSheet(css.imageStyle)
    # UI.camImgs[1].setScaledContents(True)
    # UI.camImgs[1].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    # Labels
    lClientConnected = QLabel('Cliente: ')
    UI.lClientConnectedValue = QLabel('Disconnected')
    UI.lClientConnectedValue.setStyleSheet(css.textRed)
    lImg1BlobSize = QLabel('Blob Size Imagem 1:')
    lImg2BlobSize = QLabel('Blob Size Imagem 2:')
    lSettings = QLabel('Settings')

    # Slider
    UI.lPersonSize = QLabel(str(UI.imgManager.personTesterSize))
    UI.lPersonSize.hide()
    UI.personTesterSizeSlider = QSlider(Qt.Horizontal)
    UI.personTesterSizeSlider.setRange(2, 460)
    UI.personTesterSizeSlider.setValue(UI.imgManager.personTesterSize)
    UI.personTesterSizeSlider.valueChanged.connect(UI.sliderPersonTesterSize)
    UI.personTesterSizeSlider.setPageStep(50)
    UI.personTesterSizeSlider.setTickInterval(10)
    UI.personTesterSizeSlider.hide()

    # LineEdit
    UI.inputBlobSize = []
    for i in range(2):
        UI.inputBlobSize.append(QLineEdit())
        UI.inputBlobSize[i].setMaximumSize(45, 28)
        UI.inputBlobSize[i].setStyleSheet(css.blobSizeTextEdit)
        UI.inputBlobSize[i].setText(str(UI.detector.blobSizes[i]))
        UI.inputBlobSize[i].setValidator(
            QIntValidator(UI.detector.blobSizeRange[0], UI.detector.blobSizeRange[1]))
    UI.inputBlobSize[0].textChanged.connect(lambda value: UI.detector.setBlobSize(value, 0))
    UI.inputBlobSize[1].textChanged.connect(lambda value: UI.detector.setBlobSize(value, 1))

    # Layout organization
    vBoxMain = QVBoxLayout()
    vBoxMain.setSizeConstraint(QLayout.SetMinimumSize)
    hBoxTop = QHBoxLayout()
    hBoxTop.setAlignment(Qt.AlignTop)
    hBoxBottom = QHBoxLayout()
    vBoxLogPanel = QVBoxLayout()
    vBoxImages = QVBoxLayout()
    vBoxImages.setAlignment(Qt.AlignCenter)
    vBoxSettings = QVBoxLayout()
    vBoxSettings.setAlignment(Qt.AlignTop)
    vBoxSettings.setSpacing(10)
    vBoxImages.addWidget(UI.camImgs[0])
    vBoxImages.addWidget(UI.camImgs[1])
    hBoxImg1BlobSize = QHBoxLayout()
    hBoxImg2BlobSize = QHBoxLayout()
    hBoxBlobSizeAjuste = QHBoxLayout()
    hBoxClientInfo = QHBoxLayout()
    hBoxTop.addWidget(btnGatilhos)
    hBoxImg1BlobSize.addWidget(lImg1BlobSize)
    hBoxImg1BlobSize.addWidget(UI.inputBlobSize[0], alignment=Qt.AlignLeft)
    hBoxImg2BlobSize.addWidget(lImg2BlobSize)
    hBoxImg2BlobSize.addWidget(UI.inputBlobSize[1], alignment=Qt.AlignLeft)
    vBoxSettings.addWidget(lSettings, alignment=Qt.AlignTop | Qt.AlignCenter)
    vBoxSettings.addWidget(UI.checkboxViewGatilhos)
    vBoxSettings.addWidget(checkboxBlobSize)
    hBoxBlobSizeAjuste.addWidget(UI.personTesterSizeSlider)
    hBoxBlobSizeAjuste.addWidget(UI.lPersonSize)
    vBoxSettings.addLayout(hBoxBlobSizeAjuste)
    vBoxSettings.addLayout(hBoxImg1BlobSize)
    vBoxSettings.addLayout(hBoxImg2BlobSize)
    hBoxClientInfo.addWidget(lClientConnected)
    hBoxClientInfo.addWidget(UI.lClientConnectedValue)
    hBoxClientInfo.setAlignment(Qt.AlignRight)
    hBoxTop.addLayout(hBoxClientInfo)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxBottom)
    vBoxMain.setStretchFactor(hBoxTop, 1)
    vBoxMain.setStretchFactor(hBoxBottom, 100)
    hBoxBottom.addLayout(vBoxImages)
    hBoxBottom.setStretchFactor(vBoxImages, 5)
    hBoxBottom.addLayout(vBoxSettings)
    hBoxBottom.setStretchFactor(vBoxSettings, 1)

    UI.setLayout(vBoxMain)
    UI.show()

def gatilhosWindowLayout(UI):
    UI.setObjectName('window')
    UI.setStyleSheet(css.windowStyle)

    # Buttons
    btnAdd = QPushButton("Adicionar Gatilho")
    btnAdd.clicked.connect(UI.openDrawAreaWindow)
    btnAdd.setMinimumWidth(150)
    btnAdd.setStyleSheet(css.btnStyle)
    btnVoltar = QPushButton("Voltar")
    btnVoltar.clicked.connect(UI.close)
    # btnVoltar.setMinimumWidth(100)
    btnVoltar.setStyleSheet(css.btnStyle)

    # Labels
    lTriggersList = QLabel("Lista de Gatilhos")
    scrollArea = QScrollArea()
    listaGatilhos = QWidget()

    # Layout organization
    vBoxMain = QVBoxLayout()
    UI.vBoxGatilhos = QVBoxLayout()

    scrollArea.setStyleSheet(css.scrollAreaStyle)
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scrollArea.setWidgetResizable(True)

    vBoxMain.addWidget(btnAdd, alignment=Qt.AlignLeft)
    vBoxMain.addWidget(lTriggersList, alignment=Qt.AlignHCenter)
    vBoxMain.addWidget(scrollArea)
    vBoxMain.addWidget(btnVoltar, alignment=Qt.AlignRight)

    listaGatilhos.setLayout(UI.vBoxGatilhos)
    scrollArea.setWidget(listaGatilhos)
    UI.setLayout(vBoxMain)
    UI.show()

def addTriggerWindowLayout(UI):
    UI.setObjectName('window')
    UI.setStyleSheet(css.windowStyle)
    UI.setGeometry(100, 50, 700, 440)
    UI.setWindowTitle('Adicionar Gatilho')

    # Buttons
    btnConfirm = QPushButton("Confirmar")
    btnConfirm.setMaximumWidth(150)
    btnConfirm.clicked.connect(UI.salvarGatilhoESair)
    btnConfirm.setStyleSheet(css.btnStyle)

    # Labels
    UI.camImg = QLabel()
    lDesenheArea = QLabel("Desenhe a área de detecção")
    lDesenheArea.setMaximumHeight(20)
    lNomeGatilho = QLabel("Nome do gatilho")
    lNomeGatilho.setMaximumHeight(20)
    lHorarioDisparo = QLabel("Horário de disparo")
    lHorarioDisparo.setMaximumHeight(20)
    lTempoAteDisparo = QLabel("Tempo de permanência até disparo")
    lTempoAteDisparo.setMaximumHeight(20)
    lSegundos = QLabel("segundos")
    lSegundos.setMaximumHeight(20)
    lSegundos.setMinimumWidth(20)
    lAcao = QLabel("Ação")
    lAcao.setMaximumHeight(20)
    lAte = QLabel("até")
    lAte.setMaximumHeight(20)
    lAte.setMaximumWidth(20)

    # Input widgets
    UI.nomeGatilho = QLineEdit()
    UI.nomeGatilho.setStyleSheet(css.textBlack)
    UI.tipoAlarme = QComboBox()
    UI.tipoAlarme.addItem('Alarme')
    UI.tipoAlarme.addItem('Notificação')
    UI.tipoAlarme.setStyleSheet(css.textBlack)
    UI.timeFrom = QTimeEdit()
    UI.timeFrom.setStyleSheet(css.textBlack)
    UI.timeTo = QTimeEdit()
    UI.timeTo.setStyleSheet(css.textBlack)
    UI.timePermanencia = QLineEdit()
    UI.timePermanencia.setStyleSheet(css.textBlack)

    # Layout organization
    vBoxMain = QVBoxLayout()
    hBoxMain = QHBoxLayout()
    vBoxRight = QVBoxLayout()
    hBoxTime = QHBoxLayout()
    hBoxTempoDisparo = QHBoxLayout()
    vBoxMain.addWidget(lDesenheArea)
    vBoxMain.addLayout(hBoxMain)
    hBoxMain.addWidget(UI.camImg, alignment=Qt.AlignLeft)
    hBoxMain.addLayout(vBoxRight)
    vBoxRight.addWidget(lNomeGatilho)
    vBoxRight.addWidget(UI.nomeGatilho)
    vBoxRight.addWidget(lHorarioDisparo)
    vBoxRight.addLayout(hBoxTime)
    hBoxTime.addWidget(UI.timeFrom)
    hBoxTime.addWidget(lAte)
    hBoxTime.addWidget(UI.timeTo)
    vBoxRight.addWidget(lTempoAteDisparo)
    vBoxRight.addLayout(hBoxTempoDisparo)
    hBoxTempoDisparo.addWidget(UI.timePermanencia)
    hBoxTempoDisparo.addWidget(lSegundos)
    vBoxRight.addWidget(lAcao)
    vBoxRight.addWidget(UI.tipoAlarme)
    vBoxRight.addWidget(btnConfirm, alignment=Qt.AlignBottom | Qt.AlignCenter)

    UI.setLayout(vBoxMain)
    UI.show()

def addTrigger(UI, trigger):
    trigger.widget = triggerBackground = QWidget()
    triggerBackground.setObjectName('triggerBackground')
    
    # Button delete
    btnDelete = QPushButton()
    btnDelete.setIcon(QIcon(filePath + '/Assets/delete_white.png'))
    btnDelete.clicked.connect(trigger.remove)
    btnDelete.setCursor(QCursor(Qt.PointingHandCursor))
    btnDelete.setStyleSheet(css.btnTriggerStyle)
    
    # Button reset
    btnReset = QPushButton('Resetar')
    btnReset.clicked.connect(trigger.reset)
    btnReset.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    btnReset.setStyleSheet(css.btnTriggerStyle)

    # Trigger style
    if trigger.acionado:
        triggerBackground.setStyleSheet(css.gatilhoAcionado)
    else:
        triggerBackground.setStyleSheet(css.gatilhoPadrao)

    # Labels
    lNomeGatilho = QLabel(trigger.nome if trigger.nome != '' else 'Gatilho ' + str(trigger.id))
    lNomeGatilho.setStyleSheet(css.titulo)
    lAcao = QLabel("Ação: " + trigger.acao)
    lTempoPermanencia = QLabel("Tempo de permanência: " + str(trigger.tempoPermanencia))
    lHorarios = QLabel("Horários de detecção:")
    lHorariosValues = QLabel(trigger.initialTime + ' até ' + trigger.finalTime)
    lTempoPermaneceuDescricao = QLabel('Tempo Permaneceu:')
    # lTempoPermaneceuDescricao.setSizePolicy(Qt.QSizePolicy.Fixed)
    trigger.lTempoPermaneceu = QLabel(str(round(trigger.tempoPermaneceu, 3)))

    # Layout organization
    vBoxMain = QVBoxLayout(triggerBackground) # QVBoxLayout com QWidget como parent para estilizar o layout
    hBoxInfo = QHBoxLayout()
    hBoxTop = QHBoxLayout()
    vBoxLeft = QVBoxLayout()
    vBoxTempoPermanencia = QVBoxLayout()
    hBoxTempoPermaneceu = QHBoxLayout()
    hBoxHorarios = QHBoxLayout()
    vBoxBtnReset = QVBoxLayout()
    UI.vBoxGatilhos.addWidget(triggerBackground)
    hBoxTop.addWidget(lNomeGatilho, alignment=Qt.AlignTop)
    hBoxTop.addWidget(btnDelete, alignment=Qt.AlignRight)
    hBoxInfo.setAlignment(Qt.AlignTop)
    vBoxLeft.addWidget(lAcao, alignment=Qt.AlignTop)
    vBoxTempoPermanencia.addWidget(lTempoPermanencia, alignment=Qt.AlignRight)
    vBoxTempoPermanencia.addLayout(hBoxTempoPermaneceu)
    vBoxTempoPermanencia.setAlignment(Qt.AlignRight)
    hBoxTempoPermaneceu.addWidget(lTempoPermaneceuDescricao)
    hBoxTempoPermaneceu.addWidget(trigger.lTempoPermaneceu)
    hBoxHorarios.addWidget(lHorarios)
    hBoxHorarios.addWidget(lHorariosValues)
    vBoxBtnReset.addWidget(btnReset, alignment=Qt.AlignBottom)
    vBoxLeft.addLayout(hBoxHorarios)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxInfo)
    hBoxInfo.addLayout(vBoxLeft)
    hBoxInfo.addLayout(vBoxTempoPermanencia)
    hBoxInfo.addLayout(vBoxBtnReset)