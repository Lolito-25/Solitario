import pygame as py
import os
from os import listdir
import time as tm
import random
from carta import Carta
from pila import Pila_Baraja,Pila_Fin,Pila_Mesa
#CONSTANTES
DIR = "../Solitario/Imagenes/Cartas"#Direccion donde se encuentran las imagenes

BARAJA=[]#Lista que contiene todas las cartas(Objeto) de la baraja
FONDO= py.image.load(os.path.join("Imagenes","Fondo.jpg"))#Fondo de pantalla

PILA_MESA :list[Pila_Mesa]= []#Lista que contiene las 7 pilas de la mesa de juego
PILA_FIN :list[Pila_Fin]= []#Lista que contiene las 4 pilas del fin del juego
PILA_BARAJA : Pila_Baraja = Pila_Baraja([])#Unico objeto que contiene las 2 pilas de las que se sacan las pilas que se cogen


ANCHO_VENTANA = 1600
ALTO_VENTANA = 900 
# Inicializar pygame
py.init()

#Cargo las imagenes de las cartas
for imagen in os.listdir(DIR):
    if imagen.endswith('.jpg'):
        #Imagen contiene el nombre entero del archivo, he de crear un objeto Carta
        name = imagen.replace('.jpg',"")
        img = py.image.load(os.path.join(DIR,imagen))
        BARAJA.append(Carta(name,img,REVERSO))


"""
La disposicion de las pilas de la mesa es la siguiente:
    1ºPila -> 1 carta
    2ºPila -> 2 cartas
    3ºPila -> 3 cartas
    4ºPila -> 4 cartas
    5ºPila -> 5 cartas
    6ºPila -> 6 cartas
    7ºPila -> 7 cartas
"""
def repartir_cartas():#Metodo en el que se van a repartir las cartas en las pilas adecuadas
    global PILA_BARAJA,PILA_MESA,PILA_FIN

    #Empiezo por las pilas de la mesa
    for i in range(1,8):#Van a ser las 7 pilas
        cartas = []
        for j in range(1,i+1):#Van a ser las cartas que va a tener cada pila
            index = random.randint(0,len(BARAJA)-1)
            cartas.append(BARAJA.pop(index))
        #Una vez tengo lista la lista de cartas, la paso como parametro a la pila
        PILA_MESA.append(Pila_Mesa(cartas))

    #Ahora en la lista de BARAJA quedan las cartas que sobran, por lo que ya puedo hacer la pila_baraja
    PILA_BARAJA = Pila_Baraja(BARAJA)

    #Finalmente puedo crear las ultimas 4 pilas que son las finales
    PILA_FIN = [Pila_Fin(),Pila_Fin(),Pila_Fin(),Pila_Fin()]

def draw_win(win):
    win.blit(FONDO,(0,0))

    py.display.update()


def run(win:py.Surface,clock:py.time.Clock):
    global PILA_BARAJA,PILA_MESA,PILA_FIN
    run = True
    while run:
        clock.tick(60)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                #MODIFICAR PARA QUE SE PUEDA VOLVER A JUGAR
                #------------
                py.quit()
                quit()
                #------------
        draw_win(win)
        

def main():

    win = py.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
    clock = py.time.Clock()
    run(win,clock)
    #repartir_cartas() #Reparto las cartas de la partida, esto solo se va a hacer 1 vez por partida
    



if __name__ == "__main__":
    main()