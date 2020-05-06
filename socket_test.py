# import socket
# import sys
# import io
# import json

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #bind to an address and port
# server_address = ('localhost', 24981)
# print('starting up on {} port {}'.format(server_address[0],server_address[1]))
# sock.bind(server_address)

# # Listen for incoming connections
# sock.listen(1)
# output = io.StringIO()

# while True:
#     # Wait for a connection
#     print('waiting for a connection')
#     connection, client_address = sock.accept()
#     try:
#         print('connection from ', client_address)

#         # Receive the data in small chunks and retransmit it
#         while True:
#             data = connection.recv(16)
#             # print('received ', data)
#             if data:
#                 output.write(data.decode("utf-8"))
#                 # print(data)
#             #     print >>sys.stderr, 'sending data back to the client'
#             #     connection.sendall(data)
#             else:
#                 print('no more data from ',client_address)
#                 break
            
#     finally:
#         # Clean up the connection
#         jsonObj = json.loads(output.getvalue())
#         print(json.dumps(jsonObj,indent=4))
#         connection.close()
#         output.close()

