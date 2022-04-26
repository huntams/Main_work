"""
@authors: Maksim & Konstantin
"""

import os
import sys
import testcsvread
from PyQt5.QtWidgets import QWidget, QDoubleSpinBox, QPushButton, QApplication, QGridLayout, QComboBox, QLineEdit, \
    QFileDialog, QMessageBox, QDesktopWidget

dbdirname = ''


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbdirname = dbdirname

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.qbtn = QPushButton('Загрузить', self)
        self.qbtn.clicked.connect(self.Load_Button)
        grid.addWidget(self.qbtn, 2, 1, 1, 1)
        loadbutton = QPushButton('...', self)
        loadbutton.clicked.connect(self.showLoadDialogDir)
        grid.addWidget(loadbutton, 1, 2, 1, 1)
        self.thicknessBox = QDoubleSpinBox()
        self.thicknessBox.setValue(35.0)
        self.thicknessBox.setRange(0, 270)
        grid.addWidget(self.thicknessBox, 1, 3, 1, 1)
        self.loadingTypeWid = QComboBox()
        self.loadingTypeWid.addItems(['Пуск', 'Плёнка', 'Смесь_NA'])
        self.loadingTypeWid.setCurrentText('Плёнка')
        grid.addWidget(self.loadingTypeWid, 1, 1, 1, 1)
        self.ImyaDirrectory = QLineEdit()
        self.ImyaDirrectory.setText('Выберите дирректорию (...)')
        grid.addWidget(self.ImyaDirrectory, 2, 2, 1, 2)
        #self.setGeometry(300, 300, 600, 400)
        self.setFixedSize(500, 160)
        win = self.frameGeometry()
        pos = QDesktopWidget().availableGeometry().center()
        win.moveCenter(pos)
        self.move(win.topLeft())
        self.setWindowTitle('Загрузка исходных данных')
        self.show()

    def showLoadDialogDir(self):
        self.dbdirname = QFileDialog.getExistingDirectory(self, 'Data Base to Open', os.getcwd())  # ,'/home')
        print(self.dbdirname)
        self.ImyaDirrectory.setText(self.dbdirname)

    def Load_Button(self):
        if self.dbdirname != '':
            testcsvread.fulldirload(self.dbdirname, self.loadingTypeWid.currentIndex(), self.thicknessBox.value())
            self.close()
        else:
            QMessageBox.warning(self, 'Предупреждение', "Укажите путь к данными")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
