from PyQt5.QtGui import QTextCursor

logPanel = None

def printLog(msg, end='\n'):
    if logPanel is not None:
        # logPanel.insertPlainText(str)
        logPanel.insertPlainText(str(msg) + end)
        logPanel.moveCursor(QTextCursor.End)
    else:
        raise Exception('Log Panel is None')