from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.MenuBar import MenuBar
from GUI.GridScene import *
from Shapes.Image import Image
import sys

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

        # Add MenuBar
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
        menu_bar.apply_dark_theme()

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