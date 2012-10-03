#!/usr/bin/env python2
"""
Codigo para resolver el 8puzzle
"""

from copy import deepcopy
import sqlite3


SOLVE = (1, 2, 3, 4, 5, 6, 7, 8 ,0)

class Puzzle(object):
    def __init__(self):
        self.state = deepcopy(SOLVE)
        self._register = Register()
        # estado de las fichas en el tablero
        # 0 es el espacio en blanco
        # empieza armado

    def suffle(self, moves=100):
        """Mezcla aleatoriamente el tablero. Reliza <moves> movimientos
        Los pasos intermedios no se almacenan en la bd. Solo el desarmado"""
        #         self.register.add(self.state)
        pass

    def get_possible_moves(self):
        """devuelve una listo de posibles estados
        a partir del actual."""
        pass

    def is_solve(self):
        """Chequea si esta terminado"""
        return self.state == SOLVE

    def move(self, new_state):
        self.state = new_state
        self._register.add(self.state)

    def __str__(self):
        return "{} {} {} \n{} {} {}\n{} {} {}".format(*self.state)


class Register(object):
    """Alamcena los movimiento y los padres en una bd.
    Es una sola tabla, tiene la siguiente forma.
    id | hash | move | padre_id

    TODO: faltan columnas en la tabla. LEA los tiene anotado.
    Agregalos en este string y borra este TODO.
    """

    def __init__(self):
        # if not (existe la bd en el motor con la tabla):
        #    crearla
        # else:
        #    limpiar la tabla
        pass

    def add(self, line):
        """Inserta la linea en la tabla"""
        pass

print Puzzle()
