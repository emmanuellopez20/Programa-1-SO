import tkinter as tk
import random
import time

class ProcesamientoPorLotesApp:
    """
    Esta clase representa una aplicación de procesamiento por lotes simulada utilizando la biblioteca Tkinter.
    La aplicación genera procesos aleatorios, los agrupa en lotes y los ejecuta en una interfaz gráfica.
    """

    def __init__(self):
        """
        Inicializa la ventana principal de la aplicación, las variables globales y los componentes de la interfaz.
        """
        # Crea la ventana principal
        self.window = tk.Tk()
        self.window.title("Procesamiento Por Lotes")
        self.window.geometry("600x400")
        
        # Inicializa las listas de programadores y operaciones
        self.programadores = ["José", "Carlos", "Carolina", "Juan"]
        self.operaciones = ["+", "-", "*", "/"]
        # Inicializa los contenedores para los procesos y lotes
        self.procesos = []
        self.lotes = []
        # Variables para rastrear el número de programa y el reloj global
        self.numero_programa = 1
        self.reloj_global = 0
        # Variables para procesos y lotes pendientes
        self.procesos_pendientes = 0
        self.lotes_pendientes = 0
        # Estado de procesamiento
        self.procesando = False
        
        # Crea los elementos de la interfaz gráfica
        self.create_widgets()
        # Inicia el bucle principal de la interfaz gráfica
        self.window.mainloop()

    def create_widgets(self):
        """
        Crea y posiciona todos los elementos visuales en la interfaz gráfica.
        """
        # Crea y posiciona la etiqueta del reloj global
        self.label_reloj_global = tk.Label(self.window, text="Reloj Global: 0", anchor="e", bg="#000000", fg="#FFA500")
        self.label_reloj_global.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        # Campo de entrada para el número de procesos y botón de generar
        self.label_procesos = tk.Label(self.window, text="# Procesos", anchor="e", bg="#000000", fg="#BFFF00")
        self.label_procesos.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_procesos = tk.Entry(self.window, bg="#C8A2C8", fg="#000000")
        self.entry_procesos.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.button_generar = tk.Button(self.window, text="Generar", command=self.reiniciar_programa, bg="#FFA500", fg="#000000")
        self.button_generar.grid(row=0, column=2, padx=0, pady=10, sticky="w")

        # Sección "EN ESPERA"
        self.label_en_espera = tk.Label(self.window, text="EN ESPERA", bg="#000000", fg="#BFFF00")
        self.label_en_espera.grid(row=1, column=0, padx=10, pady=0, sticky="n")
        self.listbox_en_espera = tk.Listbox(self.window, height=10, width=20, bg="#C8A2C8", fg="#000000")
        self.listbox_en_espera.grid(row=2, column=0, padx=10, pady=10)

        # Sección "EJECUCION"
        self.label_ejecucion = tk.Label(self.window, text="EJECUCION", bg="#000000", fg="#BFFF00")
        self.label_ejecucion.grid(row=2, column=1, padx=10, pady=(25, 10), sticky="n")
        self.listbox_ejecucion = tk.Listbox(self.window, height=5, width=20, bg="#C8A2C8", fg="#000000")
        self.listbox_ejecucion.grid(row=2, column=1, padx=10, pady=(50, 10), sticky="n")

        # Sección "TERMINADOS"
        self.label_terminados = tk.Label(self.window, text="TERMINADOS", bg="#000000", fg="#BFFF00")
        self.label_terminados.grid(row=1, column=2, padx=10, pady=0)
        self.listbox_terminados = tk.Listbox(self.window, height=10, width=20, bg="#C8A2C8", fg="#000000")
        self.listbox_terminados.grid(row=2, column=2, padx=10, pady=10)

        # Etiqueta para mostrar el número de lotes pendientes
        self.label_lotes_pendientes = tk.Label(self.window, text="# de lotes pendientes:", bg="#000000", fg="#BFFF00")
        self.label_lotes_pendientes.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Botón para obtener resultados
        self.button_resultados = tk.Button(self.window, text="OBTENER RESULTADOS", command=self.generar_archivo_resultados, bg="#FFA500", fg="#000000")
        self.button_resultados.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def reiniciar_programa(self):
        """
        Reinicia el programa para empezar de nuevo, eliminando los procesos y lotes previos,
        y generando nuevos procesos a partir del número ingresado por el usuario.
        """
        # Reinicia el reloj global y otras variables clave
        self.reloj_global = 0
        self.label_reloj_global.config(text="Reloj Global: 0")
        self.numero_programa = 1
        self.procesos = []
        self.lotes = []
        self.procesos_pendientes = 0
        self.lotes_pendientes = 0
        self.procesando = False

        # Limpia las listas de la interfaz
        self.listbox_en_espera.delete(0, tk.END)
        self.listbox_ejecucion.delete(0, tk.END)
        self.listbox_terminados.delete(0, tk.END)

        # Genera nuevos procesos
        self.generar_datos()

    def generar_datos(self):
        """
        Genera procesos aleatorios con operaciones básicas y los escribe en un archivo de texto.
        """
        # Obtiene el número de procesos a generar desde la entrada
        n = int(self.entry_procesos.get())
        # Abre el archivo de texto para escribir los datos de los procesos
        with open("datos.txt", "w") as file:
            for _ in range(n):
                # Genera un programador, una operación y dos números aleatorios
                programador = random.choice(self.programadores)
                operacion = random.choice(self.operaciones)
                num1 = random.randint(0, 10)
                num2 = random.randint(0, 10)
                # Evita la división por cero
                if operacion == "/" and num2 == 0:
                    num2 = random.randint(1, 10)
                # Genera un tiempo de ejecución aleatorio (TME)
                tme = random.randint(6, 12)
                # Escribe los datos del proceso en el archivo
                file.write(f"{self.numero_programa},{programador},{num1} {operacion} {num2},{tme}\n")
                # Incrementa el número del programa
                self.numero_programa += 1
        # Lee los datos generados
        self.leer_datos()

    def leer_datos(self):
        """
        Lee los datos de los procesos desde el archivo de texto y los almacena en una lista.
        """
        # Reinicia la lista de procesos
        self.procesos = []
        # Abre el archivo de texto para leer los datos de los procesos
        with open("datos.txt", "r") as file:
            for line in file:
                # Descompone cada línea en los atributos del proceso
                numero_programa, programador, operacion, tme = line.strip().split(",")
                proceso = {
                    "numero_programa": int(numero_programa),
                    "programador": programador,
                    "operacion": operacion,
                    "tme": int(tme)
                }
                # Agrega el proceso a la lista de procesos
                self.procesos.append(proceso)
        # Crea lotes a partir de los procesos
        self.crear_lotes()
        # Muestra los procesos en espera
        self.mostrar_procesos_en_espera()
        # Inicia el procesamiento de los lotes
        self.procesar_lotes()

    def crear_lotes(self):
        """
        Agrupa los procesos en lotes de 7 y actualiza el número de lotes pendientes.
        """
        # Agrupa los procesos en lotes de 7
        self.lotes = [self.procesos[i:i + 7] for i in range(0, len(self.procesos), 7)]
        # Actualiza el número de lotes pendientes
        self.lotes_pendientes = len(self.lotes)
        self.label_lotes_pendientes.config(text=f"# de lotes pendientes: {self.lotes_pendientes}")

    def mostrar_procesos_en_espera(self):
        """
        Muestra los procesos en espera en el listbox correspondiente.
        Si hay más de un proceso, muestra el siguiente proceso y la cantidad restante.
        Si solo hay un proceso, indica que no hay más procesos en espera.
        """
        # Limpiamos el contenido del listbox de procesos en espera
        self.listbox_en_espera.delete(0, tk.END)
        
        # Si hay más de un proceso pendiente
        if len(self.procesos) > 1:
            # Seleccionamos el siguiente proceso de la lista (el segundo en la fila)
            siguiente_proceso = self.procesos[1]
            # Insertamos el número de programa y el programador en el listbox
            self.listbox_en_espera.insert(tk.END, f"{siguiente_proceso['numero_programa']} - {siguiente_proceso['programador']}")
            # Insertamos la operación que realizará el proceso
            self.listbox_en_espera.insert(tk.END, siguiente_proceso['operacion'])
            # Mostramos el Tiempo Máximo Estimado (TME) del proceso
            self.listbox_en_espera.insert(tk.END, f"TME: {siguiente_proceso['tme']}")
            self.listbox_en_espera.insert(tk.END, "")  # Insertamos una línea vacía
            # Mostramos cuántos procesos pendientes quedan
            self.listbox_en_espera.insert(tk.END, f"{len(self.procesos) - 2} Procesos pendientes")
            self.listbox_en_espera.insert(tk.END, "")  # Insertamos otra línea vacía
        # Si solo hay un proceso restante
        elif len(self.procesos) == 1:
            # Indicamos que no hay más procesos en espera
            self.listbox_en_espera.insert(tk.END, "No hay más procesos en espera")
            self.listbox_en_espera.insert(tk.END, "")  # Insertamos una línea vacía
            # Mostramos el número de lotes pendientes
            self.listbox_en_espera.insert(tk.END, f"# de lotes pendientes: {self.lotes_pendientes}")

    def procesar_lotes(self):
        """
        Inicia el procesamiento de los lotes, ejecuta los procesos de manera secuencial.
        También activa el reloj global y comienza la ejecución de los procesos.
        """
        # Marcamos que el sistema está procesando
        self.procesando = True
        # Iniciamos la actualización del reloj global
        self.actualizar_reloj()
        # Comenzamos la ejecución de los procesos
        self.ejecutar_procesos()

    def actualizar_reloj(self):
        """
        Incrementa el reloj global mientras el procesamiento esté activo.
        Actualiza la interfaz gráfica cada segundo.
        """
        # Si el sistema sigue procesando
        if self.procesando:
            # Incrementamos el valor del reloj global
            self.reloj_global += 1
            # Actualizamos la etiqueta que muestra el valor del reloj global
            self.label_reloj_global.config(text=f"Reloj Global: {self.reloj_global}")
            # Llamamos a esta función de nuevo después de 1 segundo (1000 ms)
            self.window.after(1000, self.actualizar_reloj)

    def ejecutar_procesos(self):
        """
        Ejecuta cada lote de procesos de forma secuencial.
        Una vez que un lote es procesado, lo elimina de la lista de lotes y actualiza el número de lotes pendientes.
        """
        # Verificamos si hay lotes pendientes
        if self.lotes:
            # Tomamos el primer lote de la lista
            lote = self.lotes.pop(0)
            # Procesamos cada proceso dentro del lote
            for proceso in lote:
                # Limpiamos el listbox de ejecución
                self.listbox_ejecucion.delete(0, tk.END)
                # Insertamos la información del proceso en ejecución
                self.listbox_ejecucion.insert(tk.END, f"{proceso['numero_programa']} - {proceso['programador']}")
                self.listbox_ejecucion.insert(tk.END, proceso['operacion'])
                # Ejecutamos el proceso
                self.ejecutar_proceso(proceso)
            # Reducimos en 1 el número de lotes pendientes
            self.lotes_pendientes -= 1
            # Actualizamos el texto que muestra los lotes pendientes
            self.label_lotes_pendientes.config(text=f"# de lotes pendientes: {self.lotes_pendientes}")
            # Volvemos a ejecutar los procesos después de 1 segundo
            self.window.after(1000, self.ejecutar_procesos)
        else:
            # Si no quedan más lotes, marcamos que el sistema ha terminado de procesar
            self.procesando = False

    def ejecutar_proceso(self, proceso):
        """
        Ejecuta un proceso individual de un lote, mostrando su ejecución y resultado en la interfaz.
        """
        # Tomamos el Tiempo Máximo Estimado (TME) del proceso
        tme = proceso['tme']
        # Ejecutamos el proceso hasta que TME llegue a 0
        while tme > 0:
            # Actualizamos el TME en el listbox de ejecución
            self.listbox_ejecucion.delete(2, tk.END)
            self.listbox_ejecucion.insert(tk.END, f"TME: {tme}")
            # Actualizamos la interfaz gráfica
            self.window.update()
            # Esperamos 1 segundo para simular el tiempo de ejecución
            time.sleep(1)
            # Reducimos el TME en 1
            tme -= 1
        # Calculamos el resultado de la operación
        resultado = self.calcular_resultado(proceso['operacion'])
        # Mostramos el proceso terminado en el listbox de terminados
        self.listbox_terminados.insert(tk.END, f"{proceso['numero_programa']}. {proceso['programador']}")
        self.listbox_terminados.insert(tk.END, f"{proceso['operacion']} = {resultado}")
        # Limpiamos el listbox de ejecución
        self.listbox_ejecucion.delete(0, tk.END)
        # Eliminamos el proceso de la lista de procesos
        self.procesos.pop(0)
        # Actualizamos la lista de procesos en espera
        self.mostrar_procesos_en_espera()

    def calcular_resultado(self, operacion):
        """
        Calcula el resultado de una operación matemática.
        Si la operación es una división por cero, devuelve "Error".
        
        :param operacion: La operación matemática a evaluar.
        :return: El resultado de la operación o "Error" si hay una división por cero.
        """
        try:
            # Intentamos evaluar la operación usando eval()
            return eval(operacion)
        except ZeroDivisionError:
            # Si ocurre una división por cero, devolvemos "Error"
            return "Error"

    def generar_archivo_resultados(self):
        """
        Genera un archivo de texto llamado "Resultados.txt" que contiene los resultados
        de los procesos terminados, organizados por lotes.
        """
        # Abrimos el archivo "Resultados.txt" en modo escritura
        with open("Resultados.txt", "w") as file:
            # Obtenemos todos los procesos terminados desde la listbox de terminados
            lotes_terminados = self.listbox_terminados.get(0, tk.END)
            # Iniciamos el número de lote
            lote_numero = 1
            # Escribimos en el archivo el número del lote
            file.write(f"Lote {lote_numero}\n")
            # Iteramos sobre los procesos terminados
            for i in range(0, len(lotes_terminados), 2):
                # Cada 14 procesos, aumentamos el número del lote
                if i > 0 and i % 14 == 0:
                    lote_numero += 1
                    file.write(f"\nLote {lote_numero}\n")
                # Escribimos en el archivo los detalles del proceso terminado
                file.write(f"{lotes_terminados[i]}\n{lotes_terminados[i+1]}\n\n")

if __name__ == "__main__":
    # Inicia la aplicación ProcesamientoPorLotesApp
    app = ProcesamientoPorLotesApp()
