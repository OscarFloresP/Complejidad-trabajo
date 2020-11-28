#Librerias y referencias
from regla import *
import random
import copy
from sys import maxsize
minint = -maxsize - 1

#seleccionamos los limites para identificar los limites donda gana cada jugador
winnerRow = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
winnerRow1 = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
oppRow = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
oppRow1 =  [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]

class BOT(Jugador):
    def __init__(self, num):
        super(BOT, self).__init__(num)
        if self.jugador_num == 1:
            self.win_fila = winnerRow
            self.opp_fila = oppRow
            self.opp = 0
        else:
            self.opp_fila =oppRow1
            self.win_fila = winnerRow1
            self.opp = 1

#Algoritmo para verificar el funcionamiento del bot
class Minimax(BOT):
    def __init__(self, num):
        super(Minimax, self).__init__(num)

    def finalMovimiento(self, ruler):
        movimientos = {}
        posible_paredes = self.wallOption(ruler)
        posible_movimientos = self.wayOptions(ruler)
       
        for m in posible_movimientos:
            node = Node(self.jugador_num, ruler, "movimiento", None, m.x, m.y)
            movimientos[node] = self.miniMax(node, 0, True)
        for w in posible_paredes:
            node = Node(self.jugador_num, ruler, "pared", w)
            movimientos[node] = self.miniMax(node, 0, True)

        movimiento = max(movimientos, key=movimientos.get)

        if movimiento.movimiento_type == "movimiento":
            self.movimiento(movimiento.movimientoX,
                            movimiento.movimientoY, ruler)
        else:
            self.colocar_pared(ruler, movimiento.pared)

    def miniMax(self, node, depth, Maximizing):
        if depth == 0 or self.ganadorMovimiento(node):
            return self.heuristic(node, node.ruler)

        if Maximizing:
            bestValue = minint
            bestMovimiento = None
            hijos = node.hijos(Maximizing)
            for child in hijos:
                v = self.miniMax(child, depth - 1, False)
                bestValue = max(bestValue, v)
            return bestValue

        else:
            bestValue = maxsize
            hijos = node.hijos(Maximizing)
            for child in hijos:
                v = self.miniMax(child, depth - 1, True)
                bestValue = min(bestValue, v)
            return bestValue

    def ganadorMovimiento(self, node):
        if node.movimiento_type == "movimiento":
            if (node.movimientoX, node.movimientoY) in self.win_fila:
                return True
        return False

    def heuristic(self, node, ruler):
        opp = ruler.jugadores[self.opp]
        if node.movimiento_type == "movimiento":
            minMovimientoCamino = minCaminoLen(
                node.movimientoX, node.movimientoY, self.win_fila, ruler)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, ruler)
            return minOppCamino - minMovimientoCamino
        else:
            ruler.paredes = ruler.paredes + [node.pared]
            minWinCamino = minCaminoLen(self.x, self.y, self.win_fila, ruler)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, ruler)
            ruler.paredes = ruler.paredes[:-1]
            return minOppCamino - minWinCamino

#Nodos
class Node:
    def __init__(self, jugador_num, ruler, movimiento_type, pared=None, movimientoX=None, movimientoY=None):
        self.movimiento_type = movimiento_type
        self.pared = pared
        self.movimientoX = movimientoX
        self.movimientoY = movimientoY
        self.jugador_num = jugador_num
        new_ruler = copy.deepcopy(ruler)
        if self.movimiento_type == "movimiento":
            new_ruler.jugadores[self.jugador_num].x = self.movimientoX
            new_ruler.jugadores[self.jugador_num].y = self.movimientoY
        else:
            new_ruler.jugadores[self.jugador_num].colocar_pared(
                new_ruler, self.pared)

        self.ruler = new_ruler
        self.opp_num = new_ruler.jugadores[self.jugador_num].opp

    def hijos(self, Maximizing):
        hijos = []
        oponente_posible_movimientos = self.ruler.jugadores[self.opp_num].wayOptions(
            self.ruler, True)
        oponente_posible_paredes = self.ruler.jugadores[self.jugador_num].wallOption(
            self.ruler, True)
        for m in oponente_posible_movimientos:
            node = Node(self.opp_num, self.ruler, "movimiento", None, m.x, m.y)
            hijos.append(node)
        for w in oponente_posible_paredes:
            hijos.append(Node(self.opp_num, self.ruler, "pared", w))
        return hijos


def minCaminoLen(x, y, win_fila, ruler):
    minCamino = maxsize
    for fin in win_fila:
        camino_len = regla.camino((x, y), fin, ruler)
        if camino_len < minCamino:
            minCamino = camino_len
    return minCamino
