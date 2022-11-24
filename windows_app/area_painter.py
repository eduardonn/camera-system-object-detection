import cv2
import numpy as np
from PyQt5.QtGui import QCursor
import gatilhos

class AreaPainter:
    AREA_COLOR_STANDARD = (0, 255, 0)
    AREA_COLOR_DETECTING = (0, 255, 255)
    AREA_COLOR_GATILHO_ACIONADO = (0, 0, 255)
    AREA_CONTOUR_COLOR = (80, 0, 80)
    
    def __init__(self):
        self.areaStartPoint = None
        self.areaEndPoint = None
        self.areas = [[[0, 0], [0, 0]]]

    def paintAreasAddGatilho(self, frame):
        areas = np.zeros_like(frame, np.uint8)

        # Draw saved areas
        for area in self.areas:
            cv2.rectangle(areas, area[0], area[1], self.AREA_COLOR_STANDARD, cv2.FILLED)
            # cv2.rectangle(areas, area[0], area[1], self.AREA_CONTOUR_COLOR, 2) # Contorno
        
        # Draw area being drawn
        if (self.areaStartPoint != None) & (self.areaEndPoint != None):
            cv2.rectangle(areas, self.areaStartPoint, self.areaEndPoint, self.AREA_COLOR_STANDARD, cv2.FILLED)
            # cv2.rectangle(areas, self.areaStartPoint, self.areaEndPoint, self.AREA_CONTOUR_COLOR, 2) # Contorno

        mask = areas.astype(bool)
        alpha = 0.5
        frame[mask] = cv2.addWeighted(frame, alpha, areas, 1 - alpha, 0)[mask]

    def paintAreasMainImg(self, frame):
        areas = np.zeros_like(frame)
        h, w = frame.shape[:2]
        
        for gatilho in gatilhos.triggerList:
            startPoint = (int(gatilho.areaStartX * w), int(gatilho.areaStartY * h))
            endPoint = (int(gatilho.areaEndX * w), int(gatilho.areaEndY * h))
            
            if gatilho.acionado:
                areaColor = self.AREA_COLOR_GATILHO_ACIONADO
            elif gatilho.bDetectionInside:
                areaColor = self.AREA_COLOR_DETECTING
            else:
                areaColor = self.AREA_COLOR_STANDARD
            cv2.rectangle(areas, startPoint, endPoint, areaColor, cv2.FILLED)
            
        beta = 0.25
        return cv2.addWeighted(frame, 1, areas, beta, 0)

        # Too slow
        alpha = 0.5
        mask = areas.astype(bool)
        frame[mask] = cv2.addWeighted(frame, alpha, areas, 1 - alpha, 0)[mask]
    
    def updateArea(self):
        self.areaEndPoint = self.getWidgetCoord()

    def startArea(self, widget):
        self.widget = widget
        self.areaStartPoint = self.getWidgetCoord()
        self.areaEndPoint = self.getWidgetCoord()

    def saveArea(self):
        # self.areas.append([self.areaStartPoint, self.areaEndPoint]) # For more than one area per trigger
        self.areas[0] = [self.areaStartPoint, self.areaEndPoint]
        self.areaStartPoint = None
        self.areaEndPoint = None

    def deleteLastArea(self):
        if len(self.areas) > 0:
            self.areas.pop()

    def getWidgetCoord(self):
        globalCoords = QCursor.pos()
        coords = self.widget.mapFromGlobal(globalCoords)
        return (coords.x(), coords.y())