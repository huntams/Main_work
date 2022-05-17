import os

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget,
                             QSizePolicy, QPushButton, QGridLayout, QLabel)
import choice
from db_worker import Data, DataGraph


class Plot(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.name, self.name2, self.name_dot = '', '', ''
        self.color_name = []
        self.filename=''
        # Создание QChart(График, в который отправляются все линии)
        self.chart = QChart()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        # Загрузка анимаций при работе с графиком
        self.chart.setAnimationOptions(QChart.AllAnimations)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # Right Layout
        self.chart_view.setSizePolicy(size)
        self.grid.addWidget(self.chart_view, 1, 0, 2, 4)

        self.plot_btn4 = QPushButton('Save')
        self.grid.addWidget(self.plot_btn4, 0, 0, 1, 1)
        # Проверка нажатие кнопок
        self.plot_btn = QPushButton('Отрисовать график времен срабатывания от поля', self)
        self.plot_btn.clicked.connect(self.test_func)
        self.grid.addWidget(self.plot_btn, 0, 1, 1, 1)

        self.plot_btn2 = QPushButton('Отрисовать график прозрачности от поля', self)
        self.plot_btn2.clicked.connect(self.test_func2)
        self.grid.addWidget(self.plot_btn2, 0, 2, 1, 1)

        self.plot_btn3 = QPushButton('Отрисовка вычисленного', self)
        self.plot_btn3.clicked.connect(self.test_func3)
        self.grid.addWidget(self.plot_btn3, 0, 3, 1, 1)

    def save_jpg(self, filename=''):
        if not os.path.isdir("images"):
            os.mkdir("images")
        p = QPixmap(self.chart_view.grab())
        p.save('images/'+filename + '.png', "PNG")

    def test_func(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_time_proc)

    def test_func2(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_transpare_proc)

    def test_func3(self):
        self.choice_wid = choice.Choicer()
        self.choice_wid.qbtn.clicked.connect(self.add_series_otrisovka_graf)

    def axis_plot(self, x_axis, y_axis):
        """
        Настройка осей графика
        """
        # Setting X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText(x_axis)
        self.chart.setAxisX(self.axis_x)
        # подсоединение данных к оси x
        self.series.attachAxis(self.axis_x)
        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(y_axis)
        self.chart.setAxisY(self.axis_y)
        # подсоединение данных к оси Y
        self.series.attachAxis(self.axis_y)

    def add_series_transpare_proc(self):
        try:
            slovar, sorted_dict, sorted_values = {}, {}, {}
            self.color_name = []
            self.chart.removeAllSeries()
            # Create QLineSeries
            series_dot2 = QScatterSeries(self.chart)
            self.series = QLineSeries()
            series_dot = QScatterSeries(self.chart)
            if self.name_dot != '':
                for BD_item in Data.select().where(self.name == Data.name):
                    if BD_item.membrane.composition.name_composition == self.name2:
                        self.series.setName("UphMAX" + ' ' + self.name2)
                        print(self.name2)
                        self.series_plot_transpare(self.name2, slovar, sorted_dict, series_dot)
                        series_dot2.append(sorted_dict[float(self.name_dot)], float(self.name_dot))
                self.chart.addSeries(series_dot2)
                self.axis_plot("Управляющее поле, В/мкм", "Время, мс")
                series_dot2.attachAxis(self.axis_x)
                series_dot2.attachAxis(self.axis_y)
                self.filename = self.name2+' '+self.name
                # series_dot2.pen().setColor(QtGui.QColor(255, 0, 0))
            else:
                for info, item in enumerate(self.choice_wid.choice_mas):
                    self.series = QLineSeries()
                    series_dot = QScatterSeries(self.chart)
                    self.series.setName("UphMAX" + ' ' + str(item))
                    slovar, sorted_dict, sorted_values = {}, {}, {}
                    slovar, sorted_dict = self.series_plot_transpare(item, slovar, sorted_dict, series_dot)

                    # self.plot_btn.setStyleSheet('background:' + self.color_name[0])
                    self.filename += self.choice_wid.choice_mas[0]+' '
                self.axis_plot("Управляющее поле, В/мкм", "Время, мс")
            self.save_jpg(self.filename)
            self.name, self.name2, self.name_dot = '', '', ''
        except Exception as e:
            print(e)

    def series_plot_transpare(self, item, slovar, sorted_dict, series_dot):
        for BD_data in Data.select():
            if item == BD_data.membrane.composition.name_composition:
                if BD_data.active:
                    slovar[BD_data.Umax] = BD_data.Emax
        sorted_values = sorted(slovar.values())
        for i in sorted_values:
            for k in slovar.keys():
                if slovar[k] == i:
                    sorted_dict[k] = slovar[k]
                    break
        for k in sorted_dict.keys():
            self.series.append(slovar[k], k)
            series_dot.append(slovar[k], k)
        self.chart.addSeries(self.series)
        self.chart.addSeries(series_dot)
        # Getting the color from the QChart to use it on the QTableView
        self.color_name.append("{}".format(self.series.pen().color().name()))
        self.color_name.append(item)
        return slovar, sorted_dict

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
                self.axis_plot("Время, мс","Управляющее поле, В/мкм")
                self.dot_series.attachAxis(self.axis_x)
                self.dot_series.attachAxis(self.axis_y)
            else:
                # many plots
                for info, item in enumerate(self.choice_wid.choice_mas):
                    self.dot_series = QScatterSeries()
                    self.series = QLineSeries()
                    self.series2 = QLineSeries()
                    self.series.setName("t_on" + item)
                    self.series2.setName("t_off")
                    for BD_data in Data.select():
                        if item == BD_data.membrane.composition.name_composition:
                            self.series_otrisovka_append(BD_data)
                    self.chart.addSeries(self.series)
                    self.chart.addSeries(self.series2)
                    self.chart.addSeries(self.dot_series)
                    self.axis_plot("Время, мс", "Управляющее поле, В/мкм")
                    self.dot_series.attachAxis(self.axis_x)
                    self.dot_series.attachAxis(self.axis_y)
                    #self.axis_plot_graf()
            self.name, self.name2 = '', ''
        except Exception as e:
            print(e)
        # self.axis_plot("Время, мс", "Управляющее поле, В/мкм")

    def series_otrisovka_append(self, BD_data):
        if BD_data.active:
            print("time1")
            for BD_item in DataGraph.select().where(DataGraph.index == BD_data.dirname):
                self.series2.append(BD_item.Edata1, BD_item.Edata2)
                self.series.append(BD_item.Udata1, BD_item.Udata2)
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
