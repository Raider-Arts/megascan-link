
import megascan_link
from megascan_link import utilities
from megascan_link import dialogs
import sd
from sd.api.sdresourcefolder import *
from sd.api.sdresourcebitmap import *
from sd.api.sdresourcescene import *
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2 import QtWidgets
from pathlib import Path

class ResourceImporter(object):
    data = None

    def _isAlreadyImported(self, name, package):
        for resource in package.getChildrenResources(False): 
            if resource.getIdentifier() == name:
                return True 
        return False


    def processImportForPacakges(self, packages):
        for package in packages:
            parentFolder = None
            for resource in package.getChildrenResources(False): 
                if resource.getIdentifier() == "Resources":
                    parentFolder = resource
            if not parentFolder:
                parentFolder = SDResourceFolder.sNew(package)
                parentFolder.setIdentifier("Resources")
            for imprt in self.data:
                folder = SDResourceFolder.sNew(parentFolder)
                folder.setIdentifier(imprt['name'])
                for bitmap in imprt['components']: 
                    SDResourceBitmap.sNewFromFile(folder, bitmap['path'], EmbedMethod.Linked)
                for mesh in imprt['meshList']:
                    SDResourceScene.sNewFromFile(folder, mesh['path'], EmbedMethod.Linked)

    def importFromData(self, data):
        self.data = data
        sdPackageMgr = utilities.getApp().getPackageMgr()
        packages = sdPackageMgr.getPackages()
        parentWindow = utilities.getUiManager().getMainWindow()
        if packages.getSize() != 0:
            dialog = dialogs.SelectPackageDialog(packages, parent=parentWindow)
            dialog.returnValue.connect(self.processImportForPacakges)
            dialog.show()
        

