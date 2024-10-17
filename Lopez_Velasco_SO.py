import tkinter as tk  # Importa la biblioteca tkinter para la creación de interfaces gráficas.
import random  # Importa la biblioteca random para generar números aleatorios.
import time  # Importa la biblioteca time para manejar el tiempo y las pausas.

class ProcesamientoPorLotesApp:
    """
    Clase que representa la aplicación de procesamiento por lotes.
    Esta clase gestiona la interfaz gráfica y la lógica del procesamiento por lotes de procesos.
    """
    def __init__(self):
        """
        Inicializa la aplicación, configurando la ventana y las variables necesarias.
        """
        self.window = tk.Tk()  # Crea una ventana principal de la aplicación.
        self.window.title("Procesamiento Por Lotes")  # Establece el título de la ventana.
        self.window.geometry("600x400")  # Configura las dimensiones de la ventana.

        self.programadores = ["José", "Carlos", "Carolina", "Juan"]  # Lista de nombres de programadores.
        self.operaciones = ["+", "-", "*", "/"]  # Lista de operaciones matemáticas.
        self.procesos = []  # Lista de procesos.
        self.lotes = []  # Lista de lotes.
        self.numero_programa = 1  # Contador de número de programa.
        self.reloj_global = 0  # Inicializa el reloj global.
        self.procesos_pendientes = 0  # Inicializa el contador de procesos pendientes.
        self.lotes_pendientes = 0  # Inicializa el contador de lotes pendientes.
        self.procesando = False  # Bandera para saber si se está procesando.

        self.create_widgets()  # Llama a la función para crear los widgets.
        self.window.mainloop()  # Inicia el bucle principal de la interfaz.

    def create_widgets(self):
        """
        Crea y configura los widgets de la interfaz gráfica.
        """
        # Leyenda "Reloj Global"
        self.label_reloj_global = tk.Label(self.window, text="Reloj Global: 0", anchor="e", bg="#000000", fg="#FFA500")
        self.label_reloj_global.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        # Campo para ingresar # de procesos y botón Generar
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
        """
        Reinicia las variables y la interfaz para comenzar un nuevo procesamiento.
        """
        self.reloj_global = 0  # Reinicia el reloj global.
        self.label_reloj_global.config(text="Reloj Global: 0")  # Actualiza la etiqueta del reloj global.
        self.numero_programa = 1  # Reinicia el contador de número de programa.
        self.procesos = []  # Vacía la lista de procesos.
        self.lotes = []  # Vacía la lista de lotes.
        self.procesos_pendientes = 0  # Reinicia el contador de procesos pendientes.
        self.lotes_pendientes = 0  # Reinicia el contador de lotes pendientes.
        self.procesando = False  # Establece la bandera de procesamiento en False.

        # Limpia los listboxes
        self.listbox_en_espera.delete(0, tk.END)
        self.listbox_ejecucion.delete(0, tk.END)
        self.listbox_terminados.delete(0, tk.END)

        # Genera nuevos datos
        self.generar_datos()

    def generar_datos(self):
        """
        Genera datos aleatorios de procesos y los guarda en un archivo.
        """
        n = int(self.entry_procesos.get())  # Obtiene el número de procesos del campo de entrada.
        with open("datos.txt", "w") as file:  # Abre el archivo datos.txt para escribir.
            for _ in range(n):
                programador = random.choice(self.programadores)  # Selecciona un programador aleatorio.
                operacion = random.choice(self.operaciones)  # Selecciona una operación aleatoria.
                num1 = random.randint(0, 10)  # Genera un número aleatorio entre 0 y 10.
                num2 = random.randint(0, 10)  # Genera un número aleatorio entre 0 y 10.
                if operacion == "/" and num2 == 0:
                    num2 = random.randint(1, 10)  # Evita la división por cero.
                tme = random.randint(6, 12)  # Genera un tiempo de ejecución aleatorio entre 6 y 12.
                file.write(f"{self.numero_programa},{programador},{num1} {operacion} {num2},{tme}\n")  # Escribe el proceso en el archivo.
                self.numero_programa += 1  # Incrementa el contador de número de programa.
        self.leer_datos()  # Lee los datos generados.

    def leer_datos(self):
        """
        Lee los datos generados desde el archivo y los carga en la lista de procesos.
        """
        self.procesos = []  # Vacía la lista de procesos.
        with open("datos.txt", "r") as file:  # Abre el archivo datos.txt para leer.
            for line in file:
                numero_programa, programador, operacion, tme = line.strip().split(",")  # Divide la línea en componentes.
                proceso = {
                    "numero_programa": int(numero_programa),
                    "programador": programador,
                    "operacion": operacion,
                    "tme": int(tme)
                }  # Crea un diccionario con los datos del proceso.
                self.procesos.append(proceso)  # Añade el proceso a la lista de procesos.
        self.crear_lotes()  # Crea lotes de procesos.
        self.mostrar_procesos_en_espera()  # Muestra los procesos en espera.
        self.procesar_lotes()  # Procesa los lotes de procesos.

    def crear_lotes(self):
        """
        Crea lotes de procesos dividiendo la lista de procesos en sublistas de tamaño 7.
        """
        self.lotes = [self.procesos[i:i + 7] for i in range(0, len(self.procesos), 7)]  # Divide los procesos en lotes de 7
        self.lotes_pendientes = len(self.lotes) - 1  # Solo cuenta los lotes pendientes (excluyendo el lote actual)
        self.label_lotes_pendientes.config(text=f"# de lotes pendientes: {self.lotes_pendientes}")  # Actualiza la etiqueta de lotes pendientes

    def mostrar_procesos_en_espera(self):
        """
        Muestra los procesos en espera en el listbox correspondiente.
        """
        self.listbox_en_espera.delete(0, tk.END)  # Limpia el listbox de procesos en espera
        if len(self.procesos) > 1:  # Si hay más de un proceso pendiente
            siguiente_proceso = self.procesos[1]  # Obtiene el siguiente proceso
            self.listbox_en_espera.insert(tk.END, f"{siguiente_proceso['numero_programa']} - {siguiente_proceso['programador']}")  # Muestra el número y programador
            self.listbox_en_espera.insert(tk.END, siguiente_proceso['operacion'])  # Muestra la operación
            self.listbox_en_espera.insert(tk.END, f"TME: {siguiente_proceso['tme']}")  # Muestra el TME
            self.listbox_en_espera.insert(tk.END, "")  # Espacio en blanco para separación
            self.listbox_en_espera.insert(tk.END, f"{len(self.procesos) - 2} Procesos pendientes")  # Muestra el número de procesos pendientes
        elif len(self.procesos) == 1:  # Si solo hay un proceso pendiente
            self.listbox_en_espera.insert(tk.END, "No hay más procesos en espera")  # Mensaje de no hay más procesos

    def procesar_lotes(self):
        """
        Comienza el procesamiento de los lotes de procesos.
        """
        self.procesando = True  # Marca que el procesamiento está en curso
        self.actualizar_reloj()  # Actualiza el reloj global
        self.ejecutar_procesos()  # Ejecuta los procesos

    def actualizar_reloj(self):
        """
        Actualiza el reloj global cada segundo si se está procesando.
        """
        if self.procesando:  # Si se está procesando
            self.reloj_global += 1  # Incrementa el reloj global
            self.label_reloj_global.config(text=f"Reloj Global: {self.reloj_global}")  # Actualiza la etiqueta del reloj global
            self.window.after(1000, self.actualizar_reloj)  # Llama a sí mismo después de 1 segundo

    def ejecutar_procesos(self):
        """
        Ejecuta los procesos del lote actual.
        """
        if self.lotes:  # Si hay lotes pendientes
            lote = self.lotes.pop(0)  # Obtiene el primer lote
            self.procesos = lote  # Actualiza los procesos actuales al lote obtenido
            self.procesos_pendientes = len(lote)  # Cuenta los procesos pendientes en el lote actual
            self.mostrar_procesos_en_espera()  # Muestra los procesos en espera
            while self.procesos:  # Mientras haya procesos en el lote
                proceso = self.procesos[0]  # Obtiene el primer proceso
                self.listbox_ejecucion.delete(0, tk.END)  # Limpia el listbox de ejecución
                self.listbox_ejecucion.insert(tk.END, f"{proceso['numero_programa']} - {proceso['programador']}")  # Muestra el número y programador del proceso
                self.listbox_ejecucion.insert(tk.END, proceso['operacion'])  # Muestra la operación
                self.ejecutar_proceso(proceso)  # Ejecuta el proceso
            self.lotes_pendientes -= 1  # Decrementa el contador de lotes pendientes
            self.label_lotes_pendientes.config(text=f"# de lotes pendientes: {self.lotes_pendientes}")  # Actualiza la etiqueta de lotes pendientes
            self.window.after(1000, self.ejecutar_procesos)  # Llama a sí mismo después de 1 segundo para seguir procesando lotes
        else:
            self.procesando = False  # Marca que el procesamiento ha terminado

    def ejecutar_proceso(self, proceso):
        """
        Ejecuta un proceso individual.
        """
        tme = proceso['tme']  # Obtiene el tiempo de ejecución del proceso
        while tme > 0:  # Mientras el tiempo de ejecución sea mayor que 0
            self.listbox_ejecucion.delete(2, tk.END)  # Limpia la línea de TME en el listbox de ejecución
            self.listbox_ejecucion.insert(tk.END, f"TME: {tme}")  # Muestra el TME actual
            self.window.update()  # Actualiza la ventana para reflejar los cambios
            time.sleep(1)  # Pausa la ejecución por 1 segundo
            tme -= 1  # Decrementa el TME
        resultado = self.calcular_resultado(proceso['operacion'])  # Calcula el resultado de la operación
        self.listbox_terminados.insert(tk.END, f"{proceso['numero_programa']}. {proceso['programador']}")  # Muestra el número y programador del proceso terminado
        self.listbox_terminados.insert(tk.END, f"{proceso['operacion']} = {resultado}")  # Muestra la operación y su resultado
        self.listbox_ejecucion.delete(0, tk.END)  # Limpia el listbox de ejecución
        self.procesos.pop(0)  # Elimina el proceso actual de la lista de procesos
        self.procesos_pendientes -= 1  # Decrementa el contador de procesos pendientes
        self.mostrar_procesos_en_espera()  # Actualiza la vista de los procesos en espera

    def calcular_resultado(self, operacion):
        """
        Evalúa una operación matemática representada como cadena de texto y devuelve el resultado.
        Si se produce una división por cero, se captura la excepción y se devuelve "Error".

        Args:
            operacion (str): La operación matemática a evaluar, por ejemplo, "3 + 5".

        Returns:
            int/float/str: El resultado de la operación matemática o "Error" si hay una división por cero.
        """
        try:
            return eval(operacion)  # Evalúa la operación y devuelve el resultado.
        except ZeroDivisionError:
            return "Error"  # Retorna "Error" en caso de división por cero.

    def generar_archivo_resultados(self):
        """
        Genera un archivo de texto con los resultados de los procesos terminados.
        El archivo incluye la información de cada lote y sus procesos correspondientes.

        El archivo se llama "Resultados.txt" y se guarda en el mismo directorio del script.

        Args:
            Ninguno

        Returns:
            Ninguno
        """
        with open("Resultados.txt", "w") as file:  # Abre o crea el archivo Resultados.txt en modo escritura.
            lotes_terminados = self.listbox_terminados.get(0, tk.END)  # Obtiene todos los elementos de la listbox de terminados.
            lote_numero = 1  # Inicia el contador de lotes.
            file.write(f"Lote {lote_numero}\n")  # Escribe el encabezado del primer lote.
            for i in range(0, len(lotes_terminados), 2):
                if i > 0 and i % 14 == 0:  # Cada 14 líneas de resultados, cambia al siguiente lote.
                    lote_numero += 1
                    file.write(f"\nLote {lote_numero}\n")  # Escribe el encabezado del siguiente lote.
                file.write(f"{lotes_terminados[i]}\n{lotes_terminados[i+1]}\n\n")  # Escribe los resultados de los procesos.

if __name__ == "__main__":
    app = ProcesamientoPorLotesApp()
