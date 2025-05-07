import tkinter as tk
from tkinter import ttk

class MonitorUI:
    def __init__(self, actualizar_callback):
        self.root = tk.Tk()
        self.root.title("Monitor de Tiempos")
        self.root.state('zoomed')  # Maximizar la ventana al iniciar
        self.actualizar_callback = actualizar_callback

        # Definir las columnas y sus tipos
        self.columnas = [
            "Pec", "Posición", "Número", "Piloto", "Vueltas", "T. Total",
            "Mejor T. Vuelta", "Dif. 1°", "Dif. Ant.", "En Vuelta",
            "S1", "S2", "S3", "Pit", "Categoría", "Localidad"
        ]
        self.tipos_columnas = {
            "Pec": "num",
            "Posición": "num",
            "Número": "num",
            "Vueltas": "num",
            "En Vuelta": "num",
            "Pit": "num",
            "Piloto": "text",
            "Categoría": "text",
            "Localidad": "text",
            "T. Total": "time",
            "Mejor T. Vuelta": "time",
            "Dif. 1°": "time",
            "Dif. Ant.": "time",
            "S1": "time",
            "S2": "time",
            "S3": "time",
        }

        # Crear Treeview con columnas
        self.tree = ttk.Treeview(self.root, columns=self.columnas, show="headings")

        # Configurar encabezados y columnas
        for col in self.columnas:
            self.tree.heading(col, text=col)
            align = self._get_alignment(col)
            self.tree.column(col, anchor=align, width=100)  # Ancho inicial

        self.tree.pack(expand=True, fill="both")

        # Autoajuste de columnas al cambiar el tamaño de la ventana
        self.tree.bind("<Configure>", self.ajustar_columnas)

        # Botones de control
        self.boton_quality = tk.Button(self.root, text="QUALITY", command=self.modo_quality)
        self.boton_quality.pack(side="left")
        self.boton_race = tk.Button(self.root, text="RACE", command=self.modo_race)
        self.boton_race.pack(side="left")

        self.actualizar()
        self.root.mainloop()

    def _get_alignment(self, columna):
        """Determina la alineación según el tipo de columna."""
        tipo = self.tipos_columnas.get(columna, "text")
        if tipo == "num":
            return "e"  # Derecha
        elif tipo == "time":
            return "center"  # Centro
        else:
            return "w"  # Izquierda

    def ajustar_columnas(self, event):
        """Ajusta el ancho de las columnas al tamaño de la tabla."""
        total_width = self.tree.winfo_width()
        col_width = max(total_width // len(self.columnas), 50)  # Mínimo ancho de columna
        for col in self.columnas:
            self.tree.column(col, width=col_width)

    def actualizar(self):
        """Actualiza los datos en la tabla."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        datos = self.actualizar_callback()
        for fila in datos:
            # Extraer valores para cada columna
            valores = [
                fila.get("Pec", ""),
                fila.get("Posición", ""),
                fila.get("Número", ""),
                fila.get("Piloto", ""),
                fila.get("Vueltas", ""),
                fila.get("T. Total", ""),
                fila.get("Mejor T. Vuelta", ""),
                fila.get("Dif. 1°", ""),
                fila.get("Dif. Ant.", ""),
                fila.get("En Vuelta", ""),
                fila.get("S1", ""),
                fila.get("S2", ""),
                fila.get("S3", ""),
                fila.get("Pit", ""),
                fila.get("Categoría", ""),
                fila.get("Localidad", "")
            ]
            self.tree.insert("", "end", values=valores)
        
        self.root.after(1000, self.actualizar)  # Actualización cada segundo

    def modo_quality(self):
        print("Modo QUALITY activado.")

    def modo_race(self):
        print("Modo RACE activado.")