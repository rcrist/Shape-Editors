from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *

class Text(QGraphicsTextItem):
    def __init__(self, x, y):
        super().__init__("Hello World!")
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setDefaultTextColor(Qt.GlobalColor.blue)
        font = QFont()
        font.setPointSize(18)
        self.setFont(font)
        self.setPos(x, y)
        # Use setFlag, not setFlags, for QGraphicsTextItem
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def rect(self):
        # Return a QRectF for compatibility
        return QRectF(self.pos().x(), self.pos().y(), self.boundingRect().width(), self.boundingRect().height())

    def setRect(self, rect):
        # Move the text to the new position
        self.setPos(rect.left(), rect.top())

    def setPen(self, pen):
        self.setDefaultTextColor(pen.color())

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Snap the new position to the grid
            x, y = value.x(), value.y()
            snapped_x, snapped_y = GridScene.snap_to_grid(x, y)
            return GridScene.snap_to_grid(x, y)
        return super().itemChange(change, value)
    
    def to_dict(self):
        pos = self.pos()
        font = self.font()
        return {
            "type": "text",
            "x": self.rect().x(),
            "y": self.rect().y(),
            "text_string": self.toPlainText(),
            "rotation": self.rotation(),
            "border_color": self.pen().color().name(),
            "border_width": self.pen().widthF(),
            "pos_x": pos.x(),
            "pos_y": pos.y(),
            "font_family": font.family(),
            "font_size": font.pointSize()
        }

    @classmethod
    def from_dict(cls, data):
        rect = cls(
            data.get("x", 0),
            data.get("y", 0)
        )
        rect.setPlainText(data.get("text_string", "Hello World!"))
        rect.setRotation(data.get("rotation", 0))
        rect.setPen(QPen(
            QColor(data.get("border_color", "#000000")),
            data.get("border_width", 3)
        ))
        # Restore font
        font = rect.font()
        font.setFamily(data.get("font_family", font.family()))
        font.setPointSize(data.get("font_size", font.pointSize()))
        rect.setFont(font)
        # Set the scene position after creation
        rect.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        return rect