##Utilizamos varias guias de youtube como videos para hacer damas o ajedrez
##Ademas usamos algunos codigos de Github para guiarnos con la creacion de paredes y algoritmos para el 
##Movimiento del bot

#Librerias y referencias
import os
import Mapa
from Mapa import *

##Si fuese tan amable de decirnos como realizar el salto de linea estaria bien 

print("""Ingrese el tipo de modo a jugar:
1.- humano vs bot
2.- bot vs bot
3.- Humano vs humano""")
op = input()
if (op=='1'):
    os.system('python Mapa.py 1')
if (op=='2'):
    os.system('python Mapa.py 2')
if (op=='3'):
    os.system('python Mapa.py')





