from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Shapes.BaseShapeItem import BaseShapeItem
from GUI.Grid import snap_to_grid, GRID_SIZE

class Triangle(QGraphicsPolygonItem, BaseShapeItem):
    def __init__(self, x, y, w, h):
        super().__init__()
        # Define the three points of the triangle
        points = [
            QPointF(x + w / 2, y),           # Top center
            QPointF(x, y + h),               # Bottom left
            QPointF(x + w, y + h)            # Bottom right
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)
        self.setBrush(QBrush(Qt.GlobalColor.blue))
        self.setPen(QPen(Qt.GlobalColor.darkGray, 3))
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

    def rect(self):
        # Return the bounding rectangle for compatibility
        return self.polygon().boundingRect()

    def setRect(self, rect):
        # Update the triangle's points based on the new rect
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        points = [
            QPointF(x + w / 2, y),
            QPointF(x, y + h),
            QPointF(x + w, y + h)
        ]
        self.setPolygon(QPolygonF(points))

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Force the view to update to prevent artifacts
            scene = self.scene()
            if scene is not None:
                for view in scene.views():
                    view.viewport().update()
            return snap_to_grid(value, GRID_SIZE)
        return super().itemChange(change, value)
    
    def to_dict(self):
        pos = self.pos()
        return {
            "type": "triangle",
            "x": self.rect().x(),
            "y": self.rect().y(),
            "width": self.rect().width(),
            "height": self.rect().height(),
            "rotation": self.rotation(),
            "fill_color": self.brush().color().name(),
            "border_color": self.pen().color().name(),
            "border_width": self.pen().widthF(),
            "pos_x": pos.x(),
            "pos_y": pos.y()
        }

    @classmethod
    def from_dict(cls, data):
        rect = cls(
            data.get("x", 0),
            data.get("y", 0),
            data.get("width", 100),
            data.get("height", 100)
        )
        rect.setRotation(data.get("rotation", 0))
        rect.setBrush(QBrush(QColor(data.get("fill_color", "#0000ff"))))
        rect.setPen(QPen(
            QColor(data.get("border_color", "#000000")),
            data.get("border_width", 3)
        ))
        # Set the scene position after creation
        rect.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        return rect