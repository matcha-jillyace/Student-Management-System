from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, 
                           QPushButton, QVBoxLayout, QHBoxLayout, 
                           QMessageBox, QInputDialog, QLineEdit, QLabel)
from PyQt5.QtCore import Qt
from sms_backend import add_user, get_users, delete_user

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_users()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("User Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add User")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.add_btn.clicked.connect(self.show_add_user_dialog)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_users)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addStretch()
        
        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Actions"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add to main layout
        layout.addWidget(title)
        layout.addLayout(btn_layout)
        layout.addWidget(self.user_table)
        
        self.setLayout(layout)
    
    def load_users(self):
        users = get_users()
        self.user_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            user_id, username, role = user
            
            # Add user data to table
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.user_table.setItem(row, 1, QTableWidgetItem(username))
            self.user_table.setItem(row, 2, QTableWidgetItem(role))
            
            # Add delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_btn.clicked.connect(lambda _, uid=user_id: self.delete_user(uid))
            self.user_table.setCellWidget(row, 3, delete_btn)
        
        self.user_table.resizeColumnsToContents()
    
    def show_add_user_dialog(self):
        username, ok = QInputDialog.getText(self, "Add User", "Username:")
        if not ok or not username:
            return
        
        password, ok = QInputDialog.getText(self, "Add User", "Password:", QLineEdit.Password)
        if not ok or not password:
            return
        
        role, ok = QInputDialog.getItem(self, "Add User", "Role:", ["admin", "user"], 1, False)
        if not ok:
            return
        
        if add_user(username, password, role):
            QMessageBox.information(self, "Success", "User added successfully")
            self.load_users()
        else:
            QMessageBox.warning(self, "Error", "Username already exists")
    
    def delete_user(self, user_id):
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if delete_user(user_id):
                QMessageBox.information(self, "Success", "User deleted successfully")
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete user")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = AdminPanel()
    window.show()
    app.exec_()