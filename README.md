# Simple HTTP Client and Server Using Sockets

The goal of this project is to create a basic HTTP client and server using socket programming. The project is coded entirely using Python. The libraries used are `os` (for basic file management), `time`, `datetime`,`socket`, and `argparse` (for parsing command line arguments). Python 3 is the minimum version of Python required to run both the client and the server.

This project consists of the following two files which run the client and server, respectively:
- `simple_client.py`
- `simple_server.py`

## HTTP Client

The file `simple_client.py` is capable of making simple HTTP GET and PUT requests.  

Basic usage:

```
python simple_client.py localhost 2020 GET index.html

```

Note that there are 4 acceptable command line arguments. In order from left to right:
- **Host**. The hostname or IP address of the host on which the HTTP server is running. In the above example, the host is `localhost` because the HTTP server is running locally.
- **Port**. The port on which the HTTP server is listening. If no port is specified, this value defaults to `80`.
- **Request Type**. The type of HTTP request. Currently, the supported methods are `GET` and `PUT`.
- **File Path**. The path to the file in question. In the case of `GET`, this file will be retrieved. In the case of `PUT`, this file will be created.

### Program Flow

This program begins by creating a socket and establishing a connection to the existing socket for the HTTP server and port indicated in the command-line options specified by the user.

The program proceeds to parse the user-provided arguments into a valid HTTP request. In order to maintain simplicity, only the following headers are included:
- **Host**
- **User-Agent** (hard-coded to `simple_client`)
- **Accept** (hard-coded to `*/*`)

This request is then encoded into bytes and is sent to the HTTP server over the socket. The client waits for a valid response from the HTTP server. This client is equipped to handle chunked transfer of data, meaning that it will 
continue to listen for valid HTTP responses until it receives no more response from the server (allowing a single transfer from server to client to be split up into multiple chunks). Once a response is received from the server,
the client socket closes, ending the program flow.

Additionally, there is a timeout mechanism in place so that for blocking socket operations, the `recv` operation does not hang up program execution. This means that the socket will only stay open for the allotted time. The value (in seconds) can be altered if needed by changing the `SOCKET_TIMEOUT` constant.

Should a keyboard interrupt occur at any point in the course of the program flow, the client socket will close gracefully.

## HTTP Server

The file `simple_server.py` is capable of processing simple HTTP GET and PUT requests and sending appropriate responses.

Basic usage:

```
python simple_server.py 2020

```

There is only one command line argument accepted:
- **Port**. The port on which the HTTP server will listen. Defaults to 80 is no port is specified.

### Program Flow

This program begins by creating the server-side socket and having it listen for incoming connections. The server continuously checks for client connections unless a KeyboardInterrupt occurs or the process is manually killed.
When the server is stopped via either of these methods, the socket is also gracefully closed.

If the server receives a request from an HTTP client, it parses out the method type and file name from the request. This is the minimum information it needs to process `GET` or `PUT` requests.

This server is capable of returning the following HTTP status codes and messages:
- **200 OK**. Returned when the client makes a successful `GET` request.
- **200 OK File Created**. Returned when the client makes a successful `PUT` request and the new file has been created.
- **404 Not Found**. Returned when the user makes a `GET` request for a file that does not exist.
- **405 Method not Allowed**. Returned when the client sends an HTTP request using an unsupported or nonexistent request type (other than `GET` and `PUT`).

In the case of a `GET` request, the **200 OK** status code will be sent along with the requested file. In the case of a `PUT` request, a new file will be created in the server directory.

Along with the status code header, the response from this server will also include HTTP headers with information about the current date and time, and other file-related data such as `Last-Modified`, `Content-Type`, and `Content-Length`.

## Possible Improvements

Some possible extensions/improvements that can be made to this simple client/server:
- **Adding chunk transfer capability to HTTP server**. While `simple_client.py` is equipped to handle chunked transfer of data, the HTTP server is not. This would be the first enhancement that I would make to this code.
- **Adding more HTTP method types**. Currently the only supported methods are `GET` and `PUT`, however there are a number of unsupported HTTP methods that could be supported in the future.
- **Adding in more header information**. A minimal amount of HTTP header information is current included in the client code. This can be expanded and made more complete.
- **Adding more status codes**. Only a few HTTP status codes are included, however in reality, there are number of HTTP status codes. Support for more of these could be added into the server code.
- **Concurrency**. The server is currently not a concurrent server, meaning that it cannot handle multiple incoming requests concurrently. This could be a future enhancement.
