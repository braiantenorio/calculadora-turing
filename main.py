
import time

from transiciones import (
        transiciones_incrementador,
        transiciones_decrementador,
        transiciones_sumador,
        transiciones_copiar_en_resultado,
        transiciones_iniciador
        )

class MaquinaTuring:
    submaquinas_globales = {}

    def __init__(self, cinta, transiciones, estado_inicial, estado_final, submaquinas=None):
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
        else:
            self.llamar_submaquina(mover)
            return False  # detener ejecución principal

        # proteger límites
        if self.cabezal >= len(self.cinta):
            self.cinta.append(' ')
        elif self.cabezal < 0:
            self.cinta.insert(0, ' ')
            self.cabezal = 0

        return True


    def llamar_submaquina(self, mover):
        print("🔁 Ejecutando submáquina (compartiendo cinta)...\n")

        if mover in self.submaquinas:
            submaquina = self.submaquinas[mover]
        else:
            submaquina = MaquinaTuring.submaquinas_globales.get(mover,None)

        if submaquina is None:
            print("no se encontro la maquina")
            return


        submaquina.cinta = self.cinta
        submaquina.cabezal = self.cabezal

        submaquina.ejecutar()

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

if __name__ == "__main__":
    incrementador = MaquinaTuring("", transiciones_incrementador,"s0","s2")
    decrementador = MaquinaTuring("", transiciones_decrementador,"s0","s2") 
    copiar_en_resultado = MaquinaTuring("", transiciones_copiar_en_resultado, "s0","s9")
    sumador = MaquinaTuring("", transiciones_sumador,"s0","s1")

    MaquinaTuring.submaquinas_globales = {"I": incrementador, "D": decrementador, "CaR": copiar_en_resultado,"S":sumador}


    iniciador = MaquinaTuring(
            "1110 101 + ",
            transiciones_iniciador,
            "s0",
            "s9"    )

    iniciador.ejecutar()

