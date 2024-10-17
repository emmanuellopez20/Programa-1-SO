import tkinter as tk
import random
import time

class ProcesamientoPorLotesApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Procesamiento Por Lotes")
        self.window.geometry("600x400")
        
        self.programadores = ["José", "Carlos", "Carolina", "Juan"]
        self.operaciones = ["+", "-", "*", "/"]
        self.procesos = []
        self.lotes = []
        self.numero_programa = 1
        self.reloj_global = 0
        self.procesos_pendientes = 0
        self.lotes_pendientes = 0
        self.procesando = False
        
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        # Leyenda "Reloj Global"
        self.label_reloj_global = tk.Label(self.window, text="Reloj Global: 0", anchor="e", bg="#000000", fg="#FFA500")
        self.label_reloj_global.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        # Campo para ingresar # procesos y botón Generar
        self.label_procesos = tk.Label(self.window, text="# Procesos", anchor="e", bg="#000000", fg="#BFFF00")
        self.label_procesos.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_procesos = tk.Entry(self.window, bg="#C8A2C8", fg="#000000")
        self.entry_procesos.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.button_generar = tk.Button(self.window, text="Generar", command=self.reiniciar_programa, bg="#FFA500", fg="#000000")
        self.button_generar.grid(row=0, column=2, padx=0, pady=10, sticky="w")


        # Sección EN ESPERA
        self.label_en_espera = tk.Label(self.window, text="EN ESPERA", bg="#000000", fg="#BFFF00")
        self.label_en_espera.grid(row=1, column=0, padx=10, pady=0, sticky="n")
        self.listbox_en_espera = tk.Listbox(self.window, height=10, width=20, bg="#C8A2C8", fg="#000000")
        self.listbox_en_espera.grid(row=2, column=0, padx=10, pady=10)

        # Sección EJECUCION
        self.label_ejecucion = tk.Label(self.window, text="EJECUCION", bg="#000000", fg="#BFFF00")
        self.label_ejecucion.grid(row=2, column=1, padx=10, pady=(25, 10), sticky="n")
        self.listbox_ejecucion = tk.Listbox(self.window, height=5, width=20, bg="#C8A2C8", fg="#000000")
        self.listbox_ejecucion.grid(row=2, column=1, padx=10, pady=(50, 10), sticky="n")

        # Sección TERMINADOS
        self.label_terminados = tk.Label(self.window, text="TERMINADOS", bg="#000000", fg="#BFFF00")
        self.label_terminados.grid(row=1, column=2, padx=10, pady=0)
        self.listbox_terminados = tk.Listbox(self.window, height=10, width=20, bg="#C8A2C8", fg="#000000")
        self.listbox_terminados.grid(row=2, column=2, padx=10, pady=10)

        # Leyenda # de lotes pendientes
        self.label_lotes_pendientes = tk.Label(self.window, text="# de lotes pendientes:", bg="#000000", fg="#BFFF00")
        self.label_lotes_pendientes.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Botón OBTENER RESULTADOS
        self.button_resultados = tk.Button(self.window, text="OBTENER RESULTADOS", command=self.generar_archivo_resultados, bg="#FFA500", fg="#000000")
        self.button_resultados.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def reiniciar_programa(self):
        # Reiniciar variables
        self.reloj_global = 0
        self.label_reloj_global.config(text="Reloj Global: 0")
        self.numero_programa = 1
        self.procesos = []
        self.lotes = []
        self.procesos_pendientes = 0
        self.lotes_pendientes = 0
        self.procesando = False

        # Limpiar listboxes
        self.listbox_en_espera.delete(0, tk.END)
        self.listbox_ejecucion.delete(0, tk.END)
        self.listbox_terminados.delete(0, tk.END)

        # Generar nuevos datos
        self.generar_datos()

    def generar_datos(self):
        n = int(self.entry_procesos.get())
        with open("datos.txt", "w") as file:
            for _ in range(n):
                programador = random.choice(self.programadores)
                operacion = random.choice(self.operaciones)
                num1 = random.randint(0, 10)
                num2 = random.randint(0, 10)
                if operacion == "/" and num2 == 0:
                    num2 = random.randint(1, 10)
                tme = random.randint(6, 12)
                file.write(f"{self.numero_programa},{programador},{num1} {operacion} {num2},{tme}\n")
                self.numero_programa += 1
        self.leer_datos()

    def leer_datos(self):
        self.procesos = []
        with open("datos.txt", "r") as file:
            for line in file:
                numero_programa, programador, operacion, tme = line.strip().split(",")
                proceso = {
                    "numero_programa": int(numero_programa),
                    "programador": programador,
                    "operacion": operacion,
                    "tme": int(tme)
                }
                self.procesos.append(proceso)
        self.crear_lotes()
        self.mostrar_procesos_en_espera()
        self.procesar_lotes()

    def crear_lotes(self):
        self.lotes = [self.procesos[i:i + 7] for i in range(0, len(self.procesos), 7)]
        self.lotes_pendientes = len(self.lotes)
        self.label_lotes_pendientes.config(text=f"# de lotes pendientes: {self.lotes_pendientes}")

    def mostrar_procesos_en_espera(self):
        self.listbox_en_espera.delete(0, tk.END)
        if len(self.procesos) > 1:
            siguiente_proceso = self.procesos[1]
            self.listbox_en_espera.insert(tk.END, f"{siguiente_proceso['numero_programa']} - {siguiente_proceso['programador']}")
            self.listbox_en_espera.insert(tk.END, siguiente_proceso['operacion'])
            self.listbox_en_espera.insert(tk.END, f"TME: {siguiente_proceso['tme']}")
            self.listbox_en_espera.insert(tk.END, "")
            self.listbox_en_espera.insert(tk.END, f"{len(self.procesos) - 2} Procesos pendientes")
            self.listbox_en_espera.insert(tk.END, "")
        elif len(self.procesos) == 1:
            self.listbox_en_espera.insert(tk.END, "No hay más procesos en espera")
            self.listbox_en_espera.insert(tk.END, "")
            self.listbox_en_espera.insert(tk.END, f"# de lotes pendientes: {self.lotes_pendientes}")

    def procesar_lotes(self):
        self.procesando = True
        self.actualizar_reloj()
        self.ejecutar_procesos()

    def actualizar_reloj(self):
        if self.procesando:
            self.reloj_global += 1
            self.label_reloj_global.config(text=f"Reloj Global: {self.reloj_global}")
            self.window.after(1000, self.actualizar_reloj)

    def ejecutar_procesos(self):
        if self.lotes:
            lote = self.lotes.pop(0)
            for proceso in lote:
                self.listbox_ejecucion.delete(0, tk.END)
                self.listbox_ejecucion.insert(tk.END, f"{proceso['numero_programa']} - {proceso['programador']}")
                self.listbox_ejecucion.insert(tk.END, proceso['operacion'])
                self.ejecutar_proceso(proceso)
            self.lotes_pendientes -= 1
            self.label_lotes_pendientes.config(text=f"# de lotes pendientes: {self.lotes_pendientes}")
            self.window.after(1000, self.ejecutar_procesos)
        else:
            self.procesando = False

    def ejecutar_proceso(self, proceso):
        tme = proceso['tme']
        while tme > 0:
            self.listbox_ejecucion.delete(2, tk.END)
            self.listbox_ejecucion.insert(tk.END, f"TME: {tme}")
            self.window.update()
            time.sleep(1)
            tme -= 1
        resultado = self.calcular_resultado(proceso['operacion'])
        self.listbox_terminados.insert(tk.END, f"{proceso['numero_programa']}. {proceso['programador']}")
        self.listbox_terminados.insert(tk.END, f"{proceso['operacion']} = {resultado}")
        self.listbox_ejecucion.delete(0, tk.END)
        self.procesos.pop(0)
        self.mostrar_procesos_en_espera()

    def calcular_resultado(self, operacion):
        try:
            return eval(operacion)
        except ZeroDivisionError:
            return "Error"

    def generar_archivo_resultados(self):
        with open("Resultados.txt", "w") as file:
            lotes_terminados = self.listbox_terminados.get(0, tk.END)
            lote_numero = 1
            file.write(f"Lote {lote_numero}\n")
            for i in range(0, len(lotes_terminados), 2):
                if i > 0 and i % 14 == 0:
                    lote_numero += 1
                    file.write(f"\nLote {lote_numero}\n")
                file.write(f"{lotes_terminados[i]}\n{lotes_terminados[i+1]}\n\n")

if __name__ == "__main__":
    app = ProcesamientoPorLotesApp()
