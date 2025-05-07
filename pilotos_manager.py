class PilotosManager:
    def __init__(self):
        self.pilotos = {}

    def actualizar_piloto(self, datos):
        numero = datos.get("numero")
        if not numero:
            print(f"Error: Trama sin número válido: {datos}")
            return

        if numero not in self.pilotos:
            self.pilotos[numero] = {
                "Pec": "",
                "Posición": "",
                "Número": numero,
                "Piloto": "",
                "Vueltas": 0,
                "T. Total": "",
                "Mejor T. Vuelta": "",
                "Dif. 1°": "",
                "Dif. Ant.": "",
                "En Vuelta": "",
                "S1": "",
                "S2": "",
                "S3": "",
                "Pit": "",
                "Categoría": "",
                "Localidad": "",
            }

        piloto = self.pilotos[numero]
        tipo = datos.get("tipo")

        if tipo == "piloto":
            piloto["Piloto"] = datos.get("nombre", piloto["Piloto"])
            piloto["Localidad"] = datos.get("ciudad", piloto["Localidad"])
            piloto["Categoría"] = datos.get("categoria", piloto["Categoría"])  # Actualizar con el nombre
        elif tipo == "mejor_vuelta":
            piloto["Mejor T. Vuelta"] = datos.get("mejor_vuelta", piloto["Mejor T. Vuelta"])
            piloto["En Vuelta"] = datos.get("en_vuelta", piloto["En Vuelta"])
        elif tipo == "total":
            piloto["Vueltas"] = datos.get("vueltas", piloto["Vueltas"])
            piloto["T. Total"] = datos.get("total_tiempo", piloto["T. Total"])

    def obtener_pilotos(self, modo="quality"):
        if modo == "quality":
            return sorted(self.pilotos.values(), key=lambda p: p.get("Mejor T. Vuelta", "99:99:99.999"))
        elif modo == "race":
            return sorted(self.pilotos.values(), key=lambda p: p.get("T. Total", "99:99:99.999"))
        return list(self.pilotos.values())

    def limpiar_pilotos(self):
        self.pilotos.clear()