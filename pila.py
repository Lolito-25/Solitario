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

    def __init__(self, cartas:list[Carta], x:int, y:int) :
        self.cartas = cartas #Lista de cartas que contendra la pila de cartas de las cuales inicialmente solo 1 estara dada la vuelta y el resto no
        #Ambas coordenadas x e y representan donde se van a dibujar las pilas 
        self.x = x
        self.y = y

    def pop(self,carta:Carta):
        if len(self.cartas)>0:
            index = self.cartas.index(carta)#Veo cual es el indice de la carta
            pop_item = self.cartas[:index+1]#Pop_item contiene una lista de cartas de todas las que van desde ella hasta el principio
            self.cartas = self.cartas[index+1:]#La lista ahora contendra las cartas restantes menos las que se han quitado
            if len(self.cartas)>0:#Si quedan mas cartas en la pila giro la que este en el principio
                self.pila_refresh()
    
    def join(self,carta:Carta):
        self.cartas = [carta]  + self.cartas
    
    def join_rev(self,carta:Carta):
        self.cartas = self.cartas + [carta]

    def pila_refresh(self):
        if self.get_num_cartas()>0:#Si hay cartas en la pila la refresco
            #Compruebo si la pila en la cima de la pila esta girada o no
            if self.cartas[0].girado:#Si la carta esta girada le doy la vuelta
                self.cartas[0].girar()
        
        #Si no esta girada no hago nada

    def get_num_cartas(self) -> int:
        if self.cartas == []:
            return 0
        else:
            return len(self.cartas)
    
    #Para dibujar la pila solo necesito la ventana 
    def draw_pila(self,win:py.Surface):
        #Para ser mas eficiente, no he de pintar todas las cartas una encima de otra, no tendira sentido ya que no se verian, solo pinto la que esta mas arriba
        num = self.get_num_cartas()
        if num > 0:
            self.cartas[-1].draw_carta(win,self.x,self.y)
        else:
            rect = JOKER.get_rect(topleft = (self.x,self.y))#Obtengo el rectangulo asociado a la imagen(hitbox) y cambio sus coordenadas a las pasadas como parametros en la funcion
            win.blit(JOKER,rect.topleft)#Dibujo la imagen


class Pila_Mesa(Pila):#Pila que corresponde a las cartas del juego inicial

    def __init__(self, cartas:list[Carta], x:int, y:int) :
        super().__init__(cartas,x,y)#Llamo al constructor del padre con las cartas
        self.pila_refresh()


    def join(self, cartas_unir :list[Carta]):
        '''
        La logica detras de este join es el siguiente:
        ->Si la pila esta vacia hemos de colocar solamente K
        ->Si la pila no esta vacia hemos de colocar una carta de menor valor y del color contrario
        Colocara la lista de cartas delante de las que ya habia en la pila
        Hemos de comprobar que coincide la ultima carta de la lista que nos pasan, por lo que miraremos cartas_unir[-1]
        '''
        
        if len(self.cartas) == 0: #Caso 1
            if cartas_unir[-1].get_valor()==13:
                self.cartas = cartas_unir + self.cartas
        else: #Caso 2
            if (cartas_unir[-1].get_valor() < self.cartas[0].get_valor()) and (cartas_unir[-1].color != self.cartas[0].color):
                self.cartas = cartas_unir + self.cartas

    def draw_pila(self,win:py.Surface):
        #Para estas, he de sumarle el offset para que se vean las cartas 
        for pos in range(len(self.cartas)-1,-1,-1):#Recorro la lista desde el ultimo elemento hasta el principio
            y_mod = self.y + (len(self.cartas)-1 - pos)*OFFSET_Y
            self.cartas[pos].draw_carta(win,self.x,y_mod)




class Pila_Baraja():#Pila de la que saldran y se pondran las cartas
    #Contendra 2 pilas del tipo Pila, de las cuales 1 sera la pila con todas las cartas restantes y la otra una pila vacia inicialmente
    def __init__(self, cartas: list[Carta], x:int, y:int):
        
        self.pila_ini = Pila(cartas,x,y) #Esta pila se colocara a la derecha, por lo que no le sumaremos el offset
        self.pila_fin = Pila([],x+OFFSET_X,y)
    '''
    Creo una distincion:
        -> pop_ini() : Sirve para sacar una carta de la baraja principal y ponerlo en la baraja final
        -> pop_fin() : Devuelve la carta que este en el principio del mazo fin
    '''
    def pop_ini(self):
        if self.pila_ini.get_num_cartas() > 0: #Si tengo cartas en la pila de inicio, simplemente la giro y la envio a la pila_fin
            carta = self.pila_ini.cartas.pop(0)#Quito la carta que se encuentra en la cima de la pila
            self.pila_ini.pila_refresh()#Refresco la pila
            self.pila_fin.join(carta)#Inserto la carta al inicio de la pila_fin
        else:#En caso de que no queden cartas en la pila inicial y se pulse, se devolveran todas las pilas en el orden inverso y se giraran
            for carta in self.pila_fin.cartas:
                carta.girar()
                self.pila_ini.join_rev(carta)
            
    def pop_fin(self) -> Carta:
        if self.pila_fin.get_num_cartas() > 0:
            return self.pila_fin.pop(0)
    
    def get_num_cartas_ini(self) -> int:
        return self.pila_ini.get_num_cartas()

    def get_num_cartas_fin(self) -> int:
        return self.pila_fin.get_num_cartas()


    def draw_pila(self,win:py.Surface):
        self.pila_ini.draw_pila(win)
        self.pila_fin.draw_pila(win)

class Pila_Fin(Pila):#Pila en la que se colocaran las pilas finales

    def __init__(self,x:int ,y:int):#Inicialmente las pilas van a estar vacias
        self.cartas= []
        self.x = x
        self.y = y
    
    def join(self, carta: Carta):
        '''
        Hay que ver las condiciones en las que se puede meter una carta en esta pila:
            -> Las cartas debe ir de orden creciente empezando por la mas pequeña y terminando por la mayor
            -> Solo se podran poner cartas en los que coincida el tipo de carta (nombre)
        '''
        if self.get_num_cartas() == 0:
            if carta.get_valor() == 1:  
                self.join_rev(carta)
        elif (carta.valor - self.cartas[0] == 1) and (self.cartas[0].tipo == carta.tipo):
            self.join_rev(carta)

