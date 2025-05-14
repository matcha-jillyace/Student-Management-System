import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import ( QApplication, QWidget, QVBoxLayout, QTableWidget, 
                              QDialog, QTableWidgetItem, QPushButton, QHBoxLayout )

class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Table")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(8)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Name', 'Age', 'Student ID', 'Course', 'Year', 'Birthday', 'Email'])

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Row")
        remove_button = QPushButton("Remove Selected Row")
        add_button.clicked.connect(self.add_row)
        remove_button.clicked.connect(self.remove_selected_row)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def remove_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
    

