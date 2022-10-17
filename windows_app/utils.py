from PyQt5.QtGui import QTextCursor

logPanel = None

def printLog(msg, end='\n'):
    if logPanel is None:
        raise Exception('Log Panel is None')
        
    # logPanel.insertPlainText(str)
    logPanel.insertPlainText(str(msg) + end)
    logPanel.moveCursor(QTextCursor.End)