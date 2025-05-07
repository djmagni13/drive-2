
import socket
import threading

class Conexion:
    def __init__(self, ip, puerto, callback_trama):
        self.ip = ip
        self.puerto = puerto
        self.callback_trama = callback_trama
        self.socket = None
        self.thread = None
        self.conectado = False

    def conectar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.puerto))
        self.conectado = True
        self.thread = threading.Thread(target=self.escuchar)
        self.thread.daemon = True
        self.thread.start()

    def escuchar(self):
        buffer = ""
        while self.conectado:
            try:
                data = self.socket.recv(1024)
                if not data:
                    continue
                buffer += data.decode(errors="ignore")
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    self.callback_trama(linea.strip())
            except:
                self.conectado = False
                break

    def desconectar(self):
        self.conectado = False
        if self.socket:
            self.socket.close()
