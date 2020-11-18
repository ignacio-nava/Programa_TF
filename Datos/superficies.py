
import os,sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir  = os.path.dirname(currentDir)
sys.path.append(parentDir)

from Calculos.algebra import crearVectorNormal,multiplicarVectorEscalar,getMagnitudVector

class Superficie:
    def __init__(self, orden, nombre, padre, indice, grafica=True, **datos):
        self.orden = orden
        self.nombre = nombre
        self.padre = padre
        self.indice = indice
        #self.lineasChildren = []
        self.lineas = []
        self.color = (0, 0, 0, 255)
        self.grafica = grafica
        self.vertices = []
        self.normal = []
        self.vertices = {'vertice_1':'',
                         'vertice_2':'',
                         'vertice_3':'',
                         'vertice_4':''}
        self.normal_direccion = {'direccion':False}
        self.normal_visible = {'visibilidad':True}
        self.material_info = {'m_nombre':'',
                              'm_125':'',
                              'm_250':'',
                              'm_500':'',
                              'm_1000':'',
                              'm_2000':'',
                              'm_4000':'',
                              'm_nrc':'',}
        self.verts_list = self.getVertices()
        self.normal_lineas = []
        self.area = None
        self.color_area = None
        self.pared_relleno = None
        self.alpha_relleno = 0
        for key, value in datos.items():
            setattr(self, key, value)
    def setVertices(self,key,arg):
        if type(arg) == list:
            for i in range(len(arg)):
                arg[i] = str(arg[i])
            arg = (','.join(arg)).replace(',',', ')
        self.vertices[key] = arg
    def setNormal(self):
        if self.comprobarCondicion(0):
            puntos = self.comprobarCondicion(1)
            if puntos != None:
                self.normal = crearVectorNormal(self.verts_list[puntos[0]],
                                                self.verts_list[puntos[1]],
                                                self.verts_list[puntos[2]])
                if self.normal_direccion['direccion']:
                    self.normal = multiplicarVectorEscalar(self.normal,-1)
            else:
                self.normal = None
        else:
            self.normal = None
    def getVertices(self, orden_inverso=False):
        vertices = []
        vers = [self.vertices['vertice_1'],self.vertices['vertice_2'],self.vertices['vertice_3'],self.vertices['vertice_4']]
        for ver in vers:
            ver = (ver.replace(' ','')).split(',')
            if len(ver) == 3:
                vertice = []
                for i in range(len(ver)):
                    vertice.append(float(ver[i]))
                vertices.append(vertice)
            else:
                vertices.append('')
        self.verts_list = vertices
        if orden_inverso:
            x, y, z = [], [], []
            for vertice in vertices:
                x.append(vertice[0])
                y.append(vertice[1])
                z.append(vertice[2])
            vertices = [list(zip(x, y, z))]
        return vertices
    def comprobarCondicion(self,condicion):
        '''condicion (int);
        Condiciones que se pueden comprobar:
        - Todos los puntos ingresados => 0
        - Al menos 3 puntos distinos => 1'''
        if condicion == 0:
            if type(self.verts_list[0]) == type(self.verts_list[1]) == type(self.verts_list[2]) == type(self.verts_list[3]):
                return True
            else:
                return False
        elif condicion == 1:
            for i in range(-1,3):
                if self.verts_list.count(self.verts_list[i]) == 1:
                    if self.verts_list[i+1] != self.verts_list[i+2]:
                        return (i,i+1,i+2)
                    elif self.verts_list[i+1] != self.verts_list[i+3]:
                        return (i,i+1,i+3)
                    elif self.verts_list[i+2] != self.verts_list[i+3]:
                        return (i,i+2,i+3)
            return None
        else:
            print('No se puede comprobar esta la condición: "%s"'%(condicion))
            return None
    def getArea(self):
        n1 = crearVectorNormal(self.verts_list[0],self.verts_list[1],self.verts_list[2],unitario=False)
        n2 = crearVectorNormal(self.verts_list[0],self.verts_list[2],self.verts_list[3],unitario=False)
        area = getMagnitudVector(n1)/2 + getMagnitudVector(n2)/2
        self.area = area
    def getColorGrafica(self, relleno=False):
        if not relleno:
            if type(self.color) == str:
                self.color = (0,0,0,255)
            color = [self.color[i]/256 for i in range(len(self.color))]
        else:
            if type(self.color_area) == str or self.color_area == None:
                self.color_area = (255, 255, 255, 255)
            color = [self.color_area[i]/256 for i in range(len(self.color_area))]
        return color
        
