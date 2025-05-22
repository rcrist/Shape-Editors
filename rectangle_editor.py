from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.MenuBar import MenuBar
from GUI.RightDock import RightDock
from GUI.Grid import *
from Shapes.Rectangle import Rectangle
from GUI.GridView import GridView
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rectangle Editor")
        self.setGeometry(200, 100, 1200, 600)

        # Add MenuBar
        self.setMenuBar(MenuBar(self))

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create a QGraphicsView for the scene and set it as the central widget
        self.view = GridView(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.view)

        # Draw the shape on the scene
        self.shape = Rectangle(50, 50, 100, 100)
        self.scene.addItem(self.shape)

        # Right Dock (Properties) 
        self.right_dock = RightDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)
        self.right_dock.set_controls(self.shape)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())