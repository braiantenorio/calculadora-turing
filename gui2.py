import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from transiciones import (
    transiciones_incrementador, transiciones_decrementador, transiciones_sumador,
    transiciones_copiar_en_resultado, transiciones_iniciador, transiciones_mover_resultado,
    transiciones_restador, transiciones_copiar_al_inicio, transiciones_multiplicador,
    transiciones_recargar_operador, transiciones_divisor
)

class MaquinaTuring:
    submaquinas_globales = {}

    def __init__(self, cinta, transiciones, estado_inicial, estado_final, nombre="Main", submaquinas=None):
        self.cinta = list(cinta)
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado = estado_inicial
        self.estado_final = estado_final
        self.cabezal = 0
        self.submaquinas = submaquinas or {}
        self.nombre = nombre
        self.callback_paso = None
        self.delay = 0.1
        self.running_flag = None

    def set_callback_paso(self, callback):
        self.callback_paso = callback

    def set_delay(self, delay):
        self.delay = delay

    def paso(self):
        simbolo = self.cinta[self.cabezal]
        clave = (self.estado, simbolo)

        if clave not in self.transiciones:
            return False

        nuevo_estado, escribir, mover = self.transiciones[clave]

        if escribir != 'n':
            self.cinta[self.cabezal] = escribir

        self.estado = nuevo_estado

        if self.callback_paso:
            self.callback_paso(self)

        if mover == "R":
            self.cabezal += 1
        elif mover == "L":
            self.cabezal -= 1
        elif mover == "N":
            pass
        else:
            resultado = self.llamar_submaquina(mover)
            return resultado

        if self.cabezal >= len(self.cinta):
            self.cinta.append(' ')
        elif self.cabezal < 0:
            self.cinta.insert(0, ' ')
            self.cabezal = 0

        return True

    def llamar_submaquina(self, mover):
        if mover in self.submaquinas:
            submaquina = self.submaquinas[mover]
        else:
            submaquina = MaquinaTuring.submaquinas_globales.get(mover, None)

        if submaquina is None:
            return False

        submaquina.cinta = self.cinta
        submaquina.cabezal = self.cabezal
        submaquina.estado = submaquina.estado_inicial

        if self.callback_paso:
            submaquina.set_callback_paso(self.callback_paso)
        submaquina.set_delay(self.delay)

        resultado = submaquina.ejecutar(delay=self.delay)
        if not resultado:
            return False

        self.cinta = submaquina.cinta
        self.cabezal = submaquina.cabezal

        return True

    def ejecutar(self, delay=0.1):
        while self.estado != self.estado_final:
            if self.running_flag and not self.running_flag():
                return False
            if not self.paso():
                break
            time.sleep(delay)
        return True


class TuringMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora - Maquina Turing")
        self.root.geometry("900x500")

        self.maquina_actual = None
        self.running = False
        self.step_count = 0

        self.setup_gui()
        self.initialize_submachines()
         
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        input_frame = ttk.LabelFrame(main_frame, text="Parametros", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Label(input_frame, text="Numero 1 (decimal):").grid(row=0, column=0, sticky=tk.W)
        self.num1_entry = ttk.Entry(input_frame, width=15)
        self.num1_entry.grid(row=0, column=1)
        self.num1_entry.insert(0, "2")

        ttk.Label(input_frame, text="Numero 2 (decimal):").grid(row=1, column=0, sticky=tk.W)
        self.num2_entry = ttk.Entry(input_frame, width=15)
        self.num2_entry.grid(row=1, column=1)
        self.num2_entry.insert(0, "3")

        ttk.Label(input_frame, text="Operador (+, -, *, /):").grid(row=2, column=0, sticky=tk.W)
        self.operator_entry = ttk.Entry(input_frame, width=15)
        self.operator_entry.grid(row=2, column=1)
        self.operator_entry.insert(0, "*")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="Iniciar", command=self.start_execution)
        self.start_button.grid(row=0, column=0, padx=5)

        self.step_button = ttk.Button(button_frame, text="Paso", command=self.step_execution)
        self.step_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Detener", command=self.stop_execution, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_machine)
        self.reset_button.grid(row=0, column=3, padx=5)

        ttk.Label(button_frame, text="Delay:").grid(row=0, column=4, padx=(20, 5))
        self.speed_var = tk.DoubleVar(value=0.5)
        self.speed_scale = ttk.Scale(button_frame, from_=0.1, to=2.0, variable=self.speed_var,
                                    orient=tk.HORIZONTAL, length=120)
        self.speed_scale.grid(row=0, column=5, padx=5)

        machine_frame = ttk.LabelFrame(main_frame, text="Ejecución", padding="5")
        machine_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        ttk.Label(machine_frame, text="Maquina:").grid(row=0, column=0, sticky=tk.W)
        self.machine_label = ttk.Label(machine_frame, text="Ninguna", font=("Arial", 10, "bold"))
        self.machine_label.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(machine_frame, text="Estado:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.state_label = ttk.Label(machine_frame, text="---", font=("Arial", 10, "bold"))
        self.state_label.grid(row=0, column=3)

        ttk.Label(machine_frame, text="Pasos:").grid(row=0, column=4, sticky=tk.W, padx=(20, 5))
        self.steps_label = ttk.Label(machine_frame, text="0", font=("Arial", 10, "bold"))
        self.steps_label.grid(row=0, column=5)

        tape_frame = ttk.LabelFrame(main_frame, text="Cinta", padding="5")
        tape_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.tape_canvas = tk.Canvas(tape_frame, height=120, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.tape_canvas.pack(fill=tk.BOTH, expand=True)

    def initialize_submachines(self):
        incrementador = MaquinaTuring("", transiciones_incrementador, "s0", "s2", "Incrementador")
        decrementador = MaquinaTuring("", transiciones_decrementador, "s0", "s2", "Decrementador")
        copiar_en_resultado = MaquinaTuring("", transiciones_copiar_en_resultado, "s0", "s9", "CopiarEnResultado")
        mover_resultado = MaquinaTuring("", transiciones_mover_resultado, "s0", "s6", "MoverResultado")
        copiar_al_principio = MaquinaTuring("", transiciones_copiar_al_inicio, "s0", "s12", "CopiarAlInicio")
        recargar_operador = MaquinaTuring("", transiciones_recargar_operador, "s0", "s16", "RecargarOperador")
        sumador = MaquinaTuring("", transiciones_sumador, "s2", "s11", "Sumador")
        restador = MaquinaTuring("", transiciones_restador, "s2", "s11", "Restador")
        multiplicador = MaquinaTuring("", transiciones_multiplicador, "s0", "s30", "Multiplicador")
        divisor = MaquinaTuring("", transiciones_divisor, "s0", "s40", "Divisor")

        MaquinaTuring.submaquinas_globales = {
            "I": incrementador, "D": decrementador, "CaR": copiar_en_resultado,
            "S": sumador, "MR": mover_resultado, "X": restador, 
            "CaP": copiar_al_principio, "M": multiplicador, "RO": recargar_operador,
            "Div": divisor
        }

        for m in MaquinaTuring.submaquinas_globales.values():
            m.running_flag = lambda: self.running

    def decimal_to_binary(self, s):
        try:
            n = int(s)
            return bin(n)[2:]
        except:
            messagebox.showerror("Error", "Ingrese numeros válidos")
            return None

    def create_tape_string(self, num1, num2, operator):
        b1 = self.decimal_to_binary(num1)
        b2 = self.decimal_to_binary(num2)
        if b1 is None or b2 is None:
            return None
        return f"{b1} {b2} {operator} "

    def on_paso_callback(self, maquina):
        self.step_count += 1
        self.maquina_actual = maquina
        self.root.after(0, self.update_display)

    def update_display(self):
        if not self.maquina_actual:
            return

        self.tape_canvas.delete("all")
        tape = self.maquina_actual.cinta
        head = self.maquina_actual.cabezal

        w = 40
        y = 60
        for i, s in enumerate(tape):
            x = 20 + i * w
            self.tape_canvas.create_rectangle(x, y - 20, x + w, y + 20, outline="black", fill="lightblue")
            self.tape_canvas.create_text(x + w//2, y, text=s, font=("Arial", 12, "bold"))
            if i == head:
                self.tape_canvas.create_rectangle(x, y - 20, x + w, y + 20, outline="red", width=3)
                self.tape_canvas.create_polygon(x+w//2-10, y-40, x+w//2+10, y-40, x+w//2, y-20,
                                                fill="red")

        self.machine_label.config(text=self.maquina_actual.nombre)
        self.state_label.config(text=self.maquina_actual.estado)
        self.steps_label.config(text=str(self.step_count))

    def start_execution(self):
        if self.running:
            return

        tape_str = self.create_tape_string(self.num1_entry.get(), self.num2_entry.get(), self.operator_entry.get())
        if tape_str is None:
            return

        self.step_count = 0
        self.maquina_actual = MaquinaTuring(tape_str, transiciones_iniciador, "s0", "s21", "Iniciador")
        self.maquina_actual.set_callback_paso(self.on_paso_callback)
        self.maquina_actual.running_flag = lambda: self.running
        self.maquina_actual.set_delay(self.speed_var.get())

        self.update_display()

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.step_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        threading.Thread(target=self.run_machine, daemon=True).start()

    def run_machine(self):
        while self.running and self.maquina_actual.estado != self.maquina_actual.estado_final:
            self.maquina_actual.set_delay(self.speed_var.get())
            if not self.maquina_actual.paso():
                break
            time.sleep(self.speed_var.get())
        self.root.after(0, self.execution_finished)

    def step_execution(self):
        if not self.maquina_actual:
            tape_str = self.create_tape_string(self.num1_entry.get(), self.num2_entry.get(), self.operator_entry.get())
            if tape_str is None:
                return
            self.maquina_actual = MaquinaTuring(tape_str, transiciones_iniciador, "s0", "s21", "Iniciador")
            self.maquina_actual.set_callback_paso(self.on_paso_callback)
            self.step_count = 0

        if self.maquina_actual.estado != self.maquina_actual.estado_final:
            self.maquina_actual.paso()

    def stop_execution(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.step_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def execution_finished(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.step_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_machine(self):
        self.running = False
        self.maquina_actual = None
        self.step_count = 0

        self.tape_canvas.delete("all")
        self.machine_label.config(text="Ninguna")
        self.state_label.config(text="---")
        self.steps_label.config(text="0")

        self.start_button.config(state=tk.NORMAL)
        self.step_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = TuringMachineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
