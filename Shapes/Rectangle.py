from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Shapes.BaseShapeItem import BaseShapeItem
from GUI.Grid import snap_to_grid, GRID_SIZE

class Rectangle(QGraphicsRectItem, BaseShapeItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        self.setBrush(QBrush(Qt.GlobalColor.blue))
        self.setPen(QPen(Qt.GlobalColor.black, 3))
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Force the view to update to prevent artifacts
            for view in self.scene().views():
                view.viewport().update()
            return snap_to_grid(value, GRID_SIZE)
        return super().itemChange(change, value)