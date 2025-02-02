import os
import shutil
import pickle
import pygame as py
from carta import Carta
from pila_baraja import *
from pila_mesa import Pila_Mesa
from pila_fin import Pila_Fin

ANCHO_CARTA = 125
ALTO_CARTA = 175

class Estado():
    CARPETA = 'ESTADOS'
    NOMBRE = 'estado_'
    def __init__(self):
        #Si ya existia la carpeta, la borro y creo una nueva
        if os.path.exists(self.CARPETA):
            shutil.rmtree(self.CARPETA)
        os.makedirs(self.CARPETA, exist_ok=True)
        pass
    
    '''
    Esta funcion recibira todos los parametros de la partida y los guardara en un archivo en la carpeta estados
    Los parametros son:
        -> num: Representa el identificador del archivo
        -> lista_pm: Representa la lista de las pila de la mesa
        -> pila_baraja : Representa la pila baraja
        -> lista_pf : Representa la lista de pilas finales
        -> punt : Representa la puntuacion
    '''

    def guardar_estado(self, num: int, lista_pm: list[Pila_Mesa], pila_baraja: Pila_Baraja, lista_pf: list[Pila_Fin], puntuacion: int):
        archivo = self.NOMBRE + str(num) + '.txt'  # Nombre del archivo
        ruta = os.path.join(self.CARPETA, archivo)
        
        # Crear un diccionario con los datos serializables, incluyendo el atributo 'girado' para cada carta
        estado = {
            "lista_pm": [[{"nombre": carta.nombre, "girado": carta.girado} for carta in pila.cartas] for pila in lista_pm],
            "pila_baraja": {
                "pila_ini": [{"nombre": carta.nombre, "girado": carta.girado} for carta in pila_baraja.pila_ini.cartas],
                "pila_fin": [{"nombre": carta.nombre, "girado": carta.girado} for carta in pila_baraja.pila_fin.cartas]
            },
            "lista_pf": [[{"nombre": carta.nombre, "girado": carta.girado} for carta in pila.cartas] for pila in lista_pf],
            "puntuacion": puntuacion
        }

        with open(ruta, "wb") as f:
            pickle.dump(estado, f)
        print("Estado guardado correctamente.")
        f.close()
    
    def cargar_estado(self, num,l_m:list[Pila_Mesa],p_b:Pila_Baraja,l_f:list[Pila_Fin]):
        archivo = self.NOMBRE + str(num) + '.txt'  # Nombre del archivo
        ruta = os.path.join(self.CARPETA, archivo)
        
        try:
            with open(ruta, "rb") as f:
                estado = pickle.load(f)
                print("Estado cargado correctamente.")

                # Reconstruir las pilas con las cartas, incluyendo el atributo 'girado' y la imagen
                lista_pm = self.reconstruir_pila_mesa(estado["lista_pm"], l_m)
                pila_baraja = self.reconstruir_pila_baraja(estado["pila_baraja"], p_b)
                lista_pf = self.reconstruir_pila_fin(estado["lista_pf"], l_f)

            f.close()
            if num >= 0:
                archivo = self.NOMBRE + str(num+1) + '.txt'  # Nombre del archivo
                ruta = os.path.join(self.CARPETA, archivo)
                os.remove(ruta)
                print("Estado eliminado correctamente")
            
            # Retornar el estado restaurado     
            return lista_pm, pila_baraja, lista_pf, estado["puntuacion"]

        except FileNotFoundError:
            print("No hay un estado guardado.")
            return None


    def reconstruir_pila_mesa(self, datos_pilas, lista_pm:list[Pila_Mesa]):
        nuevas_pilas = []
        for pos, cartas_nombres in enumerate(datos_pilas):
            cartas = []
            for carta_data in cartas_nombres:
                carta = Carta(carta_data["nombre"], self.obtener_imagen(carta_data["nombre"]))  # Obtener la imagen y crear la carta
                carta.girado = carta_data["girado"]  # Restaurar si está girada o no
                cartas.append(carta)
            pila = Pila_Mesa(cartas, lista_pm[pos].x, lista_pm[pos].y, lista_pm[pos].id)
            nuevas_pilas.append(pila)
        return nuevas_pilas


    def reconstruir_pila_baraja(self, datos_baraja, pila_bar:Pila_Baraja):
        cartas_ini = []
        cartas_fin = []

        # Reconstruir las cartas de la pila_ini
        for carta_data in datos_baraja["pila_ini"]:
            carta = Carta(carta_data["nombre"], self.obtener_imagen(carta_data["nombre"]))
            carta.girado = carta_data["girado"]
            cartas_ini.append(carta)
        
        # Reconstruir las cartas de la pila_fin
        for carta_data in datos_baraja["pila_fin"]:
            carta = Carta(carta_data["nombre"], self.obtener_imagen(carta_data["nombre"]))
            carta.girado = carta_data["girado"]
            cartas_fin.append(carta)

        return Pila_Baraja(cartas_ini, cartas_fin, pila_bar.pila_ini.x, pila_bar.pila_ini.y, pila_bar.pila_ini.id)


    def reconstruir_pila_fin(self, datos_pilas, lista_pf:list[Pila_Fin]):
        nuevas_pilas = []
        for pos, cartas_nombres in enumerate(datos_pilas):
            cartas = []
            for carta_data in cartas_nombres:
                carta = Carta(carta_data["nombre"], self.obtener_imagen(carta_data["nombre"]))  # Obtener la imagen y crear la carta
                carta.girado = carta_data["girado"]  # Restaurar si está girada o no
                cartas.append(carta)
            pila = Pila_Fin(cartas, lista_pf[pos].x, lista_pf[pos].y, lista_pf[pos].id)
            nuevas_pilas.append(pila)
        return nuevas_pilas
    
    def obtener_imagen(self,nombre):
        if nombre == "JOKER":
            return py.transform.scale(py.image.load(f"Imagenes/{nombre}.jpg"),(ANCHO_CARTA,ALTO_CARTA))  # Ajusta la ruta si es necesario
        else:
            return py.transform.scale(py.image.load(f"Imagenes/Cartas/{nombre}.jpg"),(ANCHO_CARTA,ALTO_CARTA))  # Ajusta la ruta si es necesario
        


def main():
    e = Estado()



if __name__ == '__main__':
    main()