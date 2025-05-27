from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *
from Shapes.Rectangle import Rectangle
from Shapes.Ellipse import Ellipse
from Shapes.Triangle import Triangle
from Shapes.Line import Line
from Shapes.Text import Text
from Shapes.Image import Image

class LeftDock(QDockWidget):
    def __init__(self, parent=None, scene=None, view=None):
        super().__init__("Shapes", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.scene = scene
        self.view = view
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Shape buttons
        self.rect_button = QPushButton("Rectangle")
        self.ellipse_button = QPushButton("Ellipse")
        self.triangle_button = QPushButton("Triangle")
        self.line_button = QPushButton("Line")
        self.text_button = QPushButton("Text")
        self.image_button = QPushButton("Image")

        self.layout.addWidget(self.rect_button)
        self.layout.addWidget(self.ellipse_button)
        self.layout.addWidget(self.triangle_button)
        self.layout.addWidget(self.line_button)
        self.layout.addWidget(self.text_button)
        self.layout.addWidget(self.image_button)
        self.layout.addStretch()
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

        # Connect buttons
        self.rect_button.clicked.connect(lambda: self.add_shape("rectangle"))
        self.ellipse_button.clicked.connect(lambda: self.add_shape("ellipse"))
        self.triangle_button.clicked.connect(lambda: self.add_shape("triangle"))
        self.line_button.clicked.connect(lambda: self.add_shape("line"))
        self.text_button.clicked.connect(lambda: self.add_shape("text"))
        self.image_button.clicked.connect(lambda: self.add_shape("image"))

    def add_shape(self, shape_type):
        if not self.scene:
            return

        shape_map = {
            "rectangle": (Rectangle, (100, 50, 100, 100)),
            "ellipse": (Ellipse, (100, 50, 100, 100)),
            "triangle": (Triangle, (100, 50, 100, 100)),
            "line": (Line, (50, 50, 100, 100)),
            "text": (Text, (100, 100)),
            "image": (Image, (100, 50, 100, 100)),
        }

        if shape_type in shape_map:
            shape_class, args = shape_map[shape_type]
            item = shape_class(*args)
            self.scene.addItem(item)
            item.setSelected(True)