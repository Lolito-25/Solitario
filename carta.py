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
        #Estas 3 variables son las caracteristicas de una carta
        self.tipo = nombre.split("_")[0]#Indicara de que tipo es la carta
        self.valor = VALORES.get(nombre.split("_")[-1])#Consigo el ultimo caracter del nombre que indica el tipo de carta y del diccionario de valores lo traduzco por un valor numerico del que aplicarle el valor
        self.color = self.calc_color()
        

        #Estas son las propiedades con las que podemos jugar
        self.img = img #Imagen de la carta
        self.girado = girado #Indica si la carta va a estar girada o no


    def girar(self):
        global REVERSO
        self.girado = not(self.girado)
        if self.girado :#Si esta girado entonces la imagen que he de poner es la del revers
            self.IMAGEN = REVERSO
        else:#Si no pongo la imagen normal
            self.IMAGEN = self.img

    def get_valor(self) -> int:
        return self.valor
    
    def get_imagen(self) :
        return self.IMAGEN

    def calc_color(self) -> str:
        
        if self.tipo == "Corazones" or self.tipo == "Rombo":
            return "R"
        else :
            return "N"

    '''
    Devuelve la hitbox de la carta si no esta girada y si esta girada devuelve None
    '''
    def get_mask(self):
        if not(self.girado):
            return py.mask.from_surface(self.IMAGEN)
        else:
            return None
    
    #Esta funcion solo se encargara de pintar las cartas, las coordenadas deberan de manejarlas las pilas correspondientes
    def draw_carta(self,win:py.Surface,x:int,y:int):
        rect = self.IMAGEN.get_rect(topleft = (x,y))#Obtengo el rectangulo asociado a la imagen(hitbox) y cambio sus coordenadas a las pasadas como parametros en la funcion
        win.blit(self.IMAGEN,rect.topleft)#Dibujo la imagen

        
        

    

