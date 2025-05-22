from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

GRID_SIZE = 10
GRID_COLOR = QColor("#333333")
IS_GRID_ENABLED = True

def draw_grid_background(scene, painter, rect, grid_size=GRID_SIZE, grid_color=GRID_COLOR):
    """
    Draws a grid background on the given QGraphicsScene using the provided painter and rect.
    """
    if not IS_GRID_ENABLED:
        return
    left = int(rect.left()) - (int(rect.left()) % grid_size)
    top = int(rect.top()) - (int(rect.top()) % grid_size)
    lines = []
    for x in range(left, int(rect.right()), grid_size):
        lines.append(QLineF(x, rect.top(), x, rect.bottom()))
    for y in range(top, int(rect.bottom()), grid_size):
        lines.append(QLineF(rect.left(), y, rect.right(), y))
    painter.setPen(QPen(grid_color, 1))
    painter.drawLines(lines)

def snap_to_grid(point, grid_size=20):
    """
    Snaps a point to the nearest grid line based on the specified grid size.
    """
    # Always return a QPointF for QPointF input
    if hasattr(point, 'x') and hasattr(point, 'y'):
        if not IS_GRID_ENABLED:
            return point
        x = round(point.x() / grid_size) * grid_size
        y = round(point.y() / grid_size) * grid_size
        return QPointF(x, y)
    elif isinstance(point, (int, float)):
        if not IS_GRID_ENABLED:
            return point
        return round(point / grid_size) * grid_size
    else:
        raise TypeError("snap_to_grid expects QPointF, QPoint, int, or float")