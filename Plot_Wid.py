from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget,
                             QSizePolicy, QPushButton, QGridLayout, QLabel, QComboBox)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries

from db_worker import Data, DataGraph
import choice


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
        plot_btn.clicked.connect(self.test_func2)
        self.grid.addWidget(plot_btn, 0, 1, 1, 1)

        plot_btn2 = QPushButton('Отрисовать график прозрачности от поля', self)
        plot_btn2.clicked.connect(self.test_func)
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

    def test_func2(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_time_proc)

    def test_func(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_transpare_proc)

    def add_series_transpare_proc(self):
        # Create QLineSeries
        try:
            massive1, massive2 = [], []
            self.chart.removeAllSeries()
            for info, item in enumerate(self.choice_wid.choice_mas):
                self.series = QLineSeries()
                series_dot = QScatterSeries(self.chart)
                self.series.setName("UphMAX" + ' ' + str(item))
                for BD_data in Data.select():
                    if item == BD_data.membrane.composition.name_composition:
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
        except Exception as e:
            print(e)

    def add_series_time_proc(self):
        # Create QLineSeries
        mas = [[], [], [], []]
        massive1, massive2, massive3 = [], [], []
        self.chart.removeAllSeries()
        for info, item in enumerate(self.choice_wid.choice_mas):
            self.series = QLineSeries()
            self.series2 = QLineSeries()
            self.series3 = QLineSeries()
            self.series.setName("t_on" + ' ' + str(item))
            self.series2.setName("t_off" + ' ' + str(item))
            self.series3.setName("t_work" + ' ' + str(item))
            for BD_data in Data.select():
                if item == BD_data.membrane.composition.name_composition:
                    if BD_data.active:
                        mas[0].append(BD_data.Emax)
                        mas[1].append(BD_data.dTph_On)
                        mas[2].append(BD_data.dTph_Off)
                        mas[3].append(BD_data.dTph_max)
            for i in range(len(mas)):
                mas[i].sort()
            for index in range(len(mas)):
                self.series.append(mas[0][index], mas[1][index])
                self.series2.append(mas[0][index], mas[2][index])
                self.series3.append(mas[0][index], mas[3][index])
            self.chart.addSeries(self.series)
            self.chart.addSeries(self.series2)
            self.chart.addSeries(self.series3)
        #
        self.axis_plot("Управляющее поле, В/мкм", "Время, мс")

    def addSeries_otrisovka_graf(self):
        massive1, massive2 = [], []
        self.chart.removeAllSeries()
        dot_series = QScatterSeries(self.chart)
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
                if BD_data.Uph_active:
                    dot_series.append(BD_data.dTph_On, BD_data.Uph_On)
                    dot_series.append(BD_data.dTph_Off, BD_data.Uph_Off)
                print(BD_data.name, end='')
                print(' -- ploted')
            else:
                print(BD_data.name, end='')
                print(' -- NOT ploted')
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.series2)
        self.chart.addSeries(dot_series)
        self.axis_plot("Управляющее поле, В/мкм", "Время, мс")
