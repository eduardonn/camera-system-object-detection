import ctypes
from math import ceil
import socket
import cv2, base64
import os, time, json, datetime
from threading import Thread
import keyboard
from image_manager import ImageManager

class ServerConnection(Thread):
    CHECK_CONNECTION_MSG_SEND = 'connected?'
    CHECK_CONNECTION_MSG_RECEIVED = 'connected'
    MSG_REQUEST_VIDEO = 'send-video'
    SEC_UNTIL_TIMEOUT_CONNECTION = 8
    FRAGMENT_SIZE = 1000
    IMAGE_PORT = 4444
    NOTIFICATION_PORT = 4445

    def __init__(self, onClientUpdate):
        super(ServerConnection, self).__init__()
        self.setDaemon(True)
        self.serverIP = '0.0.0.0'
        self.onClientUpdate = onClientUpdate
        self.triggerQueue = []
        # self.serverIP = '127.0.0.1'
        # self.serverIP = '192.168.0.9'
        # self.clientIP = None
        # self.sendVideoThread = Thread(target=self.sendVideo, daemon=True)
        self.bSendVideo = False
        self.ImageSocket = None
        self.notifConn = None
        self.imageConn = None

        # self.filePath = __file__[:-len(os.path.basename(__file__))]
        # self.cap = cv2.VideoCapture(
        #     'C:/repos/Codes/CameraSurveillanceTCC/WindowsApp/recordings/Estabelecimento1.mp4')
        # # self.cap = cv2.VideoCapture(1)
        # frameShape = self.cap.read()[1].shape
        # self.aspectRatio = (float)(frameShape[0]) / frameShape[1]
        self.aspectRatio = 1080.0 / 1920.0
        self.newImgSize = 500

        self.ImageSocket = self.createTCPSocket((self.serverIP, self.IMAGE_PORT))
        self.NotificationSocket = self.createTCPSocket((self.serverIP, self.NOTIFICATION_PORT))
        self.NotificationSocket.listen(1)
        print("LISTENING AT:", (self.serverIP, self.NOTIFICATION_PORT))

    def run(self):
        while True:
            print('[Notifications] Waiting connection')
            self.onClientUpdate(False)
            self.notifConn, address = self.NotificationSocket.accept()
            print('[Notifications] GOT CONNECTION FROM:', address)
            self.queryTriggerEvents()
            # self.clientIP = address[0]

            try:
                self.notifConn.settimeout(self.SEC_UNTIL_TIMEOUT_CONNECTION)
                self.notifConn.send(bytes(self.CHECK_CONNECTION_MSG_SEND, encoding='utf-8'))
                msg = self.notifConn.recv(1024).decode('utf-8')
            except:
                self.stopSendingVideo()
                self.notifConn.close()
                continue
            
            print('msg =', msg)
            if (msg.startswith(self.CHECK_CONNECTION_MSG_RECEIVED)
                or msg.startswith(self.MSG_REQUEST_VIDEO)):
                self.onClientUpdate(True)
                self.checkConnection()
            else:
                self.stopSendingVideo()
                continue


    def checkConnection(self):
        while True:
            try:
                self.notifConn.send(bytes(self.CHECK_CONNECTION_MSG_SEND, encoding='utf-8'))
                msg = self.notifConn.recv(1024).decode('utf-8')
            except Exception as e:
                print(e)
                self.stopSendingVideo()
                break
        
            print('msg>', msg)

            if msg.startswith(self.MSG_REQUEST_VIDEO):
                if not self.bSendVideo:
                    self.startSendingVideo()
            elif not msg.startswith(self.CHECK_CONNECTION_MSG_RECEIVED):
                self.stopSendingVideo()
                break

            time.sleep(3)

    def startSendingVideo(self):
        # Connect socket to client
        self.ImageSocket.listen(1)
        print('[Image] Waiting connection')
        self.imageConn, address = self.ImageSocket.accept()
        print('[Image] GOT CONNECTION FROM:', address)

        self.bSendVideo = True
        ImageManager.updateFrameEvent.append(self.sendFrame)

    def stopSendingVideo(self):
        self.bSendVideo = False
        try:
            ImageManager.updateFrameEvent.remove(self.sendFrame)
        except:
            print('exception while removing self.sendFrame')

    def sendFrame(self, frame):
        frame = cv2.resize(frame, (self.newImgSize, int(self.newImgSize * self.aspectRatio)))
        ret, frame = cv2.imencode('.jpg', frame)
        
        if not ret:
            print('Encoding failed')
            return

        frameSize = len(frame)
        numPackets = ceil(frameSize / self.FRAGMENT_SIZE)

        # MESSAGE FORMAT: [----: 4 bytes][framesize: 4 bytes][imageFragment: (FRAGMENT_SIZE) bytes]
        data = (b'----'
                + bytes(ctypes.c_uint32(frameSize))
                + bytes(frame[:self.FRAGMENT_SIZE]))

        try:
            self.imageConn.send(data)

            packetID = 1
            while(packetID < numPackets):
                fragIni = packetID * self.FRAGMENT_SIZE
                data = bytes(frame[fragIni:fragIni + self.FRAGMENT_SIZE])
                self.imageConn.send(data)
                packetID += 1
        except Exception as e:
            print('couldn\'t send frame:')
            print(e)
            self.stopSendingVideo()
            return

    def createTCPSocket(self, address) -> socket.socket:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)
            
        try:
            sock.bind(address)
        except socket.error as message:
            print('Bind failed. Msg: ' + message)
            os._exit(1)

        # sock.listen(2)

        return sock

    def sendNotification(self, trigger):
        print('sending notification')
        try:
            # local = 'Estabelecimento'
            # print('datetime:', datetime.datetime.now())
            alarmInfo = {
                'local': trigger.nome,
                'dateTime': time.mktime(datetime.datetime.now().timetuple()),
            }
            # print('json:', json.dumps(alarmInfo))
            
            if self.notifConn is not None:
                # data = b'trigger-alarm' + bytes(nomeAlarme, encoding='utf-8') + b'-'
                data = b'trigger-notification' + bytes(json.dumps(alarmInfo), encoding='utf-8')
                self.notifConn.send(data)
                return True
            else:
                print('notifConn is None')
                return False
        except Exception as e:
            print('[exception while sending alarm]')
            print(e)
            os._exit(1)

    def sendAlarm(self, trigger):
        try:
            alarmInfo = {
                'local': trigger.nome,
                'dateTime': time.mktime(datetime.datetime.now().timetuple()),
            }
            
            if self.notifConn is not None:
                # data = b'trigger-alarm' + bytes(nomeAlarme, encoding='utf-8') + b'-'
                data = b'trigger-alarm' + bytes(json.dumps(alarmInfo), encoding='utf-8')
                self.notifConn.send(data)
                return True

                #           TRYING TO SEND IMAGE THROUGH NOTIFICATION CONNECTION
                # frame = cv2.resize(self.cap.read()[1], (self.newImgSize, int(self.newImgSize * self.aspectRatio)))
                # ret, frameEncoded = cv2.imencode('.jpg', frame)
                # if not ret:
                #     print('error encoding on send alarm')
                #     return

                # frameSize = len(frameEncoded)
                # numPackets = ceil(frameSize / self.FRAGMENT_SIZE)

                # data = b'frame-packet----' + bytes(ctypes.c_uint32(frameSize)) + bytes(frameEncoded[:self.FRAGMENT_SIZE])
                        
                # self.notifConn.send(data)

                # packetID = 1
                # while(packetID < numPackets):
                #     fragIni = packetID * self.FRAGMENT_SIZE
                #     data = b'frame-packet' + bytes(frameEncoded[fragIni:fragIni + self.FRAGMENT_SIZE])
                #     self.notifConn.send(data)
                #     packetID += 1
                #     time.sleep(.02)

                # self.notifConn.send(data)
            else:
                print('notifConn is None')
                return False
        except Exception as e:
            print('exception while sending alarm:')
            print(e)
            os._exit(1)

    def queryTriggerEvents(self):
        for trigger in self.triggerQueue:
            self.sendTrigger(trigger)

    def sendTrigger(self, trigger):
        isSent = True
        try:
            self.triggerQueue.remove(trigger)
        except:
            pass

        if trigger.acao == 'Alarme':
            isSent = self.sendAlarm(trigger)
        elif trigger.acao == 'Notificação':
            isSent = self.sendNotification(trigger)

        if not isSent:
            self.triggerQueue.append(trigger)

