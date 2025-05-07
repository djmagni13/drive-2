from conexion_tcp import ConexionTCP
from trama_parser import interpretar_trama
from pilotos_manager import PilotosManager
from gui import MonitorUI

def procesar_trama(linea):
    datos = interpretar_trama(linea)
    if datos:
        manager.actualizar_piloto(datos)

if __name__ == "__main__":
    # Solicitar IP del servidor
    ip = input("Ingrese la IP del servidor Orbits: ")
    puerto = 50000  # Puerto por defecto

    # Inicializar los gestores
    manager = PilotosManager()

    # Establecer conexión TCP
    conexion = ConexionTCP(ip, puerto, procesar_trama)
    conexion.conectar()

    # Iniciar la interfaz gráfica
    MonitorUI(manager.obtener_pilotos)