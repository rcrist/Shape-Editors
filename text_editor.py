from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.MenuBar import *
from GUI.Grid import *
from Shapes.Text import Text
import sys

class GridScene(QGraphicsScene):
    GRID_SIZE = 10

    def drawBackground(self, painter, rect):
        painter.save()
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        left = int(rect.left()) - (int(rect.left()) % self.GRID_SIZE)
        top = int(rect.top()) - (int(rect.top()) % self.GRID_SIZE)
        right = int(rect.right())
        bottom = int(rect.bottom())
        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += self.GRID_SIZE
        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += self.GRID_SIZE
        painter.restore()

    @staticmethod
    def snap_to_grid(x, y):
        grid = GridScene.GRID_SIZE
        return round(x / grid) * grid, round(y / grid) * grid

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
        self.shape = Text(100, 100)
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
        self.rotation_slider.valueChanged.connect(self.rotate_text)

        # Text color controls (color picker)
        layout.addWidget(QLabel("Text Color:"))
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_text_color)
        layout.addWidget(self.color_button)

        # Font family controls
        layout.addWidget(QLabel("Font:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(self.shape.font())
        layout.addWidget(self.font_combo)
        self.font_combo.currentFontChanged.connect(self.update_text_font)

        # Font size controls
        layout.addWidget(QLabel("Font Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 72)
        self.font_size_spin.setValue(self.shape.font().pointSize())
        layout.addWidget(self.font_size_spin)
        self.font_size_spin.valueChanged.connect(self.update_text_font)

        dock.setWidget(slider_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def update_text_font(self):
        font = self.font_combo.currentFont()
        font.setPointSize(self.font_size_spin.value())
        self.shape.setFont(font)

    def rotate_text(self, angle):
        # Get the center of the text item's bounding rect in item coordinates
        rect = self.shape.boundingRect()
        center = rect.center()
        self.shape.setTransformOriginPoint(center)
        self.shape.setRotation(angle)

    def choose_text_color(self):
        color = QColorDialog.getColor(initial=self.shape.pen().color(), parent=self, title="Select Line Color")
        if color.isValid():
            self.shape.line_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_text_pen()

    def update_text_pen(self):
        color = getattr(self.shape, "line_color", Qt.GlobalColor.white)
        pen = QPen(color)
        self.shape.setPen(pen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())