
import configparser
import importlib
import logging
import os
import time
from queue import Queue
# import ptvsd
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
# Designer imports
import sd
# plugin module imports
import megascan_link
from megascan_link import config, dialogs
from megascan_link import icon as mIcon
from megascan_link import resourceImporter as resImporter
from megascan_link import sockets, ui, utilities

# Realod the modules when in dev mode
importlib.reload(megascan_link)
importlib.reload(sockets)
importlib.reload(utilities)
importlib.reload(resImporter)
importlib.reload(config)
importlib.reload(dialogs)
importlib.reload(ui)
importlib.reload(mIcon)

class Data(object):
    """"Dataclass" for storing plugin variables
    So the python garbage collector doesn't dispose them
    """    
    socketThread = None
    toolbarAction = None
    toolbar = None
    settingDialog = None

def openSettings():
    """function for setup and open the SettingsDialog
    """    
    uiMgr = utilities.getUiManager()  
    mainWindow = uiMgr.getMainWindow()
    Data.settingDialog = dialogs.SettingsDialog(Data.socketThread,parent=mainWindow)
    Data.settingDialog.show()

def createToolBarAction():
    """function for create and setup the Megascan top toolbar icon for opening the plugin settings
    """ 
    uiMgr = utilities.getUiManager()  
    mainWindow = uiMgr.getMainWindow()
    toolbars = mainWindow.findChildren(QtWidgets.QToolBar)
    # ===================================================
    # Very hackish way to insert the Action on the top toolbar of Substance Designer
    for toolbar in toolbars:
        if mainWindow.toolBarArea(toolbar) == Qt.ToolBarArea.TopToolBarArea:
            Data.toolbar = toolbar
            icon = QtGui.QIcon(mIcon.MegascanIcon.path)
            Data.toolbarAction = toolbar.addAction(icon, None)
            Data.toolbar = Data.toolbarAction.parentWidget()
            break
    Data.toolbarAction.triggered.connect(openSettings)


def initializeSDPlugin():
    """**Main entry point of the plugin**
    """
	# Debug Stub
    # ptvsd.enable_attach()
    # ptvsd.wait_for_attach()
    # ptvsd.break_into_debugger()

    # Set up initial config proprieties
    conf = config.ConfigSettings()
    initConfig = configparser.ConfigParser()
    initConfig["Socket"] = {"port": 24981,
                            "timeout": 5}
    conf.setUpInitialConfig(initConfig)

    uiMgr = utilities.getUiManager()  
    # Get the main window to set the thread parent of
    mainWindow = uiMgr.getMainWindow()

    # ===================================================
    # Create and start the listening socket thread
    # Set up and link the resource importer class
    # Link the recaiver to the socket thread for receiving and processing the incoming data
    Data.socketThread = sockets.SocketThread(parent=mainWindow)
    importer = resImporter.ResourceImporter()
    receiver = sockets.SocketReceiver(parent=mainWindow,importer=importer)
    print(Data.socketThread,receiver)
    Data.socketThread.onDataReceived.connect(receiver.onReceivedData, Qt.QueuedConnection)
    Data.socketThread.start()


def uninitializeSDPlugin():
    """**Exit point of the plugin**
    """    
    # ===================================================
    # Clear the socket and remove the Action for the top toolbar of Substance Designer
    Data.socketThread.close()
    Data.toolbar.removeAction(Data.toolbarAction)
