from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2 import QtWidgets
from pathlib import Path
import megascan_link
from megascan_link import config
from megascan_link.ui import settings_dialog
from megascan_link.ui import import_dialog


class SelectPackageDialog(QtWidgets.QDialog, import_dialog.Ui_Dialog):
    returnValue = QtCore.Signal(object)

    def __init__(self,  packageList, parent=None,):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.selectedPackages = []
        self.packageWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.packageWidget.itemSelectionChanged.connect(self._getSelected)

        for package in packageList:
            name = package.getFilePath()
            if not name:
                name = "Unsaved Package*" 
            else:
                name = Path(name).stem
            listItem = QtWidgets.QListWidgetItem(name)
            listItem.setData(Qt.UserRole, package)
            self.packageWidget.addItem(listItem)

        self.okBtn.clicked.connect(lambda: self._returnFromDialog(False))
        self.cancelBtn.clicked.connect(lambda: self._returnFromDialog(True))

    def _getSelected(self):
        self.selectedPackages.clear()
        packages = self.packageWidget.selectedItems()
        print(self.packageWidget.selectedItems())
        for package in packages:
            self.selectedPackages.append(package.data(Qt.UserRole))
            print(package.data(Qt.UserRole))
    
    def _returnFromDialog(self, isCancel):
        if isCancel:
            self.close()
        else:
            self.returnValue.emit(self.selectedPackages)
            self.close()


class SettingsDialog(QtWidgets.QDialog, settings_dialog.Ui_Dialog):

    def __init__(self, parent=None):
        self.config = config.ConfigSettings()
        super().__init__(parent=parent)
        self.setupUi(self)
        self.portNumber.setText(self.config.getConfigSetting("Socket", "port"))
        self.portNumber.setValidator(QtGui.QIntValidator(self))
        self.timeoutNumber.setText(self.config.getConfigSetting("Socket", "timeout"))
        self.timeoutNumber.setValidator(QtGui.QIntValidator(0,60,self))