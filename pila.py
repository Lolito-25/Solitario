from carta import Carta

#Estructura de datos que se correspondera con una pila

'''
Estos son los tipos de pila que van a haber:
-> 1 pilas de tipo Pila_Baraja, seran de las que se sacan las cartas y a las que iran las cartas si son descartadas de la baraja inicial
-> 7 pilas de tipo Pila_Mesa, seran con las cuales puedes cambiar entre pilas
-> 4 pilas de tipo Pila_Fin, seran los montones finales en los que colocar las cartas
'''

class Pila(object):

    def __init__(self, cartas:list[Carta]) :
        self.cartas = cartas #Lista de cartas que contendra la pila de cartas de las cuales inicialmente solo 1 estara dada la vuelta y el resto no
        

    def pop(self,carta:Carta):
        if len(self.cartas)>0:
            index = self.cartas.index(carta)#Veo cual es el indice de la carta
            pop_item = self.cartas[:index+1]#Pop_item contiene una lista de cartas de todas las que van desde ella hasta el principio
            self.cartas = self.cartas[index:]#La lista ahora contendra las cartas restantes menos las que se han quitado
            if len(self.cartas)>0:#Si quedan mas cartas en la pila giro la que este en el principio
                self.cartas[0].girar()
    
    def join(self,carta:Carta):
        self.cartas = [carta]+self.cartas
    
    def join_rev(self,carta:Carta):
        self.cartas +=[carta]


    def get_num_cartas(self) -> int:
        return len(self.cartas)
class Pila_Mesa(Pila):#Pila que corresponde a las cartas del juego inicial

    def __init__(self, cartas: list[Carta]):
        super().__init__(cartas)#Llamo al constructor del padre con las cartas

    def join(self, cartas_unir :list[Carta]):
        '''
        La logica detras de este join es el siguiente:
        ->Si la pila esta vacia hemos de colocar solamente K
        ->Si la pila no esta vacia hemos de colocar una carta de menor valor y del color contrario
        Colocara la lista de cartas delante de las que ya habia en la pila
        Hemos de comprobar que coincide la ultima carta de la lista que nos pasan, por lo que miraremos cartas_unir[-1]
        '''
        prim_cart = cartas_unir[-1]
        if len(self.cartas) == 0: #Caso 1
            if prim_cart.get_valor()==13:
                self.cartas = cartas_unir + self.cartas
        else: #Caso 2
            if (prim_cart.get_valor() < self.cartas[0].get_valor()) and (prim_cart.color != self.cartas[0].color):
                self.cartas = cartas_unir + self.cartas

class Pila_Baraja():#Pila de la que saldran y se pondran las cartas
    #Contendra 2 pilas del tipo Pila, de las cuales 1 sera la pila con todas las cartas restantes y la otra una pila vacia inicialmente
    def __init__(self, cartas: list[Carta]):
        self.pila_ini = Pila(cartas)
        self.pila_fin = Pila([])

    #AÑADIR DISTINCION EN EL POP, NO FUNCIONARIA ASI!!!!

    def pop(self):
        if self.pila_ini.get_num_cartas() > 0: #Si tengo cartas en la pila de inicio, simplemente la giro y la envio a la pila fin
            carta = self.pila_ini.cartas.pop()#Quito la ultima carta de la lista de la pila inicial y la meto al inicio de la otra pila
            carta.girar()#Giro la carta
            self.pila_fin.join(carta)
        else:# Si no me quedan cartas en el mazo principal, recupero todas las cartas, girandolas de nuevo
            for carta in self.pila_fin.cartas:
                carta.girar()
                self.pila_ini.join_rev()

                

    
