from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PySide6.QtCharts import QChartView, QPieSeries, QChart

from managers.expense_manager import ExpenseManager

class ChartWidget(QWidget):
    def __init__(self, manager: ExpenseManager):
        QWidget.__init__(self)
        self.manager = manager
        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.plot = QPushButton("Plot")
        self.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                background-color: #800080;
                color: white;
                border-radius: 4px;
                min-height: 30px;
            }

            QChartView {    
                border: 1px solid black;
            }
        """
        )
        self.plot.clicked.connect(self.plot_data)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.chart_view)
        main_layout.addWidget(self.plot)

        self.setLayout(main_layout)


    @Slot()
    def plot_data(self):
        series = QPieSeries()
        data = self.manager.get_total_for_plot()
        for item in data:
            # print(item)
            series.append(item[0], item[1])
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)