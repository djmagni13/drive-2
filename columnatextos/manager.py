from common import pilotos, lock

def obtener_datos_para_tabla():
    with lock:  # Asegura acceso exclusivo al diccionario
        datos = []
        for clave, piloto in pilotos.items():
            fila = [
                piloto.get("PEC", ""),
                piloto.get("Posicion", ""),
                piloto.get("Numero", ""),
                piloto.get("Piloto", ""),
                piloto.get("Vueltas", 0),
                piloto.get("Total", ""),
                piloto.get("MejorVuelta", ""),
                piloto.get("DifPrimero", ""),
                piloto.get("DifAnterior", ""),
                piloto.get("EnVuelta", ""),
                piloto.get("S1", ""),
                piloto.get("S2", ""),
                piloto.get("S3", ""),
                piloto.get("PIT", ""),
                piloto.get("Categoria", "Desconocida"),
                piloto.get("Localidad", "Desconocido")
            ]
            datos.append(fila)
        return datos