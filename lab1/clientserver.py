"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self.phonebook = {
            "Max": "123456",
            "Anna": "987654",
            "Überanna": "555000"
        }
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    if data.decode('utf-8') == "GETALL":
                        data = str(self.phonebook).encode('utf-8')
                    elif data.decode('utf-8').startswith("GET "):
                        name = data.decode('utf-8')[4:]
                        if name in self.phonebook:
                            data = self.phonebook[name].encode('utf-8')
                        else:
                            data = "Name not found".encode('utf-8')
                    connection.send(data + "*".encode('utf-8'))  # return sent data plus an "*"
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('utf-8'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('utf-8')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out
    
    def GETALL(self,msg_in ="GETALL"):
        """ Call server """
        self.sock.send(msg_in.encode('utf-8'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('utf-8')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out
    
    def GET(self, name):
        """Requst number from name."""
        command = f"GET {name}"  # формируем команду протокола
        self.sock.send(command.encode('utf-8'))  # отправляем
        data = self.sock.recv(1024)  # получаем ответ
        msg_out = data.decode('utf-8')
        print(msg_out)
        self.sock.close()
        self.logger.info("Client down.")
        return msg_out


    def close(self):
        """ Close socket """
        self.sock.close()
