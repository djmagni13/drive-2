import threading

# Elementos compartidos entre los módulos
pilotos = {}  # Diccionario global para almacenar datos de los pilotos
lock = threading.Lock()  # Candado global para sincronización
categorias_dinamicas = {}  # Diccionario dinámico para categorías recibidas en tramas $C