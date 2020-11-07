# -*- coding: utf-8 -*-

import wx
import wx.xrc
import wx.dataview
from Paneles.paneles import *
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure


class MainFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1336,830), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour(wx.Colour(236,236,236))
    #   SIZER MAIN
        sizer_main = wx.BoxSizer( wx.HORIZONTAL )
     #  SIZER DATOS
        sizer_datos = wx.BoxSizer( wx.VERTICAL )

        self.nb_datos = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_NOPAGETHEME )

        sizer_datos.Add( self.nb_datos, 1, wx.EXPAND |wx.ALL, 5 )
        self.paneles_datos = []
        self.paneles_datos.append(Panel_Recinto(self.nb_datos,name='Recinto'))
        self.paneles_datos.append(Panel_FuenteReceptor(self.nb_datos,name='Fuente/Receptor'))
        self.paneles_datos.append(Panel_OtrosDatos(self.nb_datos,name='Otros Datos'))
        for panel in self.paneles_datos:
            self.nb_datos.AddPage(panel,panel.name)

        sizer_main.Add( sizer_datos, 1, wx.EXPAND, 5 )  
     #  SIZER GRAFICA
        sizer_grafica = wx.BoxSizer( wx.VERTICAL )

        sizer_grafica_UP = wx.BoxSizer( wx.VERTICAL )
        self.figura = Figure()
        self.canvas = FigureCanvas(self,0,self.figura)
        self.ax = Axes3D(self.figura)
        self.ax.set_axis_off()

        sizer_grafica_UP.Add(self.canvas,-1,wx.ALL|wx.EXPAND,5)

        sizer_grafica.Add( sizer_grafica_UP, 3, wx.EXPAND, 5 )
        
        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        sizer_grafica.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        sizer_grafica_DOWN = wx.BoxSizer( wx.VERTICAL )

        sizer_g_D_botones = wx.BoxSizer( wx.HORIZONTAL )

        self.boton_asignar_material = wx.Button( self, wx.ID_ANY, u"Asginar", wx.DefaultPosition, wx.DefaultSize, 0)
        self.boton_asignar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK,  ) )
        sizer_g_D_botones.Add( self.boton_asignar_material, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        sizer_g_D_botones.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )

        self.boton_eliminar_material = wx.Button( self, wx.ID_ANY, u"Eliminar Material", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_eliminar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_MINUS,  ) )
        sizer_g_D_botones.Add( self.boton_eliminar_material, 0, wx.ALL, 5 )

        self.boton_agregar_material = wx.Button( self, wx.ID_ANY, u"Agregar Material", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_agregar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PLUS,  ) )
        sizer_g_D_botones.Add( self.boton_agregar_material, 0, wx.ALL, 5 )

        self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        sizer_g_D_botones.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

        self.boton_copiar_material = wx.Button( self, wx.ID_ANY, u"Copiar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_copiar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_COPY,  ) )
        sizer_g_D_botones.Add( self.boton_copiar_material, 0, wx.ALL, 5 )

        self.boton_pegar_material = wx.Button( self, wx.ID_ANY, u"Pegar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_pegar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PASTE,  ) )
        sizer_g_D_botones.Add( self.boton_pegar_material, 0, wx.ALL, 5 )

        self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        sizer_g_D_botones.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )

        self.boton_abrir_archivo_material = wx.Button( self, wx.ID_ANY, u"Abir", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_abrir_archivo_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN,  ) )
        sizer_g_D_botones.Add( self.boton_abrir_archivo_material, 0, wx.ALL, 5 )

        self.boton_guardar_material = wx.Button( self, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_guardar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE,  ) )
        sizer_g_D_botones.Add( self.boton_guardar_material, 0, wx.ALL, 5 )

        self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        sizer_g_D_botones.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )

        self.boton_buscar_material = wx.Button( self, wx.ID_ANY, u"Buscar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.boton_buscar_material.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FIND,  ) )
        sizer_g_D_botones.Add( self.boton_buscar_material, 0, wx.ALL, 5 )

        sizer_grafica_DOWN.Add( sizer_g_D_botones, 0, wx.EXPAND, 5 )

        sizer_g_D_grilla = wx.BoxSizer( wx.VERTICAL )

        self.grilla_materiales = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.grilla_materiales.CreateGrid( 0, 9 )
        self.grilla_materiales.EnableEditing( True )
        self.grilla_materiales.EnableGridLines( True )
        self.grilla_materiales.EnableDragGridSize( False )
        self.grilla_materiales.SetMargins( 0, 0 )

        # Columns
        self.grilla_materiales.EnableDragColMove( False )
        self.grilla_materiales.EnableDragColSize( True )
        self.grilla_materiales.SetColLabelSize( 25 )
        self.grilla_materiales.SetColLabelValue( 0, u"Material" )
        self.grilla_materiales.SetColSize(0,310)
        self.grilla_materiales.SetColLabelValue( 1, u"125" )
        self.grilla_materiales.SetColLabelValue( 2, u"250" )
        self.grilla_materiales.SetColLabelValue( 3, u"500" )
        self.grilla_materiales.SetColLabelValue( 4, u"1000" )
        self.grilla_materiales.SetColLabelValue( 5, u"2000" )
        self.grilla_materiales.SetColLabelValue( 6, u"4000" )
        self.grilla_materiales.SetColLabelValue( 7, u"Promedio" )
        self.grilla_materiales.SetColLabelValue( 8, u"Dispersión" )
        self.grilla_materiales.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.grilla_materiales.EnableDragRowSize( True )
        self.grilla_materiales.SetRowLabelSize( 30 )
        self.grilla_materiales.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.grilla_materiales.SetDefaultCellAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )
        sizer_g_D_grilla.Add( self.grilla_materiales, 1, wx.ALL|wx.EXPAND, 5 )


        sizer_grafica_DOWN.Add( sizer_g_D_grilla, 1, wx.EXPAND, 5 )


        sizer_grafica.Add( sizer_grafica_DOWN, 1, wx.EXPAND, 5 )


        sizer_main.Add( sizer_grafica, 5, wx.EXPAND, 5 )


        self.SetSizer( sizer_main )
        self.Layout()

        self.Centre( wx.BOTH )
 #      Inicialización de Variables
 #      Inicialización de Funciones
        self.recintar()
 #      Connect Events
        self.nb_datos.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onCambiarPagina )
    #   ------------------------------ BOTONONES GRILLA MATERIALES -------------------------------#
        self.boton_asignar_material.Bind( wx.EVT_BUTTON, self.onAsignarMaterial )
        self.boton_eliminar_material.Bind( wx.EVT_BUTTON, self.onEliminarMaterial )
        self.boton_agregar_material.Bind( wx.EVT_BUTTON, self.onAgregarMaterial )
        self.boton_copiar_material.Bind( wx.EVT_BUTTON, self.onCopiarMaterial )
        self.boton_pegar_material.Bind( wx.EVT_BUTTON, self.onPegarMaterial )
        self.boton_abrir_archivo_material.Bind( wx.EVT_BUTTON, self.onAbrirMaterial )
        self.boton_guardar_material.Bind( wx.EVT_BUTTON, self.onGuardarMaterial )
        self.boton_buscar_material.Bind( wx.EVT_BUTTON, self.onBuscarMaterial )
    #   ----------------------------------- GRILLA MATERIALES ------------------------------------#
 #      Funciones
    def __del__( self ):
        pass
    def onCambiarPagina( self, event ):
        event.Skip()
  # ------------------------------ BOTONONES GRILLA MATERIALES -------------------------------#
    def onAsignarMaterial( self, event ):           # Falta hacer
        event.Skip()
    def onEliminarMaterial( self, event ):          # Falta hacer
        rows = self.grilla_materiales.GetSelectedRows()
        rows.reverse()
        for row in rows:
            self.grilla_materiales.DeleteRows(row,1)
    def onAgregarMaterial( self, event ):        
        row = self.grilla_materiales.GetNumberRows()   
        self.grilla_materiales.AppendRows(1)
        self.grilla_materiales.SetCellValue(row,0,'Material %s'%(row+1))
    def onCopiarMaterial( self, event ):            # Falta hacer
        event.Skip()
    def onPegarMaterial( self, event ):             # Falta hacer
        event.Skip()
    def onAbrirMaterial( self, event ):             # Falta hacer
        event.Skip()
    def onGuardarMaterial( self, event ):           # Falta hacer
        event.Skip()
    def onBuscarMaterial( self, event ):            # Falta hacer
        event.Skip()
  # ----------------------------------- GRILLA MATERIALES ------------------------------------#
  # ------------------------------------ GRAFICA RECINTO -------------------------------------#     
    def recintar(self):
        piso  = [[0,0,0],[10,0,0],[10,7,0],[0,7,0]]
        techo = [[0,0,3],[10,0,3],[10,7,3],[0,7,3]]
        par_s = [[0,0,0],[10,0,0],[10,0,3],[0,0,3]]
        par_n = [[0,7,0],[10,7,0],[10,7,3],[0,7,3]]
        par_e = [[0,0,0],[0,7,0],[0,7,3],[0,0,3]]
        par_o = [[10,0,0],[10,7,0],[10,7,3],[10,0,3]]
        sups = [piso,techo,par_s,par_n,par_e,par_o]
        menor = min(min(min(sups)))
        mayor = max(max(max(sups)))
        for sup in sups:
            for i in range(-1,len(sup)-1,1):
                self.ax.plot([sup[i][0],sup[i+1][0]],
                             [sup[i][1],sup[i+1][1]],
                             [sup[i][2],sup[i+1][2]],
                             linewidth=0.6,color='#444444')
        self.ax.set_xlim(menor,mayor),self.ax.set_ylim(menor-mayor*0.1,mayor*0.9),self.ax.set_zlim(menor-mayor*0.4,mayor*0.6)


if __name__=='__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()

