# encoding: utf-8

import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import Qt
from datetime import datetime, timedelta
import licence


class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowState(Qt.WindowNoState)
        mainLayout = QtWidgets.QVBoxLayout()
        self.createMessageGroupBox(mainLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                                    QtWidgets.QDialogButtonBox.Cancel
                                                    , self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.cwd =  os.path.join(os.path.dirname(os.path.abspath(__file__)))

        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("沃易智信注册机"))
        self.resize(360,280)

    def get_lic_expr_date(self, sdate):
        span = int(self.licspanEdit.text())
        currentIndex = self.spanUnit.currentIndex()
        if currentIndex == 2:
            return sdate.replace(year = sdate.year+span)
        elif currentIndex == 1:
            return sdate.replace(year=sdate.year+int(span/12), month=sdate.month+int(span%12))
        return sdate + timedelta(days=span)


    def accept(self):
        edate = self.startdate.dateTime().toPyDateTime()

        licence.key_gen(self.macEdit.text(), self.productEdit.currentText(),
                        self.versionEdit.text(),
                        edate, self.licpathEdit.text())
        super(MainWindow, self).accept()

    def reject(self):
        super(MainWindow, self).reject()

    def select_lic_path(self):
        dlg = QtWidgets.QFileDialog(self)
        dlg.setDirectory(self.cwd)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.
        fpath, _ = dlg.getSaveFileName(self, filter=self.tr('Licence Files (*.lic)'i)
        self.licpathEdit.setText(fpath)

    def createMessageGroupBox(self, mlayout):
        macLabel = QtWidgets.QLabel(self.tr("机器码:"))
        self.macEdit = QtWidgets.QLineEdit(licence.get_maccode())

        productLabel = QtWidgets.QLabel(self.tr("产品:"))
        self.productEdit = QtWidgets.QComboBox()
        self.productEdit.addItems(['otsweb', 'scada'])
        self.versionEdit = QtWidgets.QLineEdit('1.0')

        sdateLabel = QtWidgets.QLabel(self.tr("许可到期时间:"))
        self.startdate = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.startdate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')


        licpathLabel = QtWidgets.QLabel(self.tr("许可文件路径:"))
        self.licpathEdit = QtWidgets.QLineEdit()
        self.licpathBtn = QtWidgets.QPushButton()
        self.licpathBtn.clicked.connect(self.select_lic_path)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(macLabel, 0, 0)
        layout.addWidget(self.macEdit, 0, 1)

        layout.addWidget(productLabel, 1, 0)
        layout.addWidget(self.productEdit, 1, 1)
        layout.addWidget(self.versionEdit, 1, 2)

        layout.addWidget(sdateLabel, 2, 0)
        layout.addWidget(self.startdate, 2, 1)

        layout.addWidget(licpathLabel, 3, 0)
        layout.addWidget(self.licpathEdit, 3, 1)
        layout.addWidget(self.licpathBtn, 3, 2)

        mlayout.addLayout(layout)




def main(args):
    app = QtWidgets.QApplication(args)
    dlg = MainWindow()
    dlg.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)


