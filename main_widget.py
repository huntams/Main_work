from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout,
                             QSizePolicy)

from db_worker import Data
from widTableData import Tablica
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


    def reload(self):
        for info, BD_data in enumerate(Data.select()):
            if BD_data.membrane.composition.name_composition == self.table_view.table.item(info, 0):
                informations = self.table_view.table.findItems(str(BD_data.Emax), Qt.MatchExactly)
                informations[0].setBackground(QtGui.QColor(self.chart_view.color_name[0]))
