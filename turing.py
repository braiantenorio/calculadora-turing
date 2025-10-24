
import time

 
transiciones_sumador = {   
   
    ('s0', '0'): ('s0', 'n', 'R'),   
    ('s0', '1'): ('s0', 'n', 'R'),   
    ('s0', '+'): ('s0', 'n', 'R'),   
    ('s0', ' '): ('s1', 'n', 'L'),  
   
    ('s1', '0'): ('s2', 'c', 'L'),     
    ('s1', '1'): ('s5', 'c', 'L'),  
    ('s1', '+'): ('s9', ' ', 'L'),
   
    ('s2', '0'): ('s2', 'n', 'L'),   
    ('s2', '1'): ('s2', 'n', 'L'),  
    ('s2', '+'): ('s3', 'n', 'L'),  
   
    ('s3', 'O'): ('s3', 'n', 'L'),   
    ('s3', 'I'): ('s3', 'n', 'L'),   
    ('s3', '0'): ('s4', 'O', 'R'),  
    ('s3', ' '): ('s4', 'O', 'R'),   
    ('s3', '1'): ('s4', 'I', 'R'),   
   
    ('s4', '0'): ('s4', 'n', 'R'),
    ('s4', '1'): ('s4', 'n', 'R'),   
    ('s4', 'O'): ('s4', 'n', 'R'),   
    ('s4', 'I'): ('s4', 'n', 'R'),   
    ('s4', '+'): ('s4', 'n', 'R'),   
    ('s4', 'c'): ('s1', '0', 'L'),   
   
    ('s5', '0'): ('s5', 'n', 'L'),   
    ('s5', '1'): ('s5', 'n', 'L'),   
    ('s5', '+'): ('s6', 'n', 'L'),     
   
    ('s6', 'O'): ('s6', 'n', 'L'),   
    ('s6', 'I'): ('s6', 'n', 'L'),   
    ('s6', '1'): ('s7', 'O', 'L'),   
    ('s6', '0'): ('s8', 'I', 'R'),   
    ('s6', ' '): ('s8', 'I', 'R'),   
   
    ('s7', '1'): ('s7', '0', 'L'),   
    ('s7', '0'): ('s8', '1', 'R'),   
    ('s7', ' '): ('s8', '1', 'R'),   
   
    ('s8', '0'): ('s8', 'n', 'R'),   
    ('s8', '1'): ('s8', 'n', 'R'),   
    ('s8', 'O'): ('s8', 'n', 'R'),   
    ('s8', 'I'): ('s8', 'n', 'R'),   
    ('s8', '+'): ('s8', 'n', 'R'),   
    ('s8', 'c'): ('s1', '1', 'L'),   
   
    ('s9', '0'): ('s9', 'n', 'L'),   
    ('s9', '1'): ('s9', 'n', 'L'),   
    ('s9', 'I'): ('s9', '1', 'L'),   
    ('s9', 'O'): ('s9', '0', 'L'),   
    ('s9', ' '): ('s10', 'n', 'R'),   
   
}   
   

class MaquinaTuring:
    def __init__(self, cinta, transiciones, estado_inicial, estado_final):
        """
        cinta: lista o string inicial con los símbolos (ej: '101$')
        transiciones: dict { (estado, simbolo): (nuevo_estado, escribir, mover) }
        estado_inicial: string
        estado_final: string
        """
        self.cinta = list(cinta)
        self.transiciones = transiciones
        self.estado = estado_inicial
        self.estado_final = estado_final
        self.cabezal = 0

    def paso(self):
        """Ejecuta un paso de la máquina."""
        simbolo = self.cinta[self.cabezal]
        clave = (self.estado, simbolo)

        if clave not in self.transiciones:
            print(f"⚠️  No hay transición definida para {clave}")
            return False

        nuevo_estado, escribir, mover = self.transiciones[clave]
        # Escribir en la cinta
        if escribir != 'n':  # 'n' = no escribir
            self.cinta[self.cabezal] = escribir

        # Actualizar estado
        self.estado = nuevo_estado

        if mover in ["R", "L", "N"]:
            if mover == "R":
                self.cabezal += 1
            elif mover == "L":
                self.cabezal -= 1
        elif mover.startswith(("RT", "LT")):
            self.mover_especial(mover)

# para que no se salga de rango
        if self.cabezal >= len(self.cinta):
            self.cinta.append(' ')
        elif self.cabezal < 0:
            self.cinta.insert(0, ' ')
            self.cabezal = 0

        return True

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
    
    ('s2','1'):('s3','n','S'),
    ('s2','0'):('s3','n','S'),
}

if __name__ == "__main__":
    # Crear y ejecutar el visualizador
    mt_visual = MaquinaTuring("111+101", transiciones_iniciador, "s0", "s3")
    mt_visual.ejecutar()
