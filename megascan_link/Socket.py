from PySide2 import QtCore
# import time
import socket
import sys
import io
import json

class SocketThread(QtCore.QThread):
    onDataReceived = QtCore.Signal(object)

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket = sock
        #bind to an address and port
        server_address = ('localhost', 24981)
        print('starting up Socket on {} with port {}'.format(server_address[0],server_address[1]))
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            output = io.StringIO()
            try:
                print('connection from ', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    if data:
                        output.write(data.decode("utf-8"))
                    else:
                        print('no more data from ',client_address)
                        break
            finally:
                # Clean up the connection
                jsonObj = json.loads(output.getvalue())
                print(json.dumps(jsonObj,indent=4))
                connection.close()
                output.close()
                self.onDataReceived.emit(jsonObj)
    
    def close(self):
        if self._socket:
            self._socket.close()



class SocketReceiver(QtCore.QObject):
    def __init__(self, parent=None):
        super(SocketReceiver, self).__init__(parent)

    def onReceivedData(self, data):
        # This is called on the main thread. It is safe to use the sd API here.
        print("Tick received in thread {} with data {}".format(QtCore.QThread.currentThread(),data))