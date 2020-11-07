# -*- coding: utf-8 -*-


import wx
import wx.xrc
import wx.aui

from Paneles.paneles import *

class MainFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1336,830), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        sizer_main = wx.BoxSizer( wx.HORIZONTAL )
    #   ====================================== SIZER DATOS ======================================= #
        sizer_datos = wx.BoxSizer( wx.VERTICAL )

        # self.nb_datos = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_NOPAGETHEME )
        # self.paneles_datos = []
        # self.paneles_datos.append(Panel_Recinto(self.nb_datos,name='Recinto'))
        # self.paneles_datos.append(Panel_FuenteReceptor(self.nb_datos,name='Fuente/Receptor'))
        # self.paneles_datos.append(Panel_OtrosDatos(self.nb_datos,name='Otros Datos'))
        # for panel in self.paneles_datos:
        #     self.nb_datos.AddPage(panel,panel.name)

        # sizer_datos.Add( self.nb_datos, 1, wx.EXPAND |wx.ALL, 5 )

        self.aui_nb_datos = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.paneles_datos = []
        self.paneles_datos.append(PanelRecinto(self.aui_nb_datos,name='Recinto'))
        self.paneles_datos.append(Panel_FuenteReceptor(self.aui_nb_datos,name='Fuente/Receptor'))
        self.paneles_datos.append(Panel_OtrosDatos(self.aui_nb_datos,name='Otros'))
        for panel in self.paneles_datos:
            self.aui_nb_datos.AddPage(panel,panel.name)
        sizer_datos.Add( self.aui_nb_datos, 1, wx.EXPAND |wx.ALL, 5 )


        sizer_main.Add( sizer_datos, 1, wx.EXPAND, 5 )
    #   ===================================== SIZER GRAFICA ====================================== # 
        sizer_grafica = wx.BoxSizer( wx.VERTICAL )

        # panel_grafica = PanelGraficaRecinto(self)
        # sizer_grafica.Add( panel_grafica, 4, wx.ALL|wx.EXPAND, 5 )

        self.aui_nb_grafica = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.panel_grafica = PanelGraficaRecinto(self.aui_nb_grafica)
        self.aui_nb_grafica.AddPage(self.panel_grafica,'Recinto')
        sizer_grafica.Add( self.aui_nb_grafica, 3, wx.EXPAND |wx.ALL, 5 )
   
        self.panel_materiales = PanelMateriales(self)
        sizer_grafica.Add( self.panel_materiales, 1, wx.ALL|wx.EXPAND, 5 )

        sizer_main.Add( sizer_grafica, 5, wx.EXPAND, 5 )

        self.SetSizer( sizer_main )
        self.Layout()

    #   ======================================== MENUBAR ========================================= #    
        self.menubar = wx.MenuBar( 0 )
        self.menubar.OSXGetAppleMenu()
        self.menu_archivo = wx.Menu()
        self.archivo_Abrir = wx.MenuItem( self.menu_archivo, wx.ID_ANY, u"Abrir"+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_archivo.Append( self.archivo_Abrir )

        self.archivo_Guardar = wx.MenuItem( self.menu_archivo, wx.ID_ANY, u"Guardar"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_archivo.Append( self.archivo_Guardar )

        self.archivo_GuardarComo = wx.MenuItem( self.menu_archivo, wx.ID_ANY, u"Guardar Como"+ u"\t" + u"Shift+Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_archivo.Append( self.archivo_GuardarComo )

        self.menu_archivo.AppendSeparator()

        self.archivo_Salir = wx.MenuItem( self.menu_archivo, wx.ID_ANY, u"Salir"+ u"\t" + u"Ctrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_archivo.Append( self.archivo_Salir )

        self.menubar.Append( self.menu_archivo, u"Archivo" )

        self.menu_Herramientas = wx.Menu()
        self.menubar.Append( self.menu_Herramientas, u"Herramientas" )

        self.menu_Visualizacion = wx.Menu()
        self.menubar.Append( self.menu_Visualizacion, u"Visualización" )

        self.SetMenuBar( self.menubar )
        self.Centre( wx.BOTH )

    #   Connect Events
        self.Bind( wx.EVT_MENU, self.onClickArchivoAbrir, id = self.archivo_Abrir.GetId() )
        self.Bind( wx.EVT_MENU, self.onClickArchivoGuardar, id = self.archivo_Guardar.GetId() )
        self.Bind( wx.EVT_MENU, self.onClickArchivoGuardarComo, id = self.archivo_GuardarComo.GetId() )
        self.Bind( wx.EVT_MENU, self.onClickArchivoSalir, id = self.archivo_Salir.GetId() )
 # FUNCIOENS 
    def __del__( self ):
        pass
   # ----------------------------------------- Datos ------------------------------------------ #
    def onCambiarPagina( self, event ):
        event.Skip()
    # Recinto
    def asignar_material(self,valores):
        '''valores => list'''
        self.paneles_datos[0].asignarMaterial(valores)
   # ---------------------------------------- Grafica ----------------------------------------- #
    def ajustar_grilla(self,x,y,z):
        self.panel_grafica.ajustar_grilla(x,y,z)
    def cambiar_color(self,old,new):
        self.panel_grafica.cambiar_color(old,new)
    def cambiar_linea(self,superficie,indice):
        self.panel_grafica.cambiar_linea(superficie,indice)
    def direccion_normal(self,superficie):
        self.panel_grafica.cambiar_normales(superficie)
    def eliminar_lineas(self,superficie,todas=False):
        if todas:
            self.panel_grafica.eliminar_lineas(superficie,todas=todas)
        else:
            self.panel_grafica.eliminar_lineas(superficie)
    def graficar(self,superficie):
        self.panel_grafica.crear_lineas(superficie)
   # --------------------------------------- Materiales --------------------------------------- #
   # ---------------------------------------- MenuBar ----------------------------------------- #
    def onClickArchivoAbrir(self,event):
        event.Skip()
    def onClickArchivoGuardar(self,event):
        event.Skip()
    def onClickArchivoGuardarComo(self,event):
        event.Skip()
    def onClickArchivoSalir(self,event):
        dial = wx.MessageDialog(None,'¿Desea cerrar el programa?','SALIR',wx.YES_NO)
        resp = dial.ShowModal()
        if resp == wx.ID_YES:
            dial.Destroy()
            self.Close()
        else: 
            dial.Destroy()

if __name__=='__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()