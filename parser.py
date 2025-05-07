# Diccionario de categorías
categorias = {
    "1": "Moto 3",
    "2": "SBK 1000",
    "3": "SBK 600",
    "4": "Stock 1000",
    "5": "Stock 300",
    "6": "300 PRO"
}

pilotos = {}

def interpretar_trama(tipo, linea):
    partes = linea.split(",")

    if tipo == "A":
        # Trama $A: Información de piloto
        categoria_codigo = partes[7].strip()  # Último campo es la categoría
        numero = partes[1].strip('"')
        transponder = partes[3].strip('"')
        nombre = f"{partes[4].strip('"')} {partes[5].strip('"')}"
        localidad = partes[6].strip('"')

        # Buscar categoría en el diccionario
        categoria = categorias.get(categoria_codigo, None)
        if not categoria:
            print(f"DEBUG: Categoría no registrada para piloto \"{numero}\": {categoria_codigo}")
            return

        # Registrar piloto
        clave = f"{numero}-{transponder}"
        pilotos[clave] = {
            "Numero": numero,
            "Transponder": transponder,
            "Nombre": nombre,
            "Ciudad": localidad,
            "Categoria": categoria
        }
        print(f"DEBUG: Piloto registrado: {pilotos[clave]}")

# Ejemplo de procesamiento de tramas tipo $A
tramas = [
    'A,"1","1",1005,"Tome","Mauro","Pontevedra",1',
    'A,"5","5",1002,"Marker","Cristian","",4',
    'A,"8","8",1001,"Aleman","Mauricio","Bs As",5',
    'A,"10","10",1008,"Alarcon","Matias","chile",6'
]

for trama in tramas:
    interpretar_trama("A", trama)