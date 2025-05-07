import socket
import time

# Función para procesar las tramas (usando el parser que ya construimos)
def procesar_trama(linea):
    # Aquí reutilizamos el parser que ya está implementado
    # (El código del parser se puede copiar aquí o importar desde otro archivo)
    partes = linea.split(",", 1)
    tipo = partes[0].strip('$')
    datos = partes[1] if len(partes) > 1 else ""

    if tipo == "H":
        h_partes = datos.split(",")
        tramas["H"].append({
            "posicion": h_partes[0],
            "piloto": h_partes[1].strip('"'),
            "vuelta": h_partes[2],
            "mejor_tiempo": h_partes[3].strip('"')
        })
    elif tipo == "G":
        g_partes = datos.split(",")
        tramas["G"].append({
            "posicion": g_partes[0],
            "piloto": g_partes[1].strip('"'),
            "vueltas": g_partes[2],
            "tiempo_total": g_partes[3].strip('"')
        })
    elif tipo == "B":
        b_partes = datos.split(",")
        tramas["B"] = {
            "codigo": b_partes[0],
            "descripcion": b_partes[1].strip('"')
        }
    # Agregar más tipos según el parser original...


# Diccionario para almacenar tramas
tramas = {
    "H": [],
    "G": [],
    "B": {},
    "A": {},
    "COMP": [],
    "C": {},
    "E": {},
    "F": [],
    "J": [],
    "I": []
}

# Configuración del servidor
IP_SERVIDOR = input("Ingrese la IP del servidor: ")
PUERTO_SERVIDOR = int(input("Ingrese el puerto del servidor: "))

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    print(f"Conectando al servidor {IP_SERVIDOR}:{PUERTO_SERVIDOR}...")
    sock.connect((IP_SERVIDOR, PUERTO_SERVIDOR))
    print("Conexión establecida.")

    # Recibir datos en tiempo real
    while True:
        # Leer datos del servidor
        datos = sock.recv(1024)  # Leer hasta 1024 bytes
        if not datos:
            break  # Cerrar conexión si no hay más datos

        # Decodificar los datos recibidos
        linea = datos.decode("utf-8").strip()

        # Procesar la trama recibida
        procesar_trama(linea)

        # Mostrar datos en pantalla (por ejemplo, la tabla)
        print("\n--- DATOS ACTUALIZADOS ---")
        for g in tramas["G"]:
            print(f"Posición: {g['posicion']}, Piloto: {g['piloto']}, Vueltas: {g['vueltas']}, Tiempo Total: {g['tiempo_total']}")

except Exception as e:
    print(f"Error: {e}")
finally:
    # Cerrar la conexión
    print("Cerrando conexión.")
    sock.close()