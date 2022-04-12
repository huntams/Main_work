from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                             QSizePolicy, QPushButton, QGridLayout, QLabel)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from db_worker import database, Composition, Membrane, Data, DataGraph
import sys


class Plot(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Creating QChart
        self.chart = QChart()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.add_series_time_proc()

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # Right Layout
        self.chart_view.setSizePolicy(size)
        self.grid.addWidget(self.chart_view, 1, 0, 2, 4)

        self.grid.addWidget(QLabel("Графики"), 0, 0, 1, 1)

        plot_btn = QPushButton('Отрисовать график времен срабатывания от поля', self)
        plot_btn.clicked.connect(self.add_series_time_proc)
        self.grid.addWidget(plot_btn, 0, 1, 1, 1)

        plot_btn2 = QPushButton('Отрисовать график прозрачности от поля', self)
        plot_btn2.clicked.connect(self.add_series_transpare_proc)
        self.grid.addWidget(plot_btn2, 0, 2, 1, 1)

        plot_btn3 = QPushButton('Отрисовка графиков данных', self)
        plot_btn3.clicked.connect(self.add_series_transpare_proc)
        self.grid.addWidget(plot_btn3, 0, 3, 1, 1)

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

    def add_series_time_proc(self):
        # Create QLineSeries
        self.chart.removeAllSeries()
        self.series = QLineSeries()
        self.series2 = QLineSeries()
        self.series3 = QLineSeries()
        self.series.setName("t_on")
        self.series2.setName("t_off")
        self.series3.setName("t_work")

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
