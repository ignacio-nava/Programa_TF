import numpy as np 
from math import sqrt

def crearVector(inicial,final):
    '''Crea un vector entre un punto incial y uno final
    inicial => list
    final => list
    '''
    vector = restarVectores(final,inicial)
    return vector
def crearVectorNormal(A,B,C,unitario=True):
    '''Crea un vector normal con tres puntos (A, B y C) sobre un mismo plano, usando A como pivot
    A => list
    B => list
    C => list
    '''
    vector_1 = crearVector(A,B)
    vector_2 = crearVector(A,C)
    normal = list(np.cross(vector_1,vector_2))
    if unitario:
        magnitud = getMagnitudVector(normal)
        nomal_unitario = [normal[0]/magnitud,normal[1]/magnitud,normal[2]/magnitud]
        return nomal_unitario
    else:
        return normal
def getMagnitudVector(vector):
    '''Retorna la magnitud de un vector de 1D
    vector => list
    '''
    suma = 0
    for i in vector:
        suma += i**2
    suma = sqrt(suma)
    return suma
def multiplicarVectorEscalar(A,b):
    '''Multiplica el vector A por el escalar b
    A => list (1D)
    b => float
    '''
    for i in range(len(A)):
        A[i] = A[i] * b
    return A
def restarVectores(A,B):
    '''Retorna el vector C como la resta A - B = C
    A => list
    B => list
    '''
    resta = []
    for a,b in zip(A,B):
        resta.append(a-b)
    return resta
def sumarVectores(A,B):
    '''Retorna la suma de los vectores A y B
    A => list
    B => list
    '''
    suma = []
    for a,b in zip(A,B):
        suma.append(a+b)
    return suma

