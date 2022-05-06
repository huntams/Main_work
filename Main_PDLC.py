"""
@authors: Maksim & Konstantin
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp, QAction, QApplication, QDockWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic.properties import QtGui

import myinterface
import widTableData
import datetime
import main_widget
from db_worker import Data

now = datetime.datetime.now()
cur_date = now.strftime("%d-%m-%Y")
import choice


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_w = main_widget.Widget()
        self.set_menu_tools_UI()
        self.central_wid_table()
        self.setWindowTitle("test plot")
        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")
        #self.main_w.chart_view.choice_wid.qbtn.clicked.connect(self.test_test)
        self.main_w.chart_view.plot_btn.clicked.connect(self.prosto_test)
        self.main_w.chart_view.plot_btn2.clicked.connect(self.prosto_test)
        self.main_w.chart_view.plot_btn3.clicked.connect(self.prosto_test)
        # fff = choice.Choicer()
        # fff.qbtn.clicked.connect(self.test_test)
        # Window dimensions

    def Manual_read_Widget(self):
        self.listwidget = myinterface.Example()
        self.listwidget.setFixedSize(500, 160)
        # self.setWindowTitle("PDLC Reader")
        self.listwidget.qbtn.clicked.connect(self.main_w.table_view.zapolnenietablici)
    def prosto_test(self):
        self.main_w.chart_view.choice_wid.qbtn.clicked.connect(self.test_test)
    def test_test(self):
        self.main_w.table_view.color_name = self.main_w.chart_view.color_name
        print(self.main_w.table_view.color_name)
        self.main_w.table_view.zapolnenietablici()

    def central_wid_table(self):
        self.listwidget2 = widTableData.Tablica()
        self.main_w = main_widget.Widget()
        self.setCentralWidget(self.main_w)

    def set_menu_tools_UI(self):
        RawReadAction = QAction(QIcon('icons/rawread.png'),
                                '&Загрузка исходных данных', self)
        RawReadAction.setShortcut('Ctrl+R')
        RawReadAction.setStatusTip('Собрать исходники в БД')
        RawReadAction.triggered.connect(self.Manual_read_Widget)
        testAction = QAction(QIcon('icons/rawread.png'), '&test', self)
        testAction.setShortcut('Ctrl+U')
        testAction.triggered.connect(self.test_test)
        exitAction = QAction(QIcon('icons/exit.png'), '&Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть приложение')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(RawReadAction)
        fileMenu.addAction(testAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        geometry = self.screen().availableGeometry()
        self.resize(geometry.width() * 0.8, geometry.height() * 0.7)  # setGeometry(300, 300, 300, 600)
        self.setWindowTitle('PDLC Reader')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Предупреждение',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('LOGO-PDLC.png'))
        ex = Example()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
