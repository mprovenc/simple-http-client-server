"""
Simple HTTP Server

A simple HTTP server that can process basic GET and PUT requests and send
appropriate responses.

"""

import socket
import argparse
import os
import datetime
import time

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("port", type=int, nargs='?', default=80 )
args = parser.parse_args()
PORT = args.port

# create socket and listen for client connections
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("localhost", PORT))
serversocket.listen(1)
print(f"HTTP server started, serving at port {PORT}\n")

# infinite loop to check if a client is connecting
while 1:
    clientsocket = None
    try:
        clientsocket, address = serversocket.accept()
        request = clientsocket.recv(4096).decode()

        # GET or PUT
        method = request.split()[0]

        # get the file/directory associated with request
        # remove extra backslash char at beginning
        request_uri = request.split()[1][1:]

        msg = str()

        # process GET requests
        if method.strip() == 'GET':
            #check if the file exists
            if os.path.exists(request_uri):
                modifiedTime = time.localtime(os.path.getmtime(request_uri))
                _, ext = os.path.splitext(request_uri)
                #send the status
                msg = (f"HTTP/1.1 200 OK\r\n"
                       f"Date: {str(datetime.datetime.now())}\r\n"
                       f"Server: simple_server\r\n"
                       f"Last-Modified: {time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)}\r\n"
                       f"Content-Type: text/{ext[1:]}\r\n"
                       f"Content-Length: {str(os.path.getsize(request_uri))}\r\n\r\n" +
                        open(request_uri, "r").read())

            else:
                msg = (f"HTTP/1.1 404 Not Found\r\n"
                       f"Date: {str(datetime.datetime.now())}\r\n"
                       f"Server: Simple_Server\r\n")

        # process PUT requests
        elif method.strip() == 'PUT':
            f = open(request_uri, "w")
            if os.path.exists(request_uri):
                msg = (f"HTTP/1.1 200 OK File Created\r\n"
                       f"Date: {str(datetime.datetime.now())}\r\n"
                       f"Server: Simple_Server\r\n")
        else:
            # invalid method specified by user
            msg = (f"HTTP/1.1 405 Method not Allowed\r\n"
                   f"Date: {str(datetime.datetime.now())}\r\n"
                   f"Server:Simple_Server\r\n")

        clientsocket.send(msg.encode())
    except KeyboardInterrupt:
        # gracefully close socket on keyboard interrupt
        if clientsocket:
            clientsocket.close()
        break

serversocket.close()
