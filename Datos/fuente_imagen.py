import os,sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir  = os.path.dirname(currentDir)
sys.path.append(parentDir)

from Calculos.algebra import crearVector,getMagnitudVector

class FuenteImagen:
    '''Objeto que almacena los datos de la fuente imagen'''
    def __init__(self,posicion,fuente,receptor,madre,orden):
        self.posicion = posicion 
        self.fuente = fuente
        self.receptor = receptor
        self.destanciaFunete = self.getDistancia(fuente)
        self.distanciaReceptor = self.getDistancia(receptor)
        self.fuenteMadre = madre
        self.orden = orden
    def getDistancia(self,punto_final):
        distancia = getMagnitudVector(crearVector(self.posicion,punto_final))
        return distancia
