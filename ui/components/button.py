from PySide6.QtWidgets import QPushButton

from ui.widgets.category_widget import CategoryWidget
from ui.widgets.expense_widget import ExpenseWidget

class Button(QPushButton):
    def __init__(self, text: str, target_widget: CategoryWidget | ExpenseWidget):
      super().__init__(text)
      self.apply_styles()
      self.target_widget = target_widget
      self.clicked.connect(self.on_button_clicked)

    def apply_styles(self):
      self.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                min-height: 30px;
            }

            QPushButton:hover {
                background-color: rgba(76, 175, 80, 0.8);  /* Green color with reduced opacity on hover */
            }
            
            QPushButton#updateButton {
                background-color: #007BFF;  /* Blue color for delete button */
            }               

            QPushButton#updateButton:hover {
                background-color: rgba(0, 123, 255, 0.7);  /* Lighter red with reduced opacity on hover */
            }
                           
            QPushButton#deleteButton {
                background-color: #FF3333;  /* Red color for delete button */
            }               

            QPushButton#deleteButton:hover {
                background-color: rgba(255, 99, 71, 0.7);  /* Lighter red with reduced opacity on hover */
            }
""")

    def on_button_clicked(self):
      if self.text() == "Add":
        self.target_widget.add()
      elif self.text() == "Update":
        self.target_widget.update()
      if self.text() == "Delete":
        self.target_widget.delete()