from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from GUI.Grid import *
from Shapes.Rectangle import Rectangle
import json

IS_DARK_MODE = True

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # File Menu
        file_menu = self.addMenu("File")
        new_action = file_menu.addAction("New")
        new_action.triggered.connect(self.new_file)
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        print_action = file_menu.addAction("Print")
        print_action.triggered.connect(self.print_diagram)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)

        # Settings Menu
        settings_menu = self.addMenu("Settings")
        toggle_grid_action = settings_menu.addAction("Toggle Grid")
        toggle_grid_action.triggered.connect(self.toggle_grid)
        toggle_theme_action = settings_menu.addAction("Toggle Theme")
        toggle_theme_action.triggered.connect(self.toggle_theme)

    def toggle_theme(self):
        IS_DARK_MODE = not IS_DARK_MODE

        main_window = self.parent()
        if hasattr(main_window, "view"):
            if IS_DARK_MODE:
                main_window.view.setBackgroundBrush(QBrush(Qt.GlobalColor.black))
            else:
                main_window.view.setBackgroundBrush(QBrush(Qt.GlobalColor.white))

        # Simple dark/light mode toggle using QApplication palette
        app = QApplication.instance()
        palette = app.palette()
        if not IS_DARK_MODE:
            # Switch to light mode
            app.setPalette(QApplication.style().standardPalette())
            # Set menubar and menu drop downs to light mode
            self.setStyleSheet("""
                QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                    background: #f0f0f0;
                    color: #000;
                }
                QMenuBar::item:selected, QMenu::item:selected {
                    background: #d0d0d0;
                }
            """)
        else:
            # Switch to dark mode
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
            dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(0, 0, 0))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            app.setPalette(dark_palette)
            # Set menubar and menu drop downs to dark mode
            self.setStyleSheet("""
                QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                    background: #000000;
                    color: #fff;
                }
                QMenuBar::item:selected, QMenu::item:selected {
                    background: #2a82da;
                }
            """)

    def toggle_grid(self):
        # Toggle grid visibility in the scene if it supports it
        main_window = self.parent()
        if hasattr(main_window, "view") and hasattr(main_window.view, "toggle_grid"):
            main_window.view.toggle_grid()
        else:
            QMessageBox.information(self, "Toggle Grid", "Grid toggling is not implemented in the view.")

    def new_file(self):
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.clear()
        else:
            QMessageBox.information(self, "New", "Scene clearing is not implemented.")

    def open_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Open", "Scene loading is not implemented.")
            return
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    items_data = json.load(f)
                main_window.scene.clear()
                for item_data in items_data:
                    item = self.deserialize_item(item_data)
                    if item:
                        main_window.scene.addItem(item)
            except Exception as e:
                QMessageBox.warning(self, "Open", f"Failed to open file:\n{e}")

    def save_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Save", "Scene saving is not implemented.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                items_data = [self.serialize_item(item) for item in main_window.scene.items()]
                # Remove None items (if any)
                items_data = [item for item in items_data if item is not None]
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(items_data, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Save", f"Failed to save file:\n{e}")

    def serialize_item(self, item):
        # Rectangle
        if isinstance(item, Rectangle):
            rect = item.rect()
            color = item.brush().color()
            pos = item.pos()
            return {
                "type": "rect",
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "color": color.name(QColor.NameFormat.HexArgb),
                "pos_x": pos.x(),
                "pos_y": pos.y()
            }
        return None

    def deserialize_item(self, data):
        if not data:
            return None
        pos_x = data.get("pos_x", 0)
        pos_y = data.get("pos_y", 0)
        if data.get("type") == "rect":
            x, y, w, h = data["x"], data["y"], data["w"], data["h"]
            color = QColor(data["color"])
            item = Rectangle(x, y, w, h)
            item.setBrush(QBrush(color))
            item.setPos(pos_x, pos_y)
            return item
        return None
    
    def print_diagram(self):
        main_window = self.parent()
        if not hasattr(main_window, "view"):
            QMessageBox.information(self, "Print", "Nothing to print.")
            return

        view = getattr(main_window, "view", None)
        scene = getattr(main_window, "scene", None)

        # Hide grid before printing if it exists
        if hasattr(view, "grid_visible"):
            old_grid_visible = view.grid_visible
            view.grid_visible = False
        else:
            old_grid_visible = None

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec():
            painter = QPainter(printer)
            main_window.view.render(painter)
            painter.end()

        # Restore grid visibility
        if old_grid_visible is not None:
            view.grid_visible = old_grid_visible