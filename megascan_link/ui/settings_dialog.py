# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(421, 418)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.connTab = QWidget()
        self.connTab.setObjectName(u"connTab")
        self.gridLayout_2 = QGridLayout(self.connTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.connTab)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.portNumber = QLineEdit(self.connTab)
        self.portNumber.setObjectName(u"portNumber")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portNumber.sizePolicy().hasHeightForWidth())
        self.portNumber.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.portNumber)

        self.timeoutNumber = QLineEdit(self.connTab)
        self.timeoutNumber.setObjectName(u"timeoutNumber")
        sizePolicy.setHeightForWidth(self.timeoutNumber.sizePolicy().hasHeightForWidth())
        self.timeoutNumber.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.timeoutNumber)

        self.label_2 = QLabel(self.connTab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.connTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel{\n"
"	color:rgb(140, 140, 140)\n"
"}")
        self.label_3.setWordWrap(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_3)


        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.connTab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_5 = QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.checkBox_2)


        self.gridLayout_5.addLayout(self.formLayout_3, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.checkBox = QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName(u"checkBox")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.checkBox)


        self.gridLayout_4.addLayout(self.formLayout_2, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_2)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.saveBtn = QPushButton(Dialog)
        self.saveBtn.setObjectName(u"saveBtn")

        self.horizontalLayout.addWidget(self.saveBtn)

        self.cancelBtn = QPushButton(Dialog)
        self.cancelBtn.setObjectName(u"cancelBtn")

        self.horizontalLayout.addWidget(self.cancelBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Megascan Link (Unofficial)", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Port Number:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Timeout (sec)", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Changing port number require a restart of the socket after the current timeout expires (so wait at least the current timeout to use the export on Bridge)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connTab), QCoreApplication.translate("Dialog", u"Connection", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"General", None))
        self.checkBox_2.setText(QCoreApplication.translate("Dialog", u"Create New Graph", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"3D Asset", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"Import LODs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Import", None))
        self.saveBtn.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.cancelBtn.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

