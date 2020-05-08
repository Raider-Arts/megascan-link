
# Designer imports
import sd
import os
import time
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import configparser
from queue import Queue

import megascan_link
from megascan_link import socket,config,utilities,dialogs,ui
from megascan_link import resourceImporter as resImporter
import importlib
importlib.reload(socket)
importlib.reload(utilities)
importlib.reload(resImporter)
importlib.reload(config)
importlib.reload(dialogs)
importlib.reload(ui)
import ptvsd

class Data(object):
    socketThread = None
    toolbarAction = None
    toolbar = None
    settingDialog = None

def getIcon():
    return os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'megascan_logo.png')

def openSettings():
    uiMgr = utilities.getUiManager()  
    mainWindow = uiMgr.getMainWindow()
    Data.settingDialog = dialogs.SettingsDialog(Data.socketThread,parent=mainWindow)
    Data.settingDialog.show()

# Plugin entry points.
#
def initializeSDPlugin():
	# Debug Studd
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
    toolbars = mainWindow.findChildren(QtWidgets.QToolBar)

    for toolbar in toolbars:
        if mainWindow.toolBarArea(toolbar) == Qt.ToolBarArea.TopToolBarArea:
            Data.toolbar = toolbar
            icon = QtGui.QIcon(getIcon())
            Data.toolbarAction = toolbar.addAction(icon, None)
            Data.toolbar = Data.toolbarAction.parentWidget()
            break
    Data.toolbarAction.triggered.connect(openSettings)

    Data.socketThread = socket.SocketThread(parent=mainWindow)
    importer = resImporter.ResourceImporter()
    receiver = socket.SocketReceiver(parent=mainWindow,importer=importer)
    print(Data.socketThread,receiver)
    Data.socketThread.onDataReceived.connect(receiver.onReceivedData, Qt.QueuedConnection)
    Data.socketThread.start()


def uninitializeSDPlugin():
    #stopping socket
    Data.socketThread.close()
    Data.toolbar.removeAction(Data.toolbarAction)
