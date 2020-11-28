#Librerias y referencias
import copy
import random
import regla
from sys import maxsize

##Esta parte fue codificada de un github de damas y de un juego incompleto en github como referencia 
class Jugador(object):
    def __init__(self, jugador_num):
        self.paredes = 10 # el juego pide solo 10
        self.jugador_num = jugador_num #de normal deben ser 2
        self.ganador_posicion = False

        if (jugador_num == 0):
            self.x = 4
            self.y = 0
            self.opp = 1
        elif (jugador_num == 1):
            self.x = 4
            self.y = 8
            self.opp = 0

        self.pared_opciones = []
        for i in range(8):
            for j in range(8):
                for k in ["horizontal", "vertical"]:
                    top_l = Casilla(i, j)
                    top_r = Casilla(i + 1, j)
                    IAl = Casilla(i, j + 1)
                    IAr = Casilla(i + 1, j + 1)
                    pared = Pared(top_l, top_r, IAl, IAr, k)
                    self.pared_opciones.append(pared)

    def movimiento(self, x, y, tablero):
        if self.legal_movimiento(x, y, tablero):
            self.x = x
            self.y = y
            if self.jugador_num == 0 and self.y == 8:
                self.ganador_posicion = True
            elif self.jugador_num == 1 and self.y == 0:
                self.ganador_posicion = True
        else:
            raise ("Movimento no permitido")

    def colocar_pared(self, tablero, pared):
        if self.legal_colocamiento(tablero, pared):
            self.paredes -= 1
            tablero.paredes.append(pared)
        else:
            raise ("No es valido colocar la pared")

    def legal_movimiento(self, x, y, tablero):

        if (x < 0 or x > 8 or y < 0 or y > 8):
            return False

        if (self.x == x and self.y == y):
            return False

        if (not self.legal_saltar(x, y, tablero) and (
                abs(self.y - y) > 1 or abs(self.x - x) > 1 or (abs(self.y - y) == 1 and abs(self.x - x) == 1))):
            return False

        if self.ocupado(x, y, tablero):
            return False
 
        if self.bloqueado(self.x, self.y, x, y, tablero):
            return False
        return True

    def ocupado(self, x, y, b):
        if (self.jugador_num == 0 and b.jugadores[1].x == x and b.jugadores[1].y == y):
            return True
        if (self.jugador_num == 1 and b.jugadores[0].x == x and b.jugadores[0].y == y):
            return True
        return False

    def legal_saltar(self, x, y, b):
        if self.jugador_num == 0:
            opp_num = 1
        else:
            opp_num = 0

        oppx = b.jugadores[opp_num].x
        oppy = b.jugadores[opp_num].y

        if (self.adyacente(self.x, self.y, oppx, oppy) and self.adyacente(oppx, oppy, x, y) and (
        not self.bloqueado(oppx, oppy, x, y, b))):
            if (not self.bloqueado(self.x, self.y, oppx, oppy, b)):
                logicalx = self.x
                logicaly = self.y
                if self.x < oppx:
                    logicalx = oppx + 1
                elif self.x > oppx:
                    logicalx = oppx - 1

                if self.y < oppy:
                    logicaly = oppy + 1
                elif self.y > oppy:
                    logicaly = oppy - 1

                if self.bloqueado(oppx, oppy, logicalx, logicaly, b) or (logicaly < 0) or (logicaly > 8) or (
                        logicalx < 0) or (logicalx > 8):
                    return True
                if x == logicalx and y == logicaly:
                    return True

        return False

    def bloqueado(self, x1, y1, x2, y2, tablero):
        for pared in tablero.paredes:
            if (pared.orientacion == "horizontal"):
                if (y1 < y2):
                    if (pared.top_l.y == y1 and (pared.top_l.x == x1 or (pared.top_l.x + 1) == x1)):
                        return True
                if (y1 > y2):
                    if (pared.top_l.y == y2 and (pared.top_l.x == x2 or (pared.top_l.x + 1) == x2)):
                        return True
            if (pared.orientacion == "vertical"):
                if (x1 < x2):
                    if (pared.top_l.x == x1 and (pared.top_l.y == y1 or (pared.top_l.y + 1) == y1)):
                        return True
                if (x1 > x2):
                    if (pared.top_l.x == x2 and (pared.top_l.y == y2 or (pared.top_l.y + 1) == y2)):
                        return True
        return False

    def adyacente(self, x1, y1, x2, y2):
        if ((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or (abs(y1 - y2) == 1 and abs(x1 - x2) == 0)):
            return True
        return False

    def legal_colocamiento(self, tablero, pared):

        if self.paredes == 0:
            return False
        if (pared.top_l.x < 0 or pared.top_l.x > 8 or pared.top_l.y < 0 or pared.top_l.y > 8):
            return False
        # Posicion no choca
        for w in tablero.paredes:
            if w.orientacion == "horizontal" and pared.orientacion == "horizontal":
                if w.top_l.y == pared.top_l.y and ((w.top_l.x == pared.top_l.x) or (w.top_l.x - 1 == pared.top_l.x) or (
                        w.top_l.x + 1 == pared.top_l.x)):
                    return False
            if w.orientacion == "vertical" and pared.orientacion == "vertical":
                if w.top_l.x == pared.top_l.x and ((w.top_l.y == pared.top_l.y) or (w.top_l.y - 1 == pared.top_l.y) or (
                        w.top_l.y + 1 == pared.top_l.y)):
                    return False
            if (w.top_l.x == pared.top_l.x and w.top_l.y == pared.top_l.y):
                return False
        if not self.isWay(tablero, pared):
            return False

        return True

    def isWay(self, b, w):
        b.paredes = b.paredes + [w]
        p1_camino = False
        p2_camino = False
        win_fila1 = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
        win_fila2 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]

        for casilla in win_fila1:
            if bfs((b.jugadores[0].x, b.jugadores[0].y), casilla, b):
                p1_camino = True
        for casilla in win_fila2:
            if bfs((b.jugadores[1].x, b.jugadores[1].y), casilla, b):
                p2_camino = True
        b.paredes = b.paredes[:-1]
        return (p1_camino and p2_camino)

    def wayOptions(self, regla, oponente=False):
        movimientos = []
        if not oponente:
            movimientos.append(Casilla(self.x, self.y - 1))
            movimientos.append(Casilla(self.x, self.y + 1))
            movimientos.append(Casilla(self.x + 1, self.y))
            movimientos.append(Casilla(self.x - 1, self.y))
            movimientos.append(Casilla(self.x, self.y - 2))
            movimientos.append(Casilla(self.x, self.y + 2))
            movimientos.append(Casilla(self.x - 2, self.y))
            movimientos.append(Casilla(self.x + 2, self.y))
            movimientos.append(Casilla(self.x - 1, self.y - 1))
            movimientos.append(Casilla(self.x + 1, self.y + 1))
            movimientos.append(Casilla(self.x + 1, self.y - 1))
            movimientos.append(Casilla(self.x - 1, self.y + 1))

            result = []
            for m in movimientos:
                if self.legal_movimiento(m.x, m.y, regla):
                    result.append(m)
        else:
            opp = regla.jugadores[self.opp]
            movimientos.append(Casilla(opp.x, opp.y - 1))
            movimientos.append(Casilla(opp.x, opp.y + 1))
            movimientos.append(Casilla(opp.x + 1, opp.y))
            movimientos.append(Casilla(opp.x - 1, opp.y))
            movimientos.append(Casilla(opp.x, opp.y - 2))
            movimientos.append(Casilla(opp.x, opp.y + 2))
            movimientos.append(Casilla(opp.x - 2, opp.y))
            movimientos.append(Casilla(opp.x + 2, opp.y))
            movimientos.append(Casilla(opp.x - 1, opp.y - 1))
            movimientos.append(Casilla(opp.x + 1, opp.y + 1))
            movimientos.append(Casilla(opp.x + 1, opp.y - 1))
            movimientos.append(Casilla(opp.x - 1, opp.y + 1))

            result = []
            for m in movimientos:
                if opp.legal_movimiento(m.x, m.y, regla):
                    result.append(m)

        return result

    def wallOption(self, regla, oponente=False):
        paredes = []
        if not oponente:
            for pared in self.pared_opciones:
                if self.legal_colocamiento(regla, pared):
                    paredes.append(pared)
        else:
            opp = regla.jugadores[self.opp]
            for pared in self.pared_opciones:
                if opp.legal_colocamiento(regla, pared):
                    paredes.append(pared)

        return paredes;

    def print_jugador(self):
        return "Ubicacion jugador: (%d, %d)\nParedes restantes: %d\n" % (self.x, self.y, self.paredes)

class Casilla:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_casilla(self):
        return "Casilla ubicacion: (%d, %d)" % (self.x, self.y)

##Atributos necesarios para que funcione la pared
class Pared:

    def __init__(self, top_l, top_r, IAl, IAr, direccion):
       
        self.IAr = IAr
        self.orientacion = direccion
        self.top_l = top_l
        self.top_r = top_r
        self.IAl = IAl

class Regla:

    def __init__(self, IAcontador='0'):
        import IA
        if IAcontador == '1':
            self.jugadores = [Jugador(0), IA.Minimax(1)]
        elif IAcontador == '2':
            self.jugadores = [IA.Minimax(0), IA.Minimax(1)]
        else:
            self.jugadores = [Jugador(0), Jugador(1)]
        self.paredes = []
        self.casillas = [[], [], [], [], [], [], [], [], []]
        self.actual = 0
        self.actual = random.randint(0, 1)

        for i in range(0, 8):
            for j in range(0, 8):
                self.casillas[i].append(Casilla(i, j))

    def printTablero(self):
        print(self.casillas)

    def sigTurno(self):
        if self.actual == 0:
            self.actual = 1
        else:
            self.actual = 0
            
def make_camino(origen, actual):
    tot_camino = [actual]
    while actual in origen.keys():
        actual = origen[actual]
        tot_camino.append(actual)
    return tot_camino

##BFS para reducir el camino
def bfs(inicio, fin, tablero):
    frontera = []
    visitado = set()
    frontera.append(inicio)
    visitado.add(inicio)
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == fin):
            return True

        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                if not bloqueado(hijo[0], hijo[1], padre[0], padre[1], tablero):
                    frontera.append(hijo)
                    visitado.add(hijo)
    return False

def camino(inicio, fin, tablero):
    frontera = []
    visitado = set()
    frontera.append(inicio)
    visitado.add(inicio)
    distancia = {}
    distancia[inicio] = 0
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == fin):
            return distancia[fin]

        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                if not bloqueado(hijo[0], hijo[1], padre[0], padre[1], tablero):
                    frontera.append(hijo)
                    distancia[hijo] = distancia[padre] + 1
                    visitado.add(hijo)

    return maxsize

##Otro algoritmo para reducir espacios
def dijkstra(inicio, fin, tablero):

        fila = len(fin)
        columna = len(fin[0])
        distancia = [float("Inf")] * fila
        padre = [-1] * fila
        distancia[tablero] = 0

        cola = []
        for i in range(fila):
            cola.append(i)

        while cola:
            u = inicio.minDistance(distancia, cola)
            cola.remove(u)
            for i in range(cola):
                if fin[u][i] and i in cola:
                    if distancia[u] + fin[u][i] < distancia[i]:
                        distancia[i] = distancia[u] + fin[u][i]
                        padre[i] = u

        return distancia

##El codigo que nos costo mas dificil de entender(permite agilizar los algoritmos de busqueda de camino minimo)
def get_sucesores(padre):
    hijos = set()
    p0 = padre[0]
    p1 = padre[1]
    x1 = padre[0] - 1
    x2 = padre[0] + 1
    y1 = padre[1] - 1
    y2 = padre[1] + 1
    if (x1 >= 0):
        hijos.add((x1, p1))
    if (y1 >= 0):
        hijos.add((p0, y1))
    if (x2 <= 8):
        hijos.add((x2, p1))
    if (y2 <= 8):
        hijos.add((p0, y2))
    return hijos

##Impide avanzar si hay un muro
def bloqueado(x1, y1, x2, y2, tablero):                                                         
    for pared in tablero.paredes:
        if (pared.orientacion == "horizontal"):
            if (y1 < y2):
                if (pared.top_l.y == y1 and (pared.top_l.x == x1 or (pared.top_l.x + 1) == x1)):
                    return True
            if (y1 > y2):
                if (pared.top_l.y == y2 and (pared.top_l.x == x1 or (pared.top_l.x + 1) == x1)):
                    return True
        if (pared.orientacion == "vertical"):
            if (x1 < x2):
                if (pared.top_l.x == x1 and (pared.top_l.y == y1 or (pared.top_l.y + 1) == y1)):
                    return True
            if (x1 > x2):
                if (pared.top_l.x == x2 and (pared.top_l.y == y2 or (pared.top_l.y + 1) == y2)):
                    return True
    return False