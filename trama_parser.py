# Diccionario para almacenar las categorías globalmente
categorias = {}
cola_tramas_pilotos = []  # Cola para almacenar tramas de pilotos pendientes

def interpretar_trama(trama):
    tipo = trama.split(",")[0]
    if tipo == "$A":
        return procesar_trama_a(trama)
    elif tipo == "$H":
        return procesar_trama_h(trama)
    elif tipo == "$G":
        return procesar_trama_g(trama)
    elif tipo == "$COMP":
        return procesar_trama_comp(trama)
    elif tipo == "$C":
        procesar_trama_c(trama)
        procesar_cola_pilotos()  # Intentar procesar pilotos pendientes
        return None
    elif tipo == "$F":
        return procesar_trama_f(trama)
    else:
        print(f"Trama no reconocida: {trama}")
        return None

def procesar_trama_a(trama):
    """Procesa tramas de pilotos ($A)."""
    partes = trama.split(",")
    if len(partes) < 8:
        print(f"Trama $A inválida: {trama}")
        return None

    categoria_id = partes[7].strip('"')
    if categoria_id not in categorias:
        print(f"DEBUG: Categoría no registrada para piloto {partes[2].strip()}: {categoria_id}")
        cola_tramas_pilotos.append(trama)  # Guardar en la cola para reprocesar
        return None

    categoria_nombre = categorias[categoria_id]
    print(f"DEBUG: Categoría del piloto {partes[2].strip()}: {categoria_id} -> {categoria_nombre}")  # LOG DEBUG
    return {
        "tipo": "piloto",
        "numero": partes[2].strip('"'),
        "transponder": partes[3],
        "nombre": f"{partes[5].strip().strip('"')} {partes[4].strip().strip('"')}",
        "ciudad": partes[6].strip('"'),
        "categoria": categoria_nombre
    }

def procesar_trama_c(trama):
    """Procesa tramas de categorías ($C)."""
    partes = trama.split(",")
    if len(partes) < 3:
        print(f"Trama $C inválida: {trama}")
        return None

    categoria_id = partes[1].strip('"')
    categoria_nombre = partes[2].strip('"')
    categorias[categoria_id] = categoria_nombre  # Actualizar el diccionario global de categorías
    print(f"Categoría registrada: {categoria_id} -> {categoria_nombre}")

def procesar_cola_pilotos():
    """Reprocesa las tramas de pilotos en la cola."""
    global cola_tramas_pilotos
    tramas_procesadas = []
    for trama in cola_tramas_pilotos:
        datos = procesar_trama_a(trama)
        if datos:
            tramas_procesadas.append(trama)
            print(f"DEBUG: Trama de piloto reprocesada: {datos}")
    # Eliminar las tramas procesadas de la cola
    cola_tramas_pilotos = [trama for trama in cola_tramas_pilotos if trama not in tramas_procesadas]

def procesar_trama_h(trama):
    """Procesa tramas de mejor vuelta ($H)."""
    partes = trama.split(",")
    if len(partes) < 5:
        print(f"Trama $H inválida: {trama}")
        return None

    return {
        "tipo": "mejor_vuelta",
        "numero": partes[2].strip('"'),
        "mejor_vuelta": partes[4].strip('"'),
        "en_vuelta": partes[3]
    }

def procesar_trama_g(trama):
    """Procesa tramas de tiempo total ($G)."""
    partes = trama.split(",")
    if len(partes) < 5:
        print(f"Trama $G inválida: {trama}")
        return None

    return {
        "tipo": "total",
        "numero": partes[2].strip('"'),
        "vueltas": int(partes[3]),
        "total_tiempo": partes[4].strip('"')
    }

def procesar_trama_comp(trama):
    """Procesa tramas de pilotos ($COMP)."""
    partes = trama.split(",")
    if len(partes) < 7:
        print(f"Trama $COMP inválida: {trama}")
        return None

    categoria_id = partes[7].strip('"') if len(partes) > 7 else ""
    if categoria_id not in categorias:
        print(f"DEBUG: Categoría no registrada para piloto {partes[2].strip()}: {categoria_id}")
        cola_tramas_pilotos.append(trama)  # Guardar en la cola para reprocesar
        return None

    categoria_nombre = categorias[categoria_id]
    print(f"DEBUG: Categoría del piloto {partes[2].strip()}: {categoria_id} -> {categoria_nombre}")  # LOG DEBUG
    return {
        "tipo": "piloto",
        "numero": partes[2].strip('"'),
        "nombre": f"{partes[5].strip().strip('"')} {partes[4].strip().strip('"')}",
        "ciudad": partes[6].strip('"'),
        "categoria": categoria_nombre
    }

def procesar_trama_f(trama):
    """Procesa tramas de estado ($F)."""
    partes = trama.split(",")
    if len(partes) < 5:
        print(f"Trama $F inválida: {trama}")
        return None

    return {
        "tipo": "estado",
        "bandera": partes[4].strip()
    }