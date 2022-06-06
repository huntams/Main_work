import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout,
                             QSizePolicy, QTabWidget, QVBoxLayout, QLabel, QPushButton)
from numpy import exp

from db_worker import Data
from widTableData import Tablica
from Plot_Wid import Plot


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.chart_view = Plot()
        # Getting the Model
        #        self.model = Tablica()

        # Creating a QTableView
        self.table_view = Tablica()
        #        self.table_view.setModel(self.model)

        # QTableView Headers
        resize = QHeaderView.ResizeToContents

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Right Layout
        # self.tab_widget = MyTabWidget(self)
        #
        # self.tab_widget.tabs.tabBarClicked.connect(self.choice_click)
        self.main_layout.addWidget(self.chart_view)

        # self.main_layout.addWidget(self.chart_view)
        # Set the layout to the QWidget
        self.setLayout(self.main_layout)



    def choice_click(self):
        print('3123123123')
        # self.tabs.tab

        # self.tab2.chart_view.choice_wid.qbtn.clicked.connect(self.update_color)

    def update_color(self):
        print('rweqaewerqqwerqw')

    def reload(self):
        for info, BD_data in enumerate(Data.select()):
            if BD_data.membrane.composition.name_composition == self.table_view.table.item(info, 0):
                informations = self.table_view.table.findItems(str(BD_data.Emax), Qt.MatchExactly)
                informations[0].setBackground(QtGui.QColor(self.chart_view.color_name[0]))


class MyTabWidget(QWidget):
    '''
    Класс загрузки графиков в интерфейс в изменённым видом
    '''

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Add tabs
        self.tabs.addTab(self.tab1, "Отрисовать графиков времен срабатывания от поля и прозрачности от поля")
        self.tabs.addTab(self.tab2, "Отрисовка вычисленного")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        self.chart_view = Plot()

        self.tab1.layout.addWidget(self.chart_view.chart_view)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.layout.addWidget(self.chart_view.chart_view)
        self.tab2.setLayout(self.tab2.layout)
        # Add tabs to widget

        self.layout.addWidget(self.tabs)
        self.plot_btn4 = QPushButton('Save')
        # self.grid.addWidget(self.plot_btn4, 0, 0, 1, 1)
        self.layout.addWidget(self.plot_btn4)
        self.setLayout(self.layout)
