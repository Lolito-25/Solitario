import pygame as py
import os
from os import listdir
import time as tm
import random
from carta import Carta
#CONSTANTES
DIR = "../Solitario/Imagenes/Cartas"#Direccion donde se encuentran las imagenes

BARAJA=[]#Lista que contiene todas las cartas(Objeto) de la baraja
REVERSO= py.image.load(os.path.join("Imagenes","Reverso.jpg"))#Reverso de la carta
FONDO= py.image.load(os.path.join("Imagenes","Fondo.jpg"))#Fondo de pantalla

ANCHO_VENTANA = 1600
ALTO_VENTANA = 900 
# Inicializar pygame
py.init()

#Cargo las imagenes de las cartas
for imagen in os.listdir(DIR):
    if imagen.endswith('.jpg'):
        #Imagen contiene el nombre entero del archivo, he de crear un objeto Carta
        name = imagen.replace('.jpg',"")
        img = py.image.load(os.path.join(DIR,imagen))
        BARAJA.append(Carta(name,img,REVERSO))




