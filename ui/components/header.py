from PySide6.QtWidgets import QLabel

class Label(QLabel):
  def __init__(self, text):
    QLabel.__init__(self, text)
    self.setStyleSheet("font-size: 20px;")