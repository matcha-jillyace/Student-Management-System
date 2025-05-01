from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from backend import authenticate

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System - Login")
        self.setWindowIcon(QIcon("icon.jpg"))
        self.resize(550, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Student Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: #375534; padding: 5px")
        
        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.label_username = QLabel("Username:")
        self.label_password = QLabel("Password:")
        self.label_username.setStyleSheet("QLabel { font-size: 15px; font-weight: bold; color: #26425a; }")
        self.label_password.setStyleSheet("QLabel { font-size: 15px; font-weight: bold; color: #26425a; }")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.username.setStyleSheet("QLineEdit { font-size: 17px; padding: 15px; }")
    
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("font-size: 17px; padding: 15px;")
        
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #728156;
                color: white;
                border: None;
                padding: 19px;
                font-size: 18px;
                border-radius: 8px;
                margin-top: 30px;
            }
            QPushButton:hover {
                background-color: #3c5148;
            }
        """)
        login_btn.clicked.connect(self.authenticate)
        
        # Add widgets to layout
        form_layout.addWidget(self.label_username)
        form_layout.addWidget(self.username)
        form_layout.addWidget(self.label_password)
        form_layout.addWidget(self.password)
        form_layout.addWidget(login_btn)
        
        # Main layout
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.setContentsMargins(20,20,20,20)
        
        self.setLayout(layout)
    
    def authenticate(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
"""        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        role = authenticate(username, password)
        if role:
            self.hide()
            from main_window import MainWindow
            self.main = MainWindow(role)
            self.main.show()
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials")"""

if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.setStyleSheet("QWidget { background-color: #b6c99b}")
    window.show()
    app.exec_()
