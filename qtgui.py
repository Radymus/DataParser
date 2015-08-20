# -*- coding: utf-8 -*-

__author__ = "Radim Spigel"
__version__ = "1.0"

import sys
from PySide import *
from PySide.QtCore import *
from PySide.QtGui import *
from dataparser import DataParser


class QTGUI(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(453, 294)
        MainWindow.setFixedSize(453, 300)
        self.fname = None
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 421, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.allowGraphs = QCheckBox(self.formLayoutWidget)
        self.allowGraphs.setEnabled(True)
        self.allowGraphs.setObjectName("allowGraphs")
        self.verticalLayout.addWidget(self.allowGraphs)
        self.separateGraphs = QCheckBox(self.formLayoutWidget)
        self.separateGraphs.setObjectName("separateGraphs")
        self.verticalLayout.addWidget(self.separateGraphs)
        self.allowStatistics = QCheckBox(self.formLayoutWidget)
        self.allowStatistics.setObjectName("allowStatistics")
        self.allowGraphs.setChecked(True)
        self.allowStatistics.setChecked(True)
        self.verticalLayout.addWidget(self.allowStatistics)
        self.csvReport = QCheckBox(self.formLayoutWidget)
        self.csvReport.setObjectName("csvReport")
        self.verticalLayout.addWidget(self.csvReport)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileChooseBtn = QPushButton(self.formLayoutWidget)
        self.fileChooseBtn.setObjectName("fileChooseBtn")
        self.fileChooseBtn.clicked.connect(self.select_file)
        self.horizontalLayout.addWidget(self.fileChooseBtn)
        self.analyzeBtn = QPushButton(self.formLayoutWidget)
        self.analyzeBtn.setObjectName("analyzeBtn")
        self.analyzeBtn.clicked.connect(self.analyze)
        self.horizontalLayout.addWidget(self.analyzeBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.regexLabel = QLabel(self.formLayoutWidget)
        self.regexLabel.setObjectName("regexLabel")
        self.verticalLayout_2.addWidget(self.regexLabel)
        self.regexTextField = QTextEdit(self.formLayoutWidget)
        self.regexTextField.setObjectName("regexTextField")
        self.regexTextField.setText(u"o: ([\d\.]+);t: ([\d\.]+);r: ([\d\.]+);d: ([\d\.]+);f: ([\w\.\+]+)")
        self.verticalLayout_2.addWidget(self.regexTextField)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 453, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Parser {0}".format(__version__)))
        self.allowGraphs.setText(_translate("MainWindow", "allow graph"))
        self.separateGraphs.setText(_translate("MainWindow", "separate graphs"))
        self.allowStatistics.setText(_translate("MainWindow", "statistics"))
        self.csvReport.setText(_translate("MainWindow", "csv report"))
        self.fileChooseBtn.setText(_translate("MainWindow", "choose file"))
        self.analyzeBtn.setText(_translate("MainWindow", "analyze"))
        self.regexLabel.setText(_translate("MainWindow", "Insert REGEXP for parsing file:"))

    def analyze(self):
        if self.fname is None:
            print "File is not setted."
            return
        datagetter = DataParser(self.fname[0])
        if self.regexTextField.toPlainText() is None:
            print "Regexp is not setted."
            return
        datagetter.init_regex(self.regexTextField.toPlainText())
        datagetter.filled_data()
        if self.allowStatistics.isChecked():
            datagetter.print_statistics()
        if self.csvReport.isChecked():
            datagetter.save_to_csv()
        if self.allowGraphs.isChecked():
            datagetter.print_graphs(self.separateGraphs.isChecked())

    def select_file(self):
        self.fname = QFileDialog.getOpenFileName(QDialog(), 'Open File', '.')


def qt_main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    ui = QTGUI()
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
