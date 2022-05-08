"""
@authors: Maksim & Konstantin
"""

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QGridLayout, QTableWidget, QTableWidgetItem, \
    QCheckBox, QMessageBox, QDesktopWidget
from db_worker import Composition

dbdirname = ''


class Choicer(QWidget):

    def __init__(self):
        super().__init__()
        self.choice_mas = []
        self.initUI()
        self.dbdirname = dbdirname

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.table = QTableWidget(1, 2)  # Создаём таблицу self
        # table.setColumnCount(3)     # Устанавливаем три колонки
        # table.setRowCount(1)        # и одну строку в таблице
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(
            ["Адрес", "Выбор"])
        # # Устанавливаем всплывающие подсказки на заголовки
        # self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")

        # # Устанавливаем выравнивание на заголовки
        # self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        # # заполняем первую строку
        # self.table.setItem(0, 0, QTableWidgetItem("Text in column 1"))

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()
        grid.addWidget(self.table, 1, 1, 1, 1)  # Добавляем таблицу в сетку
        self.qbtn = QPushButton('Загрузить', self)
        self.qbtn.clicked.connect(self.Load_Button)
        grid.addWidget(self.qbtn, 2, 1, 1, 1)
        self.setFixedSize(300, 400)
        win = self.frameGeometry()
        pos = QDesktopWidget().availableGeometry().center()
        win.moveCenter(pos)
        self.move(win.topLeft())
        self.setWindowTitle('Загрузка исходных данных')
        self.show()
        self.zapol()

    def Load_Button(self):
        self.choice_mas = []
        for items in range(self.table.rowCount()):
            if self.table.cellWidget(items, 1).checkState() == 2:
                self.choice_mas.append(self.table.item(items, 0).text())
        if not self.choice_mas:
            QMessageBox.warning(self, 'Предупреждение', "Выберите как минимум один состав")
        else:
            self.close()

    def zapol(self):
        try:
            self.table.setShowGrid(False)
            self.table.setRowCount(len(Composition.select()) / 2)
            for i, izm in enumerate(Composition.select()[::2]):
                self.table.setItem(i, 0, QTableWidgetItem(izm.name_composition))
                self.table.setColumnWidth(0, 180)
                self.table.setCellWidget(i, 1, QCheckBox())
                self.table.setColumnWidth(1, 50)
                self.table.cellWidget(i, 1).setChecked(False)
                self.table.cellWidget(i, 1).setCheckable(True)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка загрузки базы данных, попробуйте загрузить информацию с компьютера")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def test(self):
        self.table.setShowGrid(False)
        self.table.setRowCount(3)
        for i in range(3):
            self.table.setItem(i, 0, QTableWidgetItem('Чжан Сан'))
            self.table.setColumnWidth(0, 180)
            self.table.setCellWidget(i, 1, QCheckBox())
            self.table.setColumnWidth(1, 50)
            self.table.cellWidget(i, 1).setChecked(True)
            self.table.cellWidget(i, 1).setCheckable(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Choicer()
    sys.exit(app.exec_())
