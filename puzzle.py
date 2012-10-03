#!/usr/bin/env python2
"""
Codigo para resolver el 8puzzle
"""

from copy import deepcopy
import sqlite3
from random import choice

class State(list):
    def __init__(self, state):
        list.__init__(self, state)


    def __str__(self):
        return "{} {} {} \n{} {} {}\n{} {} {}".format(*self)


SOLVE = State([1, 2, 3, 4, 5, 6, 7, 8 ,0])
DB = sqlite3.connect('ia.db')


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
        for _ in xrange(moves):
            possibles = self.get_possible_moves()
            self.state = choice(possibles)
        # self.register.add(self.state)

    def solve(self):
        pass

    def get_possible_moves(self):
        """devuelve una listo de posibles estados a partir del actual."""
        pos = self.state.index(0)
        moves = []
        for ady in self._get_adyacentes(pos):
            moves.append(self._switch(pos, ady, State(self.state)))
        return moves

    def is_solve(self):
        """Chequea si esta terminado"""
        return self.state == SOLVE

    def move(self, new_state):
        self.state = new_state
        self._register.add(self.state)

    def _get_adyacentes(self, pos):
        """Devuelve los indices de los posibles movimientos de  posicion"""
        adyacentes = []
        for i in (-1, 1):
            ady = pos + i
            if ady / 3 == pos / 3:
                adyacentes.append(ady)

        for i in (3, -3):
            ady = pos + i
            if 0 < ady < 8:
                adyacentes.append(ady)

        return adyacentes

    def _switch(self, from_, to, state=None):
        """Cambia la posicion de 2 elementos dados"""
        if state is None:
            state = self.state

        state[from_], state[to] = state[to], state[from_]
        return state


class Register(object):
    """Alamcena los movimiento y los padres en una bd.
    Es una sola tabla, tiene la siguiente forma.
    id | hash | move | padre_id

    TODO: faltan columnas en la tabla. LEA los tiene anotado.
    Agregalos en este string y borra este TODO.
    """

    def __init__(self):
        """si la tabla tiene elementos => eliminarlos"""
        try:
            cursor = DB.cursor()
            cursor.execute("SELECT count(*) FROM puzzle")

            if cursor.fetchone()[0] > 0:
                cursor.execute("DELETE FROM puzzle")
                DB.commit()

        except sqlite3.OperationalError, e:
            print "SQL error {}.".format(e)

        finally:
            cursor.close()

    def add(self, hash_, state, padre):
        """Un Insert en la tabla"""
        try:
            cursor = DB.cursor()
            cursor.execute("INSERT INTO puzzle VALUES(NULL, ?, ?, ?)",
                           (hash_, state, padre))
            DB.commit()

        except sqlite3.OperationalError, e:
            print "SQL error {}.".format(e)


p = Puzzle()
print p.state
print "suffle"

p.suffle()
