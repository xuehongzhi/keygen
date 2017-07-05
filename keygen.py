# encoding: utf-8

import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import Qt
from datetime import datetime, timedelta
import licence, keygen_rc


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
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(self.tr('生成'))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.tr('退出'))
        self.buttonBox.rejected.connect(self.reject)
        self.cwd =  os.path.join(os.path.dirname(os.path.abspath(__file__)))

        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("沃易智信注册机"))
        self.setWindowIcon(QtGui.QIcon(':/images/app.ico'))
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
                        edate, self.licpathEdit.text(),
                        **{'edition':self.editionEdit.currentText()})
        super(MainWindow, self).accept()

    def reject(self):
        super(MainWindow, self).reject()

    def select_lic_path(self):
        fpath = os.path.join(self.cwd, '%s-%s' %(self.productEdit.currentText(), self.versionEdit.text()))
        fpath, _ = QtWidgets.QFileDialog.getSaveFileName(self, directory=fpath,
                                                         filter=self.tr('Licence Files (*.lic)'))
        self.licpathEdit.setText(fpath)

    def createMessageGroupBox(self, mlayout):
        macLabel = QtWidgets.QLabel(self.tr("机器码:"))
        self.macEdit = QtWidgets.QLineEdit(licence.get_maccode())

        productLabel = QtWidgets.QLabel(self.tr("产品名称:"))
        self.productEdit = QtWidgets.QComboBox()
        self.productEdit.addItems(['otsweb', 'scada'])

        versionLabel = QtWidgets.QLabel(self.tr("产品版本:"))
        self.versionEdit = QtWidgets.QLineEdit('1.0')

        editionLabel = QtWidgets.QLabel(self.tr("产品edition:"))
        self.editionEdit = QtWidgets.QComboBox()
        self.editionEdit.addItems(['标准版', '企业版'])

        sdateLabel = QtWidgets.QLabel(self.tr("许可到期时间:"))
        self.startdate = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.startdate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')


        licpathLabel = QtWidgets.QLabel(self.tr("许可文件路径:"))
        self.licpathEdit = QtWidgets.QLineEdit()
        self.licpathBtn = QtWidgets.QPushButton()
        self.licpathBtn.clicked.connect(self.select_lic_path)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(macLabel, 0, 0)
        layout.addWidget(self.macEdit, 0, 1, 1, 2)

        layout.addWidget(productLabel, 1, 0)
        layout.addWidget(self.productEdit, 1, 1, 1, 2)

        layout.addWidget(versionLabel, 2, 0)
        layout.addWidget(self.versionEdit, 2, 1, 1, 2)

        layout.addWidget(editionLabel, 3, 0)
        layout.addWidget(self.editionEdit, 3, 1, 1, 2)

        layout.addWidget(sdateLabel, 4, 0)
        layout.addWidget(self.startdate, 4, 1, 1, 2)

        layout.addWidget(licpathLabel, 5, 0)
        layout.addWidget(self.licpathEdit, 5, 1)
        layout.addWidget(self.licpathBtn, 5, 2)

        mlayout.addLayout(layout)



def main(args):
    app = QtWidgets.QApplication(args)
    dlg = MainWindow()
    dlg.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)


