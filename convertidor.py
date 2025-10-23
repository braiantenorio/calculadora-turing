
from turing import MaquinaTuring

class Convertidor(MaquinaTuring):
    def __init__(self, cinta):
        transiciones = {
            # s0
            ('s0', '0'): ('s1', 'n', 'RT-'),
            ('s0', '1'): ('s1', 'n', 'RT-'),
            ('s0', '$'): ('s1', 'n', 'RT-'),
            ('s0', '+'): ('s1', 'n', 'RT-'),
            ('s0', '-'): ('s1', 'n', 'R'),

            # s1
            ('s1', '0'): ('s1', 'n', 'R'),
            ('s1', '1'): ('s1', 'n', 'R'),
            ('s1', '$'): ('s2', 'n', 'L'),
            ('s1', '+'): ('s2', 'n', 'L'),
            ('s1', '-'): ('s1', 'n', 'R'),

            # s2
            ('s2', '0'): ('s2', 'n', 'L'),
            ('s2', '1'): ('s3', 'n', 'L'),
            ('s2', '$'): ('s4', 'n', 'R'),

            # s3
            ('s3', '0'): ('s3', '0', 'L'),
            ('s3', '1'): ('s3', '1', 'L'),
            ('s3', '+'): ('s4', 'n', 'R'),
            ('s3', '-'): ('s4', 'n', 'N'),

            # s4 (estado final)
            ('s4', '0'): ('s4', 'n', 'N'),
            ('s4', '1'): ('s4', 'n', 'N'),
            ('s4', '$'): ('s4', 'n', 'N'),
            ('s4', '+'): ('s4', 'n', 'N'),
            ('s4', '-'): ('s4', 'n', 'N'),
        }

        super().__init__(cinta, transiciones, 's0', 's4')


# --- Ejemplo de prueba ---
if __name__ == "__main__":
    cinta = list("101-10$")
    mt = Convertidor(cinta)
    mt.ejecutar(delay=0.4)
