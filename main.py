
from conexion import Conexion
from scanner import escanear_trama
from parser import interpretar_trama
from manager import obtener_datos_para_tabla
from ui import MonitorUI

def recibir_trama(linea):
    tipo, trama = escanear_trama(linea)
    if tipo:
        interpretar_trama(tipo, trama)

if __name__ == "__main__":
    ip = input("Ingrese IP del servidor ORBITS: ")
    puerto = 50000

    conexion = Conexion(ip, puerto, recibir_trama)
    conexion.conectar()

    MonitorUI(obtener_datos_para_tabla)
