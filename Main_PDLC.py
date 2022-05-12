"""
@authors: Maksim & Konstantin
"""

import datetime
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp, QAction, QApplication

import main_widget
import myinterface
import widTableData

now = datetime.datetime.now()
cur_date = now.strftime("%d-%m-%Y")


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
        # self.main_w.chart_view.choice_wid.qbtn.clicked.connect(self.test_test)
        # Включение поиска на нажатие в таблице
        self.main_w.table_view.table.selectionModel().selectionChanged.connect(self.click_table)
        # Проверка на нажатия рисование какого-либо графика
        self.main_w.chart_view.plot_btn.clicked.connect(self.choice_click)
        self.main_w.chart_view.plot_btn2.clicked.connect(self.choice_click)
        self.main_w.chart_view.plot_btn3.clicked.connect(self.choice_click)

        # fff = choice.Choicer()
        # fff.qbtn.clicked.connect(self.test_test)
        # Window dimensions

    def Manual_read_Widget(self):
        """
        Запуск виджета загрузки данных с компьютера и  заполнение таблицы при загрузки данных
        """
        self.listwidget = myinterface.Example()
        self.listwidget.setFixedSize(500, 160)
        # self.setWindowTitle("PDLC Reader")
        self.listwidget.qbtn.clicked.connect(self.main_w.table_view.zapolnenietablici)

    def choice_click(self):
        """
        Передаёт функцию внутри виджета с полученными данными о цвете линии
        """
        self.main_w.chart_view.choice_wid.qbtn.clicked.connect(self.test_test)

    def click_table(self, selected, deselected):
        """
        Функция поиска нажатых ячеек
        """
        # Получение всех нажатых ячеек
        for ix in selected.indexes():
            if ix.column() == 1:
                # Передача название строки и название плёнки
                self.main_w.chart_view.name = self.main_w.table_view.table.item(ix.row(), ix.column()).text()
                self.main_w.chart_view.name2 = self.main_w.table_view.table.item(ix.row(), 0).text()
                # Отрисовка ячейки
                self.main_w.chart_view.add_series_otrisovka_graf()
                self.test_test()
            elif ix.column() == 4:
                # Передача название строки, название плёнки и содержание ячейки
                self.main_w.chart_view.name = self.main_w.table_view.table.item(ix.row(), 1).text()
                self.main_w.chart_view.name2 = self.main_w.table_view.table.item(ix.row(), 0).text()
                self.main_w.chart_view.name_dot = self.main_w.table_view.table.item(ix.row(), ix.column()).text()
                # выделение на графике данные, нажатой ячейки
                self.main_w.chart_view.add_series_transpare_proc()
                self.test_test()
                print('its Ph.Umax:{}'.format(self.main_w.table_view.table.item(ix.row(), ix.column()).text()))
            self.main_w.table_view.color_name = []
            self.main_w.table_view.zapolnenietablici()
            # print('Row: {0},column:{1}, text:{2}'.format(ix.row(),
            #                                             ix.column(),
            #                                             self.main_w.table_view.table.item(ix.row(),
            #                                                                               ix.column()).text()))
            break

    #

    def test_test(self):
        """
        Передача данных в таблицу для добавления цветов в ячейках
        """
        self.main_w.table_view.color_name = self.main_w.chart_view.color_name
        self.main_w.table_view.zapolnenietablici()

    def central_wid_table(self):
        """
        Определение центрального виджета программы
        """
        self.listwidget2 = widTableData.Tablica()
        self.main_w = main_widget.Widget()
        self.setCentralWidget(self.main_w)

    def set_menu_tools_UI(self):
        """
        Первичная установка интерфейса
        """
        # Создание тригерров для соединения с кнопками в программе
        RawReadAction = QAction(QIcon('icons/rawread.png'),
                                '&Загрузка исходных данных', self)
        RawReadAction.setShortcut('Ctrl+R')
        RawReadAction.setStatusTip('Собрать исходники в БД')
        RawReadAction.triggered.connect(self.Manual_read_Widget)
        exitAction = QAction(QIcon('icons/exit.png'), '&Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть приложение')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        # Создание кнопок загрузки данных и закрытия программы
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(RawReadAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        # получение данных экрана
        geometry = self.screen().availableGeometry()
        # установка размеров экрана
        self.resize(geometry.width() * 0.8, geometry.height() * 0.7)  # setGeometry(300, 300, 300, 600)
        self.setWindowTitle('PDLC Reader')
        self.show()

    def closeEvent(self, event):
        """
        Функция закрытие всей программы
        """
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
