from PySide6.QtCore import QDate
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QDateEdit, QComboBox

class InputBox(QWidget):
  def __init__(self, label_text, input_type, select_list = []):
    super().__init__()
    self.select_list = select_list
    self.input_type = input_type
    self.apply_styles()
    self.init_ui(label_text)

  def init_ui(self, label_text):
    layout = QHBoxLayout()

    self.label = QLabel(label_text)

    if self.input_type == "string":
      self.input_widget = QLineEdit()
    elif self.input_type == "date":
      self.input_widget = QDateEdit()
      self.input_widget.setDate(QDate.currentDate())  # Set the initial date to the current date
      self.input_widget.setCalendarPopup(True)
    elif self.input_type == "numeric":
      self.input_widget = QLineEdit()
      self.input_widget.setValidator(QIntValidator())
    elif self.input_type == "dropdown":
      self.input_widget = QComboBox()
      self.input_widget.addItems(self.select_list)
    else:
      raise ValueError("Unsupported input type")

    layout.addWidget(self.label)
    layout.addWidget(self.input_widget)

    self.setLayout(layout)

  def apply_styles(self):
    self.setStyleSheet("""
        font-size: 14px;
        padding: 5px;
    """)

  def get_input(self):
    if self.input_type == "string":
      return self.input_widget.text()
    elif self.input_type == "date":
      return self.input_widget.date().toString("yyyy-MM-dd")
    elif self.input_type == "numeric":
      return float(self.input_widget.text())
    elif self.input_type == "dropdown":
      self.input_widget.currentText()
    else:
      raise ValueError("Unsupported input type")
    
  def clear(self):
    if self.input_type == "date":
      self.input_widget.setDate(QDate.currentDate())
      self.input_widget.setCalendarPopup(True)
    else:
      self.input_widget.clear()