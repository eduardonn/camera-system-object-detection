backgroundColor = 'rgb(35, 35, 35)'
buttonHoverColor = 'rgb(80, 80, 80)'

windowStyle = '''
    *{
        font-size: 16px;
        font-family: Helvetica, serif;
        color: rgb(235, 235, 235);
    }

    *#windowStyle {
        background: ''' + backgroundColor + '''
    }
'''

btnStyle =  '''
    QPushButton {
        width: 85px;
        height: 25px;
        border: none;
        border-bottom: 3px solid rgb(235, 235, 235);
        padding: 5%;
        margin: 0px;
    }
    QPushButton:hover{
        background: ''' + buttonHoverColor + ''';
    }
    '''

btnTriggerStyle =  '''
    QPushButton {
        border: 1px solid gray;
        padding: 5%;
        margin: 0px;
    }
    QPushButton:hover{
        background: ''' + buttonHoverColor + ''';
    }
    '''

scrollAreaStyle = '''
    QWidget#triggersScrollArea {
        background: ''' + buttonHoverColor + ''';
        color: black;
    }
'''

gatilhoPadrao = '''
    QWidget#gatilhoBackground {
        background-color: rgb(45, 45, 45);
        border: 2px inset gray;
    }
    '''

gatilhoAcionado = '''
    QWidget#gatilhoBackground {
        background-color: rgb(45, 45, 45);
        border: 2px inset red;
    }
    '''

imageStyle = '''
    QWidget {
        border: 1px solid gray;
        margin: 0;
        padding: 0;
    }
'''

titulo = '''
    * {
        font-weight: bold;
    }
'''

checkBoxStyle = '''
    * {
        image: linear-gradient(black, white);
    }
'''

textBlack = '''
    * {
        color: black;
    }
'''

textGreen = '''
    * {
        color: green;
    }
'''

textRed = '''
    * {
        color: red;
    }
'''