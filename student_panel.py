from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, 
                           QLineEdit, QDateEdit, QComboBox, QHeaderView,
                           QLabel, QGroupBox, QFrame)
from PyQt5.QtCore import Qt, QDate
from backend import (add_student, get_students, search_students, 
                    update_student, delete_student)

class StudentPanel(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setup_ui()
        self.load_students()
        self.setWindowTitle("Student Management System")
        self.resize(1200, 900)
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Title
        title = QLabel("Student Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #375534;
                padding: 10px;
            }
        """)

        # Center container
        center_container = QWidget()
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        center_container.setLayout(center_layout)

        # Form group
        form_group = QGroupBox("Student Information")
        form_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #375534;
                border: 2px solid #a8c7a5;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 20px;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter)
        form_layout.setVerticalSpacing(12)
        form_layout.setContentsMargins(35, 35, 35, 20)

        # Fields
        self.std_id = QLineEdit()
        self.fullname = QLineEdit()
        self.course = QLineEdit()
        self.section = QLineEdit()
        self.dob = QDateEdit(calendarPopup=True)
        self.dob.setDate(QDate.currentDate())
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female"])
        self.mobile = QLineEdit()

        inputs = [self.std_id, self.fullname, self.course, self.section, self.mobile]
        for field in inputs:
            field.setMinimumWidth(250)
            field.setStyleSheet("""
                QLineEdit {
                    font-size: 14px;
                    padding: 10px;
                    border: 1px solid #a8c7a5;
                    border-radius: 4px;
                }
            """)

        self.dob.setMinimumWidth(250)
        self.dob.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 1px solid #a8c7a5;
                border-radius: 4px;
            }
        """)

        self.gender.setMinimumWidth(250)
        self.gender.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #a8c7a5;
                border-radius: 4px;
            }
        """)

        # Add fields vertically
        form_layout.addRow("Student ID:", self.std_id)
        form_layout.addRow("Full Name:", self.fullname)
        form_layout.addRow("Course:", self.course)
        form_layout.addRow("Section:", self.section)
        form_layout.addRow("Date of Birth:", self.dob)
        form_layout.addRow("Gender:", self.gender)
        form_layout.addRow("Mobile:", self.mobile)

        # Buttons layout inside form group
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(20)

        self.add_btn = QPushButton("Add Student")
        self.clear_btn = QPushButton("Clear")
        for btn in [self.add_btn, self.clear_btn]:
            btn.setFixedWidth(150)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #728156;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3c5148;
                }
                QPushButton:pressed {
                    background-color: #2a3a32;
                }
            """)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #728156;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3c5148;
            }
        """)

        self.add_btn.clicked.connect(self.add_student)
        self.clear_btn.clicked.connect(self.clear_form)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)

        # Finalize form group
        form_group_layout = QVBoxLayout()
        form_group_layout.addLayout(form_layout)
        form_group_layout.addLayout(btn_layout)
        form_group.setLayout(form_group_layout)
        form_group.setFixedWidth(1000)


        # Search part
        search_group = QGroupBox("Search Students")
        search_group.setStyleSheet(form_group.styleSheet())
        search_group.setFixedWidth(1000)

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(15, 15, 15, 15)

        self.search_field = QComboBox()
        self.search_field.addItems(["Student ID", "Full Name", "Course", "Section", "Mobile"])
        self.search_field.setFixedWidth(150)
        self.search_field.setStyleSheet(self.gender.styleSheet())

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet(self.std_id.styleSheet())

        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(100)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #5a724a;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3c5148;
            }
        """)
        self.search_btn.clicked.connect(self.search_students)

        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_group.setLayout(search_layout)

        # Assemble the center container 
        center_layout.addWidget(form_group)
        center_layout.addWidget(search_group)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #a8c7a5;")

        # Student Table 
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(9)
        self.student_table.setHorizontalHeaderLabels(
            ["ID", "Student ID", "Full Name", "Course", "Section", "DOB", "Gender", "Mobile", "Actions"]
        )
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.verticalHeader().setVisible(False)
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setSelectionMode(QTableWidget.SingleSelection)
        self.student_table.cellClicked.connect(self.populate_form_from_table)
        self.student_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #a8c7a5;
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

        # Final main layout assembly
        main_layout.addWidget(title, 0)
        main_layout.addWidget(center_container, 0)
        main_layout.addWidget(separator, 0)
        main_layout.addWidget(self.student_table, 1)
        self.setLayout(main_layout)

        if self.role != 'admin':
            self.disable_form()
    
    def disable_form(self):
        """Disable form fields for regular users"""
        self.std_id.setReadOnly(True)
        self.fullname.setReadOnly(True)
        self.course.setEnabled(False)
        self.section.setReadOnly(True)
        self.dob.setReadOnly(True)
        self.gender.setEnabled(False)
        self.mobile.setReadOnly(True)
        self.add_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def load_students(self):
        students = get_students()
        self.student_table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            for col, value in enumerate(student):
                self.student_table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(5)
            
            if self.role == 'admin':
                edit_btn = QPushButton("Edit")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        padding: 5px 10px;
                        border-radius: 3px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                edit_btn.clicked.connect(lambda _, sid=student[0]: self.update_student(sid))
                btn_layout.addWidget(edit_btn)
                
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
                delete_btn.clicked.connect(lambda _, sid=student[0]: self.delete_student(sid))
                btn_layout.addWidget(delete_btn)
            
            btn_widget.setLayout(btn_layout)
            self.student_table.setCellWidget(row, 8, btn_widget)
    
    def populate_form_from_table(self, row, col):
        """Populate form with data from selected row"""
        if self.role != 'admin':
            return
        
        student_id = self.student_table.item(row, 0).text()
        std_id = self.student_table.item(row, 1).text()
        fullname = self.student_table.item(row, 2).text()
        course = self.student_table.item(row, 3).text()
        section = self.student_table.item(row, 4).text()
        dob = self.student_table.item(row, 5).text()
        gender = self.student_table.item(row, 6).text()
        mobile = self.student_table.item(row, 7).text()
        
        #form fields
        self.std_id.setText(std_id)
        self.fullname.setText(fullname)
        self.course.setText(course)
        self.section.setText(section)
        self.dob.setDate(QDate.fromString(dob, "yyyy-MM-dd"))
        self.gender.setCurrentText(gender)
        self.mobile.setText(mobile)
        
        # button text
        self.add_btn.setText("Update")
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(lambda: self.update_student(student_id))
    
    def clear_form(self):
        """Clear all form fields"""
        self.std_id.clear()
        self.fullname.clear()
        self.course.clear()
        self.section.clear()
        self.dob.setDate(QDate.currentDate())
        self.gender.setCurrentIndex(0)
        self.mobile.clear()
        
        # Reset button
        self.add_btn.setText("Add Student")
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.add_student)
    
    def add_student(self):
        """Add a new student"""
        data = {
            'std_id': self.std_id.text().strip(),
            'fullname': self.fullname.text().strip(),
            'course': self.course.text().strip(),
            'section': self.section.text().strip(),
            'dob': self.dob.date().toString("yyyy-MM-dd"),
            'gender': self.gender.currentText(),
            'mobile': self.mobile.text().strip()
        }
        
        # Validate required fields
        if not all([data['std_id'], data['fullname'], data['course']]):
            QMessageBox.warning(self, "Error", "Student ID, Full Name, and Course are required")
            return
        
        if add_student(**data):
            QMessageBox.information(self, "Success", "Student added successfully")
            self.clear_form()
            self.load_students()
        else:
            QMessageBox.warning(self, "Error", "Student ID already exists")
        
    def update_student(self, student_id):
        """Update existing student"""
        data = {
            'std_id': self.std_id.text().strip(),
            'fullname': self.fullname.text().strip(),
            'course': self.course.text().strip(),
            'section': self.section.text().strip(),
            'dob': self.dob.date().toString("yyyy-MM-dd"),
            'gender': self.gender.currentText(),
            'mobile': self.mobile.text().strip()
        }
        
        if update_student(int(student_id), **data):
            QMessageBox.information(self, "Success", "Student updated successfully")
            self.clear_form()
            self.load_students()
        else:
            QMessageBox.warning(self, "Error", "Failed to update student")
    
    def delete_student(self, student_id):
        """Delete a student"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            "Are you sure you want to delete this student?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if delete_student(student_id):
                QMessageBox.information(self, "Success", "Student deleted successfully")
                self.load_students()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete student")
    
    def search_students(self):
        """Search students based on criteria"""
        search_by = self.search_field.currentText().lower().replace(" ", "")
        search_term = self.search_input.text().strip()
        
        if not search_term:
            self.load_students()
            return
        
        # Map UI field names to database column names
        field_map = {
            "studentid": "std_id",
            "fullname": "fullname",
            "course": "course",
            "section": "section",
            "mobile": "mobile"
        }
        
        db_field = field_map.get(search_by, "std_id")
        results = search_students(**{db_field: search_term})
        self.student_table.setRowCount(len(results))
        
        for row, student in enumerate(results):
            for col, value in enumerate(student):
                self.student_table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(5)
            
            if self.role == 'admin':
                edit_btn = QPushButton("Edit")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        padding: 5px 10px;
                        border-radius: 3px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                edit_btn.clicked.connect(lambda _, sid=student[0]: self.update_student(sid))
                btn_layout.addWidget(edit_btn)
                
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
                delete_btn.clicked.connect(lambda _, sid=student[0]: self.delete_student(sid))
                btn_layout.addWidget(delete_btn)
            
            btn_widget.setLayout(btn_layout)
            self.student_table.setCellWidget(row, 8, btn_widget)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = StudentPanel("admin")
    window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    window.showMaximized()
    app.exec_()
