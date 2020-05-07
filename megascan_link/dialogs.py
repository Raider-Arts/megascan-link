from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2 import QtWidgets
from pathlib import Path


class SelectPackageDialog(QtWidgets.QDialog):
    returnValue = QtCore.Signal(object)

    def __init__(self,  packageList, parent=None,):
        super().__init__(parent=parent)
        self.selectedPackages = []
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(QtWidgets.QLabel("Select Packages to import to:")) 
        hLayout = QtWidgets.QHBoxLayout() 
        self.packageWidget = QtWidgets.QListWidget()
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
        okBtn = QtWidgets.QPushButton('Ok')
        okBtn.clicked.connect(lambda: self._returnFromDialog(False))
        cancelBtn = QtWidgets.QPushButton('Cancel')
        cancelBtn.clicked.connect(lambda: self._returnFromDialog(True))
        hLayout.addStretch()
        hLayout.addWidget(okBtn)
        hLayout.addWidget(cancelBtn)
        vLayout.addWidget(self.packageWidget)
        vLayout.addLayout(hLayout)
        self.setLayout(vLayout)

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


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=None)