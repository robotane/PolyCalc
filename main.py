#! /usr/bin/env python3
# -*- coding:Utf8 -*-
# (C)John Robotane 10/12/2019 2:30PM
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTextBrowser, QSizePolicy, QToolButton, QLayout, QLineEdit, QLabel, QWidget, QGridLayout, \
    QApplication, QComboBox, QVBoxLayout, QHBoxLayout, QShortcut
from polynomials import Polynomial
import re


# TODO Use Pyparsing or any other parsing module to parse the user input


class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class MyWindow(QWidget):
    # input=None
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initMyWindow()
        self.polynomes = {}

    def initMyWindow(self):
        self.input = QLineEdit()
        # self.input.returnPressed(self.okClicked())
        kpadlayout = QGridLayout()
        kpadwidget = QWidget()
        self.short = QShortcut(QKeySequence("Ctr+M"), self)
        # self.short.connect(self.okClicked())
        # self.setLayout(mygrid)
        labels = [["x", "^", "S", "P", ")"],
                  ["7", "8", "9", "D", "C"],
                  ["4", "5", "6", "*", "/"],
                  ["1", "2", "3", "+", "-"],
                  ["0", ".", "OK", "=", ""]]
        for i in range(5):
            for j in range(5):
                if labels[i][j] == "D":
                    btn = self.createButton(labels[i][j], self.backspaceClicked)
                    kpadlayout.addWidget(btn, i, j)
                    continue
                if labels[i][j] == "S":
                    # btn=self.createButton(labels[i][j],self.swiperClicked)
                    # kpadlayout.addWidget(btn,i,j)
                    self.combobtn = QComboBox()
                    self.combobtn.addItem("Insert")
                    self.combobtn.addItem("Calcul")
                    self.combobtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    kpadlayout.addWidget(self.combobtn, i, j)
                    continue
                if labels[i][j] == "C":
                    btn = self.createButton(labels[i][j], self.clearallClicked)
                    kpadlayout.addWidget(btn, i, j)
                    continue
                if labels[i][j] == "OK":
                    btn = self.createButton(labels[i][j], self.okClicked)
                    kpadlayout.addWidget(btn, i, j)
                    continue
                if labels[i][j] == "=":
                    btn = self.createButton(labels[i][j], self.digitClicked)
                    kpadlayout.addWidget(btn, i, j, 1, j - 1)
                    break
                btn = self.createButton(labels[i][j], self.digitClicked)
                kpadlayout.addWidget(btn, i, j)
        # mainlayout.setSizeConstraint(QLayout.SetFixedSize)
        # kpadlayout.setSizeConstraint(QLayout.SetFixedSize)
        kpadwidget.setLayout(kpadlayout)
        kpadwidget.setFixedSize(400, 300)
        # kpadlayout.closestAcceptableSize(kpadwidget,QSize(100,100))
        mainlayout = QHBoxLayout()
        mainlayout.setStretch(1, 2)
        # mainlayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label_hist = QTextBrowser()
        # self.label_hist.setGeometry(0,0,400,200)
        self.label_hist.setMinimumSize(400, 400)
        vbox = QVBoxLayout()
        vbox.addWidget(self.input)
        vbox.addWidget(self.label_hist)
        kpVbox = QVBoxLayout()
        kpVbox.addWidget(kpadwidget)
        kpVbox.addStretch(1)
        # mainlayout.addWidget(label_pave,0,1)
        # mainlayout.addWidget(self.input,0,0)
        # mainlayout.addWidget(self.label_hist,1,0)
        # mainlayout.addWidget(kpadwidget,1,1)
        # mainlayout.setHorizontalSpacing(10)
        mainlayout.addLayout(vbox)
        mainlayout.addLayout(kpVbox)
        self.input.setFocus()
        # self.connect(self.input, SIGNAL("returnPressed()"), self.okClicked)
        self.setLayout(mainlayout)
        self.show()
        self.setGeometry(100, 100, 600, 300)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Alt:
            self.combobtn.setCurrentIndex((self.combobtn.currentIndex() + 1) % self.combobtn.count())

        # if e.key() == Qt.Key_AltGr:
        #     self.okClicked()

    def clearallClicked(self):
        self.input.setText("")

    def okClicked(self):
        if self.input.text():
            # TODO Remove the two modes and parse the input like this
            # all operations are both inputs and calculation
            # when there is an = sign,the input is stored in the given name
            # f=x+5-7x^3
            # else it is in a genirc name
            # (f + x^8 - 8)*(7x^2-1/3)
            # -->p1 = the result of the calculation

            if self.combobtn.currentText() == "Insert":
                p: Polynomial
                pol_str = self.input.text()
                p = Polynomial(pol_str)

                self.polynomes["P" + str(len(self.polynomes) + 1)] = p
                self.label_hist.append("\nP<sub>" + str(len(self.polynomes)) + "</sub>=" + p.html_str())
            elif self.combobtn.currentText() == "Calcul":
                pol_str = self.input.text()
                pol_str = pol_str.replace("p", "P")
                pat = r"P(\d)*"
                html_pol_str = pol_str
                tmp_str = ""
                poly = []
                pb = pol_str
                # pb=pb.replace("/","//")
                pb = pb.replace("^", "**")
                for match in re.finditer(pat, pol_str):
                    mg = match.group()
                    tmp_str = mg.replace("P", "P<sub>") + "</sub>"
                    html_pol_str = html_pol_str.replace(mg, tmp_str)
                    poly.append(mg)
                    # print(mg,self.polynomes[mg])
                    pb = pb.replace(mg, repr(self.polynomes[mg]))
                # print(poly)
                # print(pb)
                try:
                    p = eval(pb)  # TODO Replace this 'eval' statement with a safer method
                    self.polynomes["P" + str(len(self.polynomes) + 1)] = p
                    self.label_hist.append(
                        "\nP<sub>" + str(len(self.polynomes)) + "</sub>=" + html_pol_str + "=" + p.html_str())
                    # Display the answer in a listview like this
                    # Polynomial name: Typed string
                    #             -> Actual value in the polynomial
                    # for insertion
                    # P1 : 1/2x^3 -1 -1/6
                    #   -> 1/2x^3 -1 -1/6
                    # for calculation
                    # P2 : 2*P1 + 1/3
                    #   -> x^3 -2


                except SyntaxError as ster:
                    print("Une ereurer de syntaxe est survenue!")
                except NameError as ster:
                    print("Une ereurer de nom est survenue!")
                except AttributeError as ster:
                    print("Une ereurer d'atribut est survenue!")
            self.clearallClicked()

    def backspaceClicked(self):
        if self.input.text() != "":
            self.input.setText(self.input.text()[:-1])

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = clickedButton.text()
        self.input.setText(self.input.text() + digitValue)

    def createButton(self, text, member):
        button = Button(text)
        # self.input.setText(self.input.text()+text)
        button.clicked.connect(member)
        return button

    def parseEpression(self, expr):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    frame = MyWindow()
    app.exec_()
