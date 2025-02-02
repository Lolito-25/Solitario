import pygame as py
import os
import time
import copy
import random
from carta import Carta
from pila import OFFSET_Y
from pila_baraja import *
from pila_mesa import Pila_Mesa
from pila_fin import Pila_Fin
from estado import Estado
#CONSTANTES
DIR = "../Solitario/Imagenes/Cartas"#Direccion donde se encuentran las imagenes

ANCHO_VENTANA = 1600
ALTO_VENTANA = 900 

BARAJA=[]#Lista que contiene todas las cartas(Objeto) de la baraja
FONDO= py.transform.scale(py.image.load(os.path.join("Imagenes","Fondo.jpg")),(ANCHO_VENTANA,ALTO_VENTANA))#Fondo de pantalla

PUNTUACION:int = 0

ANCHO_CARTA = 125
ALTO_CARTA = 175

ID:int=0
TIEMPO = time.time()

CARTA_CLICADA : list[Carta] = None #Inicialmente no se va a estar clicando sobre ninguna carta

# Inicializar pygame
py.init()
fuente = py.font.Font(None, 36)

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
    pila_baraja = Pila_Baraja(BARAJA,[],160,25,id)
    id+=1
    #Finalmente puedo crear las ultimas 4 pilas que son las finales
    for i in range (4):
        lista_pf.append(Pila_Fin([],760+i*200,25,id))
        id+=1

    return (lista_pm,pila_baraja,lista_pf)

def draw_win(win:py.Surface,lista_pm:list[Pila_Mesa],pila_baraja:Pila_Baraja,lista_pf:list[Pila_Fin],cartas:list[Carta],tiempo:float):
    win.blit(FONDO,(0,0))
    
    for pila in lista_pm:
        pila.draw_pila(win)
        
    for pila in lista_pf:
        pila.draw_pila(win)

    pila_baraja.draw_pila(win)
    
    if cartas != None : 
        for carta in reversed(cartas):
            carta.draw_carta(win,carta.x,carta.y)
        
    texto_reloj = fuente.render(f"{tiempo // 60}:{tiempo % 60}", True, (255,255,255))
    win.blit(texto_reloj, (10, 40))
    texto_puntuacion = fuente.render(f"PUNTOS {PUNTUACION}",True,(255,255,255))
    win.blit(texto_puntuacion, (10, 10))

    py.display.flip()

#Este metodo devuelve una lista con las cartas disponibles de todas las pilas que hay 
def cartas_disponibles(lista_pm:list[Pila_Mesa],pila_baraja:Pila_Baraja,lista_pf:list[Pila_Fin]):
    '''
    Las cartas clicables son:
        -> Pila Mesa: Todas las que no esten giradas y que no sean JOKER
        -> Pila Fin: La ultima carta disponible si no es JOKER
        -> Pila Baraja:
            -Pila Deposito: La ultima carta que no sea JOKER
            -Pila Mazo: La ultima carta (Aunque sea JOKER)

    Las cartas disponibles son aquellas que se les puede poner cartas encima:
        -> Pila Mesa: Todas las que no esten giradas (Puede ser JOKER)
        -> Pila Fin: La ultima carta (Da igual que sea JOKER)
        -> Pila Baraja: Ninguna
    '''
    lista_clicables = [] 
    lista_disponibles = [] #Lista de cartas a las que se le podran poner cartas encima
    
    for p_m in lista_pm:
        for c in p_m.cartas:
            if not c.esta_girada() or c.nombre == "JOKER":
                lista_disponibles.append(c)
                if c.nombre != "JOKER": lista_clicables.append(c)
    
    for p_f in lista_pf:
        c=p_f.cartas[-1]
        lista_disponibles.append(c)
        if c.nombre != "JOKER":
            lista_clicables.append(c)
        
    lista_clicables.append(pila_baraja.pila_ini.cartas[-1])
    c = pila_baraja.pila_fin.cartas[-1]
    if c.nombre != "JOKER":
        lista_clicables.append(c)
    
    return (lista_disponibles,lista_clicables)



def get_pila(carta:Carta,lista_pm,pila_baraja,lista_pf):
    id = carta[-1].get_pila().id
    if id in (1,2,3,4,5,6,7):
        return lista_pm[id-1]
    elif id == 8:
        if isinstance(carta[-1].get_pila(),Pila_Mazo):
            return pila_baraja.pila_ini
        else:
            return pila_baraja.pila_fin
    else:
        return lista_pf[id-9]




def refrescar_pilas(lista_pm:list[Pila_Mesa],pila_baraja:Pila_Baraja,lista_pf:list[Pila_Fin]):
    for pm in lista_pm:
        pm.check_cartas()
        pm.pila_refresh()

    pila_baraja.pila_ini.check_cartas()
    pila_baraja.pila_ini.pila_refresh()
    pila_baraja.pila_fin.check_cartas()
    pila_baraja.pila_fin.pila_refresh()

    for pf in lista_pf:
        pf.check_cartas()
        pf.pila_refresh()

def run(win:py.Surface,clock:py.time.Clock,lista_pm,pila_baraja,lista_pf):
    global BARAJA,CARTA_CLICADA,PUNTUACION,TIEMPO,ID

    estado = Estado()
    estado.guardar_estado(ID,lista_pm,pila_baraja,lista_pf,PUNTUACION)

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
                            pila = get_pila([carta],lista_pm,pila_baraja,lista_pf)
                            if isinstance(pila,Pila_Mazo) or isinstance(pila,Pila_Deposito):
                                pila = pila_baraja
                            CARTA_CLICADA = pila.pop(carta)

                            if CARTA_CLICADA != None: 
                                for carta in CARTA_CLICADA:
                                    lista_clicable.remove(carta)
                                    if carta in lista_disponible:
                                        lista_disponible.remove(carta)
                            else:
                                if isinstance(pila,Pila_Baraja) and pila.pila_fin.cartas[0].nombre == "JOKER":
                                    PUNTUACION = max(0,PUNTUACION-50)


                                  
            if event.type == py.MOUSEBUTTONUP:
                '''
                Cuando suelte el raton se han de dar 2 casos:
                    1-> Se ha soltado encima de una pila:
                        1.1 -> Se puede hacer join en esa pila (actualizo estado y puntuacion)
                        1.2 -> No se puede hacer join en esa pila
                    2-> No se ha soltado encima de ninguna pila
                Hemos de esperar a cambiar el estado de la mesa hasta que se haga un join valido, esto implica que:
                    ->No se gire la carta que esta por debajo de la que hemos quitado
                    ->Se guarde la pila inicial de la carta
                Si se da bien el join, he de actualizar la lista de cartas disponibles
                '''

                if CARTA_CLICADA != None:
                    for carta in lista_disponible:
                        if carta != CARTA_CLICADA[-1] and carta.get_rect().colliderect(CARTA_CLICADA[-1].get_rect()):
                            pila_origen = get_pila(CARTA_CLICADA,lista_pm,pila_baraja,lista_pf)
                            pila_destino = get_pila([carta],lista_pm,pila_baraja,lista_pf)
                            CARTA_CLICADA = pila_origen.cambiar_estado(CARTA_CLICADA,pila_destino)
                            if CARTA_CLICADA != -1:
                                if isinstance(pila_origen,Pila_Fin):
                                    PUNTUACION = PUNTUACION - 5
                                else:
                                    PUNTUACION = PUNTUACION + 5
                                    ID = ID + 1
                                    estado.guardar_estado(ID,lista_pm,pila_baraja,lista_pf,PUNTUACION)
                            CARTA_CLICADA = None
                            break
                    
                    if CARTA_CLICADA != None: # En el caso 2
                        pila = get_pila(CARTA_CLICADA,lista_pm,pila_baraja,lista_pf)
                        pila.cambiar_estado(CARTA_CLICADA,pila)
                        CARTA_CLICADA = None

                res = cartas_disponibles(lista_pm,pila_baraja,lista_pf)#Obtengo la lista de cartas disponibles
                lista_disponible:list[Carta] = res[0]
                lista_clicable :list[Carta] = res[1]
            

            if event.type == py.MOUSEMOTION:
                if CARTA_CLICADA != None:
                    x, y = py.mouse.get_pos()
                    for z,carta in enumerate(CARTA_CLICADA):
                        carta.x = x - ANCHO_CARTA // 2  
                        carta.y = (y - ALTO_CARTA // 2) - (z*OFFSET_Y)
            

            if event.type == py.KEYDOWN:
                if event.key == py.K_z:
                    if ID > 0 : ID = ID - 1
                    e = estado.cargar_estado(ID,lista_pm,pila_baraja,lista_pf)
                    
                    if e:
                        # Aquí debes reconstruir los objetos a partir del estado
                        lista_pm, pila_baraja, lista_pf, PUNTUACION = e

                        refrescar_pilas(lista_pm,pila_baraja,lista_pf)
                
            res = cartas_disponibles(lista_pm,pila_baraja,lista_pf)#Obtengo la lista de cartas disponibles
            lista_disponible:list[Carta] = res[0]
            lista_clicable :list[Carta] = res[1]
            
        tiempo_transcurrido = int(time.time() - TIEMPO)
        draw_win(win,lista_pm,pila_baraja,lista_pf,CARTA_CLICADA,tiempo_transcurrido)
        

def main():
    
    win = py.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
    clock = py.time.Clock()
    lista_pm,pila_baraja,lista_pf=repartir_cartas()
    #print("El numn {}".format(pila_baraja.get_num_cartas_ini()))
    run(win,clock,lista_pm,pila_baraja,lista_pf)
    #repartir_cartas() #Reparto las cartas de la partida, esto solo se va a hacer 1 vez por partida
    

if __name__ == "__main__":
    main()