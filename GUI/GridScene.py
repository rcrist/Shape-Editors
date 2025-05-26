from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class GridScene(QGraphicsScene):
    GRID_SIZE = 10

    def drawBackground(self, painter, rect):
        painter.save()
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        left = int(rect.left()) - (int(rect.left()) % self.GRID_SIZE)
        top = int(rect.top()) - (int(rect.top()) % self.GRID_SIZE)
        right = int(rect.right())
        bottom = int(rect.bottom())
        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += self.GRID_SIZE
        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += self.GRID_SIZE
        painter.restore()

    @staticmethod
    def snap_to_grid(x, y):
        grid = GridScene.GRID_SIZE
        return round(x / grid) * grid, round(y / grid) * grid