from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                               QSizePolicy)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis

from PySide6.QtWidgets import QApplication
from widTableData import Tablica
import sys

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Getting the Model
#        self.model = Tablica(data)

        # Creating a QTableView
        self.table_view = Tablica()
#        self.table_view.setModel(self.model)

        # QTableView Headers
        resize = QHeaderView.ResizeToContents

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
#        self.add_series("test table", [0, 1])

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        self.table_view.zapolnenietablici()
#    def add_series(self, name, columns):
#        # Create QLineSeries
#        self.series = QLineSeries()
#        self.series.setName(name)
#
#        # Filling QLineSeries
#        for i in range(self.model.rowCount()):
#            # Getting the data
#            t = self.model.index(i, 0).data()
#            date_fmt = "yyyy-MM-dd HH:mm:ss.zzz"
#
#            x = QDateTime().fromString(t, date_fmt).toSecsSinceEpoch()
#            y = float(self.model.index(i, 1).data())
#
#            if x > 0 and y > 0:
#                self.series.append(x, y)
#
#        self.chart.addSeries(self.series)
#
#        # Setting X-axis
#        self.axis_x = QDateTimeAxis()
#        self.axis_x.setTickCount(10)
#        #self.axis_x.setFormat("dd.MM (h:mm)")
#        self.axis_x.setTitleText("V")
#        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
#        self.series.attachAxis(self.axis_x)
#        # Setting Y-axis
#        self.axis_y = QValueAxis()
#        self.axis_y.setTickCount(10)
#        self.axis_y.setLabelFormat("%.2f")
#        self.axis_y.setTitleText("V/mkm")
#        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
#        self.series.attachAxis(self.axis_y)
#     # Getting the color from the QChart to use it on the QTableView
#        color_name = self.series.pen().color().name()