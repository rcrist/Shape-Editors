from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *

class BaseShapeItem:
    def __init__(self):
        self.setFlags(
            QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
            
    def setWidth(self, width):
        width = GridScene.snap_to_grid(width, 0)[0]  # Use only the snapped x value
        rect = self.rect()
        rect.setWidth(width)
        self.setRect(rect)
        if hasattr(self, "setTransformOriginPoint"):
            self.setTransformOriginPoint(rect.center())

    def setHeight(self, height):
        height = GridScene.snap_to_grid(0, height)[1]  # Use only the snapped y value
        rect = self.rect()
        rect.setHeight(height)
        self.setRect(rect)
        if hasattr(self, "setTransformOriginPoint"):
            self.setTransformOriginPoint(rect.center())

    def setRotationAngle(self, angle):
        self.setRotation(angle)
        self.rotation_angle = angle