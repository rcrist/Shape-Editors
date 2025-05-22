from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.Grid import *

class BaseShapeItem:
    def __init__(self):
        self.setFlags(
            QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
            
    def setWidth(self, width):
        width = snap_to_grid(width)
        rect = self.rect()
        rect.setWidth(width)
        self.setRect(rect)
        if hasattr(self, "setTransformOriginPoint"):
            self.setTransformOriginPoint(rect.center())

    def setHeight(self, height):
        height = snap_to_grid(height)
        rect = self.rect()
        rect.setHeight(height)
        self.setRect(rect)
        if hasattr(self, "setTransformOriginPoint"):
            self.setTransformOriginPoint(rect.center())

    def setRotationAngle(self, angle):
        self.setRotation(angle)
        self.rotation_angle = angle

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            new_pos = value
            snapped_x = snap_to_grid(new_pos.x())
            snapped_y = snap_to_grid(new_pos.y())
            return QPointF(snapped_x, snapped_y)
        # Call the correct Qt base class method
        if isinstance(self, QGraphicsRectItem):
            return QGraphicsRectItem.itemChange(self, change, value)
        elif isinstance(self, QGraphicsEllipseItem):
            return QGraphicsEllipseItem.itemChange(self, change, value)
        elif isinstance(self, QGraphicsPolygonItem):
            return QGraphicsPolygonItem.itemChange(self, change, value)
        elif isinstance(self, QGraphicsLineItem):
            return QGraphicsLineItem.itemChange(self, change, value)
        elif isinstance(self, QGraphicsTextItem):
            return QGraphicsTextItem.itemChange(self, change, value)
        elif isinstance(self, QGraphicsPixmapItem):
            return QGraphicsPixmapItem.itemChange(self, change, value)
        else:
            return value  # fallback