
# Designer imports
import sd
import time
from PySide2 import QtCore
import megascan_link.Socket as Socket
import importlib
importlib.reload(Socket)

socketThread = None
#
# Plugin entry points.
#
def initializeSDPlugin():
    # pass
    # Get the application and the UI Manager.
    app = sd.getContext().getSDApplication()
    uiMgr = app.getQtForPythonUIMgr()
    # Get the main window to set the thread parent of
    mainWindow = uiMgr.getMainWindow()
    socketThread = Socket.SocketThread(parent=mainWindow)
    receiver = Socket.SocketReceiver(parent=mainWindow)
    print(socketThread,receiver)
    socketThread.onDataReceived.connect(receiver.onReceivedData, QtCore.Qt.QueuedConnection)
    socketThread.start()

def uninitializeSDPlugin():
    pass
