import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QMessageBox

from database.database_manager import DatabaseManager
from managers.user_manager import UserManager
from managers.category_manager import CategoryManager
from managers.expense_manager import ExpenseManager

from ui.authentication.auth import LoginDialog
from ui.widgets.category_widget import CategoryWidget
from ui.widgets.expense_widget import ExpenseWidget
from ui.widgets.main_content import MainContent

class MainWindow(QMainWindow):
  def __init__(self, cm: CategoryManager, em: ExpenseManager):
    super().__init__()
    self.category_manager = cm
    self.expense_manager = em

    self.setWindowTitle("Expense Tracker Application")
    self.setGeometry(300, 100, 800, 700)
    self.center()

    self.create_category_widget()
    self.create_expense_widget()
    
    # Set up the main window properties
    menu_bar = self.menuBar()
    file_menu = menu_bar.addMenu("File")

    # Export Action
    export_action = QAction("Export as excel", self)
    export_action.setShortcut("Ctrl+E")
    export_action.triggered.connect(self.export_to_excel)

    # Exit QAction
    exit_action = QAction("Exit", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.exit_app)

    file_menu.addAction(export_action)
    file_menu.addAction(exit_action)

    self.setup_layout()

  def create_expense_widget(self):
    self.expense_widget = ExpenseWidget(self.expense_manager)

  def create_category_widget(self):
    self.category_widget = CategoryWidget(self.category_manager)
  
  def export_to_excel(self):
    df = self.expense_manager.to_df()
    
    if not df.empty:
      options = QFileDialog.Options()
      options |= QFileDialog.DontUseNativeDialog
      # Get the file name with a '.xlsx' extension
      fileName, _ = QFileDialog.getSaveFileName(self, "Export as Excel", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

      if fileName:
        if not fileName.endswith('.xlsx'):
          fileName += '.xlsx'
        df.to_excel(fileName, index=False, engine='xlsxwriter')
        QMessageBox.information(self, "File Created", "Your expenses saved us excel file.")
      else:
        print("Export canceled or no file selected.")
    else:
      QMessageBox.warning(self, "Empty Data", "DataFrame is empty. Nothing to export.")
  
  def setup_layout(self):
    main_layout = QVBoxLayout()

    main_content = MainContent(self.category_widget, self.expense_widget)
    main_layout.addWidget(main_content)

    central_widget = QWidget(self)
    central_widget.setLayout(main_layout)
    self.setCentralWidget(central_widget)

  def center(self):
    screen_geometry = self.screen().geometry()
    center_point = screen_geometry.center()
    self.move(center_point - self.rect().center())

  @Slot()
  def exit_app(self, checked):
    QApplication.quit()

def start(db: DatabaseManager):
  app = QApplication(sys.argv)
  user_manager = UserManager(db)
  login_dialog = LoginDialog(user_manager)

  if login_dialog.exec() == LoginDialog.Accepted:
    user_id = login_dialog.user_id
    category_manager = CategoryManager(db, user_id)
    expense_manager = ExpenseManager(db, user_id)
    main_window = MainWindow(category_manager, expense_manager)
    main_window.show()
  sys.exit(app.exec())