from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from backend import authenticate

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System - Login")
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setStyleSheet("background-color: #CCEEC0;")
        self.setup_ui()
    
    def setup_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        login_panel = QWidget()
        login_panel.setFixedSize(750, 600)
        login_panel.setStyleSheet("""
            QWidget { 
                background-color: #ffffff; 
                border: 1px solid #ffffff; 
                border-radius: 10px;
            }
        """)
        
        panel_layout = QVBoxLayout(login_panel)
        panel_layout.setSpacing(20)
        panel_layout.setContentsMargins(100, 40, 100, 50)
        
        title = QLabel("Student Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: #375534;")
        panel_layout.addWidget(title)

        from PyQt5.QtWidgets import QFormLayout, QHBoxLayout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        self.label_username = QLabel("Username:")
        self.label_password = QLabel("Password:")
        self.label_username.setStyleSheet("font-size: 15px; font-weight: bold; color: #26425a;")
        self.label_password.setStyleSheet("font-size: 15px; font-weight: bold; color: #26425a;")
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("font-size: 17px; padding: 10px; background-color: #E4F6DA;")
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("font-size: 17px; padding: 10px; background-color: #E4F6DA;")

        form_layout.addRow(self.label_username, self.username)
        form_layout.addRow(self.label_password, self.password)
        panel_layout.addLayout(form_layout)
        
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #728156;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #3c5148;
            }
        """)
        login_btn.clicked.connect(self.authenticate)
        
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(login_btn)
        panel_layout.addLayout(btn_layout)
        
        outer_layout.addWidget(login_panel)
    
    def authenticate(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        role = authenticate(username, password)
        if role:
            self.hide()
            from dash_board import DashBoard
            self.main = DashBoard(role)
            self.main.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            self.main.showMaximized()
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials")

if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    window.showMaximized() 
    app.exec_()