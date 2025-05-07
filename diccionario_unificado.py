# Diccionario global para almacenar datos de pilotos
pilotos = {}

# Procesar una trama y actualizar datos de pilotos
def procesar_trama(trama):
    global pilotos
    partes = trama.split(",")
    tipo = partes[0].strip()

    if tipo == "$A":
        # Trama de registro de piloto
        numero = partes[1].strip('"')
        transponder = partes[3].strip('"')
        nombre = f"{partes[4].strip('"')} {partes[5].strip('"')}"
        localidad = partes[6].strip('"')
        categoria = partes[7].strip('"')

        clave = numero
        if clave not in pilotos:
            pilotos[clave] = {
                "Numero": numero,
                "Transponder": transponder,
                "Piloto": nombre,
                "Localidad": localidad,
                "Categoria": categoria,
                "Vueltas": 0,
                "T. Total": "",
                "Mejor T. Vuelta": "",
                "En Vuelta": "",
                "Dif. 1°": "",
                "Dif. Ant.": ""
            }

    elif tipo == "$H":
        # Trama de mejor vuelta
        numero = partes[2].strip('"')
        mejor_vuelta = partes[4].strip('"')
        en_vuelta = partes[3].strip()

        if numero in pilotos:
            pilotos[numero]["Mejor T. Vuelta"] = mejor_vuelta
            pilotos[numero]["En Vuelta"] = en_vuelta

    elif tipo == "$G":
        # Trama de tiempo total
        numero = partes[2].strip('"')
        vueltas = int(partes[3])
        total_tiempo = partes[4].strip('"')

        if numero in pilotos:
            pilotos[numero]["Vueltas"] = vueltas
            pilotos[numero]["T. Total"] = total_tiempo

# Función para obtener todos los datos en formato de tabla
def obtener_datos_para_tabla():
    datos = []
    for piloto in pilotos.values():
        fila = [
            piloto.get("Numero", ""),
            piloto.get("Piloto", ""),
            piloto.get("Categoria", ""),
            piloto.get("Localidad", ""),
            piloto.get("Vueltas", 0),
            piloto.get("T. Total", ""),
            piloto.get("Mejor T. Vuelta", ""),
            piloto.get("En Vuelta", ""),
            piloto.get("Dif. 1°", ""),
            piloto.get("Dif. Ant.", "")
        ]
        datos.append(fila)
    return datos

# Ejemplo de uso
if __name__ == "__main__":
    # Tramas de ejemplo
    tramas = [
        '$A,"1","1",1005,"Tome","Mauro","Pontevedra",1',
        '$H,"H",1005,3,"00:55.123"',
        '$G,"G",1005,10,"09:12.345"'
    ]

    # Procesar las tramas
    for trama in tramas:
        procesar_trama(trama)
    
    # Mostrar los datos en formato de tabla
    tabla = obtener_datos_para_tabla()
    for fila in tabla:
        print(fila)