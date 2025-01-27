from pila import Pila,OFFSET_X
from carta import Carta
import pygame as py

class Pila_Fin(Pila):#Pila en la que se colocaran las pilas finales

    def __init__(self,x:int ,y:int,id:int):#Inicialmente las pilas van a estar vacias
        super().__init__([],x,y,id)
    #Este metodo devolvera -1 si hay algun error, 0 en otro caso
    def join(self, cartas: list[Carta]) -> int:
        '''
        Hay que ver las condiciones en las que se puede meter una carta en esta pila:
            -> Las cartas debe ir de orden creciente empezando por la mas pequeña y terminando por la mayor
            -> Solo se podran poner cartas en los que coincida el tipo de carta (nombre)
        '''
        if (self.cartas[0].nombre == "JOKER" and cartas[0].get_valor()==1 #Caso de que no haya ninguna carta en la pila
            ) or (
            cartas[0].get_tipo() == self.cartas[-1].get_tipo() and cartas[0].get_valor() - 1 == self.cartas[-1].get_valor()): #Caso de que hayan cartas en la pila
            self.join_rev(cartas)
            return None
        else: #Caso de que haya habido un error
            return cartas

    def pop(self,carta:Carta) -> list[Carta]:
        self.cartas.remove(carta)
        self.check_cartas()
        return [carta]