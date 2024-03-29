from PySide6.QtWidgets import QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, QMessageBox, QComboBox, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, QLabel
import operator

from models.expense import Expense
from managers.expense_manager import ExpenseManager

from ui.widgets.chart_widget import ChartWidget
from ui.components.input_box import InputBox

from utils.input_status import INPUT_STATUS

class ExpenseWidget(QWidget):
    def __init__(self, expense_manager: ExpenseManager):
        super().__init__()
        self.manager = expense_manager
        
        self.create_chart_widget()

        # Input boxes
        self.description_input = InputBox("Expense Description:", "string")
        self.amount_input = InputBox("Expense Amount:", "numeric")
        self.date_input = InputBox("Select Date:", "date")
        self.category_select = QComboBox()
        self.category_select.addItems(self.manager.categories)

        # Buttons
        from ui.components.button import Button

        self.add_button = Button("Add", self)

        self.update_button = Button("Update", self)
        self.update_button.setObjectName("updateButton")

        self.delete_button = Button("Delete", self)
        self.delete_button.setObjectName("deleteButton")
        
        main_layout = QGridLayout(self)

        insert_layout = QVBoxLayout()
        insert_layout.addWidget(self.description_input)
        insert_layout.addWidget(self.amount_input)
        insert_layout.addWidget(self.date_input)
        insert_layout.addWidget(self.category_select)
        insert_layout.addWidget(self.add_button)

        table_layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(Expense.get_columns())
        self.update_expense_list()
        table_layout.addWidget(self.table)
        
        filter_buttons = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.on_search_input_changed)
        self.search_input.setStyleSheet("font-size: 14px;padding: 6px;")

        filter_buttons.addWidget(self.search_input)

        sort_options = QVBoxLayout()

        # Sort by
        sort_by_layout = QHBoxLayout()
        sort_by_label = QLabel("Sort by:")
        sort_by_label.setStyleSheet("font-size: 14px;")
        self.sort_by_combobox = QComboBox(self)
        self.sort_by_combobox.addItems(["id", "description", "amount", "date", "category"])

        sort_by_layout.addWidget(sort_by_label)
        sort_by_layout.addWidget(self.sort_by_combobox)

        # Order by
        order_by_layout = QHBoxLayout()
        order_by_label = QLabel("Order by:")
        order_by_label.setStyleSheet("font-size: 14px;")
        self.order_by_combobox = QComboBox(self)
        self.order_by_combobox.addItems(["ascending", "descending"])

        order_by_layout.addWidget(order_by_label)
        order_by_layout.addWidget(self.order_by_combobox)

        apply_button = QPushButton("Apply")
        apply_button.setStyleSheet("""
                                   QPushButton {
                                   font-size: 14px;
                                   background-color: #000;
                                   color: #fff;
                                   border-radius: 4px;
                                   min-height: 30px;
                                }
                                
                                   QPushButton:hover {
                                   background-color: #333;  /* Change color on hover */
                                   color: #fff;
                                   border: 1px solid #fff;  /* Add border on hover */
                                }
                                """)
        apply_button.clicked.connect(self.sort_by)

        sort_options.addWidget(self.delete_button)
        sort_options.addLayout(sort_by_layout)
        sort_options.addLayout(order_by_layout)
        sort_options.addWidget(apply_button)

        main_layout.addLayout(filter_buttons, 0, 0, 1, 6)
        main_layout.addWidget(self.table, 1, 0, 3, 5)
        main_layout.addLayout(sort_options, 1, 5, 3, 1)
        main_layout.addLayout(insert_layout, 4, 0, 2, 3)
        main_layout.addWidget(self.chart_widget, 4, 3, 2, 3)
        self.apply_styles()

    def update_category_list(self, new_cats):
        self.category_select.clear()
        self.category_select.addItems(new_cats)

    def create_chart_widget(self):
        self.chart_widget = ChartWidget(self.manager)

    def sort_by(self):
        self.update_expense_list(self.sort_by_combobox.currentText(), self.order_by_combobox.currentText())

    def on_search_input_changed(self):
        self.update_expense_list("search")

    def apply_styles(self):
        self.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 5px;
            }
            QTableWidget {
                border: 1px solid #ddd;  /* Add border */
                selection-background-color: #3498db;  /* Highlight color on selection */
                alternate-background-color: #f9f9f9;  /* Alternate row background color */
                font-size: 14px;
            }
            
            QTableWidget::section {
                font-size: 14px;  /* Add padding to table items */
            }
        """)

    def add(self):
        # Get values from UI elements
        try:
            description = self.description_input.get_input()
            amount = self.amount_input.get_input()
            date = self.date_input.get_input()
            category = self.category_select.currentText()
            if len(description) != 0 and amount > 0 and len(category) > 0:
                self.manager.add_expense(description, amount, date, category)
                self.clear_inputs()
                self.update_expense_list()
            else:
                raise "Input Error before adding"
        except Exception as e:
            QMessageBox.warning(self, "Invalid Input", INPUT_STATUS.get('EXPENSE_INSERT_ERROR')[0])

    def delete(self):
        # Get the selected row from the table
        selected_row = self.table.currentRow()
        if selected_row != -1:
            # Delete the expense from the manager
            self.manager.delete_expense(self.table.item(selected_row, 0).text())

            # Update the UI
            self.update_expense_list()

    def update_expense_list(self, params = None, order = "ascending"):
        # Clear the existing table
        self.table.setRowCount(0) 
        expenses = self.manager.get_expenses()

        if params == "amount":
            if order == "descending":
                expenses = sorted(expenses, key=operator.attrgetter('amount'), reverse=True) 
            else:
                expenses = sorted(expenses, key=operator.attrgetter('amount')) 
        elif params == "date":
            if order == "descending":
                expenses = sorted(expenses, key=operator.attrgetter('date'), reverse=True) 
            else:
                expenses = sorted(expenses, key=operator.attrgetter('date')) 
        elif params == "description":
            if order == "descending":
                expenses = sorted(expenses, key=operator.attrgetter('description'), reverse=True) 
            else:
                expenses = sorted(expenses, key=operator.attrgetter('description'))
        elif params == "category":
            if order == "descending":
                expenses = sorted(expenses, key=operator.attrgetter('category'), reverse=True) 
            else:
                expenses = sorted(expenses, key=operator.attrgetter('category'))
        elif params == "id":
            if order == "descending":
                expenses = sorted(expenses, key=operator.attrgetter('id'), reverse=True) 
            else:
                expenses = sorted(expenses, key=operator.attrgetter('id'))
        elif params == "search":
            target = self.search_input.text()
            expenses = [expense for expense in expenses if target in expense.description]
        
        expense: Expense
        for row, expense in enumerate(expenses):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(expense.id)))
            self.table.setItem(row, 1, QTableWidgetItem(expense.description))
            self.table.setItem(row, 2, QTableWidgetItem(str(expense.amount)))
            self.table.setItem(row, 3, QTableWidgetItem(str(expense.date)))
            self.table.setItem(row, 4, QTableWidgetItem(expense.category))

    def clear_inputs(self):
        self.description_input.clear()
        self.amount_input.clear()
        self.date_input.clear()