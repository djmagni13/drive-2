def escanear_trama(linea):
    if linea.startswith("$"):
        tipo = linea.split(",")[0]
        return tipo, linea
    return None, None