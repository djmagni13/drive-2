from manager import obtener_datos_para_tabla
from parser import interpretar_trama
import tkinter as tk
from tkinter import ttk

# Simulación de recepción de tramas
def recibir_tramas():
    tramas = [
        '$C,1,"Moto 3"',
        '$C,2,"SBK 600"',
        '$C,3,"Stock 300"',
        '$A,"1","1",1005,"Tome","Mauro","Pontevedra",2',
        '$G,1,"1",11,"00:07:58.846"',
        '$H,1,"1",1,"00:00:13.635"'
    ]
    for trama in tramas:
        tipo = trama[:trama.index(",")]
        linea = trama[trama.index(",") + 1:]
        interpretar_trama(tipo, linea)

# Inicializar la ventana de la interfaz gráfica
def inicializar_interfaz():
    root = tk.Tk()
    root.title("Monitor de Tiempos Modular")

    # Crear tabla
    tabla = ttk.Treeview(root, columns=("PEC", "Posición", "Número", "Piloto", "Vueltas", "T. Total",
                                        "Mejor Vuelta", "Dif. 1°", "Dif. Ant.", "En Vuelta",
                                        "S1", "S2", "S3", "PIT", "Categoría", "Localidad"),
                         show="headings")

    for col in tabla["columns"]:
        tabla.heading(col, text=col)

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = obtener_datos_para_tabla()
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

    actualizar_tabla()
    tabla.pack(expand=True, fill=tk.BOTH)
    root.mainloop()

if __name__ == "__main__":
    recibir_tramas()
    inicializar_interfaz()