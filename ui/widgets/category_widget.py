from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QInputDialog

from managers.category_manager import CategoryManager

from ui.components.input_box import InputBox
from ui.components.header import Label
from utils.input_status import INPUT_STATUS

class CategoryWidget(QWidget):
    def __init__(self, category_manager: CategoryManager):
        super().__init__()
        self.manager = category_manager

        self.init_ui()

    def init_ui(self):
        from ui.components.button import Button
        self.header = Label("Categories")
        self.list_widget = QListWidget()

        self.name_input = InputBox("Name:", "string")

        self.add_button = Button("Add", self)
        
        self.update_button = Button("Update", self)
        self.update_button.setObjectName("updateButton")

        self.delete_button = Button("Delete", self)
        self.delete_button.setObjectName("deleteButton")

        # Styles
        self.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                padding: 8px;
                border: 1px solid black;
                border-radius: 4px;
            }
        """)

        # Layout
        main_layout = QVBoxLayout(self)
        
        upd_del = QHBoxLayout()
        upd_del.addWidget(self.update_button)
        upd_del.addWidget(self.delete_button)

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(upd_del)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.add_button)


        self.update_category_list()

    def update_category_list(self):
        self.list_widget.clear()

        categories = self.manager.get_categories()
        for category in categories:
            item = QListWidgetItem(category.name)
            item.setData(1, category.id)  # Store category ID as user data
            self.list_widget.addItem(item)


    def add(self):
        category_name = self.name_input.get_input()
        if len(category_name) != 0:
            self.manager.add_category(category_name)
            self.update_category_list()
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Empty Name", INPUT_STATUS.get('NAME_ERROR')[0])

    def update(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            new_name, ok_pressed = self.get_text_input("Update Category", "Enter new category name:")
            if len(new_name) != 0 and ok_pressed:
                category_id = current_item.data(1)
                self.manager.update_category_name(category_id, new_name)
                self.update_category_list()
            elif len(new_name) == 0 and ok_pressed:
                QMessageBox.warning(self, "Empty Name", INPUT_STATUS.get('NAME_ERROR')[0])

    def delete(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            id = current_item.data(1)
            reply = self.show_message_box("Delete Category", "Are you sure you want to delete this category?")
            if reply == QMessageBox.Yes:
                self.manager.delete_category(id)
                self.update_category_list()

    def get_text_input(self, title, label):
        text, ok_pressed = QInputDialog.getText(self, title, label, QLineEdit.Normal, "")
        return text, ok_pressed

    def show_message_box(self, title, message):
        reply = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No)
        return reply