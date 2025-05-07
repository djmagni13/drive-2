
pilotos = {}

def interpretar_trama(tipo, linea):
    partes = linea.split(",")

    if tipo == "$A":
        transponder = partes[1]
        numero = partes[2]
        nombre = partes[3].strip().strip('"')
        apellido = partes[4].strip().strip('"')
        localidad = partes[5].strip().strip('"')
        categoria = partes[6].strip().strip('"')

        clave = f"{transponder}-{nombre}-{apellido}-{categoria}"

        if clave not in pilotos:
            pilotos[clave] = {
                "Transponder": transponder,
                "Numero": numero,
                "Piloto": f"{nombre} {apellido}",
                "Categoria": categoria,
                "Localidad": localidad,
                "Vueltas": 0,
                "MejorVuelta": "",
                "Total": "",
                "PEC": "",
                "Posicion": "",
                "DifPrimero": "",
                "DifAnterior": "",
                "EnVuelta": "",
                "S1": "",
                "S2": "",
                "S3": "",
                "PIT": ""
            }

    elif tipo == "$H":
        transponder = partes[1]
        mejor_vuelta = partes[4].strip()

        for clave in pilotos:
            if pilotos[clave]["Transponder"] == transponder:
                pilotos[clave]["MejorVuelta"] = mejor_vuelta

    elif tipo == "$G":
        transponder = partes[1]
        total = partes[4].strip()

        for clave in pilotos:
            if pilotos[clave]["Transponder"] == transponder:
                pilotos[clave]["Total"] = total
