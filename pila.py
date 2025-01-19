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
    def join(self,cartas:list[Carta]):
        self.cartas = cartas + self.cartas
        self.pila_refresh()
    
    #Este metodo une una lista de cartas a la pila por el final
    def join_rev(self,cartas:Carta):
        cartas.girar()
        self.cartas = self.cartas + [cartas]
        

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
        if num > 0:
            self.cartas[-1].draw_carta(win,self.x,self.y)
        else:
            rect = JOKER.get_rect(topleft = (self.x,self.y))#Obtengo el rectangulo asociado a la imagen(hitbox) y cambio sus coordenadas a las pasadas como parametros en la funcion
            win.blit(JOKER,rect.topleft)#Dibujo la imagen

    def __str__(self):
        return str(self.id)

class Pila_Mesa(Pila):#Pila que corresponde a las cartas del juego inicial

    def __init__(self, cartas:list[Carta], x:int, y:int,id:int) :
        super().__init__(cartas,x,y,id)#Llamo al constructor del padre con las cartas
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

    def pop(self,carta:Carta) -> list[Carta]:
        cartas = super().pop(carta) #LLamo al padre para eliminar las cartas
        if self.get_num_cartas()>0: #Si quedan elementos en la pila, la refresco
            self.pila_refresh()
        return cartas


    def draw_pila(self,win:py.Surface):
        #Para estas, he de sumarle el offset para que se vean las cartas 
        if(self.get_num_cartas() == 0):
            rect = JOKER.get_rect(topleft = (self.x,self.y))#Obtengo el rectangulo asociado a la imagen(hitbox) y cambio sus coordenadas a las pasadas como parametros en la funcion
            win.blit(JOKER,rect.topleft)#Dibujo la imagen
        else:
            for pos in range(self.get_num_cartas()-1,-1,-1):#Recorro la lista desde el ultimo elemento hasta el principio
                y_mod = self.y + (len(self.cartas)-1 - pos)*OFFSET_Y
                self.cartas[pos].draw_carta(win,self.x,y_mod)




class Pila_Baraja():#Pila de la que saldran y se pondran las cartas

    #Contendra 2 pilas del tipo Pila, de las cuales 1 sera la pila con todas las cartas restantes y la otra una pila vacia inicialmente
    def __init__(self, cartas: list[Carta], x:int, y:int,id:int):
        self.pila_ini = Pila(cartas,x,y,id) #Esta pila se colocara a la izquierda, por lo que no le sumaremos el offset
        self.pila_fin = Pila([],x+OFFSET_X,y,id)
    '''
    Creo una distincion:
        -> pop_ini() : Sirve para sacar una carta de la baraja principal y ponerlo en la baraja final
            -Las cartas de la baraja inicial estan todas dadas la vuelta, por lo que no tengo que preocuparme por girarlas
            -Cuando haga pop sobre la baraja inicial vacia significara que quiero traspasar todas las cartas de la pila final a la inicial de manera inversa (la ultima carta de la pila final sera la primera de la pila inicial)

        -> pop_fin() : Devuelve la carta que este en el principio del mazo fin
            -Cuando haga pop con la pila vacia no pasa nada
            -Cuando haga pop con la pila con cartas, devuelvo la carta y refresco la pila
            -Cuando la pila inicial devuelve una carta a la pila final, no he de girar el resto, solo giro la que me pasan
    '''

    def pop(self, carta:Carta):
        if carta.get_pila() == self.pila_ini:
            self.pop_ini(carta)
        else:
            self.pop_fin(carta)

    #Este metodo elimina la carta del inicio de la pila de la pila inicial (Donde se cogen las cartas)
    def pop_ini(self,carta:Carta):
        if self.pila_ini.get_num_cartas() > 0: #Caso de que haya mas cartas en la pila
            c = self.pila_ini.pop(carta) #Elimino la primera carta de la pila (girada)
            self.pila_fin.join_rev(c)#Añado la carta a la pila final de manera inversa
        else: #Caso de que no hayan cartas en la pila y quiera coger todas las cartas de la pila final
            for c in self.pila_fin.cartas:
                c.girar() #Giro la carta
                self.pila_ini.join([c]) #Añado la carta a la pila inicial
            
    
    #Este metodo elimina la carta del final de la pila de la pila final (Donde se dejan las cartas que no se usan)
    def pop_fin(self,carta:Carta) -> Carta:
        if self.pila_fin.get_num_cartas() > 0:#En el caso de que queden cartas en la pila
            c = self.pila_fin.pop(carta)[0] #Quito la carta de encima de la pila
            self.pila_fin.pila_refresh() #Refresco la pila final
            return c
        else:
            return None
    
    def get_num_cartas_ini(self) -> int:
        return self.pila_ini.get_num_cartas()

    def get_num_cartas_fin(self) -> int:
        return self.pila_fin.get_num_cartas()


    def draw_pila(self,win:py.Surface):
        self.pila_ini.draw_pila(win)
        self.pila_fin.draw_pila(win)

class Pila_Fin(Pila):#Pila en la que se colocaran las pilas finales

    def __init__(self,x:int ,y:int,id:int):#Inicialmente las pilas van a estar vacias
        super().__init__([],x,y,id)
    
    #Este metodo devolvera -1 si hay algun error, 0 en otro caso
    def join(self, carta: Carta) -> int:
        '''
        Hay que ver las condiciones en las que se puede meter una carta en esta pila:
            -> Las cartas debe ir de orden creciente empezando por la mas pequeña y terminando por la mayor
            -> Solo se podran poner cartas en los que coincida el tipo de carta (nombre)
        '''
        if (self.get_num_cartas() == 0 and carta.get_valor()==1 #Caso de que no haya ninguna carta en la pila
            ) or (
            carta.get_tipo() == self.cartas[-1].get_tipo() and carta.get_valor() - 1 == self.cartas[-1].get_valor()): #Caso de que hayan cartas en la pila
            super().join_rev([carta])
            return 0
        else: #Caso de que haya habido un error
            return -1

       
