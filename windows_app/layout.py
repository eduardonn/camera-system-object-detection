import os
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QWidget, QComboBox, QTimeEdit, QLineEdit, QScrollArea, QCheckBox, QTextEdit, QPlainTextEdit
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt, QSize
import utils
import css

filePath = __file__[:-len(os.path.basename(__file__))]

def initMainWindowLayout(UI):
    UI.setObjectName('windowStyle')
    UI.setStyleSheet(css.windowStyle)
    
    # Button grade
    btnAlterarGrade = QPushButton("Alterar Grade")
    btnAlterarGrade.setStyleSheet(css.btnStyle)
    btnAlterarGrade.clicked.connect(alterarGrade)

    # Button gatilhos
    btnGatilhos = QPushButton("Gatilhos")
    btnGatilhos.setStyleSheet(css.btnStyle)
    btnGatilhos.clicked.connect(UI.openGatilhosWindow)

    # Button visualizar detecções
    UI.btnViewGatilhos = QCheckBox('Visualizar Gatilhos')
    UI.btnViewGatilhos.setStyleSheet(css.checkBoxStyle)
    # UI.btnViewGatilhos.setChecked(True)

    # Image
    UI.camImg = QLabel()
    UI.camImg.setStyleSheet(css.imageStyle)
    UI.camImg2 = QLabel()
    UI.camImg2.setStyleSheet(css.imageStyle)

    # Labels
    lClientConnected = QLabel('Cliente: ')
    UI.lClientConnectedValue = QLabel('Disconnected')
    UI.lClientConnectedValue.setStyleSheet(css.textRed)
    # UI.lLogPanel = QLabel('Log')

    # Painel de Log
    # UI.logPanel = QTextEdit()
    # utils.logPanel = UI.logPanel

    # Layout organization
    vBoxMain = QVBoxLayout()
    hBoxTop = QHBoxLayout()
    hBoxBottom = QHBoxLayout()
    vBoxLogPanel = QVBoxLayout()
    vBoxImages = QVBoxLayout()
    hBoxClientInfo = QHBoxLayout()
    # UI.vBox.setSpacing(4)
    hBoxTop.setContentsMargins(0, 0, 0, 0)
    hBoxTop.setAlignment(Qt.AlignTop)
    hBoxTop.addWidget(btnAlterarGrade)
    hBoxTop.addWidget(btnGatilhos)
    hBoxTop.addWidget(UI.btnViewGatilhos)
    hBoxClientInfo.addWidget(lClientConnected)
    hBoxClientInfo.addWidget(UI.lClientConnectedValue)
    # UI.vBox.setSpacing(0)
    # UI.hBox.setAlignment(Qt.AlignLeft)
    hBoxClientInfo.setAlignment(Qt.AlignRight)
    vBoxImages.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    vBoxImages.addWidget(UI.camImg, alignment=Qt.AlignVCenter)
    vBoxImages.addWidget(UI.camImg2, alignment=Qt.AlignVCenter)
    hBoxBottom.setAlignment(Qt.AlignVCenter)
    hBoxTop.addLayout(hBoxClientInfo)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxBottom)
    hBoxBottom.addLayout(vBoxImages)
    # hBoxBottom.addLayout(UI.vBoxLogPanel)
    # vBoxLogPanel.addWidget(UI.lLogPanel, alignment=Qt.AlignHCenter)
    # vBoxLogPanel.addWidget(UI.logPanel)
    UI.setLayout(vBoxMain)

    UI.show()

def gatilhosWindowLayout(UI):
    UI.setObjectName('windowStyle')
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
    UI.setObjectName('windowStyle')
    UI.setStyleSheet(css.windowStyle)

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

def addGatilho(UI, gatilho):
    gatilho.widget = gatilhoBackground = QWidget()
    gatilhoBackground.setObjectName('gatilhoBackground')
    
    # Button delete
    btnDelete = QPushButton()
    btnDelete.setIcon(QIcon(filePath + '/Assets/delete_white.png'))
    btnDelete.clicked.connect(gatilho.remove)
    btnDelete.setCursor(QCursor(Qt.PointingHandCursor))
    btnDelete.setStyleSheet(css.btnTriggerStyle)
    
    # Button reset
    btnReset = QPushButton('Resetar')
    btnReset.clicked.connect(gatilho.reset)
    btnReset.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    btnReset.setStyleSheet(css.btnTriggerStyle)

    # Trigger style
    if gatilho.acionado:
        gatilhoBackground.setStyleSheet(css.gatilhoAcionado)
    else:
        gatilhoBackground.setStyleSheet(css.gatilhoPadrao)

    # Labels
    lNomeGatilho = QLabel(gatilho.nome if gatilho.nome != '' else 'Gatilho ' + str(gatilho.id))
    lNomeGatilho.setStyleSheet(css.titulo)
    lAcao = QLabel("Ação: " + gatilho.acao)
    lTempoPermanencia = QLabel("Tempo de permanência: " + str(gatilho.tempoPermanencia))
    lHorarios = QLabel("Horarios de detecção:")
    lHorariosValues = QLabel(gatilho.horarioInicial + ' até ' + gatilho.horarioFinal)
    lTempoPermaneceuDescricao = QLabel('Tempo Permaneceu:')
    # lTempoPermaneceuDescricao.setSizePolicy(Qt.QSizePolicy.Fixed)
    gatilho.lTempoPermaneceu = QLabel(str(round(gatilho.tempoPermaneceu, 3)))

    # Layout organization
    vBoxMain = QVBoxLayout(gatilhoBackground) # QVBoxLayout com QWidget como parent para estilizar o layout
    hBoxInfo = QHBoxLayout()
    hBoxTop = QHBoxLayout()
    vBoxLeft = QVBoxLayout()
    vBoxTempoPermanencia = QVBoxLayout()
    hBoxTempoPermaneceu = QHBoxLayout()
    hBoxHorarios = QHBoxLayout()
    vBoxBtnReset = QVBoxLayout()
    UI.vBoxGatilhos.addWidget(gatilhoBackground)
    hBoxTop.addWidget(lNomeGatilho, alignment=Qt.AlignTop)
    hBoxTop.addWidget(btnDelete, alignment=Qt.AlignRight)
    hBoxInfo.setAlignment(Qt.AlignTop)
    vBoxLeft.addWidget(lAcao, alignment=Qt.AlignTop)
    vBoxTempoPermanencia.addWidget(lTempoPermanencia, alignment=Qt.AlignRight)
    vBoxTempoPermanencia.addLayout(hBoxTempoPermaneceu)
    vBoxTempoPermanencia.setAlignment(Qt.AlignRight)
    hBoxTempoPermaneceu.addWidget(lTempoPermaneceuDescricao)
    hBoxTempoPermaneceu.addWidget(gatilho.lTempoPermaneceu)
    hBoxHorarios.addWidget(lHorarios)
    hBoxHorarios.addWidget(lHorariosValues)
    vBoxBtnReset.addWidget(btnReset, alignment=Qt.AlignBottom)
    vBoxLeft.addLayout(hBoxHorarios)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxInfo)
    hBoxInfo.addLayout(vBoxLeft)
    hBoxInfo.addLayout(vBoxTempoPermanencia)
    hBoxInfo.addLayout(vBoxBtnReset)

def alterarGrade(UI):
    pass