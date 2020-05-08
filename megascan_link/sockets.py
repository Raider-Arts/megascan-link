from PySide2 import QtCore
import megascan_link
from megascan_link import config
import socket
import sys
import io
import json
import ptvsd
import time

class SocketThread(QtCore.QThread):
    onDataReceived = QtCore.Signal(object)
    shouldClose = False
    shouldRestart = False
    started = False

    def run(self):
        # ptvsd.enable_attach()
        # ptvsd.wait_for_attach()
        # ptvsd.break_into_debugger()
        # get config settings
        conf = config.ConfigSettings()
        # get the port number
        port = int(conf.getConfigSetting("Socket", "port"))
        timeout = int(conf.getConfigSetting("Socket", "timeout"))

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(timeout)
        #bind to an address and port
        server_address = ('localhost', port)
        print('trying to start up socket on {} with port {} and timeout {}'.format(server_address[0], server_address[1], timeout))
        while not self.started:
            try:
                sock.bind(server_address)
                self.started = True
            except Exception:
                print("Failed to start up socket .... retrying")
                time.sleep(1)

        if not self.started:
            return
        # Listen for incoming connections
        sock.listen(1)
        while True:
            if self._tryCloseSocket(sock):
                break
            # Wait for a connection
            try:
                print('waiting for a connection')
                self._receivedData = io.StringIO()
                self._connection, client_address = sock.accept()
                print('connection from ', client_address)
                # Receive the data in small chunks and gather it until there is no more
                while True:
                    if self._tryCloseSocket(sock):
                        break
                    data =  self._connection.recv(16)
                    if data:
                        self._receivedData.write(data.decode("utf-8"))
                    else:
                        print('no more data from ', client_address)
                        break
            except socket.timeout:
                print("socket timeout")
            else:
                # Clean up the connection
                jsonObj = json.loads(self._receivedData.getvalue())
                self.onDataReceived.emit(jsonObj)
            finally:
                # print(json.dumps(jsonObj,indent=4))
                if hasattr(self, '_connection'):
                    self._connection.close()
                self._receivedData.close()
        self.shouldClose = False
        if self.shouldRestart:
            print("Restarting socket")
            self.shouldRestart = False
            self.started = False
            self.run()
        self.started = False

    def _tryCloseSocket(self, sock):
        if self.shouldClose:
            print("closing socket")
            sock.close()
            return True
        else:
            return False

    def restart(self):
        self.shouldClose = True
        self.shouldRestart = True

    def close(self):
        self.shouldClose = True


class SocketReceiver(QtCore.QObject):
    def __init__(self, parent=None, importer=None):
        self._importer = importer
        super(SocketReceiver, self).__init__(parent)

    def onReceivedData(self, data):
        # This is called on the main thread. It is safe to use the sd API here.
        # print("Tick received in thread {} with data {}".format(QtCore.QThread.currentThread(), json.dumps(data, indent=4)))
        print("Data received")
        self._importer.importFromData(data)
        