
import tkinter as tk
from tkinter import ttk

COLUMNAS = [
    "PEC", "Posicion", "Número", "Piloto", "Vueltas", "T. Total", "Mejor T. Vuelta",
    "Dif.1°", "Dif.Ant.", "En Vuelta", "S1", "S2", "S3", "Pit", "Categoría", "localidad"
]

class MonitorUI:
    def __init__(self, actualizar_callback):
        self.root = tk.Tk()
        self.root.title("Monitor de Tiempos Modular")
        self.actualizar_callback = actualizar_callback

        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()

        # Crear Treeview con todas las columnas
        self.tree = ttk.Treeview(self.root, columns=COLUMNAS, show="headings")

        # Calcular ancho por columna para ocupar toda la pantalla
        ancho_columna = ancho_pantalla // len(COLUMNAS)

        for col in COLUMNAS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho_columna, anchor="center")

        self.tree.pack(expand=True, fill="both")

        self.actualizar()
        self.root.mainloop()

    def actualizar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        datos = self.actualizar_callback()
        for fila in datos:
            self.tree.insert("", "end", values=fila)

        self.root.after(1000, self.actualizar)
