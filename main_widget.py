from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                             QSizePolicy, QPushButton)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from db_worker import database, Composition, Membrane, Data, DataGraph
from PySide6.QtWidgets import QApplication
from widTableData import Tablica
import sys


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Getting the Model
        #        self.model = Tablica()

        # Creating a QTableView
        self.table_view = Tablica()
        #        self.table_view.setModel(self.model)

        # QTableView Headers
        resize = QHeaderView.ResizeToContents

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.add_series_time_proc("test table", [0, 1])

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Right Layout
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        self.table_view.zapolnenietablici()

    def add_series_transpare_proc(self):
        # Create QLineSeries
        self.chart.removeAllSeries()
        self.series = QLineSeries()
        self.series.setName("UphMAX")
        for BD_data in Data.select():
            if BD_data.active:
                self.series.append(BD_data.Emax, BD_data.Umax)
                # Uph_ampl_list.append(BD_data.Umax)
        self.chart.addSeries(self.series)

        #        # Setting X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Управляющее поле, В/мкм")
        self.chart.setAxisX(self.axis_x)
        self.series.attachAxis(self.axis_x)
        #        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Прозрачность, В")
        self.chart.setAxisY(self.axis_y)
        self.series.attachAxis(self.axis_y)
        #     # Getting the color from the QChart to use it on the QTableView
        color_name = self.series.pen().color().name()

    def add_series_time_proc(self, name, columns):
        # Create QLineSeries
        self.chart.removeAllSeries()
        self.series = QLineSeries()
        self.series2 = QLineSeries()
        self.series3 = QLineSeries()
        self.series.setName(name)
        self.series2.setName("name")
        self.series3.setName("3")

        for BD_data in Data.select():
            if BD_data.active:
                self.series.append(BD_data.Emax, BD_data.dTph_On)
                self.series2.append(BD_data.Emax, BD_data.dTph_Off)
                self.series3.append(BD_data.Emax, BD_data.dTph_max)
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.series2)
        self.chart.addSeries(self.series3)
        #
        #        # Setting X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Управляющее поле, В/мкм")
        self.chart.setAxisX(self.axis_x)
        self.series.attachAxis(self.axis_x)
        #        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Время, мс")
        self.chart.setAxisY(self.axis_y)
        self.series.attachAxis(self.axis_y)
        #     # Getting the color from the QChart to use it on the QTableView
        color_name = self.series.pen().color().name()
