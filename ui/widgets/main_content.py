from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QStackedWidget

from ui.widgets.expense_widget import ExpenseWidget
from ui.widgets.category_widget import CategoryWidget

class MainContent(QWidget):
  def __init__(self, category_widget: CategoryWidget, expense_widget: ExpenseWidget):
    super().__init__()
    self.category_widget = category_widget
    self.expense_widget = expense_widget
    self.init_ui()

  def init_ui(self):
    view_category_button = QPushButton("View Category", self)
    view_expense_button = QPushButton("View Expense", self)

    view_category_button.clicked.connect(self.show_category)
    view_expense_button.clicked.connect(self.show_expense)
    
    # Widgets
    self.stacked_widget = QStackedWidget()
    self.stacked_widget.addWidget(self.category_widget)
    self.stacked_widget.addWidget(self.expense_widget)
    
    # Layouts
    main_layout = QVBoxLayout(self)
    buttons_layout = QHBoxLayout()
    buttons_layout.addWidget(view_category_button)
    buttons_layout.addWidget(view_expense_button)
    main_layout.addLayout(buttons_layout)
    main_layout.addWidget(self.stacked_widget)

  def show_category(self):
    self.stacked_widget.setCurrentWidget(self.category_widget)

  def show_expense(self):
    self.expense_widget.update_expense_list()
    self.expense_widget.update_category_list(self.category_widget.manager.get_categories_names_list())
    self.stacked_widget.setCurrentWidget(self.expense_widget)