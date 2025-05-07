from common import pilotos, lock, categorias_dinamicas

def interpretar_trama(tipo, linea):
    print(f"Procesando trama de tipo: {tipo} con línea: {linea}")  # Debug
    partes = linea.split(",")
    print(f"Partes de la trama: {partes} (longitud: {len(partes)})")  # Debug

    with lock:  # Protege el acceso al diccionario
        # Manejo de tramas tipo $C (Categorías)
        if tipo == "$C":
            try:
                categoria_num = partes[0].strip()
                categoria_nombre = partes[1].strip('"')
                categorias_dinamicas[categoria_num] = categoria_nombre  # Actualizar categorías dinámicas
                print(f"Categoría añadida: {categoria_num} -> {categoria_nombre}")  # Debug
            except Exception as e:
                print(f"Error procesando trama $C: {e}")  # Debug

        # Manejo de tramas tipo $A (Datos del piloto)
        elif tipo == "$A":
            if len(partes) < 7:
                print(f"Advertencia: Trama $A con longitud insuficiente. Continuando con valores predeterminados.")  # Debug

            try:
                transponder = partes[2].strip('"') if len(partes) > 2 else ""
                numero_piloto = partes[1].strip('"') if len(partes) > 1 else ""
                apellido = partes[3].strip().strip('"') if len(partes) > 3 else "Desconocido"
                nombre = partes[4].strip().strip('"') if len(partes) > 4 else "Desconocido"
                localidad = partes[5].strip().strip('"') if len(partes) > 5 else "Desconocido"
                categoria_num = partes[6].strip().strip('"') if len(partes) > 6 else "0"

                # Mapeo del código de categoría al nombre
                categoria = categorias_dinamicas.get(categoria_num, "Desconocida")

                # Generar clave única para el piloto
                clave = f"{transponder}-{numero_piloto}"
                print(f"Clave generada: {clave}")  # Debug

                if clave not in pilotos:
                    pilotos[clave] = {
                        "Transponder": transponder,
                        "Numero": numero_piloto,         # Número del piloto
                        "Piloto": f"{apellido} {nombre}", # Formato: Apellido Nombre
                        "Categoria": categoria,           # Categoría mapeada
                        "Localidad": localidad,           # Localidad del piloto
                        "Vueltas": 0,                     # Placeholder para actualizaciones
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
                    print(f"Añadido nuevo piloto: {pilotos[clave]}")  # Debug
                else:
                    print(f"Piloto ya existente, actualizando datos: {clave}")  # Debug
                    pilotos[clave].update({
                        "Categoria": categoria,
                        "Localidad": localidad
                    })
            except Exception as e:
                print(f"Error procesando trama $A: {e}")  # Debug

        # Manejo de tramas tipo $G (Vueltas y T. Total)
        elif tipo == "$G":
            try:
                transponder = partes[1].strip('"')
                vueltas = int(partes[2].strip())
                tiempo_total = partes[3].strip()

                for clave in pilotos:
                    if pilotos[clave]["Transponder"] == transponder:
                        pilotos[clave]["Vueltas"] = vueltas
                        pilotos[clave]["Total"] = tiempo_total
                        print(f"Actualizado Vueltas y T. Total para {clave}: {vueltas}, {tiempo_total}")  # Debug
            except Exception as e:
                print(f"Error procesando trama $G: {e}")  # Debug

        # Manejo de tramas tipo $H (Mejor Tiempo de Vuelta)
        elif tipo == "$H":
            try:
                transponder = partes[1].strip('"')
                mejor_vuelta = partes[3].strip()

                for clave in pilotos:
                    if pilotos[clave]["Transponder"] == transponder:
                        pilotos[clave]["MejorVuelta"] = mejor_vuelta
                        print(f"Actualizado Mejor Vuelta para {clave}: {mejor_vuelta}")  # Debug
            except Exception as e:
                print(f"Error procesando trama $H: {e}")  # Debug