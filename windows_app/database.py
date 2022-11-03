import sqlite3

def createGatilho(gatilho):
    conn = sqlite3.connect('Gatilhos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gatilhos values (?,?,?,?,?,?,?,?,?)', (
                    gatilho.nome,
                    gatilho.initialTime,
                    gatilho.finalTime,
                    gatilho.tempoPermanencia,
                    gatilho.acao,
                    gatilho.areaStartX,
                    gatilho.areaStartY,
                    gatilho.areaEndX,
                    gatilho.areaEndY))

    gatilho.id = cursor.lastrowid

    conn.commit()
    conn.close()

def selectGatilhos():
    conn = sqlite3.connect('Gatilhos.db')
    cursor = conn.cursor()

    # Verifica se a tabela de gatilhos existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gatilhos'")
    if len(cursor.fetchall()) == 0:
        cursor.execute('CREATE TABLE gatilhos(nome text, timeFrom text, timeTo text, timePermanencia integer, tipoAlarme text, areaStartX integer, areaStartY integer, areaEndX integer, areaEndY integer)')

    cursor.execute('SELECT rowid, * FROM gatilhos')
    rows = cursor.fetchall()

    conn.close()

    return rows

def deleteGatilho(id):
    conn = sqlite3.connect('Gatilhos.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM gatilhos WHERE rowid = ?', (id,))

    conn.commit()
    conn.close()

# def limparBD():
#     conn = sqlite3.connect('Gatilhos.db')
#     cursor = conn.cursor()

#     cursor.execute('DELETE FROM gatilhos')

#     conn.commit()
#     conn.close()

def printDB():
    print('------------------DB------------------')
    for row in selectGatilhos():
        print(row)