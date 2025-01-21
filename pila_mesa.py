from pila import Pila,JOKER,OFFSET_Y
from carta import Carta
import pygame as py

class Pila_Mesa(Pila):#Pila que corresponde a las cartas del juego inicial

    def __init__(self, cartas:list[Carta], x:int, y:int,id:int) :
        super().__init__(cartas,x,y,id)#Llamo al constructor del padre con las cartas
        self.pila_refresh()


    def join(self, carta_unir :Carta):
        '''
        La logica detras de este join es el siguiente:
        ->Si la pila esta vacia hemos de colocar solamente K
        ->Si la carta ya pertenecia a esta pila la metemos, da igual el valor
        ->Si la pila no esta vacia hemos de colocar una carta de menor valor y del color contrario
        Colocara la lista de cartas delante de las que ya habia en la pila
        Hemos de comprobar que coincide la ultima carta de la lista que nos pasan, por lo que miraremos cartas_unir[-1]
        '''
        
        if len(self.cartas) == 0: #Caso 1
            if carta_unir.get_valor()==13:
                self.cartas = [carta_unir] + self.cartas
        elif carta_unir.get_pila()==self:
            self.cartas = [carta_unir] + self.cartas
        else: #Caso 2
            if (self.cartas[0].get_valor()-carta_unir.get_valor() == 1) and (carta_unir.color != self.cartas[0].color):
                self.cartas = [carta_unir] + self.cartas
                carta_unir.set_pila(self)
            else:
                return carta_unir #Caso de que no se pueda unir

    def pop(self,carta:Carta) -> list[Carta]:
        cartas = super().pop(carta) #LLamo al padre para eliminar las cartas
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
