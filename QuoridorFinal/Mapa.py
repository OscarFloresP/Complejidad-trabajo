#Librerias y referencias
from regla import *
from sys import argv
import tkinter
import math
import threading
from tkinter import messagebox  
import random
import time
from pip._vendor.distlib.compat import raw_input



#Costantes y variables
#sirve para cuadrar el tamanio de la consola grafica
CASILLA_SIZE = 50
JUGADOR_SIZE = int(.8 * CASILLA_SIZE)
CASILLA_PADDING = 25
BORDER =1
NUM_FILAS = 9
NUM_COLUMNS = NUM_FILAS
CONTROL_WIDTH = 5
COLORS = {'bg': '#000000', 'casilla': '#123789', 'pared': '#CC1111', 'pared-error': '#000000', 'panel': '#333333', 'button': '#555555', 'jugadores': ['#00FFFF', '#FFFF00'],'jugadores-sombras': ['#B0C4DE', '#008000'] }
JUGADORES = ['PLAYER 1', 'Best bot ever created']

#referencia para realizar el talblero
class Tablero():
    def __init__(self):
        self.root = None
        self.canvas = None
        self.width = 0
        self.height = 0
        self.jugadores = [None, None]
        self.casillas = []
        self.paredes = {}
        self.movimiento = None
        self.jugador_sombra = None
        self.pared_sombra = None
        self.turno = 0
        self.regla = None
        self.bot_cont = '0'
        self.pared_elementos = [None, None]
        self.actual_elemento = None
        for _ in range(NUM_COLUMNS):
            self.casillas.append(list(range(NUM_FILAS)))

    def makeGame(self, bot_cont):
        if self.root:
            self.root.destroy()

        self.root = tkinter.Tk()
        self.root.title("Press 'M' for movement and 'W' for put a wall")

        self.root.bind("<Escape>", lambda e: self.handleQuit())
        self.root.bind("w", lambda e: self.setMovement("putWall"))
        self.root.bind("m", lambda e: self.setMovement("movimientorFicha"))
        self.root.bind("<Motion>", lambda e: self.handleMotion(e.x, e.y))
        self.root.bind("<Button-1>", lambda e: self.handleClick(e.x, e.y))

        self.height = (NUM_FILAS * CASILLA_SIZE) + (NUM_FILAS * CASILLA_PADDING) + (2 * BORDER)
        self.width = self.height + CONTROL_WIDTH
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, background=COLORS['bg'])
        self.canvas.pack()
        self.dibujarCasillas()
        self.generarParedes()

        self.regla = Regla(bot_cont)
        self.bot_cont = bot_cont
        self.turno = self.regla.actual
        self.drawPlayeres()
   
        self.root.mainloop()

        x = self.width - CONTROL_WIDTH / 2 - BORDER / 2
        y = 13 * BORDER
        i = "Instrucciones: \n Presionar 'm' para activar el movimiento de la ficha \n o \n 'p' para activar la colocacicon de paredes"
        self.canvas.create_text((x, y), text=i, justify='center', width=CONTROL_WIDTH)

        x = self.width - CONTROL_WIDTH / 2 - BORDER / 2
        y = self.height - 125

    def dibujarParedCount(self):
        y = self.height / 2.75
        x = self.width - CONTROL_WIDTH / 2 - BORDER
        for p in self.regla.jugadores:
            output = '' + '\n \n \n'
            output += '\n \n \n' + JUGADORES[p.jugador_num] + str(p.paredes) + '-> paredes restantes' + '\n \n' + '\n \n'
            if self.pared_elementos[p.jugador_num] == None:
                self.pared_elementos[p.jugador_num] = self.canvas.create_text((x, y), text=output, justify='center',width=CONTROL_WIDTH, font=("Arial", 10, "bold"))
            else:
                self.canvas.itemconfigure(self.pared_elementos[p.jugador_num], text=output)
            y += 3 * BORDER

    def dibujarActualJugadorTurno(self):
        y = self.height / 1.1
        x = self.width - CONTROL_WIDTH / 2 - BORDER
        output = "Es el turno de " + JUGADORES[self.turno]
        if self.actual_elemento == None:
            self.actual_elemento = self.canvas.create_text((x, y), text=output, justify='center', width=CONTROL_WIDTH,
                                                          font=("Arial", 14, "bold"))
        else:
            self.canvas.itemconfigure(self.actual_elemento, text=output)

    def dibujarCasillas(self):
        for j in range(NUM_FILAS):
            for i in range(NUM_COLUMNS):
                x = BORDER + CASILLA_PADDING / 2 + i * (CASILLA_SIZE + CASILLA_PADDING)
                y = BORDER + CASILLA_PADDING / 2 + j * (CASILLA_SIZE + CASILLA_PADDING)
                casilla = self.canvas.create_rectangle(x, y, x + CASILLA_SIZE, y + CASILLA_SIZE, fill=COLORS['casilla'])
                self.casillas[j][i] = casilla

    def generarParedes(self):
        paredes = []
        for j in range(0, NUM_FILAS - 1):
            for i in range(0, NUM_COLUMNS - 1):
                for k in [0, 1]:
                    if k == 0:
                        pared_string = str(j) + str(i) + 'H'
                    else:
                        pared_string = str(j) + str(i) + 'V'
                    x1, y1, x2, y2 = paredStrToCoords(pared_string)
                    pared = self.canvas.create_rectangle(x1, y1, x2, y2, fill='', outline='')
                    self.paredes[pared_string] = pared

    def drawPlayeres(self, sombra=False):
        for k in range(len(JUGADORES)):
            jugador = self.regla.jugadores[k]
            fila = jugador.x
            column = jugador.y
            self.drawPlayer(fila, column, k, jugador, sombra)

    def drawPlayer(self, fila, column, num, jugador, sombra):
        x, y = gridToCoords(fila, column)
        if x == None or y == None:
            return
        if not sombra and self.jugadores[num]:
            self.canvas.delete(self.jugadores[num])
            self.jugadores[num] = None
        elif sombra and self.jugador_sombra:
            self.canvas.delete(self.jugador_sombra)
        color = COLORS['jugadores'][num]
        if sombra:
            color = COLORS['jugadores-sombras'][num]
        radius = JUGADOR_SIZE / 2
        ficha = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="")
        if not sombra:
            self.jugadores[num] = ficha
        else:
            self.jugador_sombra = ficha

    def drawWall(self, legal=False):
        for pared in self.regla.paredes:
            pared_string = paredReglaToStr(pared)
            self.showWall(pared_string)
        if self.pared_sombra and self.movimiento == 'putWall':
            self.showWall(self.pared_sombra, legal)

    def hideWall(self, pared_string):
        if pared_string in self.paredes:
            self.canvas.itemconfigure(self.paredes[pared_string], fill='')

    def showWall(self, pared_string, legal=True):
        if not legal:
            color = COLORS['pared-error']
        else:
            color = COLORS['pared']
        if pared_string in self.paredes:
            w = self.paredes[pared_string]
            self.canvas.itemconfigure(w, fill=color)

    def setMovement(self, movimiento):
        self.movimiento = movimiento
        self.refresh()

    def handleQuit(self):
        self.root.destroy()

    def handleMotion(self, x, y):
        if self.bot_cont == '2' or (self.turno == 1 and self.bot_cont == '1'):
            return

        self.clearParedSombra()
        i, j = coordsToGrid(x, y)
        if i == None or j == None:
            return
        if self.movimiento == 'movimientorFicha':
            if self.regla.jugadores[self.turno].legal_movimiento(i, j, self.regla):
                self.drawPlayer(i, j, self.turno, self.regla.jugadores[self.turno], True)
            elif self.jugador_sombra != None:
                self.canvas.delete(self.jugador_sombra)
                self.jugador_sombra == None

        elif self.movimiento == 'putWall':
            pared_string = coordsToParedStr(i, j, x, y)
            self.pared_sombra = pared_string
            legal = self.regla.jugadores[self.turno].legal_colocamiento(self.regla, paredStrToRegla(pared_string))
            self.drawWall(legal)

    def handleClick(self, x, y):
        if (self.bot_cont == '2'):
            while not self.regla.jugadores[0].ganador_posicion and not self.regla.jugadores[1].ganador_posicion:
                self.regla.jugadores[self.turno].finalMovimiento(self.regla)
                self.sigTurno()
                self.refresh()
                time.sleep(.05)

        else:
            i, j = coordsToGrid(x, y)
            if i == None or j == None:
                return

            if self.movimiento == 'movimientorFicha':
                if self.regla.jugadores[self.turno].legal_movimiento(i, j, self.regla):
                    self.regla.jugadores[self.turno].movimiento(i, j, self.regla)
                    self.sigTurno()
                    self.refresh()

            if self.movimiento == 'putWall':
                pared_string = coordsToParedStr(i, j, x, y)
                if self.regla.jugadores[self.turno].legal_colocamiento(self.regla, paredStrToRegla(pared_string)):
                    self.pared_sombra = None
                    self.regla.jugadores[self.turno].colocar_pared(self.regla, paredStrToRegla(pared_string))
                    self.sigTurno()
                    self.refresh()

            if self.handleGanador():
                return

            if self.turno == 1 and self.bot_cont == '1':
                self.regla.jugadores[self.turno].finalMovimiento(self.regla)
                self.sigTurno()
                self.refresh()
                time.sleep(.05)

    def handleGanador(self):
        ganador = False
        for p in self.regla.jugadores:
            if p.ganador_posicion:
                x = self.width - CONTROL_WIDTH / 2 - BORDER
                y = self.height / 1.6
                i =" "
                messagebox.showinfo(" ", JUGADORES[p.jugador_num] + " WOOOOOOOON NICE PLAY")
                ganador = True
                break
        if ganador:
            self.root.unbind("<Motion>")
            self.root.unbind("<Button-1>")
        return ganador

    def refresh(self):
        self.clearSombra()
        self.clearParedSombra()
        self.drawWall()
        self.drawPlayeres()
        self.root.update()
        self.handleGanador()

    def sigTurno(self):
        self.regla.sigTurno()
        self.turno = self.regla.actual

    def clearSombra(self):
        if self.jugador_sombra != None:
            self.canvas.delete(self.jugador_sombra)
            self.jugador_sombra = None

    def clearParedSombra(self):
        if self.pared_sombra != None:
            self.hideWall(self.pared_sombra)
            self.pared_sombra = None

def gridToCoords(i, j):
    if (0 <= i <= 8) and (0 <= j <= 8):
        x = BORDER + CASILLA_PADDING / 2 + (i) * (CASILLA_SIZE + CASILLA_PADDING)
        y = BORDER + CASILLA_PADDING / 2 + (j) * (CASILLA_SIZE + CASILLA_PADDING)
        return (x + (CASILLA_SIZE / 2)), (y + (CASILLA_SIZE / 2))
    else:
        return None, None

def coordsToGrid(x, y):
    x -= BORDER
    y -= BORDER

    i = int(math.floor(float(x) / (CASILLA_SIZE + CASILLA_PADDING)))
    j = int(math.floor(float(y) / (CASILLA_SIZE + CASILLA_PADDING)))

    if (0 <= i <= 8) and (0 <= j <= 8):
        return i, j
    else:
        return None, None

def paredStrToCoords(pared_string):
    if len(pared_string) == 3:
        x = int(pared_string[0])
        y = int(pared_string[1])
        orientacion = pared_string[2]
        cx, cy = gridToCoords(x, y)
        if orientacion == 'H':
            x1 = cx - CASILLA_SIZE / 2
            y1 = cy + CASILLA_SIZE / 2 + CASILLA_PADDING
            x2 = x1 + 2 * CASILLA_SIZE + CASILLA_PADDING
            y2 = y1 - CASILLA_PADDING
        else:
            x1 = cx + CASILLA_SIZE / 2
            y1 = cy + 3 * (CASILLA_SIZE / 2) + CASILLA_PADDING
            x2 = x1 + CASILLA_PADDING
            y2 = cy - CASILLA_SIZE / 2
        return x1, y1, x2, y2

def coordsToParedStr(i, j, x, y):
    cx, cy = gridToCoords(i, j)
    dx = (2 ** .5) * (x - cx)
    dy = (2 ** .5) * (y - cy)
    orient = (dx - dy) * (dx + dy)
    if orient >= 0:
        orientacion = 'V'
    else:
        orientacion = 'H'
    if dx < 0 and i > 0:
        i -= 1
    if dy < 0 and j > 0:
        j -= 1
    return str(i) + str(j) + orientacion

def paredStrToRegla(pared_string):
    orientacion = 'horizontal'
    if pared_string[2] == 'V':
        orientacion = "vertical"
    i = int(pared_string[0])
    j = int(pared_string[1])
    top_l = Casilla(i, j)
    top_r = Casilla(i + 1, j)
    bot_l = Casilla(i, j + 1)
    bot_r = Casilla(i + 1, j + 1)
    return Pared(top_l, top_r, bot_l, bot_r, orientacion)

def paredReglaToStr(pared):
    pared_string = ''
    pared_string += str(pared.top_l.x) + str(pared.top_l.y)
    o = pared.orientacion
    if o == "horizontal":
        pared_string += 'H'
    else:
        pared_string += 'V'

    return pared_string

##Tiene que etsa ral final para que funque
if __name__ == '__main__':
    tablero = Tablero()
    if len(argv) == 2:
        if argv[1] == '1':
            tablero.makeGame('1')
        elif argv[1] == '2':
            tablero.makeGame('2')
    else:
        tablero.makeGame('0')