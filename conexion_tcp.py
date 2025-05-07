import socket
import threading

class ConexionTCP:
    def __init__(self, ip, puerto, callback_trama):
        self.ip = ip
        self.puerto = puerto
        self.callback_trama = callback_trama
        self.socket = None
        self.hilo = None
        self.conectado = False
        self.buffer = ""

    def conectar(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.puerto))
            self.conectado = True
            self.hilo = threading.Thread(target=self.escuchar)
            self.hilo.daemon = True
            self.hilo.start()
            print("Conexión establecida con el servidor.")
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")

    def escuchar(self):
        while self.conectado:
            try:
                datos = self.socket.recv(1024)
                if not datos:
                    continue
                self.buffer += datos.decode('latin1', errors='ignore')
                while "\n" in self.buffer:
                    linea, self.buffer = self.buffer.split("\n", 1)
                    self.callback_trama(linea.strip())
            except Exception as e:
                self.conectado = False
                print(f"Error en la conexión: {e}")
                break

    def desconectar(self):
        self.conectado = False
        if self.socket:
            self.socket.close()
            print("Conexión cerrada.")