
# Designer imports
import sd
import os
import time
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import megascan_link.socket as socket
from queue import Queue
import megascan_link.utilities as utilities
import megascan_link.resourceImporter as resImporter
import importlib
importlib.reload(socket)
importlib.reload(utilities)
importlib.reload(resImporter)
import ptvsd

class Data(object):
    socketThread = None
    toolbarAction = None
    toolbar = None

pluginData = Data()

def getIcon():
    return os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'megascan_logo.png')

# Plugin entry points.
#
def initializeSDPlugin():
	# Debug Studd
    # ptvsd.enable_attach()
    # ptvsd.wait_for_attach()
    # ptvsd.break_into_debugger() 
    uiMgr = utilities.getUiManager()  
    # Get the main window to set the thread parent of
    mainWindow = uiMgr.getMainWindow()
    print(mainWindow.findChildren(QtWidgets.QToolBar))
    toolbars = mainWindow.findChildren(QtWidgets.QToolBar)

    for toolbar in toolbars:
        if mainWindow.toolBarArea(toolbar) == Qt.ToolBarArea.TopToolBarArea:
            pluginData.toolbar = toolbar
            icon = QtGui.QIcon(getIcon())
            pluginData.toolbarAction = toolbar.addAction(icon,"")
            break

    pluginData.socketThread = socket.SocketThread(parent=mainWindow)
    importer = resImporter.ResourceImporter()
    receiver = socket.SocketReceiver(parent=mainWindow,importer=importer)
    print(pluginData.socketThread,receiver)
    pluginData.socketThread.onDataReceived.connect(receiver.onReceivedData, Qt.QueuedConnection)
    pluginData.socketThread.start()


def uninitializeSDPlugin(): 
    #stopping socket
    pluginData.socketThread.close()
    pluginData.toolbar.removeAction(pluginData.toolbarAction)
