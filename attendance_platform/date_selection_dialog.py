from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QDialogButtonBox


class DateSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")

        self.layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        self.layout.addWidget(self.calendar)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                        self)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_selected_date(self):
        return self.calendar.selectedDate().toString("yyyy-MM-dd")
