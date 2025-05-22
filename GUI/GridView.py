from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QRectF
from .Grid import draw_grid_background  # Adjust import as needed

class GridView(QGraphicsView):
    def drawBackground(self, painter: QPainter, rect: QRectF):
        if self.scene():
            draw_grid_background(self.scene(), painter, rect)