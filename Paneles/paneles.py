# -*- coding: utf-8 -*-
import os,sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir  = os.path.dirname(currentDir)
sys.path.append(parentDir)

from Calculos.algebra import sumarVectores, multiplicarVectorEscalar
from Calculos.grafica import obtenerLimites
from Utilidades.utiles import DataParaRT60

import numpy as np
import pandas as pd
import wx
import wx.xrc
import wx.dataview 
import wx.propgrid as pg
import wx.grid
import matplotlib.pyplot as plt
from Datos.superficies import Superficie
from Ventanas.ventanas import VenRecintoNuevo
from Utilidades.utiles import ordenarLista

from sympy.parsing.sympy_parser import parse_expr

from matplotlib.artist import Artist
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure

size_boton = (24,24)
ancho_linea = 0.4

class PanelRecinto ( wx.Panel ):
    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 292,631 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )
        self.name = name
        sizer_main = wx.BoxSizer( wx.VERTICAL )
    #   Tree Ctrl
        sizer_UP = wx.BoxSizer( wx.VERTICAL )
        self.toolbar = TB_Datos(self)
        
        sizer_UP.Add(self.toolbar, 0, wx.EXPAND)

        self.treeCtrl_recinto = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_EDIT_LABELS|
                                                                                                  wx.TR_LINES_AT_ROOT|
                                                                                                  wx.TR_HAS_BUTTONS|
                                                                                                  wx.TR_ROW_LINES )
        sizer_UP.Add( self.treeCtrl_recinto, 2, wx.ALL|wx.EXPAND, 5 )
        root = Superficie(-1, 'Recinto', None, None, grafica=False)
        self.ROOT = self.treeCtrl_recinto.AddRoot('Recinto',data=root)
        self.treeCtrl_recinto.SetItemBold(self.ROOT)

        sizer_main.Add( sizer_UP, 3, wx.EXPAND, 5 )

        sizer_DOWN = wx.BoxSizer( wx.VERTICAL )

        sizer_D_up = wx.BoxSizer( wx.VERTICAL )

        # self.staticText_superficie = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.staticText_superficie.Wrap( -1 )

        # sizer_D_up.Add( self.staticText_superficie, 1, wx.ALL|wx.EXPAND, 5 )


        sizer_DOWN.Add( sizer_D_up, 0, wx.EXPAND, 5 )
    #   Property Manager
        sizer_D_down = wx.BoxSizer( wx.VERTICAL )
    
        self.pm_superficie = pg.PropertyGridManager(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, pg.PGMAN_DEFAULT_STYLE|
                                                                                                         pg.PG_BOLD_MODIFIED|
                                                                                                         pg.PG_SPLITTER_AUTO_CENTER|
                                                                                                         pg.PG_STATIC_SPLITTER )                                                                                                                                                                                             
        self.pm_superficie.SetExtraStyle( wx.propgrid.PG_EX_MODE_BUTTONS )
        sizer_D_down.Add( self.pm_superficie, 1, wx.ALL|wx.EXPAND, 5 )
    
        page = self.pm_superficie.AddPage("Superficie")
        page.Append(pg.PropertyCategory('Vertices (x,y,z)', 'vertices'))
        page.Append(pg.StringProperty('Vertice 1', 'vertice_1'))
        page.Append(pg.StringProperty('Vertice 2', 'vertice_2'))
        page.Append(pg.StringProperty('Vertice 3', 'vertice_3'))
        page.Append(pg.StringProperty('Vertice 4', 'vertice_4'))
        page.Append(pg.PropertyCategory('Vector Normal', 'normal'))
        dire_normal = page.Append(pg.BoolProperty('Dirección', 'direccion', False))
        dire_normal.SetAttribute(pg.PG_BOOL_USE_CHECKBOX, True)
        page.Append(pg.PropertyCategory('Superficie', 'area_op'))
        page.Append(pg.StringProperty('Área [m2]', 'area_sup'))
        page.Append(pg.ColourProperty('Color Líneas', 'color_lineas'))
        visible_linea = page.Append(pg.BoolProperty('Línea Visible', 'mostrar_linea', True))
        visible_linea.SetAttribute(pg.PG_BOOL_USE_CHECKBOX, True)
        page.Append(pg.ColourProperty('Color Área', 'color_area'))
        page.Append(pg.StringProperty('Transparencia Área', 'alpha_area'))
        page.Append(pg.PropertyCategory('Material Superficie', 'materiales'))
        page.Append(pg.StringProperty('Nombre', 'm_nombre'))
        page.Append(pg.StringProperty('125 Hz', 'm_125'))
        page.Append(pg.StringProperty('250 Hz', 'm_250'))
        page.Append(pg.StringProperty('500 Hz', 'm_500'))
        page.Append(pg.StringProperty('1000 Hz', 'm_1000'))
        page.Append(pg.StringProperty('2000 Hz', 'm_2000'))
        page.Append(pg.StringProperty('4000 Hz', 'm_4000'))
        page.Append(pg.StringProperty('NRC', 'm_nrc'))

        self.pm_superficie.CollapseAll()
        sizer_DOWN.Add( sizer_D_down, 1, wx.EXPAND, 5 )


        sizer_main.Add( sizer_DOWN, 1, wx.EXPAND, 5 )

        self.SetSizer( sizer_main )
        self.Layout()
 #  Incializacion de Variables
        self.padre = parent.GetParent()
        self.superficie_activa = self.ROOT
 #  Incializacion de Funciones
        self.soloLectura(True)
 #  Connect Events
   # ---------------------------------------- TreeCtrl ---------------------------------------- #
        self.treeCtrl_recinto.Bind( wx.EVT_TREE_END_LABEL_EDIT, self.onEditarLabel )
        self.treeCtrl_recinto.Bind( wx.EVT_TREE_SEL_CHANGED, self.onSelecItemCambio )
   # ------------------------------------ Property Manager ------------------------------------ #
        self.pm_superficie.Bind( pg.EVT_PG_CHANGED, self.onCambioPGM )
        self.pm_superficie.Bind( pg.EVT_PG_CHANGING, self.onCambiandoPGM )
 #  FUNCIONES
    def __del__( self ):
        pass
   # ---------------------------------------- TreeCtrl ---------------------------------------- #
    def cargarSuperficie(self, datos):
        item = self.ROOT
        while (datos['orden'] - self.treeCtrl_recinto.GetItemData(item).orden) > 1 and item.IsOk():
            item = self.treeCtrl_recinto.GetLastChild(item)
        self.treeCtrl_recinto.AppendItem(item, datos['nombre'], data=Superficie(**datos))
        self.treeCtrl_recinto.Expand(item)
        #-----#
        graficar = 0
        new_item = self.treeCtrl_recinto.GetLastChild(item)
        self.treeCtrl_recinto.SelectItem(new_item)
        superficie = self.treeCtrl_recinto.GetItemData(new_item)
        if len(superficie.lineas) == 0:
            if type(superficie.verts_list[0]) != str:
                self.padre.graficar(superficie)
                graficar = 1
        return graficar
    def onSelecItemCambio( self, event):
        self.superficie_activa = event.GetItem()
        superficie = self.treeCtrl_recinto.GetItemData(event.GetItem())
        if self.superficie_activa == self.ROOT:
            self.soloLectura(True)
        else:
            self.soloLectura(False)
        self.escribirValue(superficie)
        try:
            old_superficie = self.treeCtrl_recinto.GetItemData(event.GetOldItem())
        except wx._core.wxAssertionError:
            old_superficie = None
        self.padre.cambiar_color(old_superficie,superficie)
    def restar_superficie(self):
        item = self.treeCtrl_recinto.GetSelection()
        superficie = self.treeCtrl_recinto.GetItemData(item)
        self.padre.eliminar_lineas(superficie)
        self.restarHijas(item)
        self.treeCtrl_recinto.Delete(item)
    def sumar_superficie(self):
        item = self.treeCtrl_recinto.GetSelection()
        itemData = self.treeCtrl_recinto.GetItemData(item) 
        i = self.treeCtrl_recinto.GetChildrenCount(item, recursively=False)
        nombre = 'Superficie %s'%(i+1)
        self.treeCtrl_recinto.AppendItem(item, nombre, data=Superficie(itemData.orden+1 , nombre, itemData.indice, i))
        self.treeCtrl_recinto.Expand(item)
    def reiniciarRecinto(self):
        self.treeCtrl_recinto.DeleteChildren(self.ROOT)
        superficie = self.treeCtrl_recinto.GetItemData(self.ROOT)
        self.padre.eliminar_lineas(superficie,todas=True)
    def crearNuevoRecinto(self,x,y,z):
        '''Reincia el recinto
        x => tuple (x0,x1)
        y => tuple (y0,y1)
        z => tuple (z0,z1)
        '''
        self.treeCtrl_recinto.SelectItem(self.ROOT)
        # Eliminar Data
        self.reiniciarRecinto()
        # Crear Data
        for i in range(6):
            self.sumar_superficie()
        item = self.treeCtrl_recinto.GetLastChild(self.ROOT)
        self.treeCtrl_recinto.SelectItem(item)
        s = 5
        while s >= 0:
            superficie = self.treeCtrl_recinto.GetItemData(item)
            if s == 0:
                for i in range(4):
                    key = 'vertice_' + str(i+1)
                    if i == 0:
                        arg = [x[0],y[0],z[0]]
                    elif i == 1:
                        arg = [x[0],y[1],z[0]]
                    elif i == 2:
                        arg = [x[0],y[1],z[1]]
                    else:
                        arg = [x[0],y[0],z[1]]
                    superficie.setVertices(key,arg)
                    superficie.normal_direccion['direccion'] = True
            elif s == 1:
                for i in range(4):
                    key = 'vertice_' + str(i+1)
                    if i == 0:
                        arg = [x[1],y[0],z[0]]
                    elif i == 1:
                        arg = [x[1],y[1],z[0]]
                    elif i == 2:
                        arg = [x[1],y[1],z[1]]
                    else:
                        arg = [x[1],y[0],z[1]]
                    superficie.setVertices(key,arg)
            elif s == 2:
                for i in range(4):
                    key = 'vertice_' + str(i+1)
                    if i == 0:
                        arg = [x[0],y[0],z[0]]
                    elif i == 1:
                        arg = [x[1],y[0],z[0]]
                    elif i == 2:
                        arg = [x[1],y[0],z[1]]
                    else:
                        arg = [x[0],y[0],z[1]]
                    superficie.setVertices(key,arg)
            elif s == 3:
                for i in range(4):
                    key = 'vertice_' + str(i+1)
                    if i == 0:
                        arg = [x[0],y[1],z[0]]
                    elif i == 1:
                        arg = [x[1],y[1],z[0]]
                    elif i == 2:
                        arg = [x[1],y[1],z[1]]
                    else:
                        arg = [x[0],y[1],z[1]]
                    superficie.setVertices(key,arg)
                    superficie.normal_direccion['direccion'] = True
            elif s == 4:
                for i in range(4):
                    key = 'vertice_' + str(i+1)
                    if i == 0:
                        arg = [x[0],y[0],z[0]]
                    elif i == 1:
                        arg = [x[1],y[0],z[0]]
                    elif i == 2:
                        arg = [x[1],y[1],z[0]]
                    else:
                        arg = [x[0],y[1],z[0]]
                    superficie.setVertices(key,arg)
                    superficie.normal_direccion['direccion'] = True
            else:
                for i in range(4):
                    key = 'vertice_' + str(i+1)
                    if i == 0:
                        arg = [x[0],y[0],z[1]]
                    elif i == 1:
                        arg = [x[1],y[0],z[1]]
                    elif i == 2:
                        arg = [x[1],y[1],z[1]]
                    else:
                        arg = [x[0],y[1],z[1]]
                    superficie.setVertices(key,arg)
            self.padre.graficar(superficie)
            if s > 0:
                item = self.treeCtrl_recinto.GetPrevSibling(item)
                self.treeCtrl_recinto.SelectItem(item)
            s-=1
        self.padre.ajustar_grilla(x[1],y[1],z[1])
        self.treeCtrl_recinto.SelectItem(self.ROOT)
    def onEditarLabel(self, event):
        self.treeCtrl_recinto.GetItemData(event.GetItem()).nombre = event.GetLabel()
   # ------------------------------------ Property Manager ------------------------------------ #
    def soloLectura(self,status):
        self.pm_superficie.SetPropertyReadOnly('vertices',status)
        self.pm_superficie.SetPropertyReadOnly('normal',status)
        self.pm_superficie.SetPropertyReadOnly('area_op',status)
        self.pm_superficie.SetPropertyReadOnly('materiales',status)
    def escribirValue(self,superficie):
        self.pm_superficie.SetPropertyValues(superficie.vertices)
        self.pm_superficie.SetPropertyValues(superficie.normal_direccion)
        self.pm_superficie.SetPropertyValue('mostrar_linea', superficie.grafica)
        self.pm_superficie.SetPropertyValue('area_sup', superficie.area)
        self.pm_superficie.SetPropertyValue('alpha_area', superficie.alpha_relleno)
        self.pm_superficie.SetPropertyValues(superficie.material_info)
    def onCambioPGM(self,event):
        event.Skip()
    def onCambiandoPGM(self, event):
        superficie = self.treeCtrl_recinto.GetItemData(self.superficie_activa)
        PGP = event.GetPropertyName()
        if PGP[:-1] == 'vertice_':
            cadena = event.GetPropertyValue()
            respuesta = self.comprobar_vertice(cadena)
            if respuesta != None:
                superficie.setVertices(PGP,respuesta)
                if len(superficie.lineas) == 0:
                    self.padre.graficar(superficie)
                else:
                    indice = int(PGP[-1])-1
                    self.padre.cambiar_linea(superficie,indice)
            else:
                event.SetValidationFailureMessage('Debe ingresar TRES valores separados por ",". Pulse ESC para cancelar la edición')
                event.Veto()
        elif PGP == 'direccion':
            status = event.GetPropertyValue()
            superficie.normal_direccion[PGP] = status
            self.padre.direccion_normal(superficie)
        elif PGP == 'area_sup':
            valor = event.GetPropertyValue()
            superficie = self.treeCtrl_recinto.GetItemData(self.superficie_activa)
            try: 
                valor = float(parse_expr(valor))
            except (ValueError, TypeError, SyntaxError):
                valor = superficie.area
            superficie.area = valor
            self.pm_superficie.SetPropertyValue('area_sup', superficie.area)
        elif PGP.startswith('color'):
            color = event.GetPropertyValue()
            superficie = self.treeCtrl_recinto.GetItemData(self.superficie_activa)
            if PGP.endswith('lineas'):
                superficie.color = color.Get()
            else:
                superficie.color_area = color.Get()
                self.padre.panel_grafica.cambiar_relleno(superficie)
        elif PGP == 'mostrar_linea':
            valor = event.GetPropertyValue()
            superficie = self.treeCtrl_recinto.GetItemData(self.superficie_activa)
            superficie.grafica = valor
            self.padre.panel_grafica.visibilidad_linea(superficie)
        elif PGP == 'alpha_area':
            valor = event.GetPropertyValue()
            superficie = self.treeCtrl_recinto.GetItemData(self.superficie_activa)
            try:
                valor = float(valor)
                if valor >= 0 and valor <= 1:
                    superficie.alpha_relleno = valor
                    self.padre.panel_grafica.cambiar_relleno(superficie)
                else:
                    raise ValueError
            except ValueError:
                self.pm_superficie.SetPropertyValue('alpha_area', superficie.alpha_relleno)
        elif PGP[:2] == 'm_':
            cadena = event.GetPropertyValue()
            if PGP != 'm_nombre':
                cadena = self.comprobar_rango(cadena,0,1)
                if cadena == None: 
                    event.SetValidationFailureMessage('El valor debe ser un número que se encuentre en el rango [0,1]')
                    event.Veto()
                    return
            superficie.material_info[PGP] = cadena
            self.escribirValue(superficie)
    def asignarMaterial(self,valores):
        '''valores => list'''
        item = self.treeCtrl_recinto.GetSelection()
        if item != self.ROOT:
            superficie = self.treeCtrl_recinto.GetItemData(item)
            valores.pop(2),valores.pop(0)
            keys = superficie.material_info.keys()
            for key,valor in zip(keys,valores):
                superficie.material_info[key] = valor
            self.escribirValue(superficie)
   # -------------------------------------- Herramientas -------------------------------------- #
    def comprobar_vertice(self, cadena): 
        prueba = cadena.split(',')
        if len(prueba) != 3:
            return None
        final = []
        try:
            for i in range(len(prueba)):
                valor = float(parse_expr(prueba[i]))
                final.append(valor)
            return final
        except (ValueError, TypeError, SyntaxError):
            return None
    def comprobar_rango(self,cadena,a,b):
        '''Comprueba que una cadena sea un valor que se encuentre entre dos valores [a,b]. 
        Si es así devuelve el valor de la cadena en float. De lo contrario retorna None si no se puede convertir a float la cadena.

        - cadena => str
        - a => int/float
        - b => int/float'''
        try:
            numero = float(cadena)
            if a <= numero <= b:
                return numero
            else:
                raise ValueError
        except ValueError:
            return None
    def continuar_focus(self,PGP):
        pass
    def obtener_superficies(self, madre):
        datos = []
        item, _ = self.treeCtrl_recinto.GetFirstChild(madre)
        while item.IsOk():
            datos.append(self.treeCtrl_recinto.GetItemData(item))
            if self.treeCtrl_recinto.GetChildrenCount(item) > 0:
                dato = self.obtener_superficies(item)
                datos += dato
            item = self.treeCtrl_recinto.GetNextSibling(item)
        return datos
    def recolectarVertices(self):
        vertices = []
        item = self.treeCtrl_recinto.GetFirstVisibleItem()
        while item.IsOk():
            if item == self.ROOT:
                item = self.treeCtrl_recinto.GetNextVisible(item)
            else:
                verts = self.treeCtrl_recinto.GetItemData(item).verts_list
                if type(verts[0]) != str:
                    vertices.append(verts)
                item = self.treeCtrl_recinto.GetNextVisible(item)              
        return vertices
    def restarHijas(self, item):
        next_item = self.treeCtrl_recinto.GetLastChild(item)
        while next_item.IsOk():
            if self.treeCtrl_recinto.GetChildrenCount(next_item) > 0:
                self.restarHijas(next_item)
            else:
                superficie = self.treeCtrl_recinto.GetItemData(next_item)
                self.padre.eliminar_lineas(superficie)
                self.treeCtrl_recinto.Delete(next_item)
                next_item = self.treeCtrl_recinto.GetLastChild(item)   
    def informarAreas(self, madre):
        INFO = DataParaRT60()
        item, _ = self.treeCtrl_recinto.GetFirstChild(madre)
        while item.IsOk():
            data = self.treeCtrl_recinto.GetItemData(item)
            if data.area != None:
                if data.area > 0:
                    INFO.Pared.append(data.nombre)
                    INFO.Material.append(data.material_info['m_nombre'])
                    INFO.Area.append(data.area)
                    INFO.Hz125.append(data.material_info['m_125'])
                    INFO.Hz250.append(data.material_info['m_250'])
                    INFO.Hz500.append(data.material_info['m_500'])
                    INFO.Hz1000.append(data.material_info['m_1000'])
                    INFO.Hz2000.append(data.material_info['m_2000'])
                    INFO.Hz4000.append(data.material_info['m_4000'])       
            if self.treeCtrl_recinto.GetChildrenCount(item) > 0:
                info = self.informarAreas(item)
                INFO.agregarHijas(**info.__dict__)
            item = self.treeCtrl_recinto.GetNextSibling(item)
        return INFO
    def getHexCode(self, rgba):
        cs = [hex(rgba[i]).split('x')[1] for i in range(3)]
        hexcode = '#'
        for c in cs:
            hexcode += c
        return hexcode
   # ------------------------------------ Acondicionadoras ------------------------------------ #

class Panel_FuenteReceptor ( wx.Panel ):
    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 292,631 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )
        self.name = name
        sizer_main = wx.BoxSizer( wx.VERTICAL )

        self.pgMan = pg.PropertyGridManager(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PGMAN_DEFAULT_STYLE)
        self.pgMan.SetExtraStyle( wx.propgrid.PG_EX_MODE_BUTTONS )

        self.pg_primera = self.pgMan.AddPage( u"Primera", wx.NullBitmap )

        self.pg_segunda = self.pgMan.AddPage( u"Segunda", wx.NullBitmap )
        sizer_main.Add( self.pgMan, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( sizer_main )
        self.Layout()
    def __del__( self ):
        pass

class Panel_OtrosDatos ( wx.Panel ):
    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 292,631 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )
        self.name = name
    def __del__( self ):
        pass

class PanelGraficaRecinto ( wx.Panel ):
    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        sizer_main = wx.BoxSizer( wx.VERTICAL )

        self.toolbar = TB_Grafica(self)
        sizer_main.Add(self.toolbar, 0, wx.EXPAND)

        self.figura = Figure()
        self.canvas = FigureCanvas(self,0,self.figura)
        self.ax = Axes3D(self.figura)
        self.ax.set_xlabel('X'),self.ax.set_ylabel('Y'),self.ax.set_zlabel('Z')
        self.ax.w_xaxis.pane.set_color('w')
        self.ax.w_yaxis.pane.set_color('w')
        self.ax.w_zaxis.pane.set_color('w')
        self.ax.set_autoscale_on(False)

        sizer_main.Add(self.canvas,-1,wx.ALL|wx.EXPAND,5)

        self.SetSizer( sizer_main )
        self.Layout()
 #  Inicializacion de Variables
        self.padre = parent.GetParent()
        self.LINEAS = []
 #  Inicializacion de Funciones
 #  FUNCIONES
    def __del__( self ):
        pass
    def ocultar_grilla(self,mostrar):
        '''mostrar = bool'''
        if mostrar:
            self.ax.set_axis_on()
            self.canvas.draw()
        else:
            self.ax.set_axis_off()
            self.canvas.draw()
  # ------------------------------------ GRAFICA RECINTO -------------------------------------#     
    def ajustar_grilla(self,x,y,z):
        mayor = max([x,y,z])
        res_x = x - mayor 
        res_y = y - mayor
        res_z = z - mayor
        self.ax.set_xlim3d(res_x/2, x-(res_x/2))
        self.ax.set_ylim3d(res_y/2, y-(res_y/2))
        self.ax.set_zlim3d(res_z/2, z-(res_z/2))
        self.canvas.draw()
    def ajustar_limites(self, vertices):
        xs, ys, zs = obtenerLimites(vertices)
        self.ax.set_xlim3d(xs[0], xs[1])
        self.ax.set_ylim3d(ys[0], ys[1])
        self.ax.set_zlim3d(zs[0], zs[1])
        self.canvas.draw()
    def crear_lineas(self,superficie):
        vertices = superficie.getVertices()
        color = superficie.getColorGrafica()
        if superficie.comprobarCondicion(0): # si se ingresaron los 4 vertices
            if superficie.area == None:
                superficie.getArea() # se calcula el area de la superficie
            self.padre.paneles_datos[0].pm_superficie.SetPropertyValue('area_sup', superficie.area) 
            # LINEAS SUPERFICIE
            for i in range(-1,len(vertices)-1):
                linea = self.ax.plot([vertices[i][0],vertices[i+1][0]],
                                     [vertices[i][1],vertices[i+1][1]],
                                     [vertices[i][2],vertices[i+1][2]],
                                     linewidth=ancho_linea,color=color,zorder=1, visible=superficie.grafica)
                superficie.lineas.append(linea)
                #superficie.padre.lineasChildren.append(linea)     # buscar objeto padre
            self.crear_relleno(superficie)
            # LINEAS NORMAL
            superficie.setNormal() # se obtiene el vector normal de acuerdo a los 4 vertices
            if superficie.normal != None:
                for i in range(4):
                    punto_incial = superficie.verts_list[i]
                    punto_normal = superficie.normal # sumarVectores(superficie.normal,punto_incial)
                    # linea = self.ax.plot([punto_incial[0],punto_normal[0]],
                    #                      [punto_incial[1],punto_normal[1]],
                    #                      [punto_incial[2],punto_normal[2]],
                    #                      linewidth=ancho_linea,color='red')
                    linea = self.ax.quiver3D(punto_incial[0], punto_incial[1], punto_incial[2],
                                             punto_normal[0], punto_normal[1], punto_normal[2],
                                             linewidth=ancho_linea, arrow_length_ratio=0.4, color='red')
                    superficie.normal_lineas.append(linea)
                    #superficie.padre.lineasChildren.append(linea) # buscar objeto padre
            self.canvas.draw()
        else:
            return None
    def crear_relleno(self, superficie):
        vertices = superficie.getVertices(orden_inverso=True)
        relleno = Poly3DCollection(vertices)
        relleno.set_facecolor(superficie.getColorGrafica(relleno=True))
        relleno.set_alpha(superficie.alpha_relleno)
        superficie.pared_relleno = relleno
        self.ax.add_collection(relleno)
    def cambiar_relleno(self, superfice):
        self.ax.collections.remove(superfice.pared_relleno)
        superfice.pared_relleno.set_facecolor(superfice.getColorGrafica(relleno=True))
        superfice.pared_relleno.set_verts(superfice.getVertices(orden_inverso=True))
        superfice.pared_relleno.set_alpha(superfice.alpha_relleno)
        self.ax.add_collection(superfice.pared_relleno)
        self.canvas.draw()
    def cambiar_color(self,old,new):
        if old != None:
            #old.color = old.color_lineas
            if len(old.lineas) == 4:
                for i in range(4):
                    plt.setp(old.lineas[i],color=old.getColorGrafica(),zorder=0)
                    plt.setp(old.normal_lineas[i],visible=False)
        #new.color = 'blue'
        if len(new.lineas) == 4:
            for i in range(4):
                plt.setp(new.lineas[i],color='blue',zorder=10)
                plt.setp(new.normal_lineas[i],visible=True)
        self.canvas.draw()
    def cambiar_linea(self,superficie,indice):
        superficie.verts_list = superficie.getVertices()
        superficie.getArea()
        self.padre.paneles_datos[0].pm_superficie.SetPropertyValue('area_sup', superficie.area)
        if indice == 0:
            ver_a = ((superficie.vertices['vertice_4']).replace(' ','')).split(',')
            ver_b = ((superficie.vertices['vertice_1']).replace(' ','')).split(',')
            ver_c = ((superficie.vertices['vertice_2']).replace(' ','')).split(',')
            linea_a = superficie.lineas[0]
            linea_b = superficie.lineas[1]
        elif indice == 1:
            ver_a = ((superficie.vertices['vertice_1']).replace(' ','')).split(',')
            ver_b = ((superficie.vertices['vertice_2']).replace(' ','')).split(',')
            ver_c = ((superficie.vertices['vertice_3']).replace(' ','')).split(',')
            linea_a = superficie.lineas[1]
            linea_b = superficie.lineas[2]
        elif indice == 2:
            ver_a = ((superficie.vertices['vertice_2']).replace(' ','')).split(',')
            ver_b = ((superficie.vertices['vertice_3']).replace(' ','')).split(',')
            ver_c = ((superficie.vertices['vertice_4']).replace(' ','')).split(',')
            linea_a = superficie.lineas[2]
            linea_b = superficie.lineas[3]
        else:
            ver_a = ((superficie.vertices['vertice_3']).replace(' ','')).split(',')
            ver_b = ((superficie.vertices['vertice_4']).replace(' ','')).split(',')
            ver_c = ((superficie.vertices['vertice_1']).replace(' ','')).split(',')
            linea_a = superficie.lineas[3]
            linea_b = superficie.lineas[0]
        ver_a = [float(ver_a[0]), float(ver_a[1]), float(ver_a[2])]
        ver_b = [float(ver_b[0]), float(ver_b[1]), float(ver_b[2])]
        ver_c = [float(ver_c[0]), float(ver_c[1]), float(ver_c[2])]
        linea_a[0].set_data_3d([ver_a[0],ver_b[0]],
                               [ver_a[1],ver_b[1]],
                               [ver_a[2],ver_b[2]])
        linea_b[0].set_data_3d([ver_b[0],ver_c[0]],
                               [ver_b[1],ver_c[1]],
                               [ver_b[2],ver_c[2]])
        self.canvas.draw()
        self.cambiar_normales(superficie)
        self.cambiar_relleno(superficie)
    def cambiar_normales(self,superficie):
        # Se remueven las flechas del ax
        [self.ax.collections.remove(superficie.normal_lineas[i]) for i in range(len(superficie.normal_lineas))]
        # Se calcula el vector normal
        superficie.setNormal()
        # Se grafica y guardan en la superficie
        if superficie.normal != None:
            superficie.normal_lineas.clear()
            for i in range(4):
                punto_incial = superficie.verts_list[i]
                punto_normal = superficie.normal
                linea = self.ax.quiver3D(punto_incial[0], punto_incial[1], punto_incial[2],
                                         punto_normal[0], punto_normal[1], punto_normal[2],
                                         linewidth=ancho_linea, arrow_length_ratio=0.4, color='red')
                superficie.normal_lineas.append(linea)
        self.canvas.draw()
    def eliminar_lineas(self,superficie,todas=False):
        if todas:
            while len(self.ax.lines) > 0:
                self.ax.lines[0].remove()
            self.ax.collections.clear()
            #superficie.lineasChildren = []
        else:
            # for linea in superficie.lineasChildren:
            #     i = self.ax.lines.index(linea[0])
            #     self.ax.lines[i].remove()
            lineas = superficie.lineas
            normales = superficie.normal_lineas
            for linea,normal in zip(lineas,normales):
                i = self.ax.lines.index(linea[0])
                self.ax.lines[i].remove()
                self.ax.collections.remove(normal)
            if superficie.pared_relleno in self.ax.collections:
                self.ax.collections.remove(superficie.pared_relleno)
                # j = self.ax.collections.index(normal[0])
                # self.ax.lines[j].remove()
                # superficie.padre.lineasChildren.remove(linea)
                # superficie.padre.lineasChildren.remove(normal)
        self.canvas.draw()
    def visibilidad_linea(self, superficie):
        for linea in superficie.lineas:
            plt.setp(linea, visible=superficie.grafica)
        self.canvas.draw()

class PanelMateriales ( wx.Panel ):
    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 747,160 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        sizer_main = wx.BoxSizer( wx.VERTICAL )

        self.toolbar = TB_Materiales(self)
        sizer_main.Add(self.toolbar, 0, wx.EXPAND)

        self.grilla_materiales = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.grilla_materiales.CreateGrid( 0, 9 )
        self.grilla_materiales.EnableEditing( True )
        self.grilla_materiales.EnableGridLines( True )
        self.grilla_materiales.EnableDragGridSize( True )
        self.grilla_materiales.SetMargins( 0, 0 )

        # Columns
        self.grilla_materiales.EnableDragColMove( False )
        self.grilla_materiales.EnableDragColSize( True )
        self.grilla_materiales.SetColLabelSize( 22 )
        self.grilla_materiales.SetColLabelValue( 0, u"Materiales" )
        self.grilla_materiales.SetColSize(0,150)
        self.grilla_materiales.SetColLabelValue( 1, u"Descripcion" )
        self.grilla_materiales.SetColSize(1,420)
        self.grilla_materiales.SetColLabelValue( 2, u"125" )
        self.grilla_materiales.SetColLabelValue( 3, u"250" )
        self.grilla_materiales.SetColLabelValue( 4, u"500" )
        self.grilla_materiales.SetColLabelValue( 5, u"1000" )
        self.grilla_materiales.SetColLabelValue( 6, u"2000" )
        self.grilla_materiales.SetColLabelValue( 7, u"4000" )
        self.grilla_materiales.SetColLabelValue( 8, u"NRC" )
        for i in range(2,9):
            self.grilla_materiales.SetColSize(i,60)
        self.grilla_materiales.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.grilla_materiales.EnableDragRowSize( True )
        self.grilla_materiales.SetRowLabelSize( 40 )
        self.grilla_materiales.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance
        self.grilla_materiales.SetCellHighlightROPenWidth(0)
        # Cell Defaults
        self.grilla_materiales.SetDefaultCellAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        sizer_main.Add( self.grilla_materiales, 1, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( sizer_main )
        self.Layout()
 #  Inicializacion de Variables 
        self.padre = parent
 #  Connect Events
        self.grilla_materiales.Bind( wx.grid.EVT_GRID_CELL_CHANGED, self.onCambioCelda )
        self.grilla_materiales.Bind( wx.grid.EVT_GRID_COL_SIZE, self.onColSize )
 #  FUNCIONES  
    def __del__( self ):
        pass
   # ----------------------------------------- Grilla -----------------------------------------
    def onCambioCelda( self, event):
        col = event.GetCol()
        self.grilla_materiales.ForceRefresh()
        if col == 0:
            nombres_materiales = self.informarNombreMateriales()
            self.toolbar.actualizarComboBox(nombres_materiales)
    def onColSize(self,event):
        event.Skip()
    def informarNombreMateriales(self):
        nombres_materiales = []
        rows = self.grilla_materiales.GetNumberRows()
        for row in range(rows):
            nombre = self.grilla_materiales.GetCellValue(row,0)
            if nombre != '':
                nombres_materiales.append(nombre)
        return(nombres_materiales)
   # --------------------------------- Barra de Herramientas ---------------------------------- 
    def asignarMaterial(self):
        pass
    def eliminarMaterial(self):
        pass
    def sumarMaterial(self):
        self.grilla_materiales.AppendRows(1)
        nombres_materiales = self.informarNombreMateriales
        return nombres_materiales
    def pegarMateriales(self):
        pass
    def copiarMaterials(self):
        pass
    def buscarMaterial(self):
        pass    
    def cargar_materiales(self,materiales):
        '''materiales debe ser un objeto que pueda recorrese por filas (.values) y columnas (.columns)
        materiales => objeto (class)'''
        rows = self.grilla_materiales.GetNumberRows()
        if rows > 0:
            self.grilla_materiales.DeleteRows(0,rows)
        cols = self.grilla_materiales.GetNumberCols()
        valores = materiales.values
        for row in range(len(valores)):
            self.grilla_materiales.AppendRows(1)
            self.grilla_materiales.SetCellAlignment(row,0,wx.ALIGN_LEFT,wx.ALIGN_CENTER)
            self.grilla_materiales.SetCellAlignment(row,1,wx.ALIGN_LEFT,wx.ALIGN_CENTER)
            for col in range(cols):
                self.grilla_materiales.SetCellValue(row,col,str(valores[row][col]))
        self.toolbar.actualizarComboBox(materiales[materiales.columns[0]])

# Barras de herramientas
class TB_Grafica ( wx.ToolBar ):
    def __init__( self, parent ):
        wx.ToolBar.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 686,60 ), style = wx.TB_HORIZONTAL )
        
        self.m_bpButton6 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.m_bpButton6.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_HOME,  ) )
        self.AddControl( self.m_bpButton6 )
        self.m_bpButton7 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.m_bpButton7.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HARDDISK,  ) )
        self.AddControl( self.m_bpButton7 )

        self.m_staticline17 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline17 )

        self.checkBox_grilla = wx.CheckBox( self, wx.ID_ANY, u"Grilla", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_grilla.SetValue(True)
        self.AddControl( self.checkBox_grilla )

        self.m_staticline18 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline18 )
        
        self.static_text_X = wx.StaticText( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.static_text_X.Wrap( -1 )

        self.AddControl( self.static_text_X )
        self.spin_ejeX = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_HORIZONTAL )
        self.spin_ejeX.SetRange(-10,10)
        self.spin_ejeX.SetValue(0)
        self.AddControl( self.spin_ejeX )
        self.AddSeparator()

        self.static_text_Y = wx.StaticText( self, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.static_text_Y.Wrap( -1 )

        self.AddControl( self.static_text_Y )
        self.spin_ejeY = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_HORIZONTAL )
        self.spin_ejeY.SetRange(-10,10)
        self.spin_ejeY.SetValue(0)
        self.AddControl( self.spin_ejeY )
        self.AddSeparator()

        self.static_text_Z = wx.StaticText( self, wx.ID_ANY, u"Z", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.static_text_Z.Wrap( -1 )

        self.AddControl( self.static_text_Z )
        self.spin_ejeZ = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_HORIZONTAL )
        self.spin_ejeZ.SetRange(-10,10)
        self.spin_ejeZ.SetValue(0)
        self.AddControl( self.spin_ejeZ )
        self.AddSeparator()

        self.Realize()
 #  Inicializacion de Variables
        self.padre = parent
 #  Connect Events
        self.checkBox_grilla.Bind( wx.EVT_CHECKBOX, self.onCheckGrilla )
        self.spin_ejeX.Bind( wx.EVT_SPIN_DOWN, self.onDownX )
        self.spin_ejeX.Bind( wx.EVT_SPIN_UP, self.onUpX )
        self.spin_ejeY.Bind( wx.EVT_SPIN_DOWN, self.onDownY )
        self.spin_ejeY.Bind( wx.EVT_SPIN_UP, self.onUpY )
        self.spin_ejeZ.Bind( wx.EVT_SPIN_DOWN, self.onDownZ )
        self.spin_ejeZ.Bind( wx.EVT_SPIN_UP, self.onUpZ )

    def __del__( self ):
        pass
 #  FUNCIONES
    def onCheckGrilla( self, event ):
        mostrar = self.checkBox_grilla.GetValue()
        self.padre.ocultar_grilla(mostrar)
    def onUpX(self,event):
        left,rigth = self.padre.ax.get_xlim3d()
        self.padre.ax.set_xlim3d(left+1,rigth+1)
        self.padre.canvas.draw()
        self.spin_ejeX.SetValue(0)
    def onDownX(self,event):
        left,rigth = self.padre.ax.get_xlim3d()
        self.padre.ax.set_xlim3d(left-1,rigth-1)
        self.padre.canvas.draw()
        self.spin_ejeX.SetValue(0)
    def onUpY(self,event):
        left,rigth = self.padre.ax.get_ylim3d()
        self.padre.ax.set_ylim3d(left+1,rigth+1)
        self.padre.canvas.draw()
        self.spin_ejeY.SetValue(0)
    def onDownY(self,event):
        left,rigth = self.padre.ax.get_ylim3d()
        self.padre.ax.set_ylim3d(left-1,rigth-1)
        self.padre.canvas.draw()
        self.spin_ejeY.SetValue(0)
    def onUpZ(self,event):
        left,rigth = self.padre.ax.get_zlim3d()
        self.padre.ax.set_zlim3d(left+1,rigth+1)
        self.padre.canvas.draw()
        self.spin_ejeZ.SetValue(0)
    def onDownZ(self,event):
        left,rigth = self.padre.ax.get_zlim3d()
        self.padre.ax.set_zlim3d(left-1,rigth-1)
        self.padre.canvas.draw()
        self.spin_ejeZ.SetValue(0)

class TB_Materiales ( wx.ToolBar ):
    def __init__( self, parent ):
        wx.ToolBar.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 686,65 ), style = wx.TB_HORIZONTAL )

        self.boton_asignar_material = wx.Button( self, wx.ID_ANY, u"Asginar", wx.DefaultPosition, (64,24), wx.NO_BORDER )

        self.boton_asignar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, ) )
        self.AddControl( self.boton_asignar_material )
        self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline6 )
        self.boton_eliminar_material = wx.Button( self, wx.ID_ANY, u"Eliminar", wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_eliminar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_MINUS,  ) )
        self.AddControl( self.boton_eliminar_material )
        self.boton_agregar_material = wx.Button( self, wx.ID_ANY, u"Agregar", wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_agregar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PLUS,  ) )
        self.AddControl( self.boton_agregar_material )
        self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline8 )
        self.boton_copiar_material = wx.Button( self, wx.ID_ANY, u"Copiar", wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_copiar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_COPY,  ) )
        self.AddControl( self.boton_copiar_material )
        self.boton_pegar_material = wx.Button( self, wx.ID_ANY, u"Pegar", wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_pegar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PASTE,  ) )
        self.AddControl( self.boton_pegar_material )
        self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline10 )
        self.boton_abrir_archivo_material = wx.Button( self, wx.ID_ANY, u"Abrir", wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_abrir_archivo_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN,  ) )
        self.AddControl( self.boton_abrir_archivo_material )
        self.boton_guardar_material = wx.Button( self, wx.ID_ANY, u"Guardar", wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_guardar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE,  ) )
        self.AddControl( self.boton_guardar_material )
        self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline7 )

        self.bitmap_buscar = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FIND,  ), wx.DefaultPosition, size_boton, 0 )
        self.AddControl( self.bitmap_buscar )
        self.combox_materiales = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (512,26), [], wx.CB_SORT|wx.TE_PROCESS_ENTER )
        self.AddControl( self.combox_materiales )

        self.Realize()
 #  Inicializacion de Variables
        self.padre = parent
        self.abuelo = self.padre.GetParent()
 #  Inicializacion de Funciones
 #  Connect Events
        self.boton_asignar_material.Bind( wx.EVT_BUTTON, self.onAsignarMaterial )
        self.boton_eliminar_material.Bind( wx.EVT_BUTTON, self.onEliminarMaterial )
        self.boton_agregar_material.Bind( wx.EVT_BUTTON, self.onAgregarMaterial )
        self.boton_copiar_material.Bind( wx.EVT_BUTTON, self.onCopiarMaterial )
        self.boton_pegar_material.Bind( wx.EVT_BUTTON, self.onPegarMaterial )
        self.boton_abrir_archivo_material.Bind( wx.EVT_BUTTON, self.onAbrirMaterial )
        self.boton_guardar_material.Bind( wx.EVT_BUTTON, self.onGuardarMaterial )
        self.combox_materiales.Bind( wx.EVT_COMBOBOX, self.onSelectItem )
 #  FUNCIONES
    def __del__( self ):
        pass
    def onAsignarMaterial( self, event ):
        rows = self.padre.grilla_materiales.GetSelectedRows()
        if len(rows) == 1:
            row = rows[0]
            cols = self.padre.grilla_materiales.GetNumberCols()
            valores = [row]
            for col in range(cols):
                valor = self.padre.grilla_materiales.GetCellValue(row,col)
                try:
                    valor = float(valor)
                except ValueError:
                    pass
                valores.append(valor)
            self.abuelo.asignar_material(valores)
    def onEliminarMaterial( self, event ):
        event.Skip()
    def onAgregarMaterial( self, event ):
        nombres_materiales = self.padre.sumarMaterial()
    def onCopiarMaterial( self, event ):
        event.Skip()
    def onPegarMaterial( self, event ):
        event.Skip()
    def onAbrirMaterial( self, event ):
        with wx.FileDialog(self,"Abrir Archivo", wildcard="XLSX files (*.xlsx)|*.xlsx",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                file = pd.ExcelFile(pathname)
                nom_libros = file.sheet_names
                libro = pd.read_excel(open(file,'rb'),sheet_name=nom_libros[0])
                self.padre.cargar_materiales(libro)
            except FileNotFoundError:
                dial = wx.MessageDialog(none,'El archivo no existe','Error',wx.OK)
                resp = dial.ShowModal()
                if resp == wx.OK:
                    dial.Destroy()
    def onGuardarMaterial( self, event ):
        event.Skip()
    def onSelectItem(self,event):
        material = event.GetSelection()
        item = self.materiales[material][1]
        self.padre.grilla_materiales.SelectRow(item)
        self.padre.grilla_materiales.GoToCell(item,0)
    def actualizarComboBox(self,nombres):
        '''nombres => list '''
        self.combox_materiales.Clear()
        self.acondicionarLista(nombres)
        for material in self.materiales:
            if material[0] != '':
                self.combox_materiales.Append(material[0])
    def acondicionarLista(self,nombres):
        materiales = []
        for i in range(len(nombres)):
            material = [nombres[i],i]
            materiales.append(material)
        self.materiales = ordenarLista(materiales,0)

class TB_Datos ( wx.ToolBar ):
    def __init__( self, parent ):
        wx.ToolBar.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 296,44 ), style = wx.TB_HORIZONTAL )

        self.boton_restar = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_restar.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_MINUS,  ) )
        self.AddControl( self.boton_restar )
        self.boton_sumar = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, size_boton, wx.NO_BORDER )

        self.boton_sumar.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PLUS,  ) )
        self.AddControl( self.boton_sumar )
        self.m_staticline17 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.AddControl( self.m_staticline17 )
        self.boton_reiniciar = wx.Button( self, wx.ID_ANY, u"Reiniciar Recinto", wx.DefaultPosition, wx.Size(186,24),0 )
        self.boton_reiniciar.SetBitmap( wx.NullBitmap )
        self.AddControl( self.boton_reiniciar )

        self.Realize()
 # Connect Events
        self.boton_restar.Bind( wx.EVT_BUTTON, self.onClickRestar )
        self.boton_sumar.Bind( wx.EVT_BUTTON, self.onClickSumar )
        self.boton_reiniciar.Bind( wx.EVT_BUTTON, self.onClickReiniciar )
 # Incializacion de Variables
        self.padre = parent
    def __del__( self ):
        pass
 # Funciones
    def onClickRestar( self, event ):
        self.padre.restar_superficie()
    def onClickSumar( self, event ):
        self.padre.sumar_superficie()
    def onClickReiniciar( self, event ):
        dial = wx.MessageDialog(None,'Esta acción reiniciará el recinto\n¿Desea continuar?','',wx.YES_NO)
        resp = dial.ShowModal()
        if resp == wx.ID_YES:
            dial.Destroy()
            dial = VenRecintoNuevo(None)
            resp = dial.ShowModal()
            if resp == wx.OK:
                largo,ancho,alto = dial.largo,dial.ancho,dial.alto
                dial.Destroy()
                self.padre.crearNuevoRecinto((0,largo),(0,ancho),(0,alto))
            else:
                dial.Destroy()
        else:
            dial.Destroy()