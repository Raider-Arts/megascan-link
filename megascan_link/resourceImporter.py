import megascan_link.utilities as utilities
import sd
from sd.api.sdresourcefolder import *
from sd.api.sdresourcebitmap import *
from sd.api.sdresourcescene import *

class ResourceImporter(object):

    def _isAlreadyImported(self, name, package):
        for resource in package.getChildrenResources(False): 
            if resource.getIdentifier() == name:
                return True
        return False


    def importFromData(self, data): 
        sdPackageMgr = utilities.getApp().getPackageMgr()
        packages = sdPackageMgr.getPackages()
        package = packages[0] #Change this with a dialog to let the user select the package
        if packages.getSize() != 0:
            parentFolder = None
            for resource in package.getChildrenResources(False): 
                if resource.getIdentifier() == "Resources":
                    parentFolder = resource
            if not parentFolder:
                parentFolder = SDResourceFolder.sNew(package)
                parentFolder.setIdentifier("Resources")
            print("data is type {}".format(type(data)))
            for imprt in data:
                folder = SDResourceFolder.sNew(parentFolder)
                folder.setIdentifier(imprt['name'])
                for component in imprt['components']: 
                    SDResourceBitmap.sNewFromFile(folder, component['path'], EmbedMethod.Linked)
                for mesh in imprt['meshList']:
                    SDResourceScene.sNewFromFile(folder, mesh['path'], EmbedMethod.Linked) 

