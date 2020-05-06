
# Designer imports
import sd 
import time
from PySide2 import QtCore
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
    pluginData.socketThread = socket.SocketThread(parent=mainWindow)
    importer = resImporter.ResourceImporter()
    receiver = socket.SocketReceiver(parent=mainWindow,importer=importer)
    print(pluginData.socketThread,receiver)
    pluginData.socketThread.onDataReceived.connect(receiver.onReceivedData, QtCore.Qt.QueuedConnection)
    pluginData.socketThread.start()

def uninitializeSDPlugin(): 
    #stopping socket
    pluginData.socketThread.close()
