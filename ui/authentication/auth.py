from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox

from managers.user_manager import UserManager

class LoginDialog(QDialog):
  def __init__(self, user_manager: UserManager, parent=None):
    super(LoginDialog, self).__init__(parent)
    self.user_id = -1
    self.user_manager = user_manager

    self.setWindowTitle('Login')
    self.setGeometry(500, 300, 300, 150)

    layout = QVBoxLayout(self)

    self.username_label = QLabel('Username:')
    self.username_input = QLineEdit(self)

    self.password_label = QLabel('Password:')
    self.password_input = QLineEdit(self)
    self.password_input.setEchoMode(QLineEdit.Password)

    login_button = QPushButton('Login', self)
    login_button.clicked.connect(self.authenticate)

    register_button = QPushButton('Register', self)
    register_button.clicked.connect(self.register_user)

    layout.addWidget(self.username_label)
    layout.addWidget(self.username_input)
    layout.addWidget(self.password_label)
    layout.addWidget(self.password_input)
    layout.addWidget(login_button)
    layout.addWidget(register_button)

  def closeEvent(self, event):
    # Override the close event to handle the window close button
    result = QMessageBox.question(self, 'Exit Application', 'Are you sure you want to exit?', 
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
    if result == QMessageBox.Yes:
      QApplication.quit()
    else:
      event.ignore()

  def authenticate(self):
    username = self.username_input.text()
    password = self.password_input.text()

    message, code = self.user_manager.authenticate_user(username, password)

    if code == 0:
      self.user_id = self.user_manager.get_user_id_by_username(username)
      self.accept()
    else:
      QMessageBox.warning(self, 'Login Failed', message)

  def register_user(self):
    username = self.username_input.text()
    password = self.password_input.text()

    message, code = self.user_manager.create_user(username, password)
    
    if code == 0:
      QMessageBox.information(self, 'Registration Successful', message)
      self.user_id = self.user_manager.get_user_id_by_username(username)
      self.accept()
    else:
      QMessageBox.warning(self, 'Registration Failed', message)