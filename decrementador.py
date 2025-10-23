
from turing import MaquinaTuring


transiciones_decrementador = {
    ('s0','0'): ('s0','n','R'),
    ('s0','1'): ('s0','n','R'),
    ('s0','$'): ('s1','n','L'),

    ('s1','0'): ('s1','1','L'),
    ('s1','1'): ('s2','0','N'),
    ('s1','$'): ('s2','n','N'),
}

# g ag creo que faltan si llega un =

mt = MaquinaTuring("111$", transiciones_decrementador, "s0", "s2")
mt.ejecutar(delay=0.5)
