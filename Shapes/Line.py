from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Shapes.BaseShapeItem import BaseShapeItem
from GUI.Grid import snap_to_grid, GRID_SIZE

class Line(QGraphicsLineItem, BaseShapeItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

        self.line_color = Qt.GlobalColor.darkGray
        self.line_width = 3
        self.line_style = Qt.PenStyle.SolidLine
        self.cap_style = Qt.PenCapStyle.SquareCap

        self.setPen(QPen(self.line_color, self.line_width, self.line_style, self.cap_style))
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

    def rect(self):
        return self.boundingRect()
    
    def setRect(self, rect):
        pass

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Force the view to update to prevent artifacts
            scene = self.scene()
            if scene is not None:
                for view in scene.views():
                    view.viewport().update()
            return snap_to_grid(value, GRID_SIZE)
        return super().itemChange(change, value)
    
    def set_line_color(self, color):
        self.line_color = color
        self.setPen(QPen(color, self.line_width, self.line_style, self.cap_style))

    def set_line_width(self, width):
        self.line_width = width
        self.setPen(QPen(self.line_color, width, self.line_style, self.cap_style))

    def set_line_style(self, style):
        self.line_style = style
        self.setPen(QPen(self.line_color, self.line_width, style, self.cap_style))

    def set_cap_style(self, cap_style): 
        self.cap_style = cap_style
        self.setPen(QPen(self.line_color, self.line_width, self.line_style, cap_style))