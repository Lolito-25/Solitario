from pila import Pila,OFFSET_X
from carta import Carta
import pygame as py

class Pila_Baraja(Pila):#Pila de la que saldran y se pondran las cartas

    #Contendra 2 pilas del tipo Pila, de las cuales 1 sera la pila con todas las cartas restantes y la otra una pila vacia inicialmente
    def __init__(self, cartas_m: list[Carta],cartas_d:list[Carta], x:int, y:int,id:int):
        self.pila_ini = Pila_Mazo(cartas_m,x,y,id) #Esta pila se colocara a la izquierda, por lo que no le sumaremos el offset
        self.pila_fin = Pila_Deposito(cartas_d,x+OFFSET_X,y,id)

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
        if isinstance(carta.get_pila(),Pila_Mazo):
            return self.pop_ini(carta)
        else:
            return self.pop_fin(carta)

    def check_cartas(self):
        self.pila_ini.check_cartas()
        self.pila_fin.check_cartas()

    def pila_refresh(self):
        self.pila_fin.pila_refresh()

    #Este metodo elimina la carta del inicio de la pila de la pila inicial (Donde se cogen las cartas)
    def pop_ini(self,carta:Carta):
        if self.pila_ini.get_num_cartas() > 0 and self.pila_ini.cartas[0] != Carta("JOKER",None): #Caso de que haya mas cartas en la pila
            self.pila_ini.cartas.remove(carta) #Elimino la primera carta de la pila (girada)            
            self.pila_fin.join_rev([carta])#Añado la carta a la pila final de manera inversa
            carta.girar()
            self.pila_ini.check_cartas()
            return None
        elif self.pila_ini.cartas[0] == Carta("JOKER",None): #Caso de que no hayan cartas en la pila y quiera coger todas las cartas de la pila final
            for c in self.pila_fin.cartas:
                c.girar() #Giro la carta
                self.pila_ini.join([c]) #Añado la carta a la pila inicial
            self.pila_fin.cartas = []
            self.pila_fin.check_cartas()
            self.pila_ini.check_cartas()
            return None
    
    #Este metodo elimina la carta del final de la pila de la pila final (Donde se dejan las cartas que no se usan)
    def pop_fin(self,carta:Carta) -> list[Carta]:
        if self.pila_fin.get_num_cartas() > 0:#En el caso de que queden cartas en la pila
            #Devuelvo la carta en la ultima posicion
            c = self.pila_fin.cartas[-1]
            self.pila_fin.cartas.remove(c)
            self.pila_fin.check_cartas()
            return [c]
        else:
            return None
    
    def get_num_cartas_ini(self) -> int:
        return self.pila_ini.get_num_cartas()

    def get_num_cartas_fin(self) -> int:
        return self.pila_fin.get_num_cartas()

    def contiene_carta(self, carta:Carta) -> bool:
        return carta.get_pila().id == self.pila_fin.id

    def draw_pila(self,win:py.Surface):
        self.pila_ini.draw_pila(win)
        self.pila_fin.draw_pila(win)
        


#Esta clase hace referencia a la pila donde inicialmente se dejan las cartas
class Pila_Mazo(Pila):
    def __init__(self, cartas, x, y, id):
        super().__init__(cartas, x, y, id)

#Esta clase hace referencia a la pila donde se depositan las cartas de la pila mazo
class Pila_Deposito(Pila):
    def __init__(self, cartas, x, y, id):
        super().__init__(cartas, x, y, id)