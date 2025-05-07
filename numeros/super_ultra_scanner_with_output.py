import socket
import threading
import time
import tkinter as tk
from tkinter import ttk

# Archivo donde se guardarán todas las tramas capturadas al finalizar
ARCHIVO_SALIDA = "captura_completa_orbits.txt"

# Control de la captura y almacenamiento
capturando = True
pilotos = {}
columnas = [
    "Pec", "Posicion", "Número", "Piloto", "Vueltas", "T. Total",
    "Mejor T. Vuelta", "Dif.1°", "Dif.Ant.", "En Vuelta",
    "S1", "S2", "S3", "Pit", "Categoría", "Localidad"
]

# Lista para almacenar todo lo capturado
captura_completa = []

# Interfaz gráfica
root = tk.Tk()
root.title("Announcer Style Monitor")
tree = ttk.Treeview(root, columns=columnas, show="headings")
tree.pack(expand=True, fill=tk.BOTH)

for col in columnas:
    tree.heading(col, text=col)

def actualizar_tabla():
    tree.delete(*tree.get_children())
    for p in pilotos.values():
        tree.insert("", tk.END, values=[p.get(col.lower(), "") for col in columnas])

def guardar_trama(trama):
    # Guardar trama en la lista de captura completa
    captura_completa.append(trama)
    # Mostrar en tiempo real en la consola IDLE
    print("[TRAMA CAPTURADA]", trama)

def guardar_archivo_completo():
    # Escribir todas las tramas capturadas en un archivo al finalizar
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(captura_completa))
        print(f"✅ Archivo completo guardado en: {ARCHIVO_SALIDA}")

def procesar_trama(trama):
    guardar_trama(trama)
    partes = trama.split(",")
    
    # Procesar las tramas según su tipo
    tipo = partes[0].strip()
    if tipo == "P":  # Ejemplo: Datos de posición
        numero = partes[2].strip()
        piloto = partes[3].strip()
        posicion = partes[1].strip()
        pilotos[numero] = {
            "número": numero,
            "piloto": piloto,
            "posicion": posicion,
            # Agregar más columnas si es necesario
        }
        actualizar_tabla()
    elif tipo == "T":  # Ejemplo: Tiempos parciales
        numero = partes[1].strip()
        tiempo_total = partes[2].strip()
        mejor_tiempo = partes[3].strip()
        if numero in pilotos:
            pilotos[numero]["t. total"] = tiempo_total
            pilotos[numero]["mejor t. vuelta"] = mejor_tiempo
            actualizar_tabla()

def escuchar_tramas(sock):
    global capturando
    buffer = ""
    trama_actual = ""
    sock.setblocking(True)

    while capturando:
        try:
            data = sock.recv(1024)
            if not data:
                print("[DESCONECTADO DEL SERVIDOR]")
                raise ConnectionError("Conexión perdida")
            buffer += data.decode("utf-8", errors="ignore")
            
            while buffer:
                if buffer.startswith("$"):
                    if trama_actual:
                        procesar_trama(trama_actual.strip())
                        trama_actual = ""
                    buffer = buffer[1:]
                    continue

                salto = buffer.find("\n")
                if salto != -1:
                    trama_actual += buffer[:salto]
                    procesar_trama(trama_actual.strip())
                    trama_actual = ""
                    buffer = buffer[salto + 1:]
                else:
                    trama_actual += buffer
                    buffer = ""

        except Exception as e:
            print(f"[ERROR] {e}")
            capturando = False
            break

def iniciar_captura():
    global capturando

    ip_servidor = input("Ingrese la IP del servidor Orbits: ").strip()
    puerto = 50000

    while True:  # Bucle de reconexión automática
        print(f"Conectando a {ip_servidor}:{puerto}...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip_servidor, puerto))
            print("✅ Conectado al servidor. Comenzando captura...")

            hilo = threading.Thread(target=escuchar_tramas, args=(sock,), daemon=True)
            hilo.start()

            root.mainloop()
            capturando = False
            sock.close()
            hilo.join()
            guardar_archivo_completo()  # Guardar todo al finalizar
            break

        except Exception as e:
            print(f"[ERROR AL CONECTAR] {e}")
            time.sleep(5)  # Esperar antes de intentar reconectar

if __name__ == "__main__":
    iniciar_captura()