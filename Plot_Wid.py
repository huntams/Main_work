from PyQt5 import QtGui
from PyQt5.QtCore import Qt
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
        self.name, self.name2, self.name_dot = '', '', ''
        self.color_name = []
        self.chart = QChart()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # Right Layout
        self.chart_view.setSizePolicy(size)
        self.grid.addWidget(self.chart_view, 1, 0, 2, 4)

        self.grid.addWidget(QLabel("Графики"), 0, 0, 1, 1)

        self.plot_btn = QPushButton('Отрисовать график времен срабатывания от поля', self)
        self.plot_btn.clicked.connect(self.test_func)
        self.grid.addWidget(self.plot_btn, 0, 1, 1, 1)

        self.plot_btn2 = QPushButton('Отрисовать график прозрачности от поля', self)
        self.plot_btn2.clicked.connect(self.test_func2)
        self.grid.addWidget(self.plot_btn2, 0, 2, 1, 1)

        self.plot_btn3 = QPushButton('Отрисовка вычисленного', self)
        self.plot_btn3.clicked.connect(self.test_func3)
        self.grid.addWidget(self.plot_btn3, 0, 3, 1, 1)

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

    def test_func(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_time_proc)

    def test_func2(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_transpare_proc)

    def test_func3(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_otrisovka_graf)

    def add_series_transpare_proc(self):
        #    #ошибка в цикле поменять name
        # Create QLineSeries
        try:
            self.color_name = []
            self.chart.removeAllSeries()
            if self.name_dot != '':
                series_dot2 = QScatterSeries(self.chart)
                # series_dot2.pen().setColor(QtGui.QColor(255, 0, 0))
            for info, item in enumerate(self.choice_wid.choice_mas):
                slovar, sorted_dict, sorted_values = {}, {}, {}
                self.series = QLineSeries()
                series_dot = QScatterSeries(self.chart)
                self.series.setName("UphMAX" + ' ' + str(item))
                for BD_data in Data.select():
                    if item == BD_data.membrane.composition.name_composition:
                        if BD_data.active:
                            slovar[BD_data.Umax] = BD_data.Emax
                            # informations = self.tab.table.findItems(str(BD_data.Emax), Qt.MatchExactly)
                            # information = informations[0]
                            # information.setBackground(QtGui.QColor(self.color_name))
                sorted_values = sorted(slovar.values())
                print(sorted_values)
                print(list(slovar.keys()))
                for i in sorted_values:
                    for k in slovar.keys():
                        if slovar[k] == i:
                            sorted_dict[k] = slovar[k]
                            break
                if self.name_dot != '':
                    for BD_data in Data.select().where(self.name == Data.name):
                        if BD_data.membrane.composition.name_composition == self.name2:
                            print(self.name_dot, sorted_dict[self.name_dot])
                            # series_dot2.append(self.name_dot, sorted_dict[self.name_dot])

                for k in sorted_dict.keys():
                    # if self.name_dot != '':
                    #    #ошибка в цикле поменять name
                    #    for BD_data in Data.select().where(self.name_dot == Data.Emax):
                    #        print('testestests')
                    #        if BD_data.membrane.composition.name_composition == self.name2 \
                    #                and self.name == BD_data.name:
                    #            print('yeyeyesw')
                    self.series.append(slovar[k], k)
                    series_dot.append(slovar[k], k)
                self.chart.addSeries(self.series)
                self.chart.addSeries(series_dot)
                if self.name_dot != '':
                    print('yes')
                    self.chart.addSeries(series_dot2)
                self.color_name.append("{}".format(self.series.pen().color().name()))
                self.color_name.append(item)
                # self.plot_btn.setStyleSheet('background:' + self.color_name[0])
            self.name, self.name2, self.name_dot = '', '', ''
            self.axis_plot("Управляющее поле, В/мкм", "Прозрачность, В")
        except Exception as e:
            print(e)

    #    def test_tTTTT(self):
    #
    #        test_test = widTableData.Tablica()
    #        test_test.set_color(self.color_name)
    #        test_test.color_name = self.color_name
    #        print(test_test.color_name)
    def add_series_time_proc(self):
        try:
            # Create QLineSeries
            self.color_name = []
            self.chart.removeAllSeries()
            for info, item in enumerate(self.choice_wid.choice_mas):
                slovar, sorted_dict = [{}, {}], [{}, {}]
                self.series = QLineSeries()
                self.series2 = QLineSeries()
                self.series3 = QLineSeries()
                self.series.setName("t_on" + ' ' + str(item))
                self.series2.setName("t_off")
                self.series3.setName("t_work")
                for BD_data in Data.select():
                    if item == BD_data.membrane.composition.name_composition:
                        if BD_data.active:
                            slovar[0][BD_data.dTph_On] = BD_data.Emax
                            slovar[1][BD_data.dTph_Off] = BD_data.dTph_max
                sorted_values = sorted(slovar[0].values())
                for i in sorted_values:
                    for k in slovar[0].keys():
                        if slovar[0][k] == i:
                            sorted_dict[0][k] = slovar[0][k]
                            break
                x1 = list(sorted_dict[0].keys())
                x2 = list(slovar[1].keys())
                for index in range(len(x1)):
                    self.series.append(sorted_dict[0][x1[index]], x1[index])
                    self.series2.append(sorted_dict[0][x1[index]], x2[index])
                    self.series3.append(sorted_dict[0][x1[index]], slovar[1][x2[index]])
                self.chart.addSeries(self.series)
                self.chart.addSeries(self.series2)
                self.chart.addSeries(self.series3)
                self.color_name.append(self.series.pen().color().name())
                self.color_name.append(self.series2.pen().color().name())
                self.color_name.append(self.series3.pen().color().name())
                self.color_name.append(item)
            self.axis_plot("Управляющее поле, В/мкм", "Время, мс")
        except Exception as e:
            print(e)

    def add_series_otrisovka_graf(self):
        massive1, massive2 = [], []
        try:
            self.chart.removeAllSeries()
            if self.name != '':
                self.dot_series = QScatterSeries(self.chart)
                self.series = QLineSeries()
                self.series2 = QLineSeries()
                self.series.setName("t_on")
                self.series2.setName("t_off")
                for BD_data in Data.select().where(self.name == Data.name):
                    if BD_data.membrane.composition.name_composition == self.name2:
                        self.series_otrisovka_append(BD_data)
                self.chart.addSeries(self.series)
                self.chart.addSeries(self.series2)
                self.chart.addSeries(self.dot_series)
                self.axis_x = QValueAxis()
                self.axis_x.setTitleText("Время, мс")
                self.chart.setAxisX(self.axis_x)
                self.series2.attachAxis(self.axis_x)
                self.dot_series.attachAxis(self.axis_x)
                self.axis_y = QValueAxis()
                self.axis_y.setTitleText("Управляющее поле, В/мкм")
                self.chart.setAxisY(self.axis_y)
                self.series2.attachAxis(self.axis_y)
                self.dot_series.attachAxis(self.axis_y)
            else:
                #many plots
                for info, item in enumerate(self.choice_wid.choice_mas):
                    self.dot_series = QScatterSeries()
                    self.series = QLineSeries()
                    self.series2 = QLineSeries()
                    self.series.setName("t_on")
                    self.series2.setName("t_off")
                    for BD_data in Data.select():
                        if item == BD_data.membrane.composition.name_composition:
                            self.series_otrisovka_append(BD_data)
                    self.chart.addSeries(self.series)
                    self.chart.addSeries(self.series2)
                    self.chart.addSeries(self.dot_series)
                    self.axis_x = QValueAxis()
                    self.axis_x.setTitleText("Время, мс")
                    self.chart.setAxisX(self.axis_x)
                    self.series2.attachAxis(self.axis_x)
                    self.dot_series.attachAxis(self.axis_x)
                    self.axis_y = QValueAxis()
                    self.axis_y.setTitleText("Управляющее поле, В/мкм")
                    self.chart.setAxisY(self.axis_y)
                    self.series2.attachAxis(self.axis_y)
                    self.dot_series.attachAxis(self.axis_y)
            self.name, self.name2 = '', ''
        except Exception as e:
            print(e)
        #self.axis_plot("Время, мс", "Управляющее поле, В/мкм")



    def series_otrisovka_append(self, BD_data):
        if BD_data.active:
            print("time1")
            for BD_item in DataGraph.select().where(DataGraph.index == BD_data.dirname):
                self.series.append(BD_item.Edata1, BD_item.Edata2)
                self.series2.append(BD_item.Udata1, BD_item.Udata2)
            print("time2")
            if BD_data.Uph_active:
                print(BD_data.dTph_On, BD_data.Uph_On)
                print(BD_data.dTph_Off, BD_data.Uph_Off)
                self.dot_series.append(BD_data.dTph_On, BD_data.Uph_On)
                self.dot_series.append(BD_data.dTph_Off, BD_data.Uph_Off)
            print(BD_data.name, end='')
            print(' -- ploted')
        else:
            print(BD_data.name, end='')
            print(' -- NOT ploted')
