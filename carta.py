#Clase Carta en la que se llevara la logica correspondiente a ella

class Carta:
    """
    En el constructor de la carta pasaré:
        ->Nombre de la carta
        ->La imagen de la carta
        ->Si esta girado o no
    Como parametros extra tendrá
    """
    def __init__(self ,nombre ,img ,girado=True) -> None:
        self.nombre = nombre
        self.img = img
        self.girado = girado
        