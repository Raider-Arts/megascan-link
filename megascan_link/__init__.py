
# Designer imports
import sd 
import time
from PySide2 import QtCore
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
            pluginData.toolbarAction = toolbar.addAction("prova")
            break
    pluginData.socketThread = socket.SocketThread(parent=mainWindow)
    importer = resImporter.ResourceImporter()
    receiver = socket.SocketReceiver(parent=mainWindow,importer=importer)
    print(pluginData.socketThread,receiver)
    pluginData.socketThread.onDataReceived.connect(receiver.onReceivedData, QtCore.Qt.QueuedConnection)
    pluginData.socketThread.start()


def uninitializeSDPlugin(): 
    #stopping socket
    pluginData.socketThread.close()
    pluginData.toolbar.removeAction(pluginData.toolbarAction)
