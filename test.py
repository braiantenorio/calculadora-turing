
import time

class MaquinaTuring:
    def __init__(self, cinta, transiciones, estado_inicial, estado_final, submaquinas=None):
        """
        cinta: lista o string inicial con los símbolos (ej: '101$')
        transiciones: dict { (estado, simbolo): (nuevo_estado, escribir, mover) }
        estado_inicial: string
        estado_final: string
        submaquinas: dict opcional { 'S': funcion_o_objeto_maquina }
        """
        self.cinta = list(cinta)
        self.transiciones = transiciones
        self.estado = estado_inicial
        self.estado_final = estado_final
        self.cabezal = 0
        self.submaquinas = submaquinas or {}

    def paso(self):
        """Ejecuta un paso de la máquina."""
        simbolo = self.cinta[self.cabezal]
        clave = (self.estado, simbolo)

        if clave not in self.transiciones:
            print(f"⚠️  No hay transición definida para {clave}")
            return False

        nuevo_estado, escribir, mover = self.transiciones[clave]
        
        # Escribir en la cinta
        if escribir != 'n':
            self.cinta[self.cabezal] = escribir

        # Actualizar estado
        self.estado = nuevo_estado

        # Movimiento especial
        if mover == "R":
            self.cabezal += 1
        elif mover == "L":
            self.cabezal -= 1
        elif mover == "S":
            # 'S' significa: detener y lanzar submáquina (si existe)
            self.llamar_submaquina()
            return False  # detener ejecución principal

        # proteger límites
        if self.cabezal >= len(self.cinta):
            self.cinta.append(' ')
        elif self.cabezal < 0:
            self.cinta.insert(0, ' ')
            self.cabezal = 0

        return True


    def llamar_submaquina(self):
        """Ejecuta la submáquina usando la misma cinta y cabezal."""
        if "S" not in self.submaquinas:
            print("⚠️  No hay submáquina registrada para 'S'")
            return

        submaquina = self.submaquinas["S"]
        print("🔁 Ejecutando submáquina (compartiendo cinta)...\n")

        # Sincronizar cinta y cabezal
        submaquina.cinta = self.cinta
        submaquina.cabezal = self.cabezal

        # Ejecutar la submáquina
        submaquina.ejecutar()

        # Recuperar cinta y cabezal modificados
        self.cinta = submaquina.cinta
        self.cabezal = submaquina.cabezal

        print("↩️  Submáquina finalizada. Cambios preservados.\n")

    def ejecutar(self, delay=0.3):
        """Ejecuta toda la máquina paso a paso."""
        while self.estado != self.estado_final:
            self.mostrar()
            if not self.paso():
                break
            time.sleep(delay)
        self.mostrar()
        print("✅ Máquina detenida en estado final:", self.estado)

    def mostrar(self):
        """Imprime la cinta y la posición del cabezal."""
        cinta_str = "".join(self.cinta)
        indicador = " " * self.cabezal + "^"
        print(f"{cinta_str}\n{indicador}  Estado: {self.estado}\n")


transiciones_iniciador = {
    ('s0','1'):('s0','n','R'),
    ('s0','0'):('s0','n','R'),
    ('s0','+'):('s1','n','L'),

    ('s1','1'):('s1','n','L'),
    ('s1','0'):('s1','n','L'),
    ('s1',' '):('s2','n','R'),
    
    ('s2','1'):('s3','n','S'),  # Aquí lanzará el sumador
    ('s2','0'):('s3','n','S'),
}


if __name__ == "__main__":
    sumador = MaquinaTuring("111+101", transiciones_sumador, "s0", "s10")

    incrementador = MaquinaTuring("", transiciones_incrementador,"s0","")
    decrementador = MaquinaTuring("", transiciones_decrementador,"s0","") 

    iniciador = MaquinaTuring(
        "111+101",
        transiciones_iniciador,
        "s0",
        "s3",
        submaquinas={"I": incrementador, "D": decrementador}
    )

    iniciador.ejecutar()

