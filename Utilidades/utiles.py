import os,sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir  = os.path.dirname(currentDir)
sys.path.append(parentDir)

import pandas as pd

class DataParaRT60:
    def __init__(self, **kwargs):
         self.Pared = []
         self.Material = []
         self.Area = []
         self.Hz125 = []
         self.Hz250 = []
         self.Hz500 = []
         self.Hz1000 = []
         self.Hz2000 = []
         self.Hz4000 = []
    def agregarHijas(self, **kwargs):
       for key in kwargs.keys():
           variable = getattr(self, key)
           variable += kwargs[key]
def ordenarLista(lista,indice):
    '''Ordena una lista de acuerdo a un indice dado.
    lista => list 2D
    indice => int'''
    if indice == 0:
        lista.sort(key=indice_0)
    return lista
def indice_0(lista):
    return lista[0]
