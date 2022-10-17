import os
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
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
    btnGatilhos.clicked.connect(UI.openGatilhosWindow)

    # Button
    # btnBlobSize = QPushButton()
    # btnBlobSize.setContentsMargins(0, 0, 0 ,0)
    # btnBlobSize.setStyleSheet(css.btnTriggerStyle + css.imageSettingButton)
    # btnBlobSize.setIcon(QIcon(filePath + '/Assets/blob_size_icon.png'))
    # btnBlobSize.clicked.connect(lambda: print('btn pressed'))

    # CheckBox visualizar detecções
    UI.checkboxViewGatilhos = QCheckBox('Visualizar Gatilhos')
    UI.checkboxViewGatilhos.setStyleSheet(css.checkBoxStyle)
    # UI.checkboxViewGatilhos.setChecked(True)

    # Image
    UI.camImgs = []
    UI.camImgs.append(ImageWidget(UI.handleImageClick))
    UI.camImgs[0].setStyleSheet(css.imageStyle)
    # UI.camImgs[0].setScaledContents(True)
    # UI.camImgs[0].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    UI.camImgs.append(ImageWidget(UI.handleImageClick))
    UI.camImgs[1].setStyleSheet(css.imageStyle)
    # UI.camImgs[1].setScaledContents(True)
    # # UI.camImgs[1].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    # Labels
    lClientConnected = QLabel('Cliente: ')
    UI.lClientConnectedValue = QLabel('Disconnected')
    UI.lClientConnectedValue.setStyleSheet(css.textRed)
    # UI.lLogPanel = QLabel('Log')
    lImg1BlobSize = QLabel('Blob Size Imagem 1:')
    lImg2BlobSize = QLabel('Blob Size Imagem 2:')

    # Painel de Log
    # UI.logPanel = QTextEdit()
    # utils.logPanel = UI.logPanel

    # LineEdit
    UI.inputBlobSize = []
    for i in range(2):
        UI.inputBlobSize.append(QLineEdit())
        UI.inputBlobSize[i].setMaximumSize(45, 28)
        UI.inputBlobSize[i].setStyleSheet(css.blobSizeTextEdit)
        UI.inputBlobSize[i].setText(str(UI.detector.blobSizes[i]))
        UI.inputBlobSize[i].setValidator(QIntValidator(100, 1200))
        # UI.inputBlobSize[i].textChanged.connect(lambda value: UI.imgManager.detector.setBlobSize(value, i))
    UI.inputBlobSize[0].textChanged.connect(lambda value: UI.detector.setBlobSize(value, 0))
    UI.inputBlobSize[1].textChanged.connect(lambda value: UI.detector.setBlobSize(value, 1))

    # Layout organization
    vBoxMain = QVBoxLayout()
    vBoxMain.setSizeConstraint(QLayout.SetMinimumSize)
    hBoxTop = QHBoxLayout()
    hBoxBottom = QHBoxLayout()
    vBoxLogPanel = QVBoxLayout()
    vBoxImages = QVBoxLayout()
    hBoxImg1BlobSize = QHBoxLayout()
    hBoxImg2BlobSize = QHBoxLayout()
    # vBoxImage1 = QVBoxLayout(UI.camImgs[0])
    hBoxClientInfo = QHBoxLayout()
    # hBoxTop.setContentsMargins(0, 0, 0, 0)
    hBoxTop.setAlignment(Qt.AlignTop)
    hBoxTop.addWidget(btnGatilhos)
    hBoxTop.addWidget(UI.checkboxViewGatilhos)
    hBoxClientInfo.addWidget(lClientConnected)
    hBoxClientInfo.addWidget(UI.lClientConnectedValue)
    # UI.vBox.setSpacing(0)
    # UI.hBox.setAlignment(Qt.AlignLeft)
    hBoxClientInfo.setAlignment(Qt.AlignRight)
    hBoxImg1BlobSize.addWidget(lImg1BlobSize, alignment=Qt.AlignRight)
    hBoxImg1BlobSize.addWidget(UI.inputBlobSize[0], alignment=Qt.AlignLeft)
    hBoxImg2BlobSize.addWidget(lImg2BlobSize, alignment=Qt.AlignRight)
    hBoxImg2BlobSize.addWidget(UI.inputBlobSize[1], alignment=Qt.AlignLeft)
    # vBoxImages.setAlignment(Qt.AlignTop)
    # vBoxImage1.addWidget(btnBlobSize, alignment=Qt.AlignTop | Qt.AlignRight)
    # vBoxImage1.addWidget(UI.camImgs[0], alignment=Qt.AlignCenter)
    # vBoxImages.addWidget(vBoxImage1)
    vBoxImages.addWidget(UI.camImgs[0], alignment=Qt.AlignCenter)
    vBoxImages.addWidget(UI.camImgs[1], alignment=Qt.AlignCenter)
    # hBoxBottom.setAlignment(Qt.AlignCenter)
    hBoxTop.addLayout(hBoxImg1BlobSize)
    hBoxTop.addLayout(hBoxImg2BlobSize)
    hBoxTop.addLayout(hBoxClientInfo)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxBottom)
    vBoxMain.setStretchFactor(hBoxTop, 1)
    vBoxMain.setStretchFactor(hBoxBottom, 100)
    hBoxBottom.addLayout(vBoxImages)
    # hBoxBottom.addLayout(UI.vBoxLogPanel)
    # vBoxLogPanel.addWidget(UI.lLogPanel, alignment=Qt.AlignHCenter)
    # vBoxLogPanel.addWidget(UI.logPanel)
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
    # btnLimparBD = QPushButton("Limpar Banco de Dados")
    # btnLimparBD.clicked.connect(db.limparBD)
    # btnLimparBD.setMinimumWidth(100)

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
    # vMainLayout.addWidget(btnLimparBD, alignment=Qt.AlignLeft)
    vBoxMain.addWidget(lTriggersList, alignment=Qt.AlignHCenter)
    vBoxMain.addWidget(scrollArea)
    # UI.vBoxGatilhos.setAlignment(Qt.AlignTop)
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
    # UI.lAte.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
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