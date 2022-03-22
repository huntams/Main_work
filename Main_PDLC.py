"""
@authors: Maksim & Konstantin
"""

import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QDockWidget
from PyQt6.QtGui import QIcon, QAction
import myinterface
import widTableData
import datetime
now = datetime.datetime.now()
cur_date = now.strftime("%d-%m-%Y")

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.set_menu_tools_UI()
        self.central_wid_table()

    def Manual_read_Widget(self):

        self.listwidget = myinterface.Example()
        self.listwidget.resize(500, 160)
        # self.setWindowTitle("PDLC Reader")
        self.listwidget.qbtn.clicked.connect(self.listwidget2.zapolnenietablici)

    def central_wid_table(self):

        self.listwidget2 = widTableData.Tablica()
        self.setCentralWidget(self.listwidget2)

    def set_menu_tools_UI(self):

        RawReadAction = QAction(QIcon('icons/rawread.png'),
                                '&Загрузка исходных данных', self)
        RawReadAction.setShortcut('Ctrl+R')
        RawReadAction.setStatusTip('Собрать исходники в БД')
        RawReadAction.triggered.connect(self.Manual_read_Widget)
        exitAction = QAction(QIcon('icons/exit.png'), '&Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть приложение')
        exitAction.triggered.connect(QApplication.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(RawReadAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        self.resize(900, 800)  # setGeometry(300, 300, 300, 600)
        self.setWindowTitle('PDLC Reader')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Предупреждение',
                                     "Вы действительно хотите выйти?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('LOGO-PDLC.png'))
    ex = Example()
    ex.show()
    sys.exit(app.exec())
