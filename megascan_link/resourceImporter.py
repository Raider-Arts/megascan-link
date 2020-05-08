
import sd
from sd.api.sdpackage import SDPackage
from sd.api.sdarray import SDArray
from sd.api.sdtexture import SDTexture
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sdresourcebitmap import SDResourceBitmap
from sd.ui.graphgrid import GraphGrid
from sd.api.sdusage import SDUsage
from sd.api.sdvaluearray import SDValueArray
from sd.api.sdtypeusage import SDTypeUsage
from sd.api.sdvalueusage import SDValueUsage
from sd.api.sdvaluestring import SDValueString
from sd.api.sdbasetypes import *
import megascan_link
from megascan_link import utilities
from megascan_link import dialogs
from megascan_link import config
from megascan_link import icon as mIcon
from sd.api.sdresourcefolder import *
from sd.api.sdresourcebitmap import *
from sd.api.sdresourcescene import *
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2 import QtWidgets
from pathlib import Path
from enum import Enum
from typing import List

class BitmapType(Enum):
    albedo = SDUsage.sNew('baseColor', 'RGBA', 'sRGB')
    roughness = SDUsage.sNew('roughness', 'R', 'Linear')
    metalness = SDUsage.sNew('metallic', 'R', 'Linear')
    displacement = SDUsage.sNew('height', 'R', 'Linear')
    normal = SDUsage.sNew('normal', 'RGBA', 'Linear')
    cavity = SDUsage.sNew('cavity', 'R', 'Linear')
    diffuse = SDUsage.sNew('diffuse', 'RGBA', 'sRGB')
    bump = SDUsage.sNew('bump', 'RGBA', 'Linear')
    gloss = SDUsage.sNew('glossiness', 'RGBA', 'Linear')
    specular = SDUsage.sNew('specular', 'RGBA', 'Linear')

class MegascanBitmap(object):
    def __init__(self, resource: SDResourceBitmap, path: str, usage: str, name = None):
        self.path = path
        self.resource = resource
        self.usage = BitmapType[usage]
        if not name:
            self.name = Path(self.path).stem
        else:
            self.name = Path(name).stem
    
    def __str__(self):
        return "MegascanBitmap(\n\t usage: {} \n\t resource: {} \n\t name: {} \n\t path: {} \n)".format(self.usage, self.resource, self.name, self.path)
    
    def getUsageArray(self):
        sdValueArray = SDValueArray.sNew(SDTypeUsage.sNew(), 0)
        sdValueUsage = SDValueUsage.sNew(self.usage.value)
        sdValueArray.pushBack(sdValueUsage)
        return sdValueArray

class ResourceImporter(object):
    data = None

    def _isAlreadyImported(self, name, package):
        for resource in package.getChildrenResources(False): 
            if resource.getIdentifier() == name:
                return True 
        return False

    def createGraphWith(self, graphname: str, bitmaps: List[MegascanBitmap], package: SDPackage):
        cGridSize = GraphGrid.sGetFirstLevelSize()
        # =========================================================================
        # Create a new Substance Compositing Graph in this package
        megascanCompGraph = SDSBSCompGraph.sNew(package)
        megascanCompGraph.setIdentifier(graphname)
        print(mIcon.MegascanIcon.path) 
        megascanCompGraph.setIcon(SDTexture.sFromFile(mIcon.MegascanIcon.path)) 

        for i, image in enumerate(reversed(bitmaps)): 
            # Create the Bitmap Instance Node
            megascanNodeBitmap = megascanCompGraph.newInstanceNode(image.resource)
            megascanNodeBitmap.setPosition(float2(-2 * cGridSize, -(cGridSize + cGridSize/2) * i))
            # Crete the output node and set its usage based on the bitmap usage imported from Megascan
            megascanNodeOut = megascanCompGraph.newNode('sbs::compositing::output') 
            megascanNodeOut.setAnnotationPropertyValueFromId('usages', image.getUsageArray())
            megascanNodeOut.setAnnotationPropertyValueFromId('identifier', SDValueString.sNew(image.usage.name.capitalize())) 
            megascanNodeOut.setPosition(float2(-0.5 * cGridSize, -(cGridSize + cGridSize/2) * i))
            # Perform the connection
            megascanNodeBitmap.newPropertyConnectionFromId('unique_filter_output', megascanNodeOut, 'inputNodeOutput')


    def processImportForPacakges(self, packages):
        conf = config.ConfigSettings()
        for package in packages:
            parentFolder = None
            for resource in package.getChildrenResources(False): 
                if resource.getIdentifier() == "Resources":
                    parentFolder = resource
            if not parentFolder:
                parentFolder = SDResourceFolder.sNew(package)
                parentFolder.setIdentifier("Resources")
            for imprt in self.data:
                bitmaps = []
                folder = SDResourceFolder.sNew(parentFolder)
                folder.setIdentifier(imprt['name'])
                for bitmap in imprt['components']:
                    bitmapResource = SDResourceBitmap.sNewFromFile(folder, bitmap['path'], EmbedMethod.Linked)
                    bitmaps.append(MegascanBitmap(bitmapResource, bitmap['path'], bitmap["type"], bitmap['nameOverride']))
                for mesh in imprt['meshList']:
                    SDResourceScene.sNewFromFile(folder, mesh['path'], EmbedMethod.Linked)
                if conf.checkIfOptionIsSet("General","createGraph"):
                    self.createGraphWith(imprt['name'],bitmaps,package)

    def importFromData(self, data):
        self.data = data
        sdPackageMgr = utilities.getApp().getPackageMgr()
        packages = sdPackageMgr.getUserPackages()
        parentWindow = utilities.getUiManager().getMainWindow()
        if packages.getSize() != 0:
            dialog = dialogs.SelectPackageDialog(packages, parent=parentWindow)
            dialog.returnValue.connect(self.processImportForPacakges)
            dialog.show()
        

