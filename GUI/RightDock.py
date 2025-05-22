from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.Grid import *

class RightDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.main_widget = QWidget()
        self.form_layout = QFormLayout()
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.height_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)

        self.width_slider.setRange(10, 400)
        self.height_slider.setRange(10, 400)
        self.rotation_slider.setRange(0, 360)

        self.form_layout.addRow(QLabel("Width"), self.width_slider)
        self.form_layout.addRow(QLabel("Height"), self.height_slider)
        self.form_layout.addRow(QLabel("Rotation"), self.rotation_slider)

        # --- Controls for color and border ---
        self.fill_color_btn = QPushButton("Fill Color")
        self.border_color_btn = QPushButton("Border Color")
        self.border_width_spin = QSpinBox()
        self.border_width_spin.setRange(1, 20)
        self.form_layout.addRow(QLabel("Fill Color"), self.fill_color_btn)
        self.form_layout.addRow(QLabel("Border Color"), self.border_color_btn)
        self.form_layout.addRow(QLabel("Border Width"), self.border_width_spin)
        # ----------------------------------------

        self.main_widget.setLayout(self.form_layout)
        self.setWidget(self.main_widget)
        self.item = None

        self.width_slider.valueChanged.connect(self.update_width)
        self.height_slider.valueChanged.connect(self.update_height)
        self.rotation_slider.valueChanged.connect(self.update_rotation)
        self.fill_color_btn.clicked.connect(self.change_fill_color)
        self.border_color_btn.clicked.connect(self.change_border_color)
        self.border_width_spin.valueChanged.connect(self.change_border_width)

    def set_controls(self, item):
        self.item = item
        rect = item.rect()
        self.width_slider.setValue(int(rect.width()))
        self.height_slider.setValue(int(rect.height()))
        self.rotation_slider.setValue(int(getattr(item, "rotation_angle", 0)))
        # Set color controls to current item state if available
        if hasattr(item, "pen") and hasattr(item, "brush"):
            pen = item.pen()
            self.border_width_spin.setValue(pen.width())
            # Optionally, update button color previews here
            self.fill_color_btn.setEnabled(True)
            self.border_color_btn.setEnabled(True)
            self.border_width_spin.setEnabled(True)
        else:
            self.fill_color_btn.setEnabled(False)
            self.border_color_btn.setEnabled(False)
            self.border_width_spin.setEnabled(False)

    def update_width(self, value):
        if self.item:
            self.item.setWidth(value)

    def update_height(self, value):
        if self.item:
            self.item.setHeight(value)

    def update_rotation(self, value):
        if self.item:
            self.item.setRotationAngle(value)

    def change_fill_color(self):
        if self.item:
            color = QColorDialog.getColor(self.item.brush().color(), self, "Select Fill Color")
            if color.isValid():
                self.item.setBrush(QBrush(color))

    def change_border_color(self):
        if self.item:
            color = QColorDialog.getColor(self.item.pen().color(), self, "Select Border Color")
            if color.isValid():
                pen = self.item.pen()
                pen.setColor(color)
                self.item.setPen(pen)

    def change_border_width(self, value):
        if self.item:
            pen = self.item.pen()
            pen.setWidth(value)
            self.item.setPen(pen)