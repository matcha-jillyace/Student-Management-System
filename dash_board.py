from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from admin_panel import AdminPanel
from student_panel import StudentPanel
from PyQt5.QtCore import Qt

class DashBoard(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle(f"Student Management System - {role.capitalize()} Panel")
        self.setMinimumSize(1200, 900)
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setup_ui()
        
    def setup_ui(self):
        self.tabs = QTabWidget()
        
        self.student_panel = StudentPanel(self.role)
        self.tabs.addTab(self.student_panel, "Student Management")
        
        if self.role == 'admin':
            self.admin_panel = AdminPanel()
            self.tabs.addTab(self.admin_panel, "User Management")
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.tabs)
        
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(container)
        
        self.setCentralWidget(central_widget)
        
        self.statusBar().showMessage(f"Logged in as {self.role}")
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #e0e0e0;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #fff;
                margin-bottom: -1px;
            }
        """)
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = DashBoard("admin")
    window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    window.showMaximized()
    app.exec_()