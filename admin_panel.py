from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, 
                           QPushButton, QVBoxLayout, QHBoxLayout, 
                           QMessageBox, QInputDialog, QLineEdit, QLabel, 
                           QGroupBox, QFrame, QHeaderView)
from PyQt5.QtCore import Qt
from backend import add_user, get_users, delete_user

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.resize(1200, 900)
        self.load_users()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("User Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #375534;
                padding: 10px;
            }
        """)
        
        form_group = QGroupBox("Add New User")
        form_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #375534;
                border: 1px solid #a8c7a5;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(50)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.add_btn = QPushButton("Add User")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #728156;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #3c5148;
            }
            QPushButton:pressed {
                background-color: #2a3a32;
            }
        """)
        self.add_btn.clicked.connect(self.show_add_user_dialog)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #5a724a;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #3c5148;
            }
            QPushButton:pressed {
                background-color: #2a3a32;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_users)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.refresh_btn)
        
        form_layout.addLayout(btn_layout)
        form_group.setLayout(form_layout)
        form_group.setFixedWidth(600)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #a8c7a5;")

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setMaximumSize(1500, 800)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Actions"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #a8c7a5;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #728156;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        
        main_layout.addWidget(title)
        form_hbox = QHBoxLayout()
        form_hbox.addStretch()
        form_hbox.addWidget(form_group)
        form_hbox.addStretch()
        main_layout.addLayout(form_hbox)
        
        main_layout.addWidget(separator)
        
        table_container = QWidget()
        table_layout = QHBoxLayout(table_container)
        table_layout.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(self.user_table)
        main_layout.addWidget(table_container)  
        self.setLayout(main_layout)

    def load_users(self):
        users = get_users()
        self.user_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            user_id, username, role = user
            
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.user_table.setItem(row, 1, QTableWidgetItem(username))
            self.user_table.setItem(row, 2, QTableWidgetItem(role))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_btn.clicked.connect(lambda _, uid=user_id: self.delete_user(uid))
            self.user_table.setCellWidget(row, 3, delete_btn)
        
    
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
    window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    window.showMaximized()
    app.exec_()
