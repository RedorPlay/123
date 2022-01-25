from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.QtWidgets import QApplication, QPushButton
from main_window import Ui_MainWindow
from snoska import Ui_MainWindow_snoska
import sys


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.money_1 = 1000
        self.true_2 = 0
        self.true_3 = 0
        self.money_2 = 1000
        self.price = {'1': 400, '2': 300, '3': 100, '4': 100, '5': 100, '6': 100, '7': 100, '8': 100, '9': 100, '@': 100}
        self.a = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
        self.pushButton_3.clicked.connect(self.add_1)
        self.pushButton_4.clicked.connect(self.add_2)
        self.pushButton.clicked.connect(self.generate)
        self.pushButton_2.clicked.connect(self.snoska)

    def add_1(self):
        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_3.text() != '' \
                and int(self.lineEdit.text()) < 5 and self.money_1 >= self.price[self.lineEdit_3.text()]:
            self.a[int(self.lineEdit_2.text())][int(self.lineEdit.text())] = self.lineEdit_3.text()
            self.money_1 -= self.price[self.lineEdit_3.text()]
            self.label_12.setText(f"{self.money_1} монет")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')

    def add_2(self):
        if self.lineEdit_4.text() != '' and self.lineEdit_5.text() != '' and self.lineEdit_6.text() != '' \
                and int(self.lineEdit_4.text()) > 5 and self.money_2 >= self.price[self.lineEdit_6.text()]:
            self.a[int(self.lineEdit_5.text())][int(self.lineEdit_4.text())] = self.lineEdit_6.text()
            self.money_2 -= self.price[self.lineEdit_6.text()]
            self.label_13.setText(f"{self.money_2} монет")
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')

    def generate(self):
        f = open("data/map.txt", "w").close()
        f = open('data/map.txt', 'w')
        if self.lineEdit_7.text() == '2':
            self.true_3 = 1
            for i in range(len(self.a)):
                for j in range(len(self.a[i])):
                    if self.a[i][j] == '.':
                        self.a[i][j] = ','
        for i in range(len(self.a)):
            print(''.join(self.a[i]), file=f)
        self.true_2 = 1
        self.close()

    def snoska(self):
        self.w = Snoska()
        self.w.show()


class Snoska(QMainWindow, Ui_MainWindow_snoska):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.close()
