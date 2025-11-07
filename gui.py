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
        """Set callback to be called after each step"""
        self.callback_paso = callback

    def set_delay(self, delay):
        """Set execution delay"""
        self.delay = delay

    def paso(self):
        """Ejecuta un paso de la máquina."""
        simbolo = self.cinta[self.cabezal]
        clave = (self.estado, simbolo)

        if clave not in self.transiciones:
            return False

        nuevo_estado, escribir, mover = self.transiciones[clave]

        # Escribir en la cinta
        if escribir != 'n':
            self.cinta[self.cabezal] = escribir

        # Actualizar estado
        self.estado = nuevo_estado

        # Call callback after state update but before movement
        if self.callback_paso:
            self.callback_paso(self)

        # Movimiento especial
        if mover == "R":
            self.cabezal += 1
        elif mover == "L":
            self.cabezal -= 1
        elif mover == "N":
            pass
        else:
            result = self.llamar_submaquina(mover)
            return result  # return the result of submachine execution

        # proteger límites
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
            print(f"no se encontro la maquina, mover: {mover}")
            return False

        # Set up submachine with current tape and position
        submaquina.cinta = self.cinta
        submaquina.cabezal = self.cabezal
        submaquina.estado = submaquina.estado_inicial
        
        # Set callback and delay for submachine
        if self.callback_paso:
            submaquina.set_callback_paso(self.callback_paso)
        submaquina.set_delay(self.delay)

        # Execute submachine
        #submaquina.ejecutar(delay=self.delay)
        resultado = submaquina.ejecutar(delay= self.delay)
        if not resultado:
            return false

        # Update current machine with changes from submachine
        self.cinta = submaquina.cinta
        self.cabezal = submaquina.cabezal

        return True

    def ejecutar(self, delay=0.1):
        while self.estado != self.estado_final:
            if self.running_flag and not self.running_flag():
                return False  # se detuvo desde la GUI
            if not self.paso():
                break
            time.sleep(delay)
        return True

class TuringMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Turing Machine Simulator")
        self.root.geometry("900x700")
        
        # Máquina de Turing
        self.maquina_actual = None
        self.running = False
        self.maquina_stack = []  # Stack to track machine calls
        
        self.setup_gui()
        self.initialize_submachines()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Parametros", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Number 1
        ttk.Label(input_frame, text="Numero 1 (decimal):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.num1_entry = ttk.Entry(input_frame, width=15)
        self.num1_entry.grid(row=0, column=1, padx=5)
        self.num1_entry.insert(0, "2")
        
        # Number 2
        ttk.Label(input_frame, text="Numero 2 (decimal):").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.num2_entry = ttk.Entry(input_frame, width=15)
        self.num2_entry.grid(row=1, column=1, padx=5)
        self.num2_entry.insert(0, "3")
        
        # Operator
        ttk.Label(input_frame, text="Operador (+, -, *, /):").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.operator_entry = ttk.Entry(input_frame, width=15)
        self.operator_entry.grid(row=2, column=1, padx=5)
        self.operator_entry.insert(0, "*")
        
        # Control buttons
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
        
        # Speed control
        ttk.Label(button_frame, text="Delay:").grid(row=0, column=4, padx=(20, 5))
        self.speed_var = tk.DoubleVar(value=0.5)
        self.speed_scale = ttk.Scale(button_frame, from_=0.1, to=2.0, variable=self.speed_var, 
                                   orient=tk.HORIZONTAL, length=100)
        self.speed_scale.grid(row=0, column=5, padx=5)
        
        # Machine info frame
        machine_frame = ttk.LabelFrame(main_frame, text="Ejecución", padding="5")
        machine_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(machine_frame, text="Maquina actual:").grid(row=0, column=0, sticky=tk.W)
        self.machine_label = ttk.Label(machine_frame, text="Ninguna", font=("Arial", 10, "bold"))
        self.machine_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(machine_frame, text="Estado actual:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.state_label = ttk.Label(machine_frame, text="Not started", font=("Arial", 10, "bold"))
        self.state_label.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Steps counter
        ttk.Label(machine_frame, text="Pasos:").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.steps_label = ttk.Label(machine_frame, text="0", font=("Arial", 10, "bold"))
        self.steps_label.grid(row=0, column=5, sticky=tk.W, padx=5)
        
        # Tape display
        tape_frame = ttk.LabelFrame(main_frame, text="Cinta", padding="5")
        tape_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Canvas for tape
        self.tape_canvas = tk.Canvas(tape_frame, height=120, bg='white', relief=tk.SUNKEN, borderwidth=1)
        self.tape_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = tk.Text(log_frame, height=12, width=80)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.step_count = 0
        
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
    
    def decimal_to_binary(self, decimal_str):
        """Convert decimal number to binary representation for the tape"""
        try:
            num = int(decimal_str)
            if num < 0:
                messagebox.showerror("Error", "Ingrese un numero positivo")
                return None
            return bin(num)[2:]
        except ValueError:
            messagebox.showerror("Error", "Ingrese un numero positivo")
            return None
    
    def create_tape_string(self, num1, num2, operator):
        """Create the initial tape string from inputs in binary format"""
        binary1 = self.decimal_to_binary(num1)
        binary2 = self.decimal_to_binary(num2)
        
        if binary1 is None or binary2 is None:
            return None
            
        return f"{binary1} {binary2} {operator} "
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def on_paso_callback(self, maquina):
        """Callback called after each step of any machine"""
        self.step_count += 1
        self.maquina_actual = maquina
        self.root.after(0, self.update_display)
    
    def update_display(self):
        """Update the tape visualization and state information"""
        if not self.maquina_actual:
            return
            
        # Clear canvas
        self.tape_canvas.delete("all")
        
        # Draw tape
        tape = self.maquina_actual.cinta
        head_pos = self.maquina_actual.cabezal
        
        cell_width = 40
        start_x = 20
        y_pos = 60
        
        # Draw tape cells
        for i, symbol in enumerate(tape):
            x = start_x + i * cell_width
            
            # Draw cell
            self.tape_canvas.create_rectangle(x, y_pos - 20, x + cell_width, y_pos + 20, 
                                            outline="black", fill="lightblue")
            
            # Draw symbol
            self.tape_canvas.create_text(x + cell_width // 2, y_pos, text=symbol, 
                                       font=("Arial", 12, "bold"))
            
            # Highlight current head position
            if i == head_pos:
                self.tape_canvas.create_rectangle(x, y_pos - 20, x + cell_width, y_pos + 20, 
                                                outline="red", width=3)
                # Draw head pointer
                self.tape_canvas.create_polygon(x + cell_width // 2 - 10, y_pos - 40,
                                              x + cell_width // 2 + 10, y_pos - 40,
                                              x + cell_width // 2, y_pos - 20,
                                              fill="red", outline="black")
                #self.tape_canvas.create_text(x + cell_width // 2, y_pos - 50, 
                #                           text="Cabezal", font=("Arial", 8, "bold"))
        
        # Update state information
        self.machine_label.config(text=self.maquina_actual.nombre)
        self.state_label.config(text=self.maquina_actual.estado)
        self.steps_label.config(text=str(self.step_count))
        
        # Log current state
        tape_str = "".join(tape)
        self.log(f"Step {self.step_count}: {self.maquina_actual.nombre} - State={self.maquina_actual.estado}, Position={head_pos}, Tape='{tape_str}'")
    
    def start_execution(self):
        """Start the Turing machine execution"""
        if self.running:
            return
            
        num1 = self.num1_entry.get().strip()
        num2 = self.num2_entry.get().strip()
        operator = self.operator_entry.get().strip()
        
        tape_str = self.create_tape_string(num1, num2, operator)
        if tape_str is None:
            return
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        self.step_count = 0
        
        self.maquina_actual = MaquinaTuring(tape_str, transiciones_iniciador, "s0", "s21", "Iniciador")
        self.maquina_actual.set_callback_paso(self.on_paso_callback)
        self.maquina_actual.set_delay(self.speed_var.get())
        self.maquina_actual.running_flag = lambda: self.running
        
        self.log("Starting Turing Machine...")
        self.log(f"Input: {num1} {operator} {num2}")
        self.log(f"Initial tape (binary): '{tape_str}'")
        
        self.update_display()
        
        # Start execution in a separate thread
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.step_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=self.run_machine)
        thread.daemon = True
        thread.start()
    
    def run_machine(self):
        """Run the machine continuously"""
        while (self.running and self.maquina_actual and 
               self.maquina_actual.estado != self.maquina_actual.estado_final):
            
            # Update delay dynamically from speed control
            delay = self.speed_var.get()
            self.maquina_actual.set_delay(delay)
            
            if not self.maquina_actual.paso():
                break
                
            time.sleep(delay)
        
        # Execution finished
        self.root.after(0, self.execution_finished)
    
    def step_execution(self):
        """Execute one step of the Turing machine"""
        if not self.maquina_actual:
            # Initialize machine if not already done
            num1 = self.num1_entry.get().strip()
            num2 = self.num2_entry.get().strip()
            operator = self.operator_entry.get().strip()
            
            tape_str = self.create_tape_string(num1, num2, operator)
            if tape_str is None:
                return
            
            self.maquina_actual = MaquinaTuring(tape_str, transiciones_iniciador, "s0", "s21", "Iniciador")
            self.maquina_actual.set_callback_paso(self.on_paso_callback)
            
            self.log_text.delete(1.0, tk.END)
            self.step_count = 0
            self.log("Turing Machine initialized for step-by-step execution")
            self.log(f"Input: {num1} {operator} {num2}")
            self.log(f"Initial tape (binary): '{tape_str}'")
        
        if self.maquina_actual.estado != self.maquina_actual.estado_final:
            self.maquina_actual.paso()
            
            if self.maquina_actual.estado == self.maquina_actual.estado_final:
                self.log(f"✅ {self.maquina_actual.nombre} completed execution!")
        else:
            self.log("Execution already completed!")
    
    def stop_execution(self):
        """Stop the execution"""
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.step_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Execution stopped by user")
    
    def execution_finished(self):
        """Called when execution finishes"""
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.step_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if self.maquina_actual:
            self.log("✅ Execution completed!")
            self.log(f"Final state: {self.maquina_actual.estado}")
            
            # Try to extract result from tape
            tape_str = "".join(self.maquina_actual.cinta)
            self.log(f"Final tape: '{tape_str}'")
    
    def reset_machine(self):
        """Reset the machine"""
        self.running = False
        self.maquina_actual = None
        self.step_count = 0
        
        self.tape_canvas.delete("all")
        self.machine_label.config(text="Not started")
        self.state_label.config(text="Not started")
        self.steps_label.config(text="0")
        self.log_text.delete(1.0, tk.END)
        
        self.start_button.config(state=tk.NORMAL)
        self.step_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        self.log("Machine reset")

def main():
    root = tk.Tk()
    app = TuringMachineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
