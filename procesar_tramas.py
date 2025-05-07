import csv
from collections import defaultdict

# Diccionario global para almacenar datos de pilotos
pilotos = {}

# Procesar una trama y actualizar datos de pilotos
def procesar_trama(trama):
    global pilotos
    partes = trama.split(",")
    tipo = partes[0]

    if tipo == "$A":
        # Trama de registro de piloto
        transponder = partes[3]
        numero = partes[1].strip('"')
        nombre = partes[4].strip('"')
        apellido = partes[5].strip('"')
        ciudad = partes[6].strip('"')
        categoria = partes[7].strip('"')

        clave = numero
        if clave not in pilotos:
            pilotos[clave] = {
                "N°": numero,
                "Piloto": f"{apellido} {nombre}",
                "Ciudad": ciudad,
                "Categoría": categoria,
                "Vueltas": 0,
                "Mejor T.Vuelta": "",
                "T. Total": "",
                "Dif. 1°": "",
                "Dif. Ant.": "",
                "En Vuelta": "",
            }

    elif tipo == "$H":
        # Trama de mejor vuelta
        numero = partes[2].strip('"')
        mejor_vuelta = partes[4].strip('"')
        vuelta_mejor = partes[3]

        if numero in pilotos:
            pilotos[numero]["Mejor T.Vuelta"] = mejor_vuelta
            pilotos[numero]["En Vuelta"] = vuelta_mejor

    elif tipo == "$G":
        # Trama de tiempo total
        numero = partes[2].strip('"')
        vueltas = int(partes[3])
        total = partes[4].strip('"')

        if numero in pilotos:
            pilotos[numero]["Vueltas"] = vueltas
            pilotos[numero]["T. Total"] = total

# Calcular diferencias y posiciones
def calcular_posiciones(modo="quality"):
    global pilotos
    campo_orden = "Mejor T.Vuelta" if modo == "quality" else "T. Total"
    pilotos_ordenados = sorted(
        pilotos.values(),
        key=lambda p: (p[campo_orden] or "99:99:99.999")
    )

    # Calcular diferencias
    mejor_tiempo = pilotos_ordenados[0][campo_orden]
    for i, piloto in enumerate(pilotos_ordenados):
        piloto["Pos."] = i + 1
        if i == 0:
            piloto["Dif. 1°"] = "00:00.000"
            piloto["Dif. Ant."] = "00:00.000"
        else:
            tiempo_actual = piloto[campo_orden]
            tiempo_anterior = pilotos_ordenados[i - 1][campo_orden]
            piloto["Dif. 1°"] = calcular_diferencia(mejor_tiempo, tiempo_actual)
            piloto["Dif. Ant."] = calcular_diferencia(tiempo_anterior, tiempo_actual)

    return pilotos_ordenados

# Calcular diferencia entre tiempos (formato: "MM:SS.mmm")
def calcular_diferencia(tiempo1, tiempo2):
    if not tiempo1 or not tiempo2:
        return "99:99.999"
    t1 = convertir_a_milisegundos(tiempo1)
    t2 = convertir_a_milisegundos(tiempo2)
    diferencia = abs(t2 - t1)
    return convertir_a_formato_tiempo(diferencia)

# Convertir tiempo en formato "MM:SS.mmm" a milisegundos
def convertir_a_milisegundos(tiempo):
    minutos, resto = tiempo.split(":")
    segundos, milisegundos = resto.split(".")
    return int(minutos) * 60000 + int(segundos) * 1000 + int(milisegundos)

# Convertir milisegundos a formato "MM:SS.mmm"
def convertir_a_formato_tiempo(milisegundos):
    minutos = milisegundos // 60000
    milisegundos %= 60000
    segundos = milisegundos // 1000
    milisegundos %= 1000
    return f"{minutos:02}:{segundos:02}.{milisegundos:03}"

# Exportar datos a CSV
def exportar_a_csv(pilotos_ordenados, columnas, archivo_salida):
    with open(archivo_salida, mode="w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        for piloto in pilotos_ordenados:
            escritor.writerow({col: piloto.get(col, "") for col in columnas})

# Ejemplo de uso
if __name__ == "__main__":
    # Simular tramas recibidas
    tramas = [
        '$A,"111","111",656,"Julian","Audagna","Leones","Moto 3"',
        '$H,1,"111",3,"00:01:28.934"',
        '$G,1,"111",5,"00:08:59.142"',
        '$A,"8","8",656,"Mauricio","Aleman","Bs As","Moto 3"',
        '$H,2,"8",5,"00:01:32.378"',
        '$G,2,"8",5,"00:09:02.586"',
    ]

    for trama in tramas:
        procesar_trama(trama)

    # Calcular posiciones para modo Quality
    columnas_quality = ["Pos.", "N°", "Piloto", "Vueltas", "Mejor T.Vuelta", "Dif. 1°", "Dif. Ant.", "En Vuelta", "Categoría", "Ciudad"]
    pilotos_quality = calcular_posiciones(modo="quality")
    print("Modo Quality:")
    for piloto in pilotos_quality:
        print(piloto)

    # Exportar a CSV
    exportar_a_csv(pilotos_quality, columnas_quality, "quality.csv")