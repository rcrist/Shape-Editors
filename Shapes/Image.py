from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *

class Image(QGraphicsPixmapItem):
    def __init__(self, x, y, w, h, image_path=None):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setPos(x, y)
        default_path = "C:\\python_projects\\images\\earth.jpg"
        if image_path:
            self.image_path = image_path
            self.set_image(image_path, w, h)
        else:
            self.image_path = default_path
            self.set_image(default_path, w, h)

    def set_image(self, image_path, w, h):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(int(w), int(h), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(pixmap)
            self.image_path = image_path

    def rect(self):
        return QRectF(self.pos().x(), self.pos().y(), self.pixmap().width(), self.pixmap().height())

    def setRect(self, rect):
        # Rescale the image to the new rect size
        if self.image_path:
            self.set_image(self.image_path, int(rect.width()), int(rect.height()))
        self.setPos(rect.left(), rect.top())

    def brush(self):
        # Not used, but for compatibility
        return QBrush()

    def setBrush(self, brush):
        pass

    def pen(self):
        # Not used, but for compatibility
        return QPen()

    def setPen(self, pen):
        pass

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Snap the new position to the grid
            x, y = value.x(), value.y()
            snapped_x, snapped_y = GridScene.snap_to_grid(x, y)
            return QPointF(snapped_x, snapped_y)
        return super().itemChange(change, value)
    
    def to_dict(self):
        pos = self.pos()
        return {
            "type": "image",
            "x": self.rect().x(),
            "y": self.rect().y(),
            "width": self.rect().width(),
            "height": self.rect().height(),
            "rotation": self.rotation(),
            "image_path": self.image_path,
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
        # Restore the image path
        image_path = data.get("image_path", "C:\\python_projects\\images\\earth.jpg")
        # Set the scene position after creation
        rect.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        return rect