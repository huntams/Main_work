from PyQt5.QtWidgets import (QWidget, QHeaderView, QHBoxLayout,
                             QSizePolicy)
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
        self.table_view.zapolnenietablici()