from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget,
                             QSizePolicy, QPushButton, QGridLayout, QLabel)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QScatterSeries
from PyQt5.uic.properties import QtGui

from db_worker import Data, DataGraph
from widTableData import Tablica


class Plot(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Creating QChart
        self.chart = QChart()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        try:
            self.add_series_time_proc()
        except Exception as e:
            print("Didn't except data base")
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

        plot_btn3 = QPushButton('Отрисовка вычисленного', self)
        plot_btn3.clicked.connect(self.addSeries_otrisovka_graf)
        self.grid.addWidget(plot_btn3, 0, 3, 1, 1)

    def axis_plot(self, x_axis, y_axis):
        #        # Setting X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText(x_axis)
        self.chart.setAxisX(self.axis_x)
        self.series.attachAxis(self.axis_x)
        #        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(y_axis)
        self.chart.setAxisY(self.axis_y)
        self.series.attachAxis(self.axis_y)
        #     # Getting the color from the QChart to use it on the QTableView
        color_name = self.series.pen().color().name()

    def add_series_transpare_proc(self):
        # Create QLineSeries
        massive1, massive2 = [], []
        self.chart.removeAllSeries()
        self.series = QLineSeries()
        series_dot = QScatterSeries(self.chart)
        self.series.setName("UphMAX")
        for BD_data in Data.select():
            if BD_data.active:
                massive1.append(BD_data.Emax)
                massive2.append(BD_data.Umax)
        massive1.sort()
        massive2.sort()
        for index in range(len(massive1)):
            self.series.append(massive1[index], massive2[index])
            series_dot.append(massive1[index], massive2[index])
        self.chart.addSeries(self.series)
        self.chart.addSeries(series_dot)
        self.axis_plot("Управляющее поле, В/мкм", "Прозрачность, В")

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
        self.axis_plot("Управляющее поле, В/мкм", "Время, мс")

    def addSeries_otrisovka_graf(self):
        self.chart.removeAllSeries()
        self.series = QLineSeries()
        self.series2 = QLineSeries()
        self.series.setName("t_on")
        self.series2.setName("t_off")
        for BD_data in Data.select():
            if BD_data.active:
                print("time1")
                for BD_item in DataGraph.select().where(DataGraph.index == BD_data.dirname):
                    self.series.append(BD_item.Edata1, BD_item.Edata2)
                    self.series2.append(BD_item.Udata1, BD_item.Udata2)
                print("time2")
                self.chart.addSeries(self.series)
                self.chart.addSeries(self.series2)

                if BD_data.Uph_active:
                    print("YES")
                    # self.series.append()

                print(BD_data.name)
                print(' -- ploted')
            else:
                print(BD_data.name)
                print(' -- NOT ploted')
        self.axis_plot("Управляющее поле, В/мкм", "Время, мс")
