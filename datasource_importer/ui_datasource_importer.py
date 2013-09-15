# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_datasource_importer.ui'
#
# Created: Sun Sep 15 12:37:13 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_datasource_importer(object):
    def setupUi(self, datasource_importer):
        datasource_importer.setObjectName(_fromUtf8("datasource_importer"))
        datasource_importer.resize(500, 300)
        self.verticalLayout = QtGui.QVBoxLayout(datasource_importer)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(datasource_importer)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tblDatasources = QtGui.QTableWidget(datasource_importer)
        self.tblDatasources.setObjectName(_fromUtf8("tblDatasources"))
        self.tblDatasources.setColumnCount(3)
        self.tblDatasources.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblDatasources.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblDatasources.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblDatasources.setHorizontalHeaderItem(2, item)
        self.tblDatasources.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tblDatasources)
        self.chkSelectAll = QtGui.QCheckBox(datasource_importer)
        self.chkSelectAll.setObjectName(_fromUtf8("chkSelectAll"))
        self.verticalLayout.addWidget(self.chkSelectAll)
        self.buttonBox = QtGui.QDialogButtonBox(datasource_importer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(datasource_importer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), datasource_importer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), datasource_importer.reject)
        QtCore.QMetaObject.connectSlotsByName(datasource_importer)

    def retranslateUi(self, datasource_importer):
        datasource_importer.setWindowTitle(_translate("datasource_importer", "Datasource Importer", None))
        self.label.setText(_translate("datasource_importer", "Select datasources to import to your local settings", None))
        item = self.tblDatasources.horizontalHeaderItem(0)
        item.setText(_translate("datasource_importer", "Suggested Name", None))
        item = self.tblDatasources.horizontalHeaderItem(1)
        item.setText(_translate("datasource_importer", "Type", None))
        item = self.tblDatasources.horizontalHeaderItem(2)
        item.setText(_translate("datasource_importer", "Layer", None))
        self.chkSelectAll.setText(_translate("datasource_importer", "Select all", None))

