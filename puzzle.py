#!/usr/bin/env python2
"""
Codigo para resolver el 8puzzle
"""

import sqlite3
from random import choice

class State(list):
    counter = 0

    def __init__(self, state, nivel=0 ):
        list.__init__(self, state)
        self.nivel = nivel
        self.id_ = State.counter
        State.counter += 1

    def set_nivel(self, nivel):
        self.nivel = nivel

    def __str__(self):
        return "nivel = {}\nid = {}\n{} {} {} \n{} {} {}\n{} {} {}".format(
            self.nivel, self.id_, *self)

    def to_db(self):
        return "{}{}{}{}{}{}{}{}{}".format(*self)

    def is_solve(self):
        """Chequea si esta terminado"""
        return self == SOLVE



SOLVE = State([1, 2, 3, 4, 5, 6, 7, 8 ,0])
DB = sqlite3.connect('ia.db')


class Puzzle(object):
    def __init__(self):
        self.state = State(SOLVE)
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

    def solve(self, step_by_step=False):
        if self.state.is_solve():
            print "Srly, bitch? ya esta resuelto"
            return

        hijos = list()
        id_ = 1

        while True:
            nuevos = self.get_possible_moves()
            # check si ya estan en la bd
            map(lambda state:state.set_nivel(self.state.nivel + 1), nuevos)

            for state in nuevos:
                if state.is_solve():
                    self.state = state
                    return

            hijos.extend(nuevos)
            self.state = hijos.pop(0)

            if step_by_step:
                print self.state
                raw_input("seguir?")


    def get_possible_moves(self):
        """devuelve una listo de posibles estados a partir del actual."""
        pos = self.state.index(0)
        moves = []
        for ady in self._get_adyacentes(pos):
            moves.append(self._switch(pos, ady, State(self.state)))
        return moves


    # def move(self, new_state):
    #     self.state = new_state
    #     self._register.add(self.state.to_db())

    def _get_adyacentes(self, pos):
        """Devuelve los indices de los posibles movimientos de  posicion"""
        adyacentes = []
        for i in (-1, 1):
            ady = pos + i
            if ady / 3 == pos / 3:
                adyacentes.append(ady)

        for i in (3, -3):
            ady = pos + i
            if 0 <= ady <= 8:
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
# p.suffle(20)
# print p.state


p.state = State([1, 4, 0, 7, 6, 2, 5, 3, 8])

# p.solve(True)
p.solve()
print p.state

