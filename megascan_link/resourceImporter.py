"""Contains classes to import the data from Quixel Bridge to Substance Designer
"""
from enum import Enum
from pathlib import Path
from typing import List
from logging import DEBUG

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

import megascan_link
import sd
from megascan_link import config, dialogs, log
from megascan_link import icon as mIcon
from megascan_link import utilities
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sdarray import SDArray
from sd.api.sdbasetypes import *
from sd.api.sdpackage import SDPackage
from sd.api.sdresourcebitmap import *
from sd.api.sdresourcebitmap import SDResourceBitmap
from sd.api.sdresourcefolder import *
from sd.api.sdresourcescene import *
from sd.api.sdtexture import SDTexture
from sd.api.sdtypeusage import SDTypeUsage
from sd.api.sdusage import SDUsage
from sd.api.sdvaluearray import SDValueArray
from sd.api.sdvaluestring import SDValueString
from sd.api.sdvalueusage import SDValueUsage
from sd.ui.graphgrid import GraphGrid

class BitmapType(Enum):
    """Enum class used to have a quick access to the corrensponding SDUsage
    Since the data from Quixel Bridge comes as a string we can get the corresponding SDUsage simply 
    using BitmapType[str]
    """
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
    ao = SDUsage.sNew('ambientOcclusion', 'R', 'Linear')

class MegascanBitmap(object):
    """Wrapper class composed of the data coming from Quixel Bridge and the corrispective SDResourceBitmap
    """    
    def __init__(self, resource: SDResourceBitmap, path: str, usage: str, name=None):
        """ MegascanBitmap Constructor
        :param resource: The instanced SDResourceBitmap
        :type resource: SDResourceBitmap
        :param path: the respective path of the texture
        :type path: str
        :param usage: the texture usage 
        :type usage: str
        :param name: the name override, defaults to None
        :type name: [type], optional
        """        
        self.path = path
        self.resource = resource
        self.usage = BitmapType[usage]
        if not name:
            self.name = Path(self.path).stem
        else:
            self.name = Path(name).stem
    
    def __str__(self):
        return "MegascanBitmap(\n\t usage: {} \n\t resource: {} \n\t name: {} \n\t path: {} \n)".format(self.usage, self.resource, self.name, self.path)
    
    def getUsageArray(self) -> SDValueArray:
        """Method returning an SDValueArray with the usage of the texture

        :return: SDValueArray with the usage of the texture
        :rtype: SDValueArray
        """        
        sdValueArray = SDValueArray.sNew(SDTypeUsage.sNew(), 0)
        sdValueUsage = SDValueUsage.sNew(self.usage.value)
        sdValueArray.pushBack(sdValueUsage)
        return sdValueArray

class ResourceImporter(QtCore.QObject):
    """Class responsible of importing to Substance Designer all the meshes/bitmaps/data contained
    in the payload from Quixel Bridge
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    #: Current data payload being processed
    data = None

    def _isAlreadyImported(self, name: str, package: SDPackage) -> bool:
        """Check if a Megascan asset is already imported by looking in all
        the package children 

        :param name: the Identifier to search for
        :type name: str
        :param package: the package to search
        :type package: SDPackage
        :return: True if found False elsewhere
        :rtype: bool
        """        
        for resource in package.getChildrenResources(False): 
            if resource.getIdentifier() == name:
                return True 
        return False

    def createGraphWith(self, graphname: str, bitmaps: List[MegascanBitmap], package: SDPackage):
        """Create a graph in the specified package using the specified bitmaps creating their respective outputs and finalally linking them
        as a bonus we set the graph icon to the Megascan Logo :)

        :param graphname: name of the new graph
        :type graphname: str
        :param bitmaps: List of MegascanBitmap to use in the graph
        :type bitmaps: List[MegascanBitmap]
        :param package: the package reference where to create the graph
        :type package: SDPackage
        """        

        cGridSize = GraphGrid.sGetFirstLevelSize()
        # =========================================================================
        # Create a new Substance Compositing Graph in this package
        megascanCompGraph = SDSBSCompGraph.sNew(package)
        megascanCompGraph.setIdentifier(graphname)
        megascanCompGraph.setIcon(SDTexture.sFromFile(mIcon.MegascanIcon.path)) 

        for i, image in enumerate(bitmaps): 
            # Create the Bitmap Instance Node
            megascanNodeBitmap = megascanCompGraph.newInstanceNode(image.resource)
            megascanNodeBitmap.setPosition(float2(-2 * cGridSize, (cGridSize + cGridSize/2) * i))
            # Crete the output node and set its usage based on the bitmap usage imported from Megascan
            megascanNodeOut = megascanCompGraph.newNode('sbs::compositing::output') 
            megascanNodeOut.setAnnotationPropertyValueFromId('usages', image.getUsageArray())
            megascanNodeOut.setAnnotationPropertyValueFromId('identifier', SDValueString.sNew(image.usage.name.capitalize())) 
            megascanNodeOut.setPosition(float2(-0.5 * cGridSize, (cGridSize + cGridSize/2) * i))
            # Perform the connection
            megascanNodeBitmap.newPropertyConnectionFromId('unique_filter_output', megascanNodeOut, 'inputNodeOutput')


    def processImportForPacakges(self, packages):
        """this is the actual method that performs the bitmaps/meshes import and graph creation tasks
        it does it for every package that the user selected
        this method uses the class attribute data and clears it when done and look 
        up for the settings from the configuration file

        :param packages: List of SDPackage where to import the currently processing data
        :type packages: List[SDPackage]
        """
        if not self.data:
            return
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
                if conf.checkIfOptionIsSet("3D Asset", "importLODs"):
                    for lod in imprt['lodList']:
                        SDResourceScene.sNewFromFile(folder, lod['path'], EmbedMethod.Linked)
                if conf.checkIfOptionIsSet("General","createGraph"):
                    self.createGraphWith(imprt['name'],bitmaps,package)
        self.data = None

    def importFromData(self, data):
        """**Entry point** for the data coming from the socked thread

        :param data: Json Quixel Bridge data
        :type data: List[dict]
        """
        self.data = data
        log.LoggerLink.Log(data, DEBUG)
        sdPackageMgr = utilities.getApp().getPackageMgr()
        packages = sdPackageMgr.getUserPackages()
        parentWindow = utilities.getUiManager().getMainWindow()
        if packages.getSize() != 0:
            dialog = dialogs.SelectPackageDialog(packages, parent=parentWindow)
            dialog.returnValue.connect(self.processImportForPacakges)
            dialog.show()
