
import time

from transiciones import (
    transiciones_incrementador,
    transiciones_decrementador,
    transiciones_sumador,
    transiciones_copiar_en_resultado,
    transiciones_iniciador
)

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
        """Ejecuta la submáquina usando la misma cinta y cabezal."""
        if "S" not in self.submaquinas:
            print("⚠️  No hay submáquina registrada para 'S'")
            return

        submaquina = self.submaquinas[mover]
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

transiciones_incrementador = {
    ('s0', '0'): ('s0', 'n', 'R'),
    ('s0', '1'): ('s0', 'n', 'R'),
    ('s0', ' '): ('s1', 'n', 'L'),

    ('s1', '0'): ('s2', '1', 'N'),
    ('s1', '1'): ('s3', '0', 'L'),

    ('s3', '0'): ('s1', 'n', 'N'),
    ('s3', '1'): ('s1', 'n', 'N'),
    ('s3', ' '): ('s2', '1', 'L'),
}

transiciones_decrementador = {
    ('s0','0'): ('s0','n','R'),
    ('s0','1'): ('s0','n','R'),
    ('s0',' '): ('s1','n','L'),

    ('s1','0'): ('s1','1','L'),
    ('s1','1'): ('s2','0','N'),
    ('s1',' '): ('s2','n','N'),
}

transiciones_sumador = {
    ('s0','1'): ('s0','n','R'),
    ('s0','0'): ('s0','n','R'),
}

# esta maquina en realidad copia
transiciones_copiar_en_resultado = {
    ('s0','1'):('s1','A','R'),
    ('s0','0'):('s4','B','R'),
    ('s0',' '):('s8','n','L'),

    ('s1','0'):('s1','n','R'),
    ('s1','1'):('s1','n','R'),
    ('s1',' '):('s1','n','R'),
    ('s1','+'):('s2','n','R'),
    ('s1','-'):('s2','n','R'),
    ('s1','*'):('s2','n','R'),
    ('s1','/'):('s2','n','R'),
 
    ('s2',' '):('s3','n','R'),
    
    ('s3','0'):('s3','n','R'),
    ('s3','1'):('s3','n','R'),
    ('s3',' '):('s7','1','L'), 

    ('s4','0'):('s4','n','R'),
    ('s4','1'):('s4','n','R'),
    ('s4',' '):('s4','n','R'),
    ('s4','+'):('s5','n','R'),
    ('s4','-'):('s5','n','R'),
    ('s4','*'):('s5','n','R'),
    ('s4','/'):('s5','n','R'),
   
    ('s5',' '):('s6','n','R'),

    ('s6','0'):('s6','n','R'),
    ('s6','1'):('s6','n','R'),
    ('s6',' '):('s7','0','L'), 

    ('s7','1'):('s7','n','L'),
    ('s7','0'):('s7','n','L'),
    ('s7',' '):('s7','n','L'),
    ('s7','+'):('s7','n','L'),
    ('s7','-'):('s7','n','L'),
    ('s7','*'):('s7','n','L'),
    ('s7','/'):('s7','n','L'),
    ('s7','A'):('s0','n','R'),
    ('s7','B'):('s0','n','R'),

    ('s8','A'):('s8','1','L'),
    ('s8','B'):('s8','0','L'),
    ('s8',' '):('s9','n','R'),
}

transiciones_iniciador = {
    ('s0','1'):('s0','n','R'),
    ('s0','0'):('s0','n','R'),
    ('s0',' '):('s0','n','R'),
    ('s0','+'):('s1','n','L'),
    ('s0','-'):('s','n','L'),
    ('s0','*'):('s','n','L'),
    ('s0','/'):('s','n','L'),

    ('s1',' '):('s3','n','L'),

    ('s3','0'):('s3','n','L'),
    ('s3','1'):('s3','n','L'),
    ('s3',' '):('s4','n','L'),

    ('s4','0'):('s4','n','L'),
    ('s4','1'):('s4','n','L'),
    ('s4',' '):('s5','n','R'),

    ('s5','1'):('s20','n','S'),
}
if __name__ == "__main__":
    incrementador = MaquinaTuring("", transiciones_incrementador,"s0","s2")
    decrementador = MaquinaTuring("", transiciones_decrementador,"s0","s2") 
    copiar_en_resultado = MaquinaTuring("", transiciones_copiar_en_resultado, "s0","s9")
    sumador = MaquinaTuring("", transiciones_sumador,"s0","s1")

    iniciador = MaquinaTuring(
        "1110 101 + ",
        transiciones_iniciador,
        "s0",
        "s9",
        submaquinas={"I": incrementador, "D": decrementador, "CaR": copiar_en_resultado,"S":sumador}
    )

    iniciador.ejecutar()

