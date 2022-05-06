"""
@authors: Maksim & Konstantin
"""

import sys

from PyQt5 import QtGui

import testcsvread
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QGridLayout, QComboBox, QLineEdit, QFileDialog, \
    QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox
from PyQt5.QtCore import QSize
# DefaultDataList = [[True, "all 001", 2.1, 10, 0.01, 1, 8, 3, ""], [False, "all 002", 4.1, 10, 0.03, 1, 8, 3, ""]]
from db_worker import Data, Composition


class Tablica(QWidget):
    def __init__(self):
        super().__init__()
        self.color_name = []
        grid = QGridLayout()
        self.setLayout(grid)

        self.setMinimumSize(QSize(640, 120))  # Устанавливаем размеры
        self.setWindowTitle("Работа с QTableWidget")  # Устанавливаем заголовок окна

        self.table = QTableWidget(1, 10)  # Создаём таблицу self
        # table.setColumnCount(3)     # Устанавливаем три колонки
        # table.setRowCount(1)        # и одну строку в таблице
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(
            ["", "Адрес", "E(упр.)", "dt imp", "Ph. U(max)", "t on", "t off", "t max", "Аппроксимация", "Особенности"])
        # # Устанавливаем всплывающие подсказки на заголовки
        # self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")

        # # Устанавливаем выравнивание на заголовки
        # self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        # # заполняем первую строку
        # self.table.setItem(0, 0, QTableWidgetItem("Text in column 1"))

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        grid.addWidget(QLabel("Данные"), 0, 0, 1, 1)
        grid.addWidget(self.table, 1, 0, 2, 4)  # Добавляем таблицу в сетку

        qbtn = QPushButton('Заполнить', self)
        qbtn.clicked.connect(self.zapolnenietablici)
        grid.addWidget(qbtn, 0, 1, 1, 1)

        plot_btn = QPushButton('Отрисовать сигналы', self)
        plot_btn.clicked.connect(self.Plot_Data_Eimp_Uph)
        grid.addWidget(plot_btn, 0, 2, 1, 1)

        plot_btn2 = QPushButton('Отрисовать вычисленное', self)
        plot_btn2.clicked.connect(self.Plot_TimeAndPhoto)
        grid.addWidget(plot_btn2, 0, 3, 1, 1)

    def set_color(self, color_name):
        self.color_name = color_name

    def zapolnenietablici(self):
        try:
            print(self.color_name)
            print(self.table.rowCount())
            peremennya = '#209fdf'
            self.table.setRowCount(len(Data.select()))
            # self.table.setItem()
            for i, izm in enumerate(Data.select()):
                self.table.setItem(i, 0, QTableWidgetItem(izm.membrane.composition.name_composition))
                self.table.setColumnWidth(0, 70)
                self.table.setCellWidget(i, 0, QCheckBox())
                self.table.cellWidget(i, 0).setChecked(izm.active)
                self.table.setColumnWidth(0, 180)
                self.table.setItem(i, 1, QTableWidgetItem(izm.name))
                self.table.setColumnWidth(1, 70)
                self.table.setItem(i, 2, QTableWidgetItem("{:.1f}".format(izm.Emax)))
                self.table.setColumnWidth(2, 50)
                self.table.setItem(i, 4, QTableWidgetItem("{:.3f}".format(izm.Umax)))
                self.table.setColumnWidth(4, 70)
                self.table.setItem(i, 3, QTableWidgetItem("{:.1f}".format(izm.dTimp)))
                self.table.setColumnWidth(3, 50)
                self.table.setItem(i, 5, QTableWidgetItem("{:.1f}".format(izm.dTph_On)))
                # self.table.item(i, 5).setBackground(QtGui.QColor(peremennya))
                # self.table.item(i, 5).setStyleSheet('background:'+self.color_name)
                self.table.setColumnWidth(5, 40)
                self.table.setItem(i, 6, QTableWidgetItem("{:.1f}".format(izm.dTph_Off)))
                self.table.setColumnWidth(6, 40)
                self.table.setItem(i, 7, QTableWidgetItem("{:.1f}".format(izm.dTph_max)))
                self.table.setColumnWidth(7, 40)
                for index in range(1, len(self.color_name)):
                    if self.color_name[index] == self.table.item(i, 0).text():
                        if len(self.color_name) % 4 == 0 and self.color_name[index - 2] != self.table.item(i, 0).text():
                            self.table.item(i, 5).setBackground(QtGui.QColor(self.color_name[index - 3]))
                            self.table.item(i, 6).setBackground(QtGui.QColor(self.color_name[index - 2]))
                            self.table.item(i, 7).setBackground(QtGui.QColor(self.color_name[index - 1]))
                        else:
                            self.table.item(i, 4).setBackground(QtGui.QColor(self.color_name[index - 1]))
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка загрузки базы данных, попробуйте загрузить информацию с компьютера")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def Plot_Data_Eimp_Uph(self):
        testcsvread.otrisovkagraf_mod()

    def Plot_TimeAndPhoto(self):
        testcsvread.plot_time_proc()
        testcsvread.plot_transpare_proc()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    testcsvread.fulldirload()
    tb = Tablica()
    tb.show()
    sys.exit(app.exec())
