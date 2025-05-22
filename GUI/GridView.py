from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QRectF
from .Grid import draw_grid_background

class GridView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    # Called automatically by the Qt framework whenever the background needs to be redrawn
    def drawBackground(self, painter: QPainter, rect: QRectF):
        if self.scene():
            draw_grid_background(self.scene(), painter, rect)