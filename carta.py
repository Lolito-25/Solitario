#Clase Carta en la que se llevara la logica correspondiente a ella
import pygame as py
import os
VALORES = {
    "A":1 , "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13
}
REVERSO= py.transform.scale((py.image.load(os.path.join("Imagenes","Reverso.jpg"))),(125,175))#Reverso de la carta

class Carta(object):
    """
    En el constructor de la carta pasaré:
        ->Nombre de la carta
        ->La imagen de la carta
        ->El reverso de la carta
        ->Si esta girado o no

    Como parametros extra tendrá
        ->El valor de la carta
        ->El tipo de carta
        ->
    """
    IMAGEN = REVERSO
    def __init__(self ,nombre: str ,img ,girado=True):
        #Estas 4 variables son las caracteristicas de una carta
        self.tipo = nombre.split("_")[0]#Indicara de que tipo es la carta
        self.valor = VALORES.get(nombre.split("_")[-1])#Consigo el ultimo caracter del nombre que indica el tipo de carta y del diccionario de valores lo traduzco por un valor numerico del que aplicarle el valor
        self.color = self.calc_color()
        

        #Estas son las propiedades con las que podemos jugar
        self.img = img #Imagen de la carta
        self.girado = girado #Indica si la carta va a estar girada o no
        self.pila = None

        self.x = 0
        self.y = 0

    def girar(self):
        global REVERSO
        self.girado = not(self.girado)
        if self.girado :#Si esta girado entonces la imagen que he de poner es la del revers
            self.IMAGEN = REVERSO
        else:#Si no pongo la imagen normal
            self.IMAGEN = self.img

    def get_valor(self) -> int:
        return self.valor
    
    def get_rect(self) :
        return self.img.get_rect(topleft=(self.x,self.y))

    def get_color(self):
        return self.color

    def get_tipo(self):
        return self.tipo
    
    def calc_color(self) -> str:
        
        if self.tipo == "Corazones" or self.tipo == "Rombo":
            return "R"
        else :
            return "N"

    #Devolvera true si la carta esta girada (reverso)
    def esta_girada(self):
        return self.girado

    def set_pila(self,pila):
        self.pila = pila #Cambio la pila en la que se encuentra la carta
    
    def get_pila(self):
        return self.pila
    '''
    Devuelve la hitbox de la carta si no esta girada y si esta girada devuelve None
    '''
    def get_mask(self):
        if not(self.esta_girada()):
            return py.mask.from_surface(self.IMAGEN)
        else:
            return None
    
    #Esta funcion solo se encargara de pintar las cartas, las coordenadas deberan de manejarlas las pilas correspondientes
    def draw_carta(self,win:py.Surface,x:int,y:int):
        self.x = x
        self.y = y
        rect = self.img.get_rect(topleft = (x,y))
        win.blit(self.IMAGEN,rect.topleft)#Dibujo la imagen

    def __str__(self):
        return self.get_tipo()+" "+self.get_color()+" "+str(self.get_valor())+ " PILA "+ self.get_pila().__str__()
