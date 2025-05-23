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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
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
        self.shape = Image(100, 100, 200, 200)
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
        self.rotation_slider.valueChanged.connect(self.rotate_shape)

        # Image scale control
        layout.addWidget(QLabel("Image Scale:"))
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setMinimum(10)
        self.scale_slider.setMaximum(1000)
        self.scale_slider.setValue(int(self.shape.rect().width()))
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
        self.update_image_preview(self.shape.image_path)
        layout.addWidget(self.image_preview)

        dock.setWidget(slider_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def update_image_size(self):
        scale = self.scale_slider.value()
        # Snap the current position to the grid
        x, y = GridScene.snap_to_grid(self.shape.pos().x(), self.shape.pos().y())
        self.shape.setPos(x, y)
        self.shape.set_image(self.shape.image_path, scale, scale)
        self.update_image_preview(self.shape.image_path)

    def select_image_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                # Update the image in the scene
                rect = self.shape.rect()
                self.shape.set_image(image_path, rect.width(), rect.height())
                self.update_image_preview(image_path)

    def update_image_preview(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.image_preview.width(), self.image_preview.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_preview.setPixmap(pixmap)
        else:
            self.image_preview.clear()

    def rotate_shape(self, angle):
        # Get the center of the shape item's bounding rect in item coordinates
        rect = self.shape.boundingRect()
        center = rect.center()
        self.shape.setTransformOriginPoint(center)
        self.shape.setRotation(angle)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())