from turing import MaquinaTuring

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

mt = MaquinaTuring("111", transiciones_incrementador, "s0", "s2")
mt.ejecutar(delay=0.5)
