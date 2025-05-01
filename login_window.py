from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox, QApplication)
from PyQt5.QtCore import Qt
#from backend import authenticate

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System - Login")
        self.resize(400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Student Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #98a77c;")
        
        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.label_username = QLabel("Username:")
        self.label_password = QLabel("Password:")
        self.label_username.setStyleSheet("QLabel { font-weight: bold; color: #26425a; }")
        self.label_password.setStyleSheet("QLabel { font-weight: bold; color: #26425a; }")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.username.setStyleSheet("QLineEdit { padding: 8px; }")
    
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("padding: 8px;")
        
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #728156;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 4px;
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
        
        self.setLayout(layout)
    
    def authenticate(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
"""        role = authenticate(username, password)]
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