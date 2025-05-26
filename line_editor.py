from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.MenuBar import MenuBar
from GUI.GridScene import *
from Shapes.Line import Line
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Line Editor")
        self.setGeometry(200, 100, 1200, 600)

        # Create a QGraphicsScene
        self.scene = GridScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create a QGraphicsView for the scene and set it as the central widget
        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.view)

        # Add MenuBar
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
        menu_bar.apply_dark_theme()

        # Draw the shape on the scene
        self.shape = Line(50, 50, 100, 100)
        self.scene.addItem(self.shape)

        # Add properties dock widget with line appearance controls
        self.create_properties_dock()

    def create_properties_dock(self):
        dock = QDockWidget("Properties", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
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

        dock.setWidget(slider_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def rotate_line(self, angle):
        # Get the center of the line
        line = self.shape.line()
        center = line.pointAt(0.5)
        self.shape.setTransformOriginPoint(center)
        self.shape.setRotation(angle)

    def choose_line_color(self):
        color = QColorDialog.getColor(initial=self.shape.pen().color(), parent=self, title="Select Line Color")
        if color.isValid():
            self.shape.line_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_line_pen()

    def update_line_pen(self):
        color = getattr(self.shape, "line_color", Qt.GlobalColor.white)
        width = self.width_spin.value()
        style = self.style_combo.currentData()
        cap = self.cap_combo.currentData()
        pen = QPen(color, width, style, cap)
        self.shape.setPen(pen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())