#Sean Moore
#Student Number: 3082600



import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QPushButton,
    QAbstractItemView,
    QHBoxLayout,
    QFileDialog,
    QInputDialog,
    QWidget,
    QDockWidget,
    QLabel, QDialog, QCalendarWidget, QDialogButtonBox, QFormLayout,
)
from PyQt6.QtCore import Qt, QFile, QDate, pyqtSlot
import sys
import csv
import datetime as dt
import pandas as pd
from datetime import date


class AttendancePlatform(QMainWindow):
    def __init__(self):
        super().__init__()

        self.student_data = []  # List to hold student data
        self.load_student_data_from_csv()  # Load student data from CSV
        self.init_ui()  # Initialize the UI

    def init_ui(self):
        # Create the main window layout
        self.setWindowTitle("Sean Moore - 3082600 - Repeat July 2023")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Table setup
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Buttons
        self.set_date_button = QPushButton("Set Date")
        self.mark_all_present_button = QPushButton("Mark All Present")
        self.mark_all_absent_button = QPushButton("Mark All Absent")
        self.reset_button = QPushButton("Reset Attendance")
        self.export_button = QPushButton("Export Attendance")

        self.layout.addWidget(self.set_date_button)
        self.layout.addWidget(self.mark_all_present_button)
        self.layout.addWidget(self.mark_all_absent_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.export_button)

        self.setCentralWidget(self.central_widget)

        # Dock widget setup
        self.dock = QDockWidget("Student Details", self)
        self.dock_widget = QWidget()
        self.dock_layout = QVBoxLayout(self.dock_widget)
        self.dock.setWidget(self.dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # Add labels and buttons to the dock layout
        self.student_image_label = QLabel()
        self.dock_layout.addWidget(self.student_image_label)

        self.student_details_label = QLabel("Student Details")
        self.dock_layout.addWidget(self.student_details_label)

        self.edit_button = QPushButton("Edit")
        self.dock_layout.addWidget(self.edit_button)

        self.populate_table()  # Populate the table with student data

        # Connect buttons to their respective functions
        self.set_date_button.clicked.connect(self.set_date)
        self.mark_all_present_button.clicked.connect(self.mark_all_present)
        self.mark_all_absent_button.clicked.connect(self.mark_all_absent)
        self.reset_button.clicked.connect(self.reset_attendance)
        self.export_button.clicked.connect(self.export_attendance)
        self.edit_button.clicked.connect(self.edit_student_details)

    def load_student_data_from_csv(self):
        csv_path = r"C:\Users\seanm\PycharmProjects\HCI-RepeatAssignment\students.csv"  # Use absolute path
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            self.student_data = list(reader)

    def populate_table(self):
        # Set up the table with the correct number of rows and columns
        self.table.setRowCount(len(self.student_data) - 1)  # Exclude header
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Student Number", "Name", "Programme", "Attendance", "Check"])

        for index, row in enumerate(self.student_data[1:]):  # Skip header
            self.table.setItem(index, 0, QTableWidgetItem(row[0]))
            self.table.setItem(index, 1, QTableWidgetItem(row[1]))
            self.table.setItem(index, 2, QTableWidgetItem(row[2]))
            attendance_item = QTableWidgetItem("Absent")
            self.table.setItem(index, 3, attendance_item)

            # Add toggle button for attendance
            toggle_button = QPushButton("Mark Present")
            toggle_button.clicked.connect(self.create_toggle_attendance_callback(index, attendance_item, toggle_button))
            self.table.setCellWidget(index, 4, toggle_button)

        # Connect table cell click to display_student_details
        self.table.cellClicked.connect(self.display_student_details)

    def create_toggle_attendance_callback(self, row, attendance_item, toggle_button):
        def toggle_attendance():
            if attendance_item.text() == "Absent":
                attendance_item.setText("Present")
                toggle_button.setText("Mark Absent")
            else:
                attendance_item.setText("Absent")
                toggle_button.setText("Mark Present")
        return toggle_attendance

    def set_date(self):
        # Dialog to select date
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        layout = QVBoxLayout(dialog)
        calendar = QCalendarWidget(dialog)
        layout.addWidget(calendar)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, dialog)
        layout.addWidget(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec():
            selected_date = calendar.selectedDate().toString("yyyy-MM-dd")
            self.set_date_button.setText(selected_date)

    def mark_all_present(self):
        # Mark all students as present
        for row in range(self.table.rowCount()):
            attendance_item = self.table.item(row, 3)
            attendance_item.setText("Present")
            toggle_button = self.table.cellWidget(row, 4)
            toggle_button.setText("Mark Absent")

    def mark_all_absent(self):
        # Mark all students as absent
        for row in range(self.table.rowCount()):
            attendance_item = self.table.item(row, 3)
            attendance_item.setText("Absent")
            toggle_button = self.table.cellWidget(row, 4)
            toggle_button.setText("Mark Present")

    def reset_attendance(self):
        # Reset attendance for all students
        for row in range(self.table.rowCount()):
            attendance_item = self.table.item(row, 3)
            attendance_item.setText("Absent")
            toggle_button = self.table.cellWidget(row, 4)
            toggle_button.setText("Mark Present")

    def export_attendance(self):
        # Export attendance to a text file
        today = date.today().strftime("%Y-%m-%d")
        filename = QFileDialog.getSaveFileName(self, "Save File", f"{today}_attendance.txt", "Text Files (*.txt)")

        if filename[0]:
            with open(filename[0], "w") as file:
                for row in range(self.table.rowCount()):
                    student_number = self.table.item(row, 0).text()
                    name = self.table.item(row, 1).text()
                    programme = self.table.item(row, 2).text()
                    attendance = self.table.item(row, 3).text()
                    file.write(f"{student_number}, {name}, {programme}, {attendance}\n")

    def display_student_details(self, row, column):
        # Display student details and image when a table cell is clicked
        student_number = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        programme = self.table.item(row, 2).text()
        image_path = self.student_data[row + 1][3]  # Adjusted to account for header

        self.student_details_label.setText(f"Student Number: {student_number}\nName: {name}\nProgramme: {programme}")

        # Construct the correct path to the image
        image_full_path = os.path.join(os.path.dirname(__file__), image_path)

        # Debugging: Print the image path
        print(f"Loading image from: {image_full_path}")

        if os.path.exists(image_full_path):
            pixmap = QPixmap(image_full_path)
            if not pixmap.isNull():
                self.student_image_label.setPixmap(pixmap)
                self.student_image_label.setScaledContents(True)
                self.student_image_label.setFixedSize(200, 200)
            else:
                print(f"Failed to load image from: {image_full_path}")
                self.student_image_label.clear()
        else:
            print(f"Image file does not exist: {image_full_path}")
            self.student_image_label.clear()

    def edit_student_details(self):
        # Edit student details in a dialog
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Student Details")
            layout = QFormLayout(dialog)

            student_number_input = QLineEdit(dialog)
            student_number_input.setText(self.table.item(selected_row, 0).text())
            layout.addRow("Student Number", student_number_input)

            name_input = QLineEdit(dialog)
            name_input.setText(self.table.item(selected_row, 1).text())
            layout.addRow("Name", name_input)

            programme_input = QLineEdit(dialog)
            programme_input.setText(self.table.item(selected_row, 2).text())
            layout.addRow("Programme", programme_input)

            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, dialog)
            layout.addWidget(buttons)

            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            if dialog.exec():
                self.table.setItem(selected_row, 0, QTableWidgetItem(student_number_input.text()))
                self.table.setItem(selected_row, 1, QTableWidgetItem(name_input.text()))
                self.table.setItem(selected_row, 2, QTableWidgetItem(programme_input.text()))
                self.student_data[selected_row + 1] = [student_number_input.text(), name_input.text(),
                                                       programme_input.text(), self.student_data[selected_row + 1][3]]
                csv_path = r"C:\Users\seanm\PycharmProjects\HCI-RepeatAssignment\students.csv"  # Use the provided absolute path
                with open(csv_path, "w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.student_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendancePlatform()
    window.show()
    sys.exit(app.exec())
