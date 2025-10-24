# sumador_mejorado.py
from turing import MaquinaTuring

transiciones_sumador_mejorado = {
    # Estado s0: buscar el final de la cadena
    ('s0', '0'): ('s0', 'n', 'R'),
    ('s0', '1'): ('s0', 'n', 'R'),
    ('s0', '+'): ('s0', 'n', 'R'),
    ('s0', '='): ('s1', 'n', 'L'),
    ('s0', '$'): ('s0', 'n', 'R'),

    # Estado s1: posicionarse en el último bit del segundo número
    ('s1', '0'): ('s2', 'n', 'L'),
    ('s1', '1'): ('s3', 'n', 'L'),
    ('s1', '+'): ('s1', 'n', 'L'),
    ('s1', '$'): ('s7', 'n', 'N'),  # sin más bits

    # Estado s2: bit 0 del segundo número
    ('s2', '0'): ('s4', '0', 'L'),
    ('s2', '1'): ('s4', '1', 'L'),
    ('s2', '+'): ('s7', 'n', 'N'),
    ('s2', '$'): ('s7', 'n', 'N'),

    # Estado s3: bit 1 del segundo número
    ('s3', '0'): ('s4', '1', 'L'),
    ('s3', '1'): ('s5', '0', 'L'),
    ('s3', '+'): ('s6', '1', 'N'),  # acarreo final
    ('s3', '$'): ('s6', '1', 'N'),

    # Estado s4: escribir resultado y retroceder
    ('s4', '0'): ('s4', 'n', 'L'),
    ('s4', '1'): ('s4', 'n', 'L'),
    ('s4', '+'): ('s1', 'n', 'L'),
    ('s4', '$'): ('s7', 'n', 'N'),

    # Estado s5: manejar acarreo
    ('s5', '0'): ('s4', '1', 'L'),
    ('s5', '1'): ('s5', '0', 'L'),
    ('s5', '+'): ('s6', '1', 'N'),
    ('s5', '$'): ('s6', '1', 'N'),

    # Estado s6: acarreo final pendiente
    ('s6', '0'): ('s6', 'n', 'L'),
    ('s6', '1'): ('s6', 'n', 'L'),
    ('s6', '+'): ('s6', 'n', 'L'),
    ('s6', '$'): ('s7', '1', 'R'),  # insertar acarreo final

    # Estado final
    ('s7', '0'): ('s7', 'n', 'N'),
    ('s7', '1'): ('s7', 'n', 'N'),
    ('s7', '+'): ('s7', 'n', 'N'),
    ('s7', '='): ('s7', 'n', 'N'),
    ('s7', '$'): ('s7', 'n', 'N'),
}

# Pruebas
if __name__ == "__main__":
    pruebas = [
        "101+11=$",  # 5 + 3 = 8 (1000)
        "10+1=$",    # 2 + 1 = 3 (11)
        "1+1=$",     # 1 + 1 = 2 (10)
    ]
    
    for prueba in pruebas:
        print(f"\nProbando: {prueba}")
        mt = MaquinaTuring(prueba, transiciones_sumador_mejorado, "s0", "s7")
        mt.ejecutar(delay=0.3)
