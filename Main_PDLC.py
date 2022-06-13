"""
@authors: Maksim & Konstantin
"""

import datetime
import os
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp, QAction, QApplication
from numpy import exp

import main_widget
import myinterface
import widTableData
from db_worker import Data

now = datetime.datetime.now()
cur_date = now.strftime("%d-%m-%Y")


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_w = main_widget.Widget()
        self.set_menu_tools_UI()
        self.central_wid_table()
        self.clicked_header = True
        self.setWindowTitle("test plot")
        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")
        # self.main_w.chart_view.choice_wid.qbtn.clicked.connect(self.test_test)
        # Включение поиска на нажатие в таблице
        if os.path.exists('pdlc.db'):
            try:
                self.first_load()
            except Exception as e:
                print(e)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("Ошибка загрузки базы данных, попробуйте загрузить информацию с компьютера")
            msg.setWindowTitle("Информация")
            msg.exec_()
        self.main_w.table_view.table.selectionModel().selectionChanged.connect(self.click_table)
        # Проверка на нажатия рисование какого-либо графика

        # self.main_w.chart_view.plot_btn.clicked.connect(self.choice_click)
        # self.main_w.chart_view.plot_btn2.clicked.connect(self.choice_click)
        # self.main_w.chart_view.plot_btn3.clicked.connect(self.choice_click)

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
        self.listwidget.qbtn.clicked.connect(self.first_load)

    def first_load(self):
        self.main_w.table_view.zapolnenietablici()
        self.main_w.chart_view.name = self.main_w.table_view.table.item(2, 1).text()
        self.main_w.chart_view.name2 = self.main_w.table_view.table.item(2, 0).text()
        self.main_w.chart_view.add_series_otrisovka_graf()
        self.color_update()
        self.main_w.chart_view.plot_btn4.clicked.connect(self.save_jpg)
        self.main_w.table_view.table.horizontalHeader().sectionClicked.connect(self.update_choice)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("База данных успешна загружена")
        msg.setWindowTitle("Успех")
        msg.exec_()

    def update_choice(self):
        if self.clicked_header:
            self.main_w.table_view.table.horizontalHeaderItem(0).setText("Убрать всё")
            Data.update({Data.active: self.clicked_header}).execute()
            self.clicked_header = False
        else:
            self.main_w.table_view.table.horizontalHeaderItem(0).setText("Выбрать всё")
            Data.update({Data.active: self.clicked_header}).execute()
            self.clicked_header = True
        self.main_w.table_view.zapolnenietablici()

    def choice_click(self):
        """
        Передаёт функцию внутри виджета с полученными данными о цвете линии
        """
        self.main_w.chart_view.choice_wid.qbtn.clicked.connect(self.color_update)

    def save_jpg(self):
        number = 1
        if not os.path.isdir("images"):
            os.mkdir("images")
        p = QPixmap(self.main_w.chart_view.grab())
        if not os.path.exists('images/' + self.main_w.chart_view.series.name() + '.png'):
            p.save('images/' + self.main_w.chart_view.series.name() + '.png', "PNG")
        else:
            while os.path.exists('images/' + self.main_w.chart_view.series.name() + str(number) + '.png'):
                number += 1
            p.save('images/' + self.main_w.chart_view.series.name() + str(number) + '.png')

    def change_state(self):
        Data.update({Data.active: True if self.cb.checkState() == 2 else False}).where((
                                                                                               Data.name == self.main_w.chart_view.name) & (
                                                                                               Data.Emax == self.main_w.chart_view.name2)).execute()
        print(self.cb.checkState())

    def click_table(self, selected, deselected):
        """
        Функция поиска нажатых ячеек
        """
        # Получение всех нажатых ячеек

        for ix in selected.indexes():
            # print('Row: {0},column:{1}, text:{2}'.format(ix.row(),
            #                                             ix.column(),
            #                                             self.main_w.table_view.table.item(ix.row(),
            #                                                                               ix.column()).text()))
            if ix.column() == 0:
                self.main_w.chart_view.name = self.main_w.table_view.table.item(ix.row(), 1).text()
                self.main_w.chart_view.name2 = self.main_w.table_view.table.item(ix.row(), 2).text()
                self.cb = self.main_w.table_view.table.cellWidget(ix.row(), ix.column())
                self.filename = self.main_w.chart_view.name + self.main_w.chart_view.name2
                self.cb.stateChanged.connect(self.change_state)
                # print(self.main_w.table_view.table.cellWidget(ix.row(), ix.column()).checkState())
            if ix.column() == 1:
                # Передача название строки и название плёнки
                self.main_w.chart_view.name = self.main_w.table_view.table.item(ix.row(), ix.column()).text()
                self.main_w.chart_view.name2 = self.main_w.table_view.table.item(ix.row(), 0).text()
                # Отрисовка ячейки
                self.filename = self.main_w.chart_view.name + self.main_w.chart_view.name2
                self.main_w.chart_view.add_series_otrisovka_graf()
                self.color_update()
                self.main_w.table_view.zapolnenietablici()

            elif ix.column() == 4:
                # Передача название строки, название плёнки и содержание ячейки
                self.filename = self.main_w.chart_view.name + self.main_w.chart_view.name2
                self.main_w.chart_view.name = self.main_w.table_view.table.item(ix.row(), 1).text()
                self.main_w.chart_view.name2 = self.main_w.table_view.table.item(ix.row(), 0).text()
                self.main_w.chart_view.name_dot = self.main_w.table_view.table.item(ix.row(), ix.column()).text()
                # выделение на графике данные, нажатой ячейки
                self.main_w.chart_view.add_series_transpare_proc()
                self.color_update()
                print('its Ph.Umax:{}'.format(self.main_w.table_view.table.item(ix.row(), ix.column()).text()))
                self.main_w.table_view.zapolnenietablici()
            elif ix.column() == 8:
                self.main_w.chart_view.name = self.main_w.table_view.table.item(ix.row(), 1).text()
                self.main_w.chart_view.name2 = self.main_w.table_view.table.item(ix.row(), 0).text()
                self.main_w.chart_view.flag_approx = True
                # Отрисовка ячейки
                self.filename = self.main_w.chart_view.name + self.main_w.chart_view.name2
                self.main_w.chart_view.add_series_otrisovka_graf()
                self.color_update()
                self.main_w.table_view.zapolnenietablici()
            self.main_w.table_view.color_name = []

            # print('Row: {0},column:{1}, text:{2}'.format(ix.row(),
            #                                             ix.column(),
            #                                             self.main_w.table_view.table.item(ix.row(),
            #                                                                               ix.column()).text()))
            break

    #

    def color_update(self):
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
