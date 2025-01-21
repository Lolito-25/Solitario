from carta import Carta
import pygame as py
import os
#Estructura de datos que se correspondera con una pila

'''
Estos son los tipos de pila que van a haber:
-> 1 pilas de tipo Pila_Baraja, seran de las que se sacan las cartas y a las que iran las cartas si son descartadas de la baraja inicial
-> 7 pilas de tipo Pila_Mesa, seran con las cuales puedes cambiar entre pilas
-> 4 pilas de tipo Pila_Fin, seran los montones finales en los que colocar las cartas
'''
OFFSET_X = 200 #Representa el offset que tienen las pilas de cartas entre ellas en caso de ser del mismo tipo
OFFSET_Y = 35 #Representa el offset en el eje y

JOKER= py.transform.scale((py.image.load(os.path.join("Imagenes","Joker.jpg"))),(125,175))#Reverso de la carta


class Pila(object):

    def __init__(self, cartas:list[Carta], x:int, y:int, id:int) :
        self.cartas = cartas #Lista de cartas que contendra la pila de cartas de las cuales inicialmente solo 1 estara dada la vuelta y el resto no
        for carta in cartas:
            carta.set_pila(self)
            carta.x = x
            carta.y = y
        #Ambas coordenadas x e y representan donde se van a dibujar las pilas 
        self.x = x
        self.y = y

        self.id = id #Identificador de la pila (no sirve de mucho)
        
    #Este metodo recibe una carta que ha de salir y devuelve el resto de cartas que van desde ella hasta el tope de la pila
    def pop(self,carta:Carta) -> Carta:
        if len(self.cartas)>0:
            index = self.cartas.index(carta)#Veo cual es el indice de la carta
            pop_item = self.cartas[index]#Pop_item contiene una lista de cartas de todas las que van desde ella hasta el principio
            self.cartas = self.cartas[index+1:]#La lista ahora contendra las cartas restantes menos las que se han quitado
            return pop_item
        else:
            return None
    
    #Este metodo une una lista de cartas a la pila por el principio
    def join(self,carta:Carta):
        self.cartas = [carta] + self.cartas
        carta.set_pila(self)
    
    #Este metodo une una lista de cartas a la pila por el final
    def join_rev(self,cartas:Carta):
        cartas.girar()
        self.cartas = self.cartas + [cartas]
        cartas.set_pila(self)
        

    #Este metodo refresca la pila, girando la carte de mas arriba (si no esta girada)
    def pila_refresh(self):
        if self.get_num_cartas()>0:#Si hay cartas en la pila la refresco
            #Compruebo si la pila en la cima de la pila esta girada o no
            if self.cartas[0].esta_girada():#Si la carta esta girada le doy la vuelta
                self.cartas[0].girar()
        
            #Si no esta girada no hago nada

    #Este metodo devuelve el numero de cartas
    def get_num_cartas(self) -> int:
        if self.cartas == []:
            return 0
        else:
            return len(self.cartas)
    #Este metodo devuelte todas las cartas de la pila
    def get_cartas(self):
        return self.cartas

    #Para dibujar la pila solo necesito la ventana 
    def draw_pila(self,win:py.Surface):
        #Para ser mas eficiente, no he de pintar todas las cartas una encima de otra, no tendira sentido ya que no se verian, solo pinto la que esta mas arriba
        num = self.get_num_cartas()
        if num > 0 and self.cartas[-1] != JOKER:
            self.cartas[-1].draw_carta(win,self.x,self.y)
        else:
            rect = JOKER.get_rect(topleft = (self.x,self.y))#Obtengo el rectangulo asociado a la imagen(hitbox) y cambio sus coordenadas a las pasadas como parametros en la funcion
            win.blit(JOKER,rect.topleft)#Dibujo la imagen

    '''
    Esta funcion recibira como parametros:
        -self : Es la pila en la que se va a hacer el join (sera ella misma si no funciona la cosa)
        -carta : Es la carta que se va a meter en la pila nueva (self)
        -pila : Es la pila antigua de la carta
    '''
    def cambiar_estado(self, carta : Carta, pila):
        c = self.join(carta) #Introduzco la nueva carta en la pila
        if c != None:#Caso de que algo haya ido mal en el proceso
            pila.join(c)
        pila.pila_refresh() #Refresco la pila anterior
        



    def __str__(self):
        return str(self.id)
       
