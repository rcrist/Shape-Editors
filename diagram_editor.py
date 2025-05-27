# PyQt6 & system imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Custom class imports
from GUI.GridScene import GridScene
from GUI.GridView import GridView
from GUI.MenuBar import *
from GUI.LeftDock import LeftDock
from GUI.RightDock import RightDock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagram Editor")
        self.setGeometry(200, 100, 1200, 600)

         # Add MenuBar
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
        menu_bar.apply_dark_theme()

        # Create the Scene
        self.scene = GridScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create the View
        self.view = GridView(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        # Left Dock (Shapes)
        self.left_dock = LeftDock(self, self.scene, self.view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        # Right Dock (Properties) 
        self.right_dock = RightDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)

        # Connect selection change to update properties panel
        self.scene.selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        selected_items = self.scene.selectedItems()
        if selected_items:
            self.right_dock.set_controls(selected_items[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())