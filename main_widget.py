from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                             QSizePolicy, QPushButton)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from db_worker import database, Composition, Membrane, Data, DataGraph
from PySide6.QtWidgets import QApplication
from widTableData import Tablica
import sys
from Plot_Wid import Plot

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

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        self.chart_view = Plot()
        # Right Layout
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        self.table_view.zapolnenietablici()


