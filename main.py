import pygame as py
import os
from os import listdir
import time as tm
import random
from carta import Carta
from pila import Pila_Baraja,Pila_Fin,Pila_Mesa
#CONSTANTES
DIR = "../Solitario/Imagenes/Cartas"#Direccion donde se encuentran las imagenes

ANCHO_VENTANA = 1600
ALTO_VENTANA = 900 

BARAJA=[]#Lista que contiene todas las cartas(Objeto) de la baraja
FONDO= py.transform.scale(py.image.load(os.path.join("Imagenes","Fondo.jpg")),(ANCHO_VENTANA,ALTO_VENTANA))#Fondo de pantalla



ANCHO_CARTA = 125
ALTO_CARTA = 175
# Inicializar pygame
py.init()

#Cargo las imagenes de las cartas
for imagen in os.listdir(DIR):
    if imagen.endswith('.jpg'):
        #Imagen contiene el nombre entero del archivo, he de crear un objeto Carta
        name = imagen.replace('.jpg',"")
        img = py.transform.scale((py.image.load(os.path.join(DIR,imagen))),(ANCHO_CARTA,ALTO_CARTA))
        BARAJA.append(Carta(name,img))


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
    global BARAJA
    lista_pm=lista_pf=[]
    #Empiezo por las pilas de la mesa
    for i in range(1,8):#Van a ser las 7 pilas
        cartas = []
        for j in range(1,i+1):#Van a ser las cartas que va a tener cada pila
            index = random.randint(0,len(BARAJA)-1)
            cartas.append(BARAJA.pop(index))
        #Una vez tengo lista la lista de cartas, la paso como parametro a la pila
        lista_pm.append(Pila_Mesa(cartas,160+(i-1)*200,260))#La formula la saco de unos calculos precisos (Copium)

    #Ahora en la lista de BARAJA quedan las cartas que sobran, por lo que ya puedo hacer la pila_baraja
    lista_pb = Pila_Baraja(BARAJA,160,25)

    #Finalmente puedo crear las ultimas 4 pilas que son las finales
    for i in range (4):
        lista_pf.append(Pila_Fin(760+i*200,25))

    return (lista_pm,lista_pb,lista_pf)

def draw_win(win:py.Surface,lista_pm:list[Pila_Mesa],lista_pb:Pila_Baraja,lista_pf:list[Pila_Fin]):
    win.blit(FONDO,(0,0))
    
    for pila in lista_pm:
        pila.draw_pila(win)
        
    for pila in lista_pf:
        pila.draw_pila(win)

    lista_pb.draw_pila(win)

    py.display.flip()


def run(win:py.Surface,clock:py.time.Clock,lista_pm,lista_pb,lista_pf):
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
        draw_win(win,lista_pm,lista_pb,lista_pf)
        

def main():
    
    win = py.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
    clock = py.time.Clock()
    lista_pm,lista_pb,lista_pf=repartir_cartas()
    #print("El numn {}".format(lista_pb.get_num_cartas_ini()))
    run(win,clock,lista_pm,lista_pb,lista_pf)
    #repartir_cartas() #Reparto las cartas de la partida, esto solo se va a hacer 1 vez por partida
    



if __name__ == "__main__":
    main()