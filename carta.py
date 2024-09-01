#Clase Carta en la que se llevara la logica correspondiente a ella

VALORES = {
    "A":1 , "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13
}

class Carta(object):
    """
    En el constructor de la carta pasaré:
        ->Nombre de la carta
        ->La imagen de la carta
        ->Si esta girado o no
    Como parametros extra tendrá
    """
    def __init__(self ,nombre: str ,img ,reverso ,girado=True):
        self.nombre = nombre #Nombre de la carta
        self.img = img #Imagen de la carta
        self.reverso = reverso #Imagen del reverso
        self.girado = girado #Indica si la carta va a estar girada o no
        self.valor = VALORES.get(nombre.split("_")[-1])#Consigo el ultimo caracter del nombre que indica el tipo de carta y del diccionario de valores lo traduzco por un valor numerico del que aplicarle el valor
        self.color = self.calc_color()

    def girar(self) -> None:
        self.girado = not(self.girado)

    def get_valor(self) -> int:
        return self.valor
    
    def calc_color(self) -> str:
        color = self.nombre.split("_")[0]#Obtengo el nombre de la carta
        if color == "Corazones" or color == "Rombo":
            return "R"
        else :
            return "N"

