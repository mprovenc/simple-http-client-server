
"""
Simple HTTP Client
A simple HTTP client that can perform basic HTTP GET and PUT requests.

"""
import socket
import argparse

# this client can receive this many bytes of data at a time
BUFFER_SIZE = 4096

# number of seconds before client socket times out
SOCKET_TIMEOUT = 5

# parse arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument("server", type=str, nargs='?')
parser.add_argument("port", type=int, nargs='?', default='80')
parser.add_argument("method", type=str, nargs='?')
parser.add_argument("filename", type=str, nargs='?')
args = parser.parse_args()

SERVER = args.server
PORT = args.port
METHOD = args.method
FILE = args.filename

try:
    #  create a client socket and connect it to the server socket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((SERVER, PORT))

    # formulate http request from CLI args
    request = (f"{METHOD} /{FILE} HTTP/1.1\r\nHost: {SERVER}:{PORT}\r\n"
              f"User-Agent: simple_client\r\nAccept: */*\r\n\r\n")

    # send request to server socket
    clientsocket.send(request.encode())

    # set a timeout for blocking socket operations to prevent hanging up
    clientsocket.settimeout(SOCKET_TIMEOUT)

    http_response = bytearray()

    try:
        # keep receiving bytes until a response from server is empty
        while 1:
            response = clientsocket.recv(BUFFER_SIZE)
            if not response:
                break
            http_response += response
    except socket.timeout:
        print("socket timed out, printing response")

    print(http_response.decode())

    clientsocket.close()

# close gracefully on keyboard interrupt
except KeyboardInterrupt:
    if clientsocket:
        clientsocket.close()
