import socket
import threading
import tkinter as tk
from tkinter import ttk, simpledialog
from collections import defaultdict
import time
import json
import os

# Inicializar la raíz para obtener resolución
root = tk.Tk()
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
root.state("zoomed")
root.title("MyLaps Monitor (Sin límite de pilotos)")

# Constantes dinámicas
MARGEN_UI = 230
PREFS_FILE = "preferencias.json"

def cargar_preferencias():
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_preferencias(preferencias):
    with open(PREFS_FILE, "w") as f:
        json.dump(preferencias, f)

# Cargar preferencias
prefs = cargar_preferencias()
tamaño_fuente = prefs.get("fuente", 14)
FILA_ALTURA = prefs.get("fila_altura", 35)
PILOTOS_POR_PAGINA = prefs.get("pilotos_por_pagina", max(5, (alto_pantalla - MARGEN_UI) // FILA_ALTURA))

# Diccionarios de datos
pilotos = {}
categorias = {}
tiempos = {}
vueltas_por_piloto = defaultdict(int)
mejor_vuelta = {}
categoria_por_transponder = {}
pendientes_de_actualizar = set()
lineas_buffer_por_transponder = defaultdict(list)
vueltas_set = defaultdict(set)
categorias_pendientes = {}
lineas_recientes = []
conexion_establecida = False
total_lineas_recibidas = 0
titulo_tanda = ""
bandera_actual = ""
transponder_alias = {}
iid_por_clave = {}
datos_para_mostrar = []
pagina_actual = 0
modo_orden = "RACE"
ultimo_trackname = ""
pista_detectada = False

def limpiar_datos():
    global pilotos, categorias, tiempos, vueltas_por_piloto, mejor_vuelta
    global categoria_por_transponder, pendientes_de_actualizar, lineas_buffer_por_transponder
    global vueltas_set, categorias_pendientes, lineas_recientes, datos_para_mostrar
    global iid_por_clave, pagina_actual, titulo_tanda, bandera_actual
    global transponder_alias, ultimo_trackname

    pilotos.clear()
    categorias.clear()
    tiempos.clear()
    vueltas_por_piloto.clear()
    mejor_vuelta.clear()
    categoria_por_transponder.clear()
    pendientes_de_actualizar.clear()
    lineas_buffer_por_transponder.clear()
    vueltas_set.clear()
    categorias_pendientes.clear()
    lineas_recientes.clear()
    iid_por_clave.clear()
    transponder_alias.clear()
    datos_para_mostrar.clear()
    pagina_actual = 0
    bandera_actual = ""
    titulo_tanda = ""
    ultimo_trackname = ""
    mostrar_pagina()
    titulo_var.set("CARRERA NUEVA")
    lbl_bandera.config(text="", fg="red")
    lbl_tiempo.config(text="00:00:00")

def actualizar_o_insertar(transponder):
    datos = pilotos.get(transponder)
    if not datos:
        return
    mejor = mejor_vuelta.get(transponder, ("", float("inf"), 0))
    cat_id = categoria_por_transponder.get(transponder, "")
    cat_nombre = categorias.get(cat_id, "Desconocida")
    total_vueltas = vueltas_por_piloto.get(transponder, 0)
    tiempo_transcurrido = tiempos.get(transponder, "")
    if tiempo_transcurrido == mejor[0]:
        tiempo_transcurrido = ""
    row = (
        0,
        datos.get("numero", transponder),
        f"{datos.get('apellido', '').upper()}, {datos.get('nombre', '').upper()}",
        cat_nombre.upper(),
        mejor[2],
        mejor[0],
        total_vueltas,
        tiempo_transcurrido,
        datos.get("ciudad", "").upper()
    )
    for i, fila in enumerate(datos_para_mostrar):
        if fila[1] == row[1] and fila[2] == row[2]:
            datos_para_mostrar[i] = row
            return
    datos_para_mostrar.append(row)

def procesar_linea(linea):
    global titulo_tanda, ultimo_trackname, pista_detectada, bandera_actual
    partes = linea.split(",")

    if linea.startswith("$B"):
        if len(partes) >= 3:
            nuevo_titulo = partes[2].strip('"')
            if titulo_tanda and nuevo_titulo != titulo_tanda:
                limpiar_datos()
            titulo_tanda = nuevo_titulo
            titulo_var.set(titulo_tanda)
            root.title(titulo_tanda)

    elif linea.startswith("$F"):
        if len(partes) >= 5:
            tiempo = partes[4].strip('"')
            lbl_tiempo.config(text=tiempo)
            bandera = partes[5].strip('"') if len(partes) > 5 else ""
            if bandera and bandera != bandera_actual:
                bandera_actual = bandera
                color = "white"
                if "green" in bandera.lower():
                    color = "green"
                elif "yellow" in bandera.lower():
                    color = "yellow"
                elif "red" in bandera.lower():
                    color = "red"
                lbl_bandera.config(text=bandera.upper(), fg=color)

    elif linea.startswith("$E"):
        if "TRACKNAME" in linea and len(partes) > 1:
            nuevo_nombre = partes[1].strip('"')
            if pista_detectada and nuevo_nombre != ultimo_trackname:
                limpiar_datos()
            ultimo_trackname = nuevo_nombre
            pista_detectada = True

    elif linea.startswith("$C"):
        if len(partes) >= 3:
            categorias[partes[1].strip()] = partes[2].strip('"')

    elif linea.startswith("$A") or linea.startswith("$COMP"):
        if len(partes) >= 8:
            transponder = partes[1].strip('"')
            numero_vehiculo = partes[2].strip('"')
            pilotos[transponder] = {
                "apellido": partes[5].strip('"'),
                "nombre": partes[4].strip('"'),
                "ciudad": partes[6].strip('"'),
                "numero": numero_vehiculo
            }
            cat_id = partes[7].strip() if linea.startswith("$A") else partes[3].strip()
            categoria_por_transponder[transponder] = cat_id
            transponder_alias[transponder] = numero_vehiculo
            pendientes_de_actualizar.add(transponder)

    elif linea.startswith("$H") or linea.startswith("$G"):
        if len(partes) >= 5:
            try:
                transponder = partes[2].strip('"')
                tiempo = partes[4].strip('"')
                num_vuelta = int(partes[3]) if partes[3].strip() else 0
                if tiempo:
                    if transponder not in pilotos:
                        lineas_buffer_por_transponder[transponder].append(linea)
                        return
                    vueltas_por_piloto[transponder] = max(vueltas_por_piloto[transponder], num_vuelta)
                    if tiempo not in vueltas_set[transponder]:
                        vueltas_set[transponder].add(tiempo)
                        if transponder not in mejor_vuelta or tiempo_a_segundos(tiempo) < tiempo_a_segundos(mejor_vuelta[transponder][0]):
                            mejor_vuelta[transponder] = (tiempo, tiempo_a_segundos(tiempo), num_vuelta)
                    if linea.startswith("$G"):
                        tiempos[transponder] = tiempo
                    pendientes_de_actualizar.add(transponder)
            except:
                pass

def tiempo_a_segundos(t):
    try:
        if not t or t.strip() == "":
            return float('inf')
        partes = t.split(":")
        if len(partes) == 3:
            horas = int(partes[0])
            minutos = int(partes[1])
            segundos, milis = map(int, partes[2].split("."))
            return horas * 3600 + minutos * 60 + segundos + milis / 1000
        elif len(partes) == 2:
            minutos = int(partes[0])
            segundos, milis = map(int, partes[1].split("."))
            return minutos * 60 + segundos + milis / 1000
    except:
        return float('inf')

def cambiar_pagina(delta):
    global pagina_actual
    max_pagina = (len(datos_para_mostrar) - 1) // PILOTOS_POR_PAGINA
    pagina_actual = max(0, min(pagina_actual + delta, max_pagina))
    mostrar_pagina()

def mostrar_pagina():
    tree.delete(*tree.get_children())
    inicio = pagina_actual * PILOTOS_POR_PAGINA
    fin = inicio + PILOTOS_POR_PAGINA
    for i, row in enumerate(datos_para_mostrar[inicio:fin]):
        tag = "even" if i % 2 == 0 else "odd"
        tree.insert("", "end", values=row, tags=(tag,))

def reordenar_posiciones():
    global datos_para_mostrar
    if modo_orden == "QUALIFY":
        datos_para_mostrar.sort(key=lambda x: tiempo_a_segundos(x[5]))
    elif modo_orden == "RACE":
        datos_para_mostrar.sort(key=lambda x: (-x[6], tiempo_a_segundos(x[7])))
    for idx, row in enumerate(datos_para_mostrar, start=1):
        row = list(row)
        row[0] = idx
        datos_para_mostrar[idx - 1] = tuple(row)
    mostrar_pagina()

def actualizar_tabla_batch():
    for transponder in pendientes_de_actualizar:
        actualizar_o_insertar(transponder)
    pendientes_de_actualizar.clear()
    reordenar_posiciones()
    root.after(1000, actualizar_tabla_batch)

def paginacion_automatica():
    global pagina_actual
    max_pagina = (len(datos_para_mostrar) - 1) // PILOTOS_POR_PAGINA
    pagina_actual = (pagina_actual + 1) if pagina_actual < max_pagina else 0
    mostrar_pagina()
    root.after(10000, paginacion_automatica)

def conectar():
    global conexion_establecida
    if conexion_establecida:
        return
    ip = simpledialog.askstring("Conectar", "IP del servidor Orbits:", initialvalue="192.168.1.100")
    puerto = 50000
    thread = threading.Thread(target=escuchar_datos, args=(ip, puerto))
    thread.daemon = True
    thread.start()

def escuchar_datos(ip, puerto):
    global conexion_establecida
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, puerto))
        conexion_establecida = True
        s.settimeout(5.0)
        buffer = ""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode("latin1", errors="ignore")
                while "\r\n" in buffer:
                    linea, buffer = buffer.split("\r\n", 1)
                    if linea.strip():
                        procesar_linea(linea.strip())
            except socket.timeout:
                continue
    except:
        conexion_establecida = False

def reintentar_buffer_pendientes():
    for transponder in list(lineas_buffer_por_transponder.keys()):
        if transponder in pilotos:
            for linea in lineas_buffer_por_transponder[transponder]:
                procesar_linea(linea)
            del lineas_buffer_por_transponder[transponder]
    root.after(3000, reintentar_buffer_pendientes)

# UI
titulo_var = tk.StringVar()
titulo_var.set("Cargando...")
lbl_pista = tk.Label(root, textvariable=titulo_var, font=("Verdana", 18), bg="black", fg="yellow")
lbl_pista.pack(fill="x")

style = ttk.Style()
style.configure("Treeview.Heading", font=("Verdana", 15, "bold"))
style.configure("Treeview", font=("Verdana", tamaño_fuente, "bold"), rowheight=FILA_ALTURA)

frame_tabla = tk.Frame(root)
frame_tabla.pack(expand=True, fill="both")

scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
scroll_y.pack(side="right", fill="y")

columns = ("pos", "num", "piloto", "cat", "en_vuelta", "mejor", "vueltas", "tiempo", "ciudad")
tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", yscrollcommand=scroll_y.set, selectmode="none")
scroll_y.config(command=tree.yview)

headers = ["Pos.", "N°", "PILOTO", "CATEGORÍA", "EN VUELTA", "MEJOR VUELTA", "T. VUELTAS", "T. TRANSCURRIDO", "CIUDAD"]
anchos_columnas = [20, 20, 200, 120, 40, 120, 40, 150, 120]
for col, text, ancho in zip(columns, headers, anchos_columnas):
    tree.heading(col, text=text.upper())
    tree.column(col, width=ancho, anchor="center")

tree.tag_configure("odd", background="#f0f0f0")
tree.tag_configure("even", background="#d0d0d0")
tree.pack(expand=True, fill="both")

frame_controles = tk.Frame(root)
frame_controles.pack(fill="x")

btn_anterior = tk.Button(frame_controles, text="<< Anterior", command=lambda: cambiar_pagina(-1))
btn_anterior.pack(side="left", padx=5, pady=5)

btn_siguiente = tk.Button(frame_controles, text="Siguiente >>", command=lambda: cambiar_pagina(1))
btn_siguiente.pack(side="left", padx=5, pady=5)

btn_qualify = tk.Button(frame_controles, text="QUALIFY", command=lambda: set_modo("QUALIFY"), bg="blue", fg="white", font=("Verdana", 12))
btn_qualify.pack(side="left", padx=5, pady=5)

btn_race = tk.Button(frame_controles, text="RACE", command=lambda: set_modo("RACE"), bg="red", fg="white", font=("Verdana", 12))
btn_race.pack(side="left", padx=5, pady=5)

lbl_fuente = tk.Label(frame_controles, text="Tamaño de fuente:", font=("Verdana", 10))
lbl_fuente.pack(side="left", padx=5)

slider_fuente = tk.Scale(
    frame_controles, from_=10, to=24, orient="horizontal",
    command=lambda val: [
        style.configure("Treeview", font=("Verdana", int(val), "bold")),
        guardar_preferencias({**prefs, "fuente": int(val), "fila_altura": slider_fila.get(), "pilotos_por_pagina": int(combo_pilotos.get())})
    ]
)
slider_fuente.set(tamaño_fuente)
slider_fuente.pack(side="left", padx=5)

lbl_fila = tk.Label(frame_controles, text="Altura de fila:", font=("Verdana", 10))
lbl_fila.pack(side="left", padx=5)

slider_fila = tk.Scale(
    frame_controles, from_=20, to=60, orient="horizontal",
    command=lambda val: [
        style.configure("Treeview", rowheight=int(val)),
        guardar_preferencias({**prefs, "fuente": slider_fuente.get(), "fila_altura": int(val), "pilotos_por_pagina": int(combo_pilotos.get())})
    ]
)
slider_fila.set(FILA_ALTURA)
slider_fila.pack(side="left", padx=5)

combo_pilotos = ttk.Combobox(frame_controles, values=[str(i) for i in range(10, 31)], width=5)
combo_pilotos.set(str(PILOTOS_POR_PAGINA))
combo_pilotos.pack(side="left", padx=5)
combo_pilotos.bind("<<ComboboxSelected>>", lambda e: [
    guardar_preferencias({**prefs, "fuente": slider_fuente.get(), "fila_altura": slider_fila.get(), "pilotos_por_pagina": int(combo_pilotos.get())}),
    globals().update(PILOTOS_POR_PAGINA=int(combo_pilotos.get())),
    mostrar_pagina()
])

frame_info = tk.Frame(root, bg="black")
frame_info.pack(fill="x")

lbl_bandera = tk.Label(frame_info, text="", font=("Verdana", 16), bg="black", fg="red")
lbl_bandera.pack(side="left", padx=10)

lbl_tiempo = tk.Label(frame_info, text="00:00:00", font=("Verdana", 24), bg="black", fg="green")
lbl_tiempo.pack(side="right", padx=10)

btn_conectar = tk.Button(frame_info, text="Conectar", command=conectar, bg="green", fg="white", font=("Arial", 16))
btn_conectar.pack(side="right", padx=10)

def set_modo(modo):
    global modo_orden
    modo_orden = modo
    actualizar_tabla_completa()

def actualizar_tabla_completa():
    datos_para_mostrar.clear()
    for transponder in pilotos:
        actualizar_o_insertar(transponder)
    reordenar_posiciones()

root.after(1000, actualizar_tabla_batch)
root.after(3000, reintentar_buffer_pendientes)
root.after(10000, paginacion_automatica)
root.mainloop()
