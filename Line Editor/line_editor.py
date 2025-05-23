from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
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

class Line(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

        self.line_color = Qt.GlobalColor.white
        self.line_width = 3
        self.line_style = Qt.PenStyle.SolidLine
        self.cap_style = Qt.PenCapStyle.SquareCap

        self.setPen(QPen(self.line_color, self.line_width, self.line_style, self.cap_style))

        self._dragging_point = None  # None, 0 (p1), or 1 (p2)
        self._drag_offset = QPointF(0, 0)

    def paint(self, painter, option, widget=None):
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.setPen(self.pen())
        painter.drawLine(self.line())

        # If selected, draw blue rectangles at endpoints
        if self.isSelected():
            rect_size = 10
            half = rect_size / 2
            line = self.line()
            for pt in [line.p1(), line.p2()]:
                rect = QRectF(pt.x() - half, pt.y() - half, rect_size, rect_size)
                painter.setBrush(QBrush(Qt.GlobalColor.blue))
                painter.setPen(Qt.GlobalColor.blue)
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        if self.isSelected():
            rect_size = 10
            half = rect_size / 2
            line = self.line()
            mouse_pos = event.pos()
            for idx, pt in enumerate([line.p1(), line.p2()]):
                rect = QRectF(pt.x() - half, pt.y() - half, rect_size, rect_size)
                if rect.contains(mouse_pos):
                    self._dragging_point = idx
                    self._drag_offset = mouse_pos - pt
                    event.accept()
                    return
        self._dragging_point = None
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging_point is not None:
            line = self.line()
            new_pt = event.pos() - self._drag_offset
            snapped_x, snapped_y = GridScene.snap_to_grid(new_pt.x(), new_pt.y())
            if self._dragging_point == 0:
                self.setLine(snapped_x, snapped_y, *GridScene.snap_to_grid(line.x2(), line.y2()))
            else:
                self.setLine(*GridScene.snap_to_grid(line.x1(), line.y1()), snapped_x, snapped_y)
            event.accept()
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging_point = None
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Get the new position as x, y
            x, y = value.x(), value.y()
            snapped_x, snapped_y = GridScene.snap_to_grid(x, y)
            return QPointF(snapped_x, snapped_y)
        return super().itemChange(change, value)

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