# -*- coding: utf-8 -*-
import os,sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir  = os.path.dirname(currentDir)
sys.path.append(parentDir)

import wx
import wx.xrc

class VenRecintoNuevo ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 289,209 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        sizer_main = wx.BoxSizer( wx.VERTICAL )

        sizer_datos = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Dimensiones del Recinto" ), wx.VERTICAL )


        sizer_datos.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        sizer_largo = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( sizer_datos.GetStaticBox(), wx.ID_ANY, u"Largo (x)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        sizer_largo.Add( self.m_staticText7, 1, wx.ALL, 5 )

        self.textCtrl_largo = wx.TextCtrl( sizer_datos.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_PROCESS_ENTER )
        sizer_largo.Add( self.textCtrl_largo, 1, wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( sizer_datos.GetStaticBox(), wx.ID_ANY, u"[m]", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        sizer_largo.Add( self.m_staticText8, 0, wx.ALL, 5 )


        sizer_datos.Add( sizer_largo, 0, wx.EXPAND, 5 )

        sizer_ancho = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText9 = wx.StaticText( sizer_datos.GetStaticBox(), wx.ID_ANY, u"Ancho (y)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        sizer_ancho.Add( self.m_staticText9, 1, wx.ALL, 5 )

        self.textCtrl_ancho = wx.TextCtrl( sizer_datos.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_PROCESS_ENTER )
        sizer_ancho.Add( self.textCtrl_ancho, 1, wx.ALL, 5 )

        self.m_staticText10 = wx.StaticText( sizer_datos.GetStaticBox(), wx.ID_ANY, u"[m]", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        sizer_ancho.Add( self.m_staticText10, 0, wx.ALL, 5 )


        sizer_datos.Add( sizer_ancho, 0, wx.EXPAND, 5 )

        sizer_alto = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( sizer_datos.GetStaticBox(), wx.ID_ANY, u"Alto (z)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        sizer_alto.Add( self.m_staticText11, 1, wx.ALL, 5 )

        self.textCtrl_alto = wx.TextCtrl( sizer_datos.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_PROCESS_ENTER )
        sizer_alto.Add( self.textCtrl_alto, 1, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( sizer_datos.GetStaticBox(), wx.ID_ANY, u"[m]", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        sizer_alto.Add( self.m_staticText12, 0, wx.ALL, 5 )


        sizer_datos.Add( sizer_alto, 0, wx.EXPAND, 5 )


        sizer_datos.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        sizer_main.Add( sizer_datos, 3, wx.EXPAND, 5 )

        sizer_botones = wx.BoxSizer( wx.HORIZONTAL )


        sizer_botones.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.boton_cancelar = wx.Button( self, wx.ID_ANY, u"Cancelar", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_botones.Add( self.boton_cancelar, 0, wx.ALL, 5 )

        self.boton_confirmar = wx.Button( self, wx.ID_ANY, u"Confirmar", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_botones.Add( self.boton_confirmar, 0, wx.ALL, 5 )


        sizer_botones.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        sizer_main.Add( sizer_botones, 0, wx.EXPAND, 5 )


        self.SetSizer( sizer_main )
        self.Layout()

        self.Centre( wx.BOTH )
 #  Inicializacion de Variables
        self.largo = ''
        self.ancho = ''
        self.alto = '' 
 #  Connect Events
        self.textCtrl_largo.Bind( wx.EVT_KILL_FOCUS, self.onKFLargo )
        self.textCtrl_largo.Bind( wx.EVT_TEXT_ENTER, self.onEnterLargo )
        self.textCtrl_ancho.Bind( wx.EVT_KILL_FOCUS, self.onKFAncho )
        self.textCtrl_ancho.Bind( wx.EVT_TEXT_ENTER, self.onEnterAncho )
        self.textCtrl_alto.Bind( wx.EVT_KILL_FOCUS, self.onKFAlto )
        self.textCtrl_alto.Bind( wx.EVT_TEXT_ENTER, self.onEnterAlto )
        self.boton_cancelar.Bind( wx.EVT_BUTTON, self.onClickCancelar )
        self.boton_confirmar.Bind( wx.EVT_BUTTON, self.onClickConfirmar )
    def __del__( self ):
        pass
 #  Virtual event handlers, overide them in your derived class
  # ----------------------------------------- Enter ------------------------------------------ #
    def onEnterLargo( self, event ):
        cadena = self.textCtrl_largo.GetValue()
        valor = self.revisar(cadena)
        if valor != None:
            self.largo = valor
            self.textCtrl_largo.SetValue('')
            self.textCtrl_largo.SetValue(str(self.largo))
        else:
            self.textCtrl_largo.SetValue('')
            self.textCtrl_largo.SetValue(str(self.largo))
        self.textCtrl_ancho.SetFocus()
    def onEnterAncho( self, event ):
        cadena = self.textCtrl_ancho.GetValue()
        valor = self.revisar(cadena)
        if valor != None:
            self.ancho = valor
            self.textCtrl_ancho.SetValue('')
            self.textCtrl_ancho.SetValue(str(self.ancho))
        else:
            self.textCtrl_ancho.SetValue('')
            self.textCtrl_ancho.SetValue(str(self.ancho))
        self.textCtrl_alto.SetFocus()
    def onEnterAlto( self, event ):
        cadena = self.textCtrl_alto.GetValue()
        valor = self.revisar(cadena)
        if valor != None:
            self.alto = valor
            self.textCtrl_alto.SetValue('')
            self.textCtrl_alto.SetValue(str(self.alto))
        else:
            self.textCtrl_alto.SetValue('')
            self.textCtrl_alto.SetValue(str(self.alto))
        self.onClickConfirmar(event)
  # --------------------------------------- Kill Focus --------------------------------------- #
    def onKFLargo( self, event ):
        cadena = self.textCtrl_largo.GetValue()
        valor = self.revisar(cadena)
        if valor != None:
            self.largo = valor
            self.textCtrl_largo.SetValue('')
            self.textCtrl_largo.SetValue(str(self.largo))
        else:
            self.textCtrl_largo.SetValue('')
            self.textCtrl_largo.SetValue(str(self.largo))
    def onKFAncho( self, event ):
        cadena = self.textCtrl_ancho.GetValue()
        valor = self.revisar(cadena)
        if valor != None:
            self.ancho = valor
            self.textCtrl_ancho.SetValue('')
            self.textCtrl_ancho.SetValue(str(self.ancho))
        else:
            self.textCtrl_ancho.SetValue('')
            self.textCtrl_ancho.SetValue(str(self.ancho))
    def onKFAlto( self, event ):
        cadena = self.textCtrl_alto.GetValue()
        valor = self.revisar(cadena)
        if valor != None:
            self.alto = valor
            self.textCtrl_alto.SetValue('')
            self.textCtrl_alto.SetValue(str(self.alto))
        else:
            self.textCtrl_alto.SetValue('')
            self.textCtrl_alto.SetValue(str(self.alto))
  # ---------------------------------------- Botones ----------------------------------------- # 
    def onClickCancelar( self, event ):
        self.EndModal(wx.CANCEL)
    def onClickConfirmar( self, event ):
        if type(self.largo) == float:
            if type(self.ancho) == float:
                if type(self.alto) == float:
                    self.EndModal(wx.OK)
                else:
                    eje = 'Alto (z)'
                    self.mensajeError(eje)
                    self.textCtrl_alto.SetFocus()
            else:
                eje = 'Ancho (y)'
                self.mensajeError(eje)
                self.textCtrl_ancho.SetFocus()
        else:
            eje = 'Largo (x)'
            self.mensajeError(eje)
            self.textCtrl_largo.SetFocus()
  # -------------------------------------- Herramientas -------------------------------------- #
    def revisar(self,cadena):
        try:
            valor = float(cadena)
            return valor
        except ValueError:
            return None
    def mensajeError(self,eje):
        dial = wx.MessageDialog(None,'Cantidad ingresada inválida en: %s'%(eje),'Error',wx.OK)
        resp = dial.ShowModal()
        if resp == wx.OK:
            dail.Destroy()