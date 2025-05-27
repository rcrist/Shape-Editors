from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.Grid import *
from GUI.MenuBar import rotation_snap_angle
from GUI.GridScene import *

from Shapes.Rectangle import Rectangle
from Shapes.Ellipse import Ellipse
from Shapes.Triangle import Triangle
from Shapes.Text import Text
from Shapes.Line import Line
from Shapes.Image import Image

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
        # Remove old controls
        self.setWidget(None)
        self.item = item

        if isinstance(item, (Rectangle, Ellipse, Triangle)):
            # Add default controls
            self.form_layout.addRow(QLabel("Width"), self.width_slider)
            self.form_layout.addRow(QLabel("Height"), self.height_slider)
            self.form_layout.addRow(QLabel("Rotation"), self.rotation_slider)
            self.form_layout.addRow(QLabel("Fill Color"), self.fill_color_btn)
            self.form_layout.addRow(QLabel("Border Color"), self.border_color_btn)
            self.form_layout.addRow(QLabel("Border Width"), self.border_width_spin)

            rect = item.rect()
            self.width_slider.setValue(int(rect.width()))
            self.height_slider.setValue(int(rect.height()))
            self.rotation_slider.setValue(int(getattr(item, "rotation_angle", 0)))
            if hasattr(item, "pen") and hasattr(item, "brush"):
                pen = item.pen()
                self.border_width_spin.setValue(pen.width())
                self.fill_color_btn.setEnabled(True)
                self.border_color_btn.setEnabled(True)
                self.border_width_spin.setEnabled(True)
            else:
                self.fill_color_btn.setEnabled(False)
                self.border_color_btn.setEnabled(False)
                self.border_width_spin.setEnabled(False)
        elif isinstance(item, Text):
            self.set_text_controls(item)
        elif isinstance(item, Line):
            self.set_line_controls(item)
        elif isinstance(item, Image):
            self.set_image_controls(item)
        else:
            # For other shapes, you may want to clear controls or add generic ones
            self.setWidget(QWidget())

    def update_width(self, value):
        if self.item:
            self.item.setWidth(value)
            for view in self.item.scene().views():
                view.viewport().update()

    def update_height(self, value):
        if self.item:
            self.item.setHeight(value)
            for view in self.item.scene().views():
                view.viewport().update()

    def update_rotation(self, value):
        import GUI.Grid
        if self.item:
            if GUI.Grid.IS_GRID_ENABLED:
                snapped_angle = round(value / rotation_snap_angle) * rotation_snap_angle
            else:
                snapped_angle = value
            self.item.setRotation(snapped_angle)
            for view in self.item.scene().views():
                view.viewport().update()

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

    # Text controls
    def set_text_controls(self, shape):
        self.item = shape  # Store the current item for use in other methods

        slider_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        slider_widget.setLayout(layout)

        # Rotation controls
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(int(shape.rotation()))
        layout.addWidget(QLabel("Rotation (deg):"))
        layout.addWidget(self.rotation_slider)
        self.rotation_slider.valueChanged.connect(self.rotate_text)

        # Text color controls (color picker)
        layout.addWidget(QLabel("Text Color:"))
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_text_color)
        layout.addWidget(self.color_button)

        # Font family controls
        layout.addWidget(QLabel("Font:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(shape.font())
        layout.addWidget(self.font_combo)
        self.font_combo.currentFontChanged.connect(self.update_text_font)

        # Font size controls
        layout.addWidget(QLabel("Font Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 72)
        self.font_size_spin.setValue(shape.font().pointSize())
        layout.addWidget(self.font_size_spin)
        self.font_size_spin.valueChanged.connect(self.update_text_font)

        # Set the new widget as the dock's widget
        self.setWidget(slider_widget)

    def update_text_font(self):
        font = self.font_combo.currentFont()
        font.setPointSize(self.font_size_spin.value())
        self.item.setFont(font)

    def rotate_text(self, angle):
        if self.item:
            rect = self.item.boundingRect()
            self.item.setTransformOriginPoint(rect.center())
            self.item.setRotation(angle)

    def choose_text_color(self):
        # Use defaultTextColor for QGraphicsTextItem (Text)
        if hasattr(self.item, "defaultTextColor"):
            current_color = self.item.defaultTextColor()
        else:
            current_color = Qt.GlobalColor.black
        color = QColorDialog.getColor(initial=current_color, parent=self, title="Select Text Color")
        if color.isValid():
            if hasattr(self.item, "setDefaultTextColor"):
                self.item.setDefaultTextColor(color)
            self.color_button.setStyleSheet(f"background-color: {color.name()};")

    def update_text_pen(self):
        color = getattr(self.item, "line_color", Qt.GlobalColor.white)
        pen = QPen(color)
        self.item.setPen(pen)

    # Line controls
    def set_line_controls(self, shape):
        slider_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        slider_widget.setLayout(layout)

        # Rotation controls
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        layout.addWidget(QLabel("Rotation (deg):"))
        layout.addWidget(self.rotation_slider)
        self.rotation_slider.valueChanged.connect(self.rotate_line)

        # Line color controls (color picker)
        layout.addWidget(QLabel("Line Color:"))
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_line_color)
        layout.addWidget(self.color_button)

        # Line width controls
        layout.addWidget(QLabel("Line Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 20)
        self.width_spin.setValue(3)
        layout.addWidget(self.width_spin)
        self.width_spin.valueChanged.connect(self.update_line_pen)

        # Line style controls
        layout.addWidget(QLabel("Line Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItem("Solid", Qt.PenStyle.SolidLine)
        self.style_combo.addItem("Dash", Qt.PenStyle.DashLine)
        self.style_combo.addItem("Dot", Qt.PenStyle.DotLine)
        self.style_combo.addItem("Dash Dot", Qt.PenStyle.DashDotLine)
        self.style_combo.addItem("Dash Dot Dot", Qt.PenStyle.DashDotDotLine)
        self.style_combo.setCurrentIndex(0)
        layout.addWidget(self.style_combo)
        self.style_combo.currentIndexChanged.connect(self.update_line_pen)

        # Cap style controls
        layout.addWidget(QLabel("Cap Style:"))
        self.cap_combo = QComboBox()
        self.cap_combo.addItem("Square", Qt.PenCapStyle.SquareCap)
        self.cap_combo.addItem("Flat", Qt.PenCapStyle.FlatCap)
        self.cap_combo.addItem("Round", Qt.PenCapStyle.RoundCap)
        self.cap_combo.setCurrentIndex(0)
        layout.addWidget(self.cap_combo)
        self.cap_combo.currentIndexChanged.connect(self.update_line_pen)

        # Set the new widget as the dock's widget
        self.setWidget(slider_widget)

    def rotate_line(self, angle):
        # Get the center of the line
        line = self.item.line()
        center = line.pointAt(0.5)
        self.item.setTransformOriginPoint(center)
        self.item.setRotation(angle)

    def choose_line_color(self):
        color = QColorDialog.getColor(initial=self.item.pen().color(), parent=self, title="Select Line Color")
        if color.isValid():
            self.item.line_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_line_pen()

    def update_line_pen(self):
        color = getattr(self.item, "line_color", Qt.GlobalColor.white)
        width = self.width_spin.value()
        style = self.style_combo.currentData()
        cap = self.cap_combo.currentData()
        pen = QPen(color, width, style, cap)
        self.item.setPen(pen)

    # Image controls
    def set_image_controls(self, shape):
        slider_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        slider_widget.setLayout(layout)

        # Rotation controls
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        layout.addWidget(QLabel("Rotation (deg):"))
        layout.addWidget(self.rotation_slider)
        self.rotation_slider.valueChanged.connect(self.rotate_image)

        # Image scale control
        layout.addWidget(QLabel("Image Scale:"))
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setMinimum(10)
        self.scale_slider.setMaximum(1000)
        self.scale_slider.setValue(int(self.item.rect().width()))
        layout.addWidget(self.scale_slider)
        self.scale_slider.valueChanged.connect(self.update_image_size)

        # Image file selector
        layout.addWidget(QLabel("Image File:"))
        self.image_select_button = QPushButton("Select Image")
        layout.addWidget(self.image_select_button)
        self.image_select_button.clicked.connect(self.select_image_file)

        # Image preview
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(120, 120)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_image_preview(self.item.image_path)
        layout.addWidget(self.image_preview)

        # Set the new widget as the dock's widget
        self.setWidget(slider_widget)

    def update_image_size(self):
        scale = self.scale_slider.value()
        # Snap the current position to the grid
        x, y = GridScene.snap_to_grid(self.item.pos().x(), self.item.pos().y())
        self.item.setPos(x, y)
        self.item.set_image(self.item.image_path, scale, scale)
        self.update_image_preview(self.item.image_path)

    def select_image_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                # Update the image in the scene
                rect = self.item.rect()
                self.item.set_image(image_path, rect.width(), rect.height())
                self.update_image_preview(image_path)

    def update_image_preview(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.image_preview.width(), self.image_preview.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_preview.setPixmap(pixmap)
        else:
            self.image_preview.clear()

    def rotate_image(self, angle):
        # Get the center of the item's bounding rect in item coordinates
        rect = self.item.boundingRect()
        center = rect.center()
        self.item.setTransformOriginPoint(center)
        self.item.setRotation(angle)