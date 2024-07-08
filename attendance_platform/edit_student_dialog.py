from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox


class EditStudentDialog(QDialog):
    def __init__(self, parent=None, student_details=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student Details")

        self.layout = QFormLayout(self)

        self.student_number_input = QLineEdit(self)
        self.student_number_input.setText(student_details['Student Number'])
        self.layout.addRow("Student Number", self.student_number_input)

        self.name_input = QLineEdit(self)
        self.name_input.setText(student_details['Name'])
        self.layout.addRow("Name", self.name_input)

        self.programme_input = QLineEdit(self)
        self.programme_input.setText(student_details['Programme'])
        self.layout.addRow("Programme", self.programme_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                        self)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_updated_details(self):
        return {
            'Student Number': self.student_number_input.text(),
            'Name': self.name_input.text(),
            'Programme': self.programme_input.text()
        }
