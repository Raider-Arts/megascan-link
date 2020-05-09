"""Module which contains all the dialogs used by the plugin

The dialogs are generated using QtDesigner and are located under /megascan_lin/ui/uiDesign
and then converted to python code using the buildDialogs.py script
"""

import importlib
from pathlib import Path

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

import megascan_link
from megascan_link import config, sockets
from megascan_link.ui import import_dialog, settings_dialog

importlib.reload(settings_dialog)
importlib.reload(import_dialog)

class SelectPackageDialog(QtWidgets.QDialog, import_dialog.Ui_Dialog):
    """Dialogs displayed when an import is requested from Quixel Bridge

    The user can select to which packages import the Megascan Assets or dismiss it
    """
    #: Subscribable signal emitted when the user close the dialog the param is set to the list of the selected packages
    #: 
    #: :type: QtCore.Signal
    returnValue = QtCore.Signal(object)

    def __init__(self,  packageList, parent=None,):
        super().__init__(parent=parent)
        self.setupUi(self)
        #: List of currently selected packages the data value is set to point to the corresponding SDPackage Reference
        #:
        #: :type: List[QtWidgets.QListWidgetItem]
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
        """Internal method used to update the currently selected packages
        """        
        self.selectedPackages.clear()
        packages = self.packageWidget.selectedItems()
        print(self.packageWidget.selectedItems())
        for package in packages:
            self.selectedPackages.append(package.data(Qt.UserRole))
            print(package.data(Qt.UserRole))
    
    def _returnFromDialog(self, isCancel):
        """Internal method used to dismiss the dialog

        :param isCancel: True or False depending if the user clicked *Import* or *Cancel* on the dialog
        :type isCancel: bool
        """        
        if isCancel:
            self.close()
        else:
            self.returnValue.emit(self.selectedPackages)
            self.close()


class SettingsDialog(QtWidgets.QDialog, settings_dialog.Ui_Dialog):
    """Dialog displayed to the user for editing the plugin settingss
    """    

    def __init__(self, socketRef: sockets.SocketThread, parent=None):
        self.config = config.ConfigSettings()
        self.needRestart = False
        self._sockRef = socketRef
        super().__init__(parent=parent)
        self.setupUi(self)
        self.portNumber.setText(self.config.getConfigSetting("Socket", "port"))
        self.portNumber.setValidator(QtGui.QIntValidator(self))
        self.portNumber.textChanged.connect(self._setNeedRestart)
        self.timeoutNumber.setText(self.config.getConfigSetting("Socket", "timeout"))
        self.timeoutNumber.setValidator(QtGui.QIntValidator(0, 60, self))
        self.timeoutNumber.textChanged.connect(self._setNeedRestart)
        self.createGraph.setCheckState(Qt.CheckState.Checked if self.config.checkIfOptionIsSet("General", "createGraph") else Qt.CheckState.Unchecked)
        self.importLODs.setCheckState(Qt.CheckState.Checked if self.config.checkIfOptionIsSet("3D Asset","importLODs") else Qt.CheckState.Unchecked)
        self.saveBtn.pressed.connect(self.saveSettings)
        self.cancelBtn.pressed.connect(lambda: self.close())
    
    def _setNeedRestart(self, changedStr):
        """Internal method to set the need restart flag which is later passed to the socket thread
        when the dialog is closed
        """        
        print("Port or Timeout changed socket need to restart")
        self.needRestart = True

    def saveSettings(self):
        """Saved the changed settings to file then inform the socket thread if it need to restart himself
        """        
        self.config.updateConfigSetting("Socket", "port", self.portNumber.text(), False)
        self.config.updateConfigSetting("Socket", "timeout", self.timeoutNumber.text(), False)
        createGraphState = True if self.createGraph.checkState() == Qt.CheckState.Checked else False
        self.config.updateConfigSetting("General", "creategraph", createGraphState, False)
        importLODsState = True if self.importLODs.checkState() == Qt.CheckState.Checked else False
        self.config.updateConfigSetting("3D Asset", "importLODs", importLODsState, False)
        self.config.flush()
        if self.needRestart:
            self._sockRef.restart()
        self.close()
