def obtener_datos_para_tabla():
    from parser import pilotos
    datos = []
    for clave, piloto in pilotos.items():
        datos.append({
            "Pec": piloto.get("PEC", ""),              # PEC (posición en categoría)
            "Posición": piloto.get("Posicion", ""),     # Posición general
            "Número": piloto.get("Numero", ""),
            "Piloto": piloto.get("Piloto", ""),
            "Vueltas": piloto.get("Vueltas", ""),
            "T. Total": piloto.get("Total", ""),
            "Mejor T. Vuelta": piloto.get("MejorVuelta", ""),
            "Dif. 1°": piloto.get("DifPrimero", ""),    # Diferencia con el primero
            "Dif. Ant.": piloto.get("DifAnterior", ""), # Diferencia con anterior
            "En Vuelta": piloto.get("EnVuelta", ""),    # Vuelta en que hizo el mejor tiempo
            "S1": piloto.get("S1", ""),                # Sector 1
            "S2": piloto.get("S2", ""),                # Sector 2
            "S3": piloto.get("S3", ""),                # Sector 3
            "Pit": piloto.get("PIT", ""),              # PIT count
            "Categoría": piloto.get("Categoria", ""),   # Categoría
            "Localidad": piloto.get("Localidad", "")    # Localidad
        })
    return datos