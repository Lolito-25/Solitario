import pygame as py
import os
from os import listdir
import time as tm
import random
from carta import Carta
from pila_baraja import *
from pila_mesa import Pila_Mesa
from pila_fin import Pila_Fin
#CONSTANTES
DIR = "../Solitario/Imagenes/Cartas"#Direccion donde se encuentran las imagenes

ANCHO_VENTANA = 1600
ALTO_VENTANA = 900 

BARAJA=[]#Lista que contiene todas las cartas(Objeto) de la baraja
FONDO= py.transform.scale(py.image.load(os.path.join("Imagenes","Fondo.jpg")),(ANCHO_VENTANA,ALTO_VENTANA))#Fondo de pantalla



ANCHO_CARTA = 125
ALTO_CARTA = 175


CARTA_CLICADA : Carta = None #Inicialmente no se va a estar clicando sobre ninguna carta

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
    lista_pm,lista_pf=[],[]
    id:int=1
    #Empiezo por las pilas de la mesa
    for i in range(1,8):#Van a ser las 7 pilas
        cartas = []
        for j in range(1,i+1):#Van a ser las cartas que va a tener cada pila
            index = random.randint(0,len(BARAJA)-1)
            cartas.append(BARAJA.pop(index))
        #Una vez tengo lista la lista de cartas, la paso como parametro a la pila
        lista_pm.append(Pila_Mesa(cartas,160+(i-1)*200,260,id))#La formula la saco de unos calculos precisos (Copium)
        id+=1
    #Ahora en la lista de BARAJA quedan las cartas que sobran, por lo que ya puedo hacer la pila_baraja
    pila_baraja = Pila_Baraja(BARAJA,160,25,id)
    id+=1
    #Finalmente puedo crear las ultimas 4 pilas que son las finales
    for i in range (4):
        lista_pf.append(Pila_Fin(760+i*200,25,id))
        id+=1

    return (lista_pm,pila_baraja,lista_pf)

def draw_win(win:py.Surface,lista_pm:list[Pila_Mesa],pila_baraja:Pila_Baraja,lista_pf:list[Pila_Fin],carta:Carta):
    win.blit(FONDO,(0,0))
    
    for pila in lista_pm:
        pila.draw_pila(win)
        
    for pila in lista_pf:
        pila.draw_pila(win)

    pila_baraja.draw_pila(win)
    
    if carta != None : 
        carta.draw_carta(win,carta.x,carta.y)
    py.display.flip()

#Este metodo devuelve una lista con las cartas disponibles de todas las pilas que hay 
def cartas_disponibles(lista_pm:list[Pila_Mesa],pila_baraja:Pila_Baraja,lista_pf:list[Pila_Fin]):
    lista_clicables = []
    lista_disponibles = []
    for p_m in lista_pm: #Para cada pila de la mesa, cojo las cartas que esten giradas
        for carta in p_m.get_cartas():
            if not(carta.esta_girada()):
                lista_disponibles.append(carta)
    
    if len(pila_baraja.pila_ini.get_cartas()) > 0: 
        lista_disponibles.append(pila_baraja.pila_ini.get_cartas()[0])#De la pila de barajas inicial cojo la primera
    
    if len(pila_baraja.pila_fin.get_cartas()) > 0: 
        lista_disponibles.append(pila_baraja.pila_fin.get_cartas()[-1])#De la pila de barajas inicial cojo la ultima

    for p_f in lista_pf:
        if len(p_f.get_cartas()) > 0:lista_disponibles.append(p_f.get_cartas()[-1]) #De la pila final cojo la ultima carta 

    for c in lista_disponibles:
        if c.nombre != "JOKER":
            lista_clicables.append(c)
    
    return (lista_disponibles,lista_clicables)


def run(win:py.Surface,clock:py.time.Clock,lista_pm,pila_baraja,lista_pf):
    global BARAJA,CARTA_CLICADA
    res = cartas_disponibles(lista_pm,pila_baraja,lista_pf)#Obtengo la lista de cartas disponibles
    lista_disponible:list[Carta] = res[0]
    lista_clicable :list[Carta] = res[1]
    
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

            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1: #Me aseguro de que el boton que se presiona del mouse sea el BOTON IZQUIERDO
                    #He de iterar sobre todas las cartas que hay en las pilas y sacarla con pop
                    for carta in lista_clicable:
                        if carta.get_rect().collidepoint(event.pos) and CARTA_CLICADA == None:
                            if pila_baraja.contiene_carta(carta):
                                CARTA_CLICADA = pila_baraja.pop(carta)
                            else:
                                CARTA_CLICADA = carta.get_pila().pop(carta)
                            if CARTA_CLICADA != None: lista_disponible.remove(CARTA_CLICADA)
                                  
            if event.type == py.MOUSEBUTTONUP:
                '''
                Cuando suelte el raton se han de dar 2 casos:
                    1-> Se ha soltado encima de una pila:
                        1.1 -> Se puede hacer join en esa pila
                        1.2 -> No se puede hacer join en esa pila
                    2-> No se ha soltado encima de ninguna pila
                Hemos de esperar a cambiar el estado de la mesa hasta que se haga un join valido, esto implica que:
                    ->No se gire la carta que esta por debajo de la que hemos quitado
                    ->Se guarde la pila inicial de la carta
                Si se da bien el join, he de actualizar la lista de cartas disponibles
                '''

                if CARTA_CLICADA != None:
                    
                    for carta in lista_disponible:
                        if carta.get_rect().colliderect(CARTA_CLICADA.get_rect()):
                            carta.get_pila().cambiar_estado(CARTA_CLICADA,CARTA_CLICADA.get_pila())
                            CARTA_CLICADA = None
                            break
                    
                    if CARTA_CLICADA != None: # En el caso 2
                        CARTA_CLICADA.get_pila().cambiar_estado(CARTA_CLICADA,CARTA_CLICADA.get_pila())
                        CARTA_CLICADA = None

                res = cartas_disponibles(lista_pm,pila_baraja,lista_pf)#Obtengo la lista de cartas disponibles
                lista_disponible:list[Carta] = res[0]
                lista_clicable :list[Carta] = res[1]


            if event.type == py.MOUSEMOTION:
                if CARTA_CLICADA != None:
                    x, y = py.mouse.get_pos()
                    CARTA_CLICADA.x = x - ANCHO_CARTA // 2 
                    CARTA_CLICADA.y = y - ALTO_CARTA // 2

        draw_win(win,lista_pm,pila_baraja,lista_pf,CARTA_CLICADA)
        

def main():
    
    win = py.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
    clock = py.time.Clock()
    lista_pm,pila_baraja,lista_pf=repartir_cartas()
    #print("El numn {}".format(pila_baraja.get_num_cartas_ini()))
    run(win,clock,lista_pm,pila_baraja,lista_pf)
    #repartir_cartas() #Reparto las cartas de la partida, esto solo se va a hacer 1 vez por partida
    

if __name__ == "__main__":
    main()