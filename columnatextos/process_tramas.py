# Diccionario para almacenar las tramas procesadas
tramas = {
    "H": [],  # Mejores tiempos por vuelta
    "G": [],  # Posición y tiempo general
    "B": {},  # Información general de la carrera
    "A": {},  # Información de los pilotos (por transponder)
    "COMP": [],  # Clasificación de pilotos
    "C": {},  # Definición de categorías
    "E": {},  # Información del circuito
    "F": [],  # Estados del semáforo y tiempos
    "J": [],  # Tiempos acumulados por piloto
    "I": [],  # Información de tiempo del sistema
}

# Función para procesar las tramas
def procesar_trama(linea):
    partes = linea.split(",", 1)
    tipo = partes[0].strip('$')  # Tipo de trama (H, G, B, etc.)
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

    elif tipo == "A":
        a_partes = datos.split(",")
        transponder = a_partes[2].strip()  # Transponder como clave única
        tramas["A"][transponder] = {
            "numero": a_partes[0].strip('"'),
            "transponder": transponder,
            "nombre": f"{a_partes[3].strip('"')} {a_partes[4].strip('"')}",
            "localidad": a_partes[5].strip('"'),
            "categoria": a_partes[6].strip()
        }

    elif tipo == "COMP":
        comp_partes = datos.split(",")
        tramas["COMP"].append({
            "posicion": comp_partes[0],
            "piloto": comp_partes[1],
            "nombre": f"{comp_partes[3].strip('"')} {comp_partes[4].strip('"')}",
            "localidad": comp_partes[5].strip('"')
        })

    elif tipo == "C":
        c_partes = datos.split(",")
        tramas["C"][c_partes[0]] = c_partes[1].strip('"')

    elif tipo == "E":
        e_partes = datos.split(",")
        if e_partes[0] == '"TRACKNAME"':
            tramas["E"]["nombre_circuito"] = e_partes[1].strip('"')
        elif e_partes[0] == '"TRACKLENGTH"':
            tramas["E"]["longitud"] = e_partes[1].strip('"')

    elif tipo == "F":
        f_partes = datos.split(",")
        tramas["F"].append({
            "tiempo": f_partes[1].strip('"'),
            "hora": f_partes[2].strip('"'),
            "estado": f_partes[4].strip('"')
        })

    elif tipo == "J":
        j_partes = datos.split(",")
        tramas["J"].append({
            "piloto": j_partes[0],
            "tiempo_vuelta": j_partes[1].strip('"'),
            "tiempo_total": j_partes[2].strip('"')
        })

    elif tipo == "I":
        i_partes = datos.split(",")
        tramas["I"].append({
            "hora": i_partes[0].strip('"'),
            "fecha": i_partes[1].strip('"')
        })

# Función para generar la tabla de resultados
def generar_tabla_resultados():
    tabla = []
    primeros_tiempos = {g["piloto"]: g["tiempo_total"] for g in tramas["G"][:1]}  # Tiempo del primer piloto

    for g_data in tramas["G"]:
        piloto_transponder = g_data["piloto"]
        piloto_info = next((p for t, p in tramas["A"].items() if p["numero"] == piloto_transponder), None)
        if not piloto_info:
            continue

        tiempo_total = g_data["tiempo_total"]
        mejor_vuelta = next((h["mejor_tiempo"] for h in tramas["H"] if h["