
def obtener_datos_para_tabla():
    from parser import pilotos
    datos = []
    for clave, piloto in pilotos.items():
        datos.append([
            piloto.get("PEC", ""),             # PEC (posición en categoría)
            piloto.get("Posicion", ""),        # Posición general (por ahora vacía, se calcula después)
            piloto.get("Numero", ""),
            piloto.get("Piloto", ""),
            piloto.get("Vueltas", ""),
            piloto.get("Total", ""),
            piloto.get("MejorVuelta", ""),
            piloto.get("DifPrimero", ""),      # Diferencia con el primero
            piloto.get("DifAnterior", ""),     # Diferencia con anterior
            piloto.get("EnVuelta", ""),        # Vuelta en que hizo el mejor tiempo
            piloto.get("S1", ""),              # Sector 1
            piloto.get("S2", ""),              # Sector 2
            piloto.get("S3", ""),              # Sector 3
            piloto.get("PIT", ""),             # PIT count
            piloto.get("Categoria", ""),
            piloto.get("Localidad", "")
        ])
    return datos
