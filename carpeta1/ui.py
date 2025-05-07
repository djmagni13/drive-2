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

        # Crear Treeview con columnas
        self.tree = ttk.Treeview(self.root, columns=COLUMNAS, show="headings")
        for col in COLUMNAS:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(expand=True, fill="both")

        self.filas = {}  # Mapeo de claves únicas a IDs de filas
        self.actualizar()
        self.root.mainloop()

    def actualizar(self):
        print("Actualizando la interfaz gráfica...")  # Debug
        datos = self.actualizar_callback()
        print(f"Datos recibidos para actualizar: {datos}")  # Debug

        # Actualizar o insertar filas
        claves_existentes = set(self.filas.keys())
        nuevas_claves = set()

        for fila in datos:
            clave_unica = f"{fila[2]}-{fila[3]}"  # Número y piloto como clave única
            nuevas_claves.add(clave_unica)

            if clave_unica in self.filas:
                # Actualizar fila existente
                item_id = self.filas[clave_unica]
                self.tree.item(item_id, values=fila)
            else:
                # Insertar nueva fila
                item_id = self.tree.insert("", "end", values=fila)
                self.filas[clave_unica] = item_id

        # Eliminar filas obsoletas
        for clave in claves_existentes - nuevas_claves:
            self.tree.delete(self.filas[clave])
            del self.filas[clave]

        self.root.after(1000, self.actualizar)