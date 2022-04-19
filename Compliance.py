#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import time
import functools
import subprocess, sys
from tkinter import ttk
from getpass import getuser
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font as font
from PIL import Image, ImageTk
from tkinter.ttk import Style
from threading import Thread
from ScrollableNotebook  import *
from configparser import ConfigParser
#-----------------------------------------------------------#
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
clt = ''
path_modulo = mypath+"Compliance/file/desviaciones_{}.json"
path_modulo_clave = mypath+"Compliance/file/{}.json"
path_config = mypath+"Compliance/.conf/{}.json"
path_config_ini = mypath+"Compliance/.conf/{}"

list_client = []  
list_issues = (
    "DESVIACIONES",
    "EXTRACIONES"
)
# --- VARIABLE GLOBAL ---
asigne_Cliente = ""
idOpenTab = 0
listModulo = []
listClave = []
txtWidget_focus = False
txtWidget = ""
sis_oper = ""
idpTab = 0
varNum = 0
text_aExpandir = ""
value = ""
valor_activo_list = ""
list_motion = ""
automatizar = ""
#TODO VARIABLES DE VENTANAS
PST_DESV = ""
PST_EXP = ""
PST_AUT = ""
#TODO----------------------
_tt_Desv = ""
listbox_list = []
no_exist =  False
extracion = ""
sisO = ""
lblMd = ""
lblDs = ""
com = ""
bak = ""
edi = ""
res = ""
evd = ""

#* Configuracion de APARIENCIA INICIAL
parse = ConfigParser()
parse.read(path_config_ini.format("apariencia.ini"))
bg_menu = parse.get('menu', 'background')
fg_menu = parse.get('menu', 'foreground')
acbg_menu = parse.get('menu', 'activebackground')
acfg_menu = parse.get('menu', 'activeforeground')
fg_submenu = parse.get('menu', 'foreground_submenu')
bg_submenu = parse.get('menu', 'background_submenu')
oddrow = '#CEE5D0'
evenrow = '#F3F0D7'
fondo_app = '#FBF8F1'
color_titulos = '#FF8080'
sel_bg_txt = 'lightblue'
sel_fg_txt = 'black'
active_color = '#297F87'
color_fg_list =  '#334257'
bg_panel_buscar = '#A2D5AB'
acbg_panel_buscar = '#39AEA9'
fuente_titulos = 'Open Sanz'
fuente_texto = 'Consolas'
fuente_menu = 'Consolas'
fuente_boton = 'Open Sanz'
fuente_pestañas = 'Sans-Serif'
tamñ_titulo = 14
tamñ_texto = 14
tamñ_texto_menucon = 13
tamñ_boton = 14
tamñ_menu = 14
tamñ_texto_exp = 16
tamñ_pestaña = 12
_Font_Menu = (fuente_menu, tamñ_menu, font.BOLD)
_Font_Texto = (fuente_texto, tamñ_texto)
_Font_Texto_menucon = (fuente_texto, tamñ_texto_menucon)
_Font_Boton = (fuente_boton, tamñ_boton, font.BOLD)
_Font_Titulo_bold = (fuente_titulos, tamñ_titulo, font.BOLD)
_Font_pestañas = (fuente_pestañas, tamñ_pestaña, font.BOLD)
_Font_txt_exp = (fuente_texto, tamñ_texto_exp)
_Font_tt_exp = (fuente_titulos, tamñ_texto_exp, font.BOLD)

def beep_error(f):
    '''
    Decorador que permite emitir un beep cuando un método de instancia
    decorado de un widget produce una excepción
    '''
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    return applicator

class Expandir(ttk.Frame):
    def __init__(self, parent, text_EXP, widget_EXP, customer, titulo, so, st_btnDIR, st_btnAUTH, st_btnSER, st_btnACC, st_btnCMD, st_btnIDR, varNum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global PST_EXP
        self.parent = parent
        self.customer = customer
        self.titulo = titulo
        self.so = so
        PST_EXP = self
        # Recibe el text del SRC a expandir
        self.txt_Expan = text_EXP
        self.widget_EXP = widget_EXP
        ##-----------------------------------
        self.st_btnDIR = st_btnDIR
        self.st_btnAUTH = st_btnAUTH
        self.st_btnSER = st_btnSER
        self.st_btnACC = st_btnACC
        self.st_btnCMD = st_btnCMD
        self.st_btnIDR = st_btnIDR
        self.varNum = varNum
        self.vtn_expandir = tk.Toplevel(self)
        self.vtn_expandir.config(background=fondo_app)
        window_width=1170
        window_height=650
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_expandir.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_expandir.tk.call('wm', 'iconphoto', self.vtn_expandir._w, tk.PhotoImage(file=path_icon+r'expandir1.png'))       
        self.vtn_expandir.transient(self.parent)
        self.vtn_expandir.title("DESVIACIONES : {} - {}".format(self.customer,self.so))
        self.vtn_expandir.columnconfigure(0, weight=1)
        self.vtn_expandir.rowconfigure(1, weight=1)
        self.vtn_expandir.resizable(False, False)
        # ----------------------------------------------------------------
        self.icono()
        self.menu_clickDerecho()
        self.widgets_EXPANDIR()
        self.Expan_color_lineas()
        self.bind("<Motion>", lambda e: self.EXP_motion(e))
        self.EXP_srcExpandir.bind("<Button-3><ButtonRelease-3>", self.display_menu_clickDerecho)
        self.EXP_srcExpandir.bind("<Motion>", lambda e:desviacion.activar_Focus(e))
        self.EXP_srcExpandir.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.EXP_srcExpandir.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
    ## --- MENU CONTEXTUAL --------------------------- ##
    def EXP_motion(self, event):
        global PST_EXP
        PST_EXP = event.widget
    
    def icono(self):
        self.previous_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"previous.png").resize((40, 40)))
        self.next_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"next.png").resize((40, 40)))    
    
    def cerrar_vtn_expandir(self):
        #if txtWidget_focus:
        self.vtn_expandir.destroy()
    
    def menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self.vtn_expandir, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Copiar", 
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command= desviacion.copiar_texto_seleccionado,
            state="disabled"
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=lambda : desviacion.seleccionar_todo(event=None),
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            #image=self.cerrar_icon,
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=self.cerrar_vtn_expandir
        )
    
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.srcEvent = event.widget
        self.srcEvent.focus()
        txt_select = event.widget.tag_ranges(tk.SEL)
        if txt_select:
            self.menu_Contextual.entryconfig("  Copiar", state="normal")
        else:
            self.menu_Contextual.entryconfig("  Copiar", state="disabled")
    ## ----------------------------------------------- ##
    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel","1.0","end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel","1.0","end")
    
    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel","1.0","end")
            return 'break'
        else:
            pass
        
    def _siguiente(self):
        global _tt_Desv
        self.EXP_btnScreamEvidencia.config(state="disabled")
        self.EXP_btnCopyALL.config(state="disabled")
        if self.varNum == 1:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['copia']
                        if self._txt_Desv is None:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['editar'])
                            self.varNum = 3
                            self.descativar_botones()
                        else:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.varNum = 2
                            self.descativar_botones()
        elif self.varNum == 2:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['editar']
                        if self._txt_Desv is None:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['refrescar'])
                            self.EXP_btnCopyALL.config(state="normal")                        
                            self.varNum = 4
                            self.descativar_botones()
                        else:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.varNum = 3
                            self.descativar_botones()
        elif self.varNum == 3:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['refrescar']
                        if self._txt_Desv is None:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['evidencia'])
                            self.EXP_btnScreamEvidencia.config(state="normal")
                            self.EXP_btnCopyALL.config(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
                        else:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.EXP_btnCopyALL.config(state="normal")                        
                            self.varNum = 4      
                            self.descativar_botones()
        elif self.varNum == 4:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['evidencia']
                        if self._txt_Desv is None:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['comprobacion'])
                            self.varNum = 1
                            self.activar_botones()
                        else:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.EXP_btnScreamEvidencia.config(state="normal")
                            self.EXP_btnCopyALL.config(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
        elif self.varNum == 5:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['comprobacion']
                        if self._txt_Desv is None:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['copia'])
                            self.varNum = 2
                            self.descativar_botones()
                        else:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.varNum = 1
                            self.activar_botones()
        self.Expan_color_lineas()

    def activar_botones(self):
        global PST_EXP
        if self.st_btnDIR:
            self.EXP_btn_VentanasDIR.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnAUTH:
            self.EXP_btn_VentanasAUTH.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnSER:
            self.EXP_btn_VentanasSER.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnACC:
            self.EXP_btn_VentanasACC.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnCMD:
            self.EXP_btn_VentanasCMD.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnIDR:
            self.EXP_btn_VentanasIDR.grid(row=0, column=3, pady=5, sticky='ne')

    def _anterior(self):
        global _tt_Desv
        self.EXP_btnScreamEvidencia.config(state="disabled")
        self.EXP_btnCopyALL.config(state="disabled")
        if self.varNum == 1:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['evidencia']
                        if self._txt_Desv is None:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['refrescar'])
                            self.EXP_btnCopyALL.config(state="normal")                        
                            self.varNum = 4
                            self.descativar_botones()
                        else:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.EXP_btnScreamEvidencia.config(state="normal")
                            self.EXP_btnCopyALL.config(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
        elif self.varNum == 2:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['comprobacion']
                        if self._txt_Desv is None:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['evidencia'])
                            self.EXP_btnScreamEvidencia.config(state="normal")
                            self.EXP_btnCopyALL.config(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
                        else:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.varNum = 1
                            self.activar_botones()
        elif self.varNum == 3:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['copia']
                        if self._txt_Desv is None:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['evidencia'])
                            self.varNum = 1
                            self.activar_botones()
                        else:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.varNum = 2
                            self.descativar_botones()
        elif self.varNum == 4:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['editar']
                        if self._txt_Desv is None:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['copia'])
                            self.varNum = 2
                            self.descativar_botones()
                        else:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.varNum = 3
                            self.descativar_botones()
        elif self.varNum == 5:
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['refrescar']
                        if self._txt_Desv is None:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,md['editar'])
                            self.varNum = 2
                            self.descativar_botones()
                        else:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',tk.END)
                            self.EXP_srcExpandir.insert(tk.END,self._txt_Desv)
                            self.EXP_btnCopyALL.config(state="normal")                        
                            self.varNum = 1
                            self.activar_botones()
        self.Expan_color_lineas()

    def widgets_EXPANDIR(self):
        self.EXP_lblWidget = ttk.Label(
            self.vtn_expandir, 
            text=self.titulo,
            foreground=color_titulos,
            font=_Font_tt_exp,
        )
        self.EXP_lblWidget.grid(row=0, column=0, padx=5, pady=5,sticky='w')
        self.EXP_srcExpandir = st.ScrolledText(
            self.vtn_expandir,
        )
        self.EXP_srcExpandir.config(
            font=_Font_txt_exp, 
            wrap=tk.WORD,
            highlightcolor=active_color,
            borderwidth=0, 
            highlightthickness=3,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
        )
        ## Inserta el TEXT DEL SRC RECIBIO
        self.EXP_srcExpandir.insert('1.0',self.txt_Expan)
        ## -------------------------------
        self.EXP_btn_VentanasDIR = ttk.Button(
            self.vtn_expandir,
            text='Permissions',
            compound=tk.LEFT,
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_DIRECTORY,
            state="normal"
        )
        self.EXP_btn_VentanasAUTH = ttk.Button(
            self.vtn_expandir,
            text='Authorized',
            compound=tk.LEFT,
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_AUTHORIZED,
            state="normal"
        )
        self.EXP_btn_VentanasSER = ttk.Button(
            self.vtn_expandir,
            text='Service',
            compound=tk.LEFT,
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_SERVICE,
            state="normal"
        )
        self.EXP_btn_VentanasACC = ttk.Button(
            self.vtn_expandir,
            text='Account',
            compound=tk.LEFT,
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_ACCOUNT,
            state="normal"
        )
        self.EXP_btn_VentanasCMD = ttk.Button(
            self.vtn_expandir,
            text='Command',
            compound=tk.LEFT,
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_COMMAND,
            state="normal"
        )
        self.EXP_btn_VentanasIDR = ttk.Button(
            self.vtn_expandir,
            text='Id_Rsa',
            compound=tk.LEFT,
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_IDRSA,
            state="normal"
        )
        self.EXP_btn_Siguiente = tk.Button(
            self.vtn_expandir,
            text='SIGUIENTE',
            image=self.next_icon,            
            command=self._siguiente,
            border=0,
            borderwidth=0,
            highlightthickness=0,
            background=fondo_app,
            relief="flat",
            highlightbackground=fondo_app,
            activebackground=fondo_app,
        )
        self.EXP_btn_Siguiente.grid(row=0, column=2, pady=5, padx=10, sticky='ns')
        
        self.EXP_btn_Anterior = tk.Button(
            self.vtn_expandir,
            text='ANTERIOR',
            image=self.previous_icon,            
            command=self._anterior,
            border=0,
            borderwidth=0,
            highlightthickness=0,
            background=fondo_app,
            relief="flat",
            highlightbackground=fondo_app, 
            activebackground=fondo_app,
        )
        self.EXP_btn_Anterior.grid(row=0, column=1, pady=5, sticky='ns')
        if self.st_btnDIR and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasDIR.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnAUTH and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasAUTH.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnSER and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasSER.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnACC and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasACC.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnCMD and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasCMD.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnIDR and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasIDR.grid(row=0, column=3, pady=5, sticky='ne')
        else:
            self.descativar_botones()     
        
        self.EXP_btnCopyALL = ttk.Button(
            self.vtn_expandir,
            image=desviacion.CopyALL1_icon,
            command=lambda e=self.EXP_srcExpandir : self.copiarALL(e),
            state="disabled"
        )
        self.EXP_btnCopyALL.grid(row=0, column=4, padx=20, pady=5, sticky='ne')
        self.EXP_btnScreamEvidencia = ttk.Button(
            self.vtn_expandir,
            image=desviacion.Captura1_icon,
            command=desviacion.ScreamEvidencia,
            state="disabled",
        )
        self.EXP_btnScreamEvidencia.grid(row=0, column=5, pady=5, sticky='ne')
        self.EXP_btnReducir = ttk.Button(
            self.vtn_expandir,
            image=desviacion.Reducir_icon,
            command=self.cerrar_vtn_expandir,
        )
        self.EXP_btnReducir.grid(row=0, column=6, padx=20, pady=5, sticky='ne')
        self.EXP_srcExpandir.grid(row=1, column=0, padx=5, pady=5, sticky='nsew', columnspan=7)

    def descativar_botones(self):
        self.EXP_btn_VentanasDIR.grid_forget()     
        self.EXP_btn_VentanasAUTH.grid_forget()     
        self.EXP_btn_VentanasSER.grid_forget()     
        self.EXP_btn_VentanasACC.grid_forget()     
        self.EXP_btn_VentanasCMD.grid_forget()     
        self.EXP_btn_VentanasIDR.grid_forget()

    def Expan_color_lineas(self):
        indx = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx = self.EXP_srcExpandir.search(line1, indx, nocase=1, stopindex=tk.END)
                if not indx: 
                    break
                lastidx = '%s+%dc' % (indx, len(line1))
                self.EXP_srcExpandir.tag_add('found1', indx, lastidx)
                indx = lastidx
                self.EXP_srcExpandir.tag_config(
                'found1', 
                foreground='dodgerblue',
                font=(fuente_texto, 16, font.BOLD)
                )

class TextSimilar(ttk.Frame):
    def __init__(self, parent, titulo, modulo_clave, cliente, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global no_exist
        self.titulo = titulo
        self.cliente = cliente
## ---- TOP LEVEL-----
        self.vtn_modulos = tk.Toplevel(self)
        self.vtn_modulos.config(background=fondo_app)
        window_width=1000
        window_height=300
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height)
        position_right = int(screen_width+150)
        self.vtn_modulos.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_modulos.resizable(0,0)
        self.vtn_modulos.transient(self)
        self.vtn_modulos.grab_set()
        self.vtn_modulos.focus_set()
        self.vtn_modulos.config(background=fondo_app)


## --- FRAME TITULO
        self.frame1 = ttk.Frame(
            self.vtn_modulos,
        )
        self.frame1.pack(fill='both', side='top', expand=0)

        self.titulo = ttk.Label(
            self.frame1,
            text=self.titulo,
            font=_Font_Titulo_bold,
        )
        self.titulo.pack()

## --- FRAME LISTBOX
        self.frame2 = ttk.Frame(
            self.vtn_modulos,
        )
        self.frame2.pack(fill='both', side=tk.LEFT, expand=1, pady=5, padx=5)
        self.frame2.pack_propagate(1)
        self.frame2.rowconfigure(0, weight=5)
        self.frame2.columnconfigure(0, weight=5)


## --- LISTBOX MODULO - FRAME2
        self._list_modulo = tk.Listbox(
            self.frame2,
            font=_Font_Texto,
            foreground=color_fg_list,
            selectbackground=sel_bg_txt,
            selectforeground=sel_fg_txt,
            exportselection=False,
            highlightthickness=2,
            highlightcolor = active_color,
        )

        self._list_modulo.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

## --- FUNCIONES LIST MODULO A SCROLL
        self._list_modulo.bind("<Down>", lambda e: self._OnVsb_down(e))
        self._list_modulo.bind("<Up>", lambda e: self._OnVsb_up(e))

## --- FRAME 3
        self.frame3 = ttk.Frame(
            self.vtn_modulos,
        )
        self.frame3.pack(fill='both', side='right', expand=0, pady=5, padx=5)
        self.frame3.rowconfigure(0, weight=1)

## --- LISTBOX CLAVE - FRAME 3
        self._list_clave = tk.Listbox(
            self.frame3,
            font=_Font_Texto,
            foreground=color_fg_list,
            selectbackground=sel_bg_txt,
            selectforeground=sel_fg_txt,
            exportselection=False,
            highlightthickness=2,
            highlightcolor = active_color,
            width=18,
            height=18,
        )
        self._list_clave.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

## --- LISTBOX SO - FRAME 2
        self._list_SO = tk.Listbox(
            self.frame3,
            font=_Font_Texto,
            foreground=color_fg_list,
            selectbackground=sel_bg_txt,
            selectforeground=sel_fg_txt,
            exportselection=False,
            highlightthickness=2,
            highlightcolor = active_color,
            width=12,
            height=12,
        )
        self._list_SO.grid(row=0, column=1, sticky='nsew', pady=5, padx=(0,5))

## - CREAR SCROLL
        self.vsb_scroll = tk.Scrollbar(
            self.frame3, 
            orient="vertical", 
            command=self.yview
        )

        self.vsb_scroll.grid(row=0, column=2, sticky='nsew')

## --- list asociados a los SCROLL
        self._list_modulo.configure(yscrollcommand = self.yscroll_modulo)
        self._list_clave.configure(yscrollcommand = self.yscroll_clave)
        self._list_SO.configure(yscrollcommand = self.yscroll_so)

##--------------------------------------------------------------------
## --- INSERTAR MODULO Y CLAVE A LIST BOX
        ## TRUE
        if no_exist:
            for m, c in modulo_clave.items():
                self._list_modulo.insert(tk.END, m)
                self._list_clave.insert(tk.END, c[0])
                self._list_SO.insert(tk.END, c[1])
            self._list_modulo.bind('<<ListboxSelect>>', lambda e : self.on_SelectList(e))
            self._list_modulo.bind('<Double-Button-1>', lambda e : self.on_DoubleSelectList(e))
        else:
            for m, c in modulo_clave.items():
                self._list_modulo.insert(tk.END, m)
                self._list_clave.insert(tk.END, c[0])
                self._list_SO.insert(tk.END, c[1])
            self._list_modulo.bind('<<ListboxSelect>>', lambda e : self.on_SelectList(e))
            self._list_modulo.bind('<Double-Button-1>', functools.partial(self._on_select_list))
        
##TODO --- Bloquear select listbox
        self._list_clave.bindtags((self._list_clave, app, "all"))
        self._list_SO.bindtags((self._list_clave, app, "all"))

## --- FUNCIONES PARA SCROLLBAR

    def yscroll_modulo(self, *args):
        wyview = self._list_modulo.yview()
        if  self._list_clave.yview() != wyview:
            self._list_clave.yview_moveto(args[0])
        if self._list_SO.yview() != wyview:
            self._list_SO.yview_moveto(args[0])
        self.vsb_scroll.set(*args)

    def yscroll_clave(self, *args):
        wyview = self._list_SO.yview()
        if  self._list_clave.yview() != wyview:
            self._list_clave.yview_moveto(args[0])
        if self._list_modulo.yview() != wyview:
            self._list_modulo.yview_moveto(args[0])
        self.vsb_scroll.set(*args)

    def yscroll_so(self, *args):
        wyview = self._list_clave.yview()
        if self._list_SO.yview() != wyview:
            self._list_SO.yview_moveto(args[0])
        if self._list_modulo.yview() != wyview:
            self._list_modulo.yview_moveto(args[0])
        self.vsb_scroll.set(*args)

    def yview(self, *args):
        self._list_modulo.yview(*args)
        self._list_clave.yview(*args)
        self._list_SO.yview(*args)

## --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_down(self, event):
        list_event = event.widget
        list_event.yview_scroll(1,"units")
        self._list_clave.yview_scroll(1,"units")
        self._list_SO.yview_scroll(1,"units")

## --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_up(self, event):
        list_event = event.widget
        list_event.yview_scroll(-1,"units")
        self._list_clave.yview_scroll(-1,"units")
        self._list_SO.yview_scroll(-1,"units")

## --- ACCION AL SELECIONAR
    def on_SelectList(self, event):
        global asigne_Cliente
        listbox_list_all = []
        widget = event.widget
        index = widget.curselection()
        listbox_list_all.append(self._list_modulo)   
        listbox_list_all.append(self._list_clave)
        listbox_list_all.append(self._list_SO)

        for lb in listbox_list_all:
            if lb != widget:
                lb.selection_clear(0, tk.END)
                for i in index:
                    lb.selection_set(int(i))

## --- ACCION DOBLE CLICK
    def on_DoubleSelectList(self, event):
        global asigne_Cliente
        global value
        listbox_list_all = []
        widget = event.widget
        index = widget.curselection()
        listbox_list_all.append(self._list_modulo)   
        listbox_list_all.append(self._list_clave)
        listbox_list_all.append(self._list_SO)
        clt = self._list_SO.get(index[0])
        modulo_Buscado = self._list_modulo.get(index[0])
        desviacion = Desviacion(app.cuaderno)
        app.cuaderno.add(desviacion, text='DESVIACIONES : {} '.format(clt))
        desviacion.enabled_Widgets()
        asigne_Cliente = clt
        desviacion.clientesVar.set(clt)
        with open(path_modulo.format(clt)) as g:
            data = json.load(g)
            listModulo = []
            for md in data:
                listModulo.append(md['modulo'])
        listModulo.sort()
        desviacion.DESVfr1_listbox.insert(tk.END,*listModulo)
        data = []
        modulo_Buscado = str(modulo_Buscado).replace("[","").replace("]","").replace("'","")
        with open(path_modulo.format(clt)) as g:
            data = json.load(g)
            for md in data:
                if modulo_Buscado in md['modulo']:
                    value = md['modulo']
                    # --- LIMPIAR ------------------------------------- ##                      
                    desviacion.limpiar_Widgets()
                    ## ------------------------------------------------- ##
                    desviacion.asignarValor_aWidgets(md)
            desviacion.mostrar_buttons_modulo(modulo_Buscado)
            desviacion.DESVfr1_listbox.selection_clear(0, tk.END)
            modulo_ListBox = desviacion.DESVfr1_listbox.get(0, tk.END)
            indice = modulo_ListBox.index(value)
            desviacion.DESVfr1_listbox.selection_set(indice)
        self.vtn_modulos.destroy()

    @beep_error
    def _on_select_list(self, event):
        global value
        global PST_DESV
        listbox = event.widget
        index = listbox.curselection()
        value = listbox.get(index[0])
        modulo_ListBox = PST_DESV.DESVfr1_listbox.get(0, tk.END)
        indice = modulo_ListBox.index(value)
        PST_DESV.DESVfr1_listbox.selection_set(indice)
        self.vtn_modulos.destroy()
        desviacion._cargar_elemt_selected(value)

class Desviacion(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent,*args)
        global PST_DESV
        self.parent = parent
        PST_DESV = self
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.bind("<Motion>", lambda e : self.DESV_motion(e))
# --- FUENTE PARA DESVIACIONES
# --- Fuente Menu click derecho 
        self.iconos()
        self.widgets_DESVIACION()
        self._menu_clickDerecho()
          
## --- SELECCIONAR ELEMENTO DEL LISTBOX. --- #
        self.DESVfr1_listbox.bind("<<ListboxSelect>>", self.seleccionar_Modulo)

## --- ADJUTAR EL TEXT DE LOS LABEL --- #
        self.DESVfr2_lblModulo.bind("<Configure>", self.label_resize)
        self.DESVfr2_lblDescripcion.bind("<Configure>", self.label_resize)

## --- ACTIVAR WIDGET. --- #
        #self.DESVfr2_lblModulo.bind("<Motion>",lambda e:self.activar_Focus(e))
        #self.DESV_frame2.bind("<Motion>",lambda e:self.activar_Focus(e))
        #self.DESVfr2_lblDescripcion.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr2_srcComprobacion.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr2_srcBackup.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcEditar.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcRefrescar.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcEvidencia.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr1_entModulo.bind("<Motion>",lambda e:self._act_focus_ent(e))
        app.cuaderno.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr1_listbox.bind("<Motion>",lambda e:self._activar_Focus(e))

## --- MOSTRAR MENU DERECHO  --- ##
        self.DESVfr2_srcComprobacion.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr2_srcBackup.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr3_srcEditar.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr3_srcRefrescar.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr3_srcEvidencia.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)

## --- ACTIVAR MODO SOLO LECTURA --- ##
        self.DESVfr2_srcComprobacion.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr2_srcBackup.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcEditar.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcRefrescar.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcEvidencia.bind("<Key>", lambda e: self.widgets_SoloLectura(e))


## --- SELECCIONAR TOD --- ##
        self.DESVfr2_srcComprobacion.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr2_srcBackup.bind('<Control-a>', lambda e: self._seleccionar_todo(e))

## --- BIND --- ##
        self.DESVfr1_entModulo.bind("<Return>", lambda event=None: self.buscar_Modulos(self.DESVfr1_entModulo.get()))
        self.DESVfr1_entModulo.bind("<KeyPress>", lambda e: self.clear_bsq_buttom(e))
        self.DESVfr1_listbox.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr1_listbox.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr1_listbox.bind("<Down>",lambda e : self.ListDown(e))
        self.DESVfr1_listbox.bind("<Up>",lambda e : self.ListUp(e))   
        self.DESVfr1_entModulo.bind('<Control-x>', lambda e : self._clear_busqueda(e)) 
        self.DESVfr1_entModulo.bind("<FocusIn>", lambda e: self.clear_busqueda(e))               
        self.DESVfr1_entModulo.bind("<FocusOut>", lambda e: self.clear_busqueda(e))

        self.DESVfr2_srcComprobacion.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr2_srcComprobacion.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr2_srcComprobacion.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr2_srcBackup.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))

        self.DESVfr3_srcEditar.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcRefrescar.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcEvidencia.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcEditar.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr3_srcEvidencia.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr3_srcEditar.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcRefrescar.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcEvidencia.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcEditar.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcEvidencia.bind('<Control-f>', lambda e : self.buscar(e))

## --- DESHABILITAR BOTONES --- ##
        self._btnDir = False
        self._btnAuth = False
        self._btnSer = False
        self._btnAcc = False
        self._btnCmd = False
        self._btnIdr = False

    def DESV_motion(self, event):
        global PST_DESV
        PST_DESV = event.widget

    def iconos(self): #TODO ICONOS DE VENTANA DESVIACION
        self.BuscarModulo_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"buscar.png").resize((25, 25)))
        self.LimpiarModulo_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"limpiar.png").resize((25, 25)))
        self.Expandir_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"expandir.png").resize((20, 20)))
        self.recortar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"recortar.png").resize((20, 20)))
        self.Expandir_icon1 = ImageTk.PhotoImage(
                    Image.open(path_icon+r"expandir.png").resize((30, 30)))
        self.Captura_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"captura.png").resize((20, 20)))
        self.Captura1_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"captura.png").resize((30, 30)))
        self.Reducir_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"reduce.png").resize((30, 30)))
        self.CopyALL_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"copiarALL.png").resize((20, 20)))
        self.CopyALL1_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"copiarALL.png").resize((30, 30)))
        self.risk_impacr_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"risk_impact.png").resize((20, 20)))

## --- ADJUTAR EL TEXT DE LOS LABEL -------------------------- ##
    def label_resize(self, event):
        event.widget['wraplength'] = event.width

## --- ACTIVAR MODO SOLO LECTURA ----------------------------- ##
    def widgets_SoloLectura(self, event):
        if(20==event.state and event.keysym=='c' or event.keysym=='Down' or event.keysym=='Up' or 20==event.state and event.keysym=='f' or 20==event.state and event.keysym=='a'):
            return
        else:
            return "break"

## --- ACTIVAR WIDGET ---------------------------------------- ##
    def _act_focus_ent(self, event):
        self.txtWidget = event.widget
        #self.txtWidget.select_range(0,tk.END)
        self.txtWidget.focus_set()
        self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
        self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
        self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
        self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
        self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        return 'break'

    def activar_Focus(self, event):
        global txtWidget
        global txtWidget_focus
        global PST_DESV
        txtWidget = event.widget
        if txtWidget == self.DESVfr1_entModulo:
            txtWidget.focus()
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr2_srcComprobacion:
            # srcCom = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr2_srcBackup:
            # srcBac = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == self.DESVfr3_srcEditar:
            # srcEdi = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr3_srcRefrescar:
            # srcRes = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == self.DESVfr3_srcEvidencia:
            # srcEvi = txtWidget
            txtWidget.focus()
            txtWidget_focus = True

    def _activar_Focus(self, event):
        global list_motion
        list_motion = event.widget
        list_motion.focus()
    
    def disabled_copy(self, txt_select):
        if txt_select:
            app.menu_Contextual.entryconfig('  Copiar', state='normal')
        else:
            app.menu_Contextual.entryconfig('  Copiar', state='disabled')

## ------ VENTANAS TOP EXPANDIR ------------------------------ ##
    def expandir(self, event, var): #TODO comprobando expandir

        global expandir
        global sis_oper
        global asigne_Cliente
        global varNum
        global text_aExpandir
        global value
        global PST_DESV
        index = PST_DESV.DESVfr1_listbox.curselection()
        VALOR_ACTUAL_LIST = PST_DESV.DESVfr1_listbox.get(index[0])
        value = VALOR_ACTUAL_LIST
        self.widget_Expan = event
        tittleExpand = var
        
        self.widget_Expan.focus()
        text_aExpandir = self.widget_Expan.get('1.0', tk.END)
        if tittleExpand == "COMPROBACION":
            varNum= 1
        elif tittleExpand == "BACKUP":
            varNum= 2
        elif tittleExpand == "EDITAR":
            varNum= 3            
        elif tittleExpand == "REFRESCAR":
            varNum= 4
        elif tittleExpand == "EVIDENCIA":        
            varNum= 5
        
        ## --------- LLAMADA A LA VENTANA EXPANDIR
        expandir = Expandir(self, text_aExpandir, self.widget_Expan, asigne_Cliente,tittleExpand, sis_oper, self._btnDir, self._btnAuth, self._btnSer, self._btnAcc, self._btnCmd, self._btnIdr, varNum)         
        ## ---------------------------------------
        
        if tittleExpand == "REFRESCAR":
            expandir.EXP_btnCopyALL.config(state="normal")            
        elif tittleExpand == "EVIDENCIA":        
            varNum= 5
            expandir.EXP_btnScreamEvidencia.config(state="normal")
            expandir.EXP_btnCopyALL.config(state="normal")  

## --- MENU CONTEXTUAL --- ##    
    def _menu_clickDerecho(self):   
        self.menu_Contextual = tk.Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=lambda e=self.DESVfr1_entModulo:self._buscar(e),
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=self.copiar_texto_seleccionado,
            state='disabled',
        )

        self.menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=lambda e=self.DESVfr1_entModulo:self.pegar_texto_seleccionado(e),
        )
        
        self.menu_Contextual.add_separator(background=bg_menu)
        
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=lambda : self.seleccionar_todo(event=None),
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=lambda e=None:self._clear_busqueda(e),
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=app.cerrar_vtn_desviacion
        )
    
    def _display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.scrEvent = event.widget
        self.scrEvent.focus()
        if str(self.scrEvent) == str(self.DESVfr1_entModulo):
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='normal')            
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            if len(self.DESVfr1_entModulo.get()) > 0:
                self.menu_Contextual.entryconfig('  Limpiar', state='normal')
            else:
                self.menu_Contextual.entryconfig('  Limpiar', state='disabled')
        else:
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Buscar', state='normal')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='normal')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
            self.menu_Contextual.entryconfig('  Limpiar', state='disabled')       
            txt_select = event.widget.tag_ranges(tk.SEL)
            if txt_select:
                self.menu_Contextual.entryconfig("  Copiar", state="normal")
            else:
                self.menu_Contextual.entryconfig("  Copiar", state="disabled")

## --- FUNCIONES DEL MENU CONTEXTUAL --- ##
    def seleccionar_todo(self, event):
        if txtWidget_focus:
            txtWidget.tag_add("sel","1.0","end")
            return 'break'
    
    def _seleccionar_todo(self, event):
        scr_Event = event.widget
        scr_Event.tag_add("sel","1.0","end")
        return 'break'

    def pegar_texto_seleccionado(self, event):
        entModulo_event = event
        if entModulo_event.select_present():
            self.var_entry_bsc.set("")
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
        entModulo_event.event_generate("<<Paste>>")
    
    def copiar_texto_seleccionado(self):
        global txtWidget_focus
        global txtWidget
        if txtWidget_focus:
            seleccion = txtWidget.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(txtWidget.get(*seleccion).strip())
                txtWidget.tag_remove("sel","1.0","end")
                return 'break'
    
    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel","1.0","end")
            return 'break'
        else:
            pass
    
    def buscar(self, event):
        self.DESVfr1_entModulo.focus()
        self._buscar_Ativate_focus()
    
    def _buscar_focus(self, event):
        entry_event = event.widget
        entry_event.select_range(0,tk.END)
        entry_event.focus_set()
        return 'break'

    def _buscar_Ativate_focus(self):
        self.DESVfr1_entModulo.select_range(0,tk.END)
        self.DESVfr1_entModulo.focus_set()
        return 'break'

    def _buscar(self, event):
        self._buscar_Ativate_focus()

## ------------------------------------- ##
## --- FUNCIONES AL SELECIONAR MODULO, O BUSCAR MODULO ------- ##
    def limpiar_Widgets(self):
        #self.DESVfr1_listbox.selection_clear(0, tk.END)
        self.DESV_frame2['text'] = 'SISTEMA OPERATIVO'
        self.DESVfr2_lblModulo['text'] = 'MODULO'
        self.DESVfr2_lblDescripcion['text'] = ''
        self.DESVfr2_srcComprobacion.delete('1.0',tk.END)
        self.DESVfr2_srcBackup.delete('1.0',tk.END)
        self.DESVfr3_srcEditar.delete('1.0',tk.END)
        self.DESVfr3_srcRefrescar.delete('1.0',tk.END)
        self.DESVfr3_srcEvidencia.delete('1.0',tk.END)

## --- SELECIONA UN ELEMNETO DEL LIST BOX ACTUAL
    def seleccionar_Modulo(self, event):
        global value
        list_event = event.widget
        index = list_event.curselection()
        value = list_event.get(index[0])
        self.cargar_elemt_selected(value)

## --- CARGA ELEMENTO SELECIONADO
    def cargar_elemt_selected(self, value_selecionado):#TODO CARGAR MODULO
        data = []
        with open(path_modulo.format(asigne_Cliente)) as g:
            data = json.load(g)
            for md in data:
                if value_selecionado in md['modulo']:
                    self.limpiar_Widgets()
                    self._asignarValor_aWidgets(md)
                    self.mostrar_buttons_modulo(value_selecionado)

    def _cargar_elemt_selected(self, value_selecionado):#TODO CARGAR MODULO
        data = []
        with open(path_modulo.format(asigne_Cliente)) as g:
            data = json.load(g)
            for md in data:
                if value_selecionado in md['modulo']:
                    self.limpiar_Widgets()
                    self.asignarValor_aWidgets(md)
            self.mostrar_buttons_modulo(value_selecionado)

#  --- ASIGNACION DE VALORES A WIDGETS SRC, AL CAMBIAR DE PESTAÑA
#  --- Y al buscar mas de un modulo en el mismo cliente
    def asignarValor_aWidgets(self, md):
        global sis_oper
        global PST_DESV
        global sisO
        global lblMd
        global lblDs
        global com
        global bak
        global edi
        global res
        global evd
        sisO = (PST_DESV.DESV_frame2)
        lblMd = (PST_DESV.DESVfr2_lblModulo)
        lblDs = (PST_DESV.DESVfr2_lblDescripcion)
        com = (PST_DESV.DESVfr2_srcComprobacion)
        bak = (PST_DESV.DESVfr2_srcBackup)
        edi = (PST_DESV.DESVfr3_srcEditar)
        res = (PST_DESV.DESVfr3_srcRefrescar)
        evd = (PST_DESV.DESVfr3_srcEvidencia)        
        if md['SO'] is not None:
            sis_oper = md['SO']
            sisO['text'] = md['SO']
        if md['modulo'] is not None:
            lblMd['text'] = md['modulo']
        
        if md['descripcion'] is not None:
            lblDs['text'] = md['descripcion']

        if md['comprobacion'] is not None:
            com.insert(tk.END,md['comprobacion'])
            PST_DESV.DESV_btn1Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn1Expandir.config(state='disabled')

        if md['copia'] is not None:
            bak.insert(tk.END,md['copia'])
            PST_DESV.DESV_btn2Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn2Expandir.config(state='disabled')

        if md['editar'] is not None:
            edi.insert(tk.END,md['editar'])
            PST_DESV.DESV_btn3Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn3Expandir.config(state='disabled')

        if md['refrescar'] is not None:
            res.insert(tk.END,md['refrescar'])
            PST_DESV.DESV_btn4Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn4Expandir.config(state='disabled')

        if md['evidencia'] is not None:
            evd.insert(tk.END,md['evidencia'])
            PST_DESV.DESV_btn5Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn5Expandir.config(state='disabled')
        
        PST_DESV.colour_line_com()
        PST_DESV.colour_line_bak()
        PST_DESV.colour_line_edi()
        PST_DESV.colour_line_ref()
        PST_DESV.colour_line_evi()

# --- ASIGANACION DE VALORES A WIDGETS SRC
    def _asignarValor_aWidgets(self, md):
        global sis_oper
        if md['SO'] is not None:
            sis_oper = md['SO']
            self.DESV_frame2['text'] = md['SO']
        
        if md['modulo'] is not None:
            self.DESVfr2_lblModulo['text'] = md['modulo']
        
        if md['descripcion'] is not None:
            self.DESVfr2_lblDescripcion['text'] = md['descripcion']

        if md['comprobacion'] is not None:
            self.DESVfr2_srcComprobacion.insert(tk.END,md['comprobacion'])
            self.DESV_btn1Expandir.config(state='normal')
        else:
            self.DESV_btn1Expandir.config(state='disabled')

        if md['copia'] is not None:
            self.DESVfr2_srcBackup.insert(tk.END,md['copia'])
            self.DESV_btn2Expandir.config(state='normal')
        else:
            self.DESV_btn2Expandir.config(state='disabled')

        if md['editar'] is not None:
            self.DESVfr3_srcEditar.insert(tk.END,md['editar'])
            self.DESV_btn3Expandir.config(state='normal')
        else:
            self.DESV_btn3Expandir.config(state='disabled')

        if md['refrescar'] is not None:
            self.DESV_btn4Expandir.config(state='normal')
            self.DESVfr3_srcRefrescar.insert(tk.END,md['refrescar'])
        else:
            self.DESV_btn4Expandir.config(state='disabled')

        if md['evidencia'] is not None:
            self.DESVfr3_srcEvidencia.insert(tk.END,md['evidencia'])
            self.DESV_btn5Expandir.config(state='normal')
        else:
            self.DESV_btn5Expandir.config(state='disabled')
        
        self.colour_line_com()
        self.colour_line_bak()
        self.colour_line_edi()
        self.colour_line_ref()
        self.colour_line_evi()
    
    def mostrar_buttons_modulo(self, modulo_selecionado): #TODO añadir demas botones
        global PST_DESV
# --- DIRECTORY ---------------------------------
        if str(modulo_selecionado) == "Protecting Resources-mixed/Ensure sticky bit is set on all world-writable directories" or str(modulo_selecionado) == "Protecting Resources-OSRs/CRON Command WW Permissions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /TMP Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /VAR Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /OPT Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /ETC Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /USR Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/CRON Command Group Permissions":
            self._btnDir = True
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnDirectory.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- AUTHORIZED
        elif str(modulo_selecionado) == "Password Requirements/Private Key File Restriction" or str(modulo_selecionado) == "Identify and Authenticate Users/Public Key Authentication" or str(modulo_selecionado) == "AV.1.1.6 Password Requirements" or str(modulo_selecionado) == "Identify and Authenticate Users/Public Key Label" or str(modulo_selecionado) == "AV.1.1.7 Password Requirements":
            self._btnDir = False
            self._btnAuth = True
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid(row=2, column=1, padx=5, pady=5, sticky='ne')    
# --- SERVICE
        elif str(modulo_selecionado) == "Network Settings/Ensure LDAP Server is not enabled" or str(modulo_selecionado) == "Network Settings/NFS root restrictions" or str(modulo_selecionado) == "E.1.5.22.3 Network Settings" or str(modulo_selecionado) == "Password Requirements/SSH PermitRootLogin Restriction" or str(modulo_selecionado) == "Network Settings/Prohibited Processes" or str(modulo_selecionado) == "Identify and Authenticate Users/PermitRootLogin Restriction" or str(modulo_selecionado) == "Network Settings/Disable NFS server":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = True
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnService.grid(row=2, column=1, padx=5, pady=5, sticky='ne')    
# --- ACCOUNT
        elif str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow" or str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow - Linux" or str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow - Aix" or str(modulo_selecionado) == "Password Requirements/Password MAX Age" or str(modulo_selecionado) == "AD.1.1.1.2 Password Requirements":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = True
            self._btnCmd = False
            self._btnIdr = False

            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnAccount.grid(row=2, column=1, padx=5, pady=5, sticky='ne')  
            PST_DESV.DESV_btnRecortar.grid(row=2, column=2, padx=5, pady=5, sticky='ne')  
# --- COMMAND
        elif str(modulo_selecionado) == "protecting Resources-OSRs/SUDO Command WW Permissions":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = True
            self._btnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnCommand.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- ID RSA
        elif str(modulo_selecionado) == "Password Requirements/NULL Passphrase" or str(modulo_selecionado) == "Password Requirements/Private Key Passphrase":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = True
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- MINAGE
        elif str(modulo_selecionado) == "Password Requirements/Password MIN Age Shadow":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = True
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid(row=2, column=2, padx=5, pady=5, sticky='ne')  
# --- DISABLED ALL
        else:
            self._disabled_buttons() 
    
    def mostrar_buttons_clave(self, clave_Buscado):
        global PST_DESV
# --- DIRECTORY ---------------------------------
        if clave_Buscado == "STICKY" or clave_Buscado =="OSRsCRON" or clave_Buscado == "OSRTMP" or clave_Buscado == "OSRCRON" or clave_Buscado == "OSRVAR" or clave_Buscado == "OSROPT" or clave_Buscado == "OSRETC" or clave_Buscado == "OSRUSR":
            self._btnDir = True
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget() 
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnDirectory.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- COMMAND
        elif clave_Buscado == "COMMAND":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = True
            self._btnIdr = False
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnCommand.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- ID RSA
        elif clave_Buscado == "IDRSA" or clave_Buscado == "NOT PASSPHRASE":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = True
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- SERVICE
        elif clave_Buscado == "PERMITROOTLOGIN" or clave_Buscado == "LDAP" or clave_Buscado == "PROCESSES" or clave_Buscado == "NFS":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = True
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnService.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
# --- AUTHORIZED
        elif clave_Buscado == "AUTHORIZED_KEY" or clave_Buscado == "PUBLICKEY" or clave_Buscado == "LABEL":
            self._btnDir = False
            self._btnAuth = True
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid(row=2, column=1, padx=5, pady=5, sticky='ne')    
# --- MAXAGE
        elif clave_Buscado == "MAXAGE":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = True
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnAccount.grid(row=2, column=1, padx=5, pady=5, sticky='ne')  
            PST_DESV.DESV_btnRecortar.grid(row=2, column=2, padx=5, pady=5, sticky='ne')
# --- MINAGE
        elif clave_Buscado == "MINAGE":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = True
            self._btnCmd = False
            self._btnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget() 
            self.DESV_btnRecortar.grid(row=2, column=2, padx=5, pady=5, sticky='ne')  
# --- DISABLED ALL
        else:
            self._disabled_buttons()   
    
    def solve(self, moduloBuscado):
        words = moduloBuscado.split()
        if len(words) <= 1:
            full_moduloBuscado = [w.capitalize() if '/' not in w and w[1:-1].upper() not in w else w[0].upper()+w[1:] for w in words]
        elif len(words) > 1:
            full_moduloBuscado = words
        return ' '.join(full_moduloBuscado)

    def buscar_Modulos(self, event=None):
        global value
        global no_exist

        dict_clave_modulo = {} 
        valor_aBuscar = event
        clave_Buscado = [n for n in listClave if valor_aBuscar.upper().strip() in n]
        modulo_Buscado = self.solve(valor_aBuscar) 
        modulo_Buscado = [n for n in listModulo if modulo_Buscado.strip().replace("\\","/") in n]
        
        self.DESVfr1_btnBuscar.grid_forget()
        self.DESVfr1_btnLimpiar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')        
## --- LIMPIAR ------------------------------------- ##
        self.limpiar_Widgets()
        self.enabled_Widgets()
## --------- OBTENER MODULO POR CLAVE O MODULO -------------- ## //TODO "definir si buscar por clave o modulo"
##TODO --- SI NO EXISTE, MODULO O CLAVE
        print("clave :: ", len(clave_Buscado))
        print("modulo :: ", len(modulo_Buscado))
        if len(clave_Buscado) == 0 and len(modulo_Buscado) == 0:
            print("1")
            self.DESVfr1_listbox.select_clear(tk.ANCHOR)
            self.DESVfr1_entModulo.focus()
            self._disabled_buttons()
            self.disabled_btn_expandir()
            self.DESVfr1_listbox.selection_clear(0, tk.END)
            lis_md_enct = []
            lis_clv_enct = []
            MsgBox = mb.askyesno("ERROR","El modulo no existe en este cliente.\n¿ Deseas buscar en otro cliente ?")
            if MsgBox:
                no_exist = True
                dict_clave_modulo = {}
                infile_afb = path_modulo.format("AFB")
                infile_asisa = path_modulo.format("ASISA")
                infile_cesce = path_modulo.format("CESCE")
                infile_ctti = path_modulo.format("CTTI")
                infile_enel = path_modulo.format("ENEL")
                infile_eurofred = path_modulo.format("EUROFRED")
                infile_ft = path_modulo.format("FT")
                infile_infra = path_modulo.format("INFRA")
                infile_lbk = path_modulo.format("LBK")
                infile_planeta = path_modulo.format("PLANETA")
                infile_servihabitat = path_modulo.format("SERVIHABITAT")

## --- ABRIR TODOS LOS JSON DE LOS CLIENTES
                with open(infile_afb, 'r') as infileAFB, open(infile_asisa, 'r') as infileASISA, open(infile_cesce, 'r') as infileCESCE, open(infile_ctti, 'r') as infileCTTI, open(infile_enel, 'r') as infileENEL, open(infile_eurofred, 'r') as infileEUROFRED, open(infile_ft, 'r') as tk.infitk.LEFT,  open(infile_infra, 'r') as infileINFRA, open(infile_lbk, 'r') as infileLBK, open(infile_planeta, 'r') as infilePLANETA, open(infile_servihabitat, 'r') as infileSERVIHABITAT:           
                    fileAFB_data = json.load(infileAFB)
                    fileASISA_data = json.load(infileASISA)
                    fileCESCE_data = json.load(infileCESCE)
                    fileCTTI_data = json.load(infileCTTI)
                    fileENEL_data = json.load(infileENEL)
                    fileEUROFRED_data = json.load(infileEUROFRED)
                    tk.fitk.LEFT_data = json.load(tk.infitk.LEFT)
                    fileINFRA_data = json.load(infileINFRA)
                    fileLBK_data = json.load(infileLBK)
                    filePLANETA_data = json.load(infilePLANETA)
                    fileSERVIHABITAT_data = json.load(infileSERVIHABITAT)
                    
                    ## OBTENER EL MODULO A BUSCAR
                    md_a_buscar = self.DESVfr1_entModulo.get()
                    md_a_buscar = self.solve(md_a_buscar)
## RECORRER EN TODOS LOS MODULOS DE CADA CLIENTE Y AÑADIRLO A UNA LISTA
## ---CTTI
                    for ln_ctti in fileCTTI_data:
                        lis_md_enct.append(ln_ctti['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_ctti, CUST='CTTI')
## ---ASISA
                    for ln_asisa in fileASISA_data:
                        lis_md_enct.append(ln_asisa['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_asisa, CUST='ASISA')
## ---AFB
                    for ln_afb in fileAFB_data:
                        lis_md_enct.append(ln_afb['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_afb, CUST='AFB')
## ---CESCE
                    for ln_cesce in fileCESCE_data:
                        lis_md_enct.append(ln_cesce['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_cesce, CUST='CESCE')
## ---ENEL
                    for ln_enel in fileENEL_data:
                        lis_md_enct.append(ln_enel['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_enel, CUST='ENEL')
## ---EUROFRED
                    for ln_eurofred in fileEUROFRED_data:
                        lis_md_enct.append(ln_eurofred['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_eurofred, CUST='EUROFRED')
## ---FT    
                    for ln_ft in tk.fitk.LEFT_data:
                        lis_md_enct.append(ln_ft['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_ft, CUST='FT')
## ---INFRA
                    for ln_infra in fileINFRA_data:
                        lis_md_enct.append(ln_infra['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_infra, CUST='INFRA')
## ---LBK
                    for ln_lbk in fileLBK_data:
                        lis_md_enct.append(ln_lbk['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_lbk, CUST='LBK')
## ---PLANETA
                    for ln_planeta in filePLANETA_data:
                        lis_md_enct.append(ln_planeta['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_planeta, CUST='PLANETA')
## ---SERVIHABITAT
                    for ln_servihabitat in fileSERVIHABITAT_data:
                        lis_md_enct.append(ln_servihabitat['modulo'])
                        _md_Buscado = [n for n in lis_md_enct if md_a_buscar.strip().replace("\\","/") in n]
                        self._add_newList_clt(dict_clave_modulo, _md_Buscado, ln_servihabitat, CUST='SERVIHABITAT')

## SI EL MODULO EXISTE EN ALGUN CLIENTE QUE NOS MUESTRE EN UNA VENTANA
                    if len(dict_clave_modulo) == 0:
                        # --- ABRIR TODOS LOS JSON DE LOS CLIENTES
                            clv_a_buscar = self.DESVfr1_entModulo.get()
                            clv_a_buscar = clv_a_buscar.upper()
## RECORRER EN TODOS LOS MODULOS DE CADA CLIENTE Y AÑADIRLO A UNA LISTA
## ---CTTI
                            for ln_ctti in fileCTTI_data:
                                lis_clv_enct.append(ln_ctti['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_ctti, CUST='CTTI')
## ---ASISA
                            for ln_asisa in fileASISA_data:
                                lis_clv_enct.append(ln_asisa['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_asisa, CUST='ASISA')
## ---AFB
                            for ln_afb in fileAFB_data:
                                lis_clv_enct.append(ln_afb['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_afb, CUST='AFB')
## ---CESCE
                            for ln_cesce in fileCESCE_data:
                                lis_clv_enct.append(ln_cesce['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_cesce, CUST='CESCE')
## ---ENEL
                            for ln_enel in fileENEL_data:
                                lis_clv_enct.append(ln_enel['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_enel, CUST='ENEL')
## ---EUROFRED
                            for ln_eurofred in fileEUROFRED_data:
                                lis_clv_enct.append(ln_eurofred['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_eurofred, CUST='EUROFRED')## ---FT    
## ---FT
                            for ln_ft in tk.fitk.LEFT_data:
                                lis_clv_enct.append(ln_ft['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_ft, CUST='FT')
## ---INFRA
                            for ln_infra in fileINFRA_data:
                                lis_clv_enct.append(ln_infra['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_infra, CUST='INFRA')
## ---LBK
                            for ln_lbk in fileLBK_data:
                                lis_clv_enct.append(ln_lbk['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_lbk, CUST='LBK')
## ---PLANETA
                            for ln_planeta in filePLANETA_data:
                                lis_clv_enct.append(ln_planeta['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_planeta, CUST='PLANETA')
## ---SERVIHABITAT
                            for ln_servihabitat in fileSERVIHABITAT_data:
                                lis_clv_enct.append(ln_servihabitat['clave'])
                                _clv_Buscado = [n for n in lis_clv_enct if clv_a_buscar in n]
                                self._add_newList_clt_clv(dict_clave_modulo, _clv_Buscado, ln_servihabitat, CUST='SERVIHABITAT')
                            if len(dict_clave_modulo) == 0:
                                mb.showinfo("INFORMACION","No existe el modulo, en ningun cliente !!")
                            else:
                                titulo = 'LISTA DE MODULOS ENCONTRADOS, EN LOS SIGUIENTES CLIENTES x CLAVE'
                                textsimilar = TextSimilar(self, titulo, dict_clave_modulo, asigne_Cliente)
                    else:
                        titulo = 'LISTA DE MODULOS ENCONTRADOS, EN LOS SIGUIENTES CLIENTES x MODULO'
                        textsimilar = TextSimilar(self, titulo, dict_clave_modulo, asigne_Cliente)
            else:
                no_exist = False
            return 'break'
##TODO --- POR CLAVE UNICA
        elif len(clave_Buscado) == 1 and len(modulo_Buscado) == 0:
            print("2")
            data = []
            no_exist = False
            clave_Buscado = str(clave_Buscado).replace("[","").replace("]","").replace("'","")
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if clave_Buscado in md['clave']:
                        self.limpiar_Widgets()
                        #self.enabled_Widgets()
                        value = md['modulo']
                        self.asignarValor_aWidgets(md)
                        self.mostrar_buttons_clave(clave_Buscado)
                self.DESVfr1_listbox.selection_clear(0, tk.END)
                modulo_ListBox = self.DESVfr1_listbox.get(0, tk.END)
                indice = modulo_ListBox.index(value)
                self.DESVfr1_listbox.selection_set(indice)
                return 'break'
##TODO --- SI EXISTEN MAS DE UNA CLAVE
        elif len(clave_Buscado) > 1 and len(modulo_Buscado) == 0:
            print("3")
            data = []
            no_exist = False
            self.DESVfr1_listbox.selection_clear(0, tk.END)
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    for n in clave_Buscado:
                        if n in md['clave']:
                            dict_clave_modulo[md['modulo']]=md['clave'],md['SO']
                titulo = 'LISTA DE MODULOS ENCONTRADOS, SEGUN SU CRITERIO DE BUSQUEDA, en {}'.format(asigne_Cliente)
                textsimilar = TextSimilar(self, titulo, dict_clave_modulo, asigne_Cliente)
                return 'break'
##TODO --- SI ES MODULO UNICO
        elif len(modulo_Buscado) == 1 and len(clave_Buscado) == 0:
            print("4")
            data = []
            no_exist = False
            modulo_Buscado = str(modulo_Buscado).replace("[","").replace("]","").replace("'","")
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    if modulo_Buscado in md['modulo']:
                        value = md['modulo']
                        self.asignarValor_aWidgets(md)
                self.mostrar_buttons_modulo(modulo_Buscado)
                self.DESVfr1_listbox.selection_clear(0, tk.END)
                modulo_ListBox = self.DESVfr1_listbox.get(0, tk.END)
                indice = modulo_ListBox.index(value)
                self.DESVfr1_listbox.selection_set(indice)
                return 'break'
##TODO --- SI HAY MAS DE UN MODULO
        elif len(modulo_Buscado) > 1 and len(clave_Buscado) == 0:
            print("5")
            data = []
            no_exist = False
            self.DESVfr1_listbox.selection_clear(0, tk.END) 
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    for n in modulo_Buscado:
                        if n in md['modulo']:
                            dict_clave_modulo[md['modulo']]=md['clave'],md['SO']
                titulo = 'LISTA DE MODULOS ENCONTRADOS, SEGUN SU CRITERIO DE BUSQUEDA, en {}'.format(asigne_Cliente)
                textsimilar = TextSimilar(self, titulo, dict_clave_modulo, asigne_Cliente)
                return 'break'
##TODO --- SI EXISTE UN MODULO Y UNA CLAVE
        else:
            print("6")
            data = []
            no_exist = False
            self.DESVfr1_listbox.selection_clear(0, tk.END) 
            with open(path_modulo.format(asigne_Cliente)) as g:
                data = json.load(g)
                for md in data:
                    for n in modulo_Buscado:
                        if n in md['modulo']:
                            dict_clave_modulo[md['modulo']]=md['clave'],md['SO']
                    for n in clave_Buscado:
                        if n in md['clave']:
                            dict_clave_modulo[md['modulo']]=md['clave'],md['SO']
                titulo = 'LISTA DE MODULOS ENCONTRADOS, SEGUN SU CRITERIO DE BUSQUEDA, en {}'.format(asigne_Cliente)
                textsimilar = TextSimilar(self, titulo, dict_clave_modulo, asigne_Cliente)
                return 'break'

    def _add_newList_clt(self, dict_clave_modulo, _md_Buscado, ln_clt, CUST):
        for n in _md_Buscado:
            if n in ln_clt['modulo']:
                dict_clave_modulo[ln_clt['modulo']]=ln_clt['clave'],CUST
    
    def _add_newList_clt_clv(self, dict_clave_modulo, _clv_Buscado, ln_clt, CUST):
        for n in _clv_Buscado:
            if n in ln_clt['clave']:
                dict_clave_modulo[ln_clt['modulo']]=ln_clt['clave'],CUST
        
    def _clear_busqueda(self, event):
        self.var_entry_bsc.set("")
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def clear_busqueda(self, event):
        text_widget = event.widget
        entry = self.var_entry_bsc.get()
        if entry == "":
            text_widget.icursor(0)
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def clear_bsq_buttom(self, event):
        entry = self.var_entry_bsc.get()
        long_entry = len(entry)
        if long_entry <=1:
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def limpiar_busqueda(self):
        widget_event = self.DESVfr1_entModulo
        widget_event.delete(0, tk.END)
        widget_event.focus()
        widget_event.icursor(0)
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def ListDown(self, event):
        list_event = event.widget
        list_event.yview_scroll(1,"units")
        selecion = list_event.curselection()[0]+1
        modulo_selecionado = list_event.get(selecion)
        self.cargar_elemt_selected(modulo_selecionado)
    
    def ListUp(self, event):
        list_event = event.widget
        list_event.yview_scroll(-1,"units")
        selecion = list_event.curselection()[0]-1
        modulo_selecionado = list_event.get(selecion)
        self.cargar_elemt_selected(modulo_selecionado)
    
    def enabled_Widgets(self):
        self.DESVfr1_listbox.config(state="normal")
        self.DESVfr1_entModulo.config(state="normal")
        self.DESVfr1_entModulo.focus()
        self.DESVfr1_btnBuscar.config(state="normal")
        self.DESVfr2_srcComprobacion.config(state="normal")
        self.DESVfr2_srcBackup.config(state="normal")
        self.DESVfr3_srcEditar.config(state="normal")
        self.DESVfr3_srcRefrescar.config(state="normal")
        self.DESVfr3_srcEvidencia.config(state="normal")
        self.DESV_btnRiskImpact.config(state='normal')
        self.DESV_btn1Expandir.config(state='normal')
        self.DESV_btn2Expandir.config(state='normal')
        self.DESV_btn3Expandir.config(state='normal')
        self.DESV_btn4Expandir.config(state='normal')
        self.DESV_btn5Expandir.config(state='normal')
        self.DESV_btnScreamEvidencia.config(state='normal')
        self.DESV_btnCopyALL.config(state='normal')
        self.DESV_btn1CopyALL.config(state='normal')
        self.DESV_btnDirectory.config(state='normal')

    def cargar_Modulos(self, clt_modulo=None, *args):
        global asigne_Cliente
        global listModulo
        global listClave
        self.enabled_Widgets()
        if clt_modulo is not None:
            customer = clt_modulo
            self.clientesVar.set(customer)
        else:
            customer = self.clientesVar.get()
        ## --- LIMPIAR -----------------------------
        self.DESVfr1_entModulo.delete(0, tk.END)
        self.DESVfr1_listbox.delete(0,tk.END)
        self.limpiar_Widgets()
        self._disabled_buttons() 
        self.disabled_btn_expandir()

        ## ----------------------------------------- ##
        asigne_Cliente = customer       
        with open(path_modulo.format(customer)) as g:
            data = json.load(g)
            listModulo = []
            listClave = []
            for md in data:
                listModulo.append(md['modulo'])
                listClave.append(md['clave'])
        listModulo.sort()
        self.DESVfr1_listbox.insert(tk.END,*listModulo)
        self.cambiar_NamePestaña(customer)

    def colour_line_com(self):
        global PST_DESV

        indx = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx = PST_DESV.DESVfr2_srcComprobacion.search(line1, indx, nocase=1, stopindex=tk.END)
                if not indx: #or not indx1 or not indx2 or not indx3 or not indx4: 
                    break
                lastidx = '%s+%dc' % (indx, len(line1))
                PST_DESV.DESVfr2_srcComprobacion.tag_add('found1', indx, lastidx)
                indx = lastidx
                PST_DESV.DESVfr2_srcComprobacion.tag_config(
                'found1', 
                foreground='dodgerblue',
                font=_Font_Texto
                )
    
    def colour_line_bak(self):
        indx1 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx1 = PST_DESV.DESVfr2_srcBackup.search(line1, indx1, nocase=1, stopindex=tk.END)
                if not indx1: #or not indx2 or not indx3 or not indx4: 
                    break
                lastidx1 = '%s+%dc' % (indx1, len(line1))
                PST_DESV.DESVfr2_srcBackup.tag_add('found1', indx1, lastidx1)
                indx1 = lastidx1
                PST_DESV.DESVfr2_srcBackup.tag_config(
                'found1', 
                foreground='dodgerblue',
                font=_Font_Texto
                )
    
    def colour_line_ref(self):
        indx3 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx3 = PST_DESV.DESVfr3_srcRefrescar.search(line1, indx3, nocase=1, stopindex=tk.END)
                if not indx3: #or not indx4: 
                    break
                lastidx3 = '%s+%dc' % (indx3, len(line1))
                PST_DESV.DESVfr3_srcRefrescar.tag_add('found1', indx3, lastidx3)
                indx3 = lastidx3
                PST_DESV.DESVfr3_srcRefrescar.tag_config(
                'found1', 
                foreground='dodgerblue',
                font=_Font_Texto
                )

    def colour_line_edi(self):
        indx2 = '1.0'
        # indx4 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx2 = PST_DESV.DESVfr3_srcEditar.search(line1, indx2, nocase=1, stopindex=tk.END)
                if not indx2: 
                    break
                lastidx2 = '%s+%dc' % (indx2, len(line1))
                PST_DESV.DESVfr3_srcEditar.tag_add('found1', indx2, lastidx2)
                indx2 = lastidx2
                PST_DESV.DESVfr3_srcEditar.tag_config(
                'found1', 
                foreground='dodgerblue',
                font=_Font_Texto
                )

    def colour_line_evi(self):
        indx4 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx4 = PST_DESV.DESVfr3_srcEvidencia.search(line1, indx4, nocase=1, stopindex=tk.END)
                if not indx4: 
                    break
                lastidx4 = '%s+%dc' % (indx4, len(line1))
                PST_DESV.DESVfr3_srcEvidencia.tag_add('found1', indx4, lastidx4)
                indx4 = lastidx4
                PST_DESV.DESVfr3_srcEvidencia.tag_config(
                'found1', 
                foreground='dodgerblue',
                font=_Font_Texto
                )

    def _disabled_buttons(self):
        global PST_DESV
        self._btnDir = False
        self._btnAuth = False
        self._btnSer = False
        self._btnAcc = False
        self._btnCmd = False
        self._btnIdr = False
        PST_DESV.DESV_btnDirectory.grid_forget()
        PST_DESV.DESV_btnAuthorized.grid_forget()
        PST_DESV.DESV_btnService.grid_forget()
        PST_DESV.DESV_btnAccount.grid_forget()
        PST_DESV.DESV_btnCommand.grid_forget()
        PST_DESV.DESV_btnIdrsa.grid_forget()
        PST_DESV.DESV_btnRecortar.grid_forget()

    def disabled_btn_expandir(self):
        PST_DESV.DESV_btn1Expandir.config(state='disabled')
        PST_DESV.DESV_btn2Expandir.config(state='disabled')
        PST_DESV.DESV_btn3Expandir.config(state='disabled')
        PST_DESV.DESV_btn4Expandir.config(state='disabled')
        PST_DESV.DESV_btn5Expandir.config(state='disabled')

    def _cargar_Modulos(self):
        idx = app.ClientVar.get()
        itm = list_client[idx]
        self.cargar_Modulos(clt_modulo=itm)
    
    def ScreamEvidencia(self):
        app.root.withdraw()
        os.popen('gtk-launch capture.desktop')
        time.sleep(2)
        app.root.deiconify()

    def Risk_Impact(self):
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        excel_risk_impact = mypath+"Compliance/file/RISK_IMPACT.ods"
        subprocess.call([opener, excel_risk_impact])

    def RecortarMinMax(self):
        recortar = mypath+"Compliance/recortar.sh"
        os.popen("gnome-terminal -e "+recortar)

    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel","1.0","end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel","1.0","end")
    
    def widgets_DESVIACION(self):
        from Extraciones import MyEntry
# --- DEFINIMOS LOS LABEL FRAMEs, QUE CONTENDRAN LOS WIDGETS --------------------------#
        self.DESV_frame1=ttk.LabelFrame(
            self, 
            text="CLIENTE / MODULO", 
            border=1, 
            relief='sunken'
        )
        self.DESV_frame1.grid_propagate(False)
        self.DESV_frame1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        
        self.DESV_frame2=ttk.LabelFrame(
            self, 
            text="SISTEMA OPERATIVO", 
            border=1, 
            relief='sunken'
        )
        self.DESV_frame2.grid_propagate(False)
        self.DESV_frame2.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')
        
        self.DESV_frame3=ttk.LabelFrame(
            self, 
            text="EDITAR / EVIDENCIA", 
            border=1, 
            relief='sunken'
        )
        self.DESV_frame3.grid_propagate(False)
        self.DESV_frame3.grid(column=2, row=0, padx=10, pady=10, sticky='nsew')
# -----------------------------------------------------------------------------#
        self.DESV_frame1.columnconfigure(0, weight=1)
        self.DESV_frame2.columnconfigure(0, weight=1)
        self.DESV_frame3.columnconfigure(0, weight=1)
        
        self.DESV_frame1.rowconfigure(2, weight=1)
        self.DESV_frame2.rowconfigure(3, weight=1)
        self.DESV_frame2.rowconfigure(5, weight=1)
        
        self.DESV_frame3.rowconfigure(1, weight=1)
        self.DESV_frame3.rowconfigure(3, weight=1)
        self.DESV_frame3.rowconfigure(5, weight=1)
# --- Variable del OptionMenu, lista de clientes ------------------------------#
        self.clientesVar = tk.StringVar(self)
        self.clientesVar.set('CLIENTES')
        # -----------------------------------------------------------------------------#
        ## ======================== FRAME 1 ========================================= ##
        # ---------------- OptionMenu, lista de clientes ---------------------------- ##
        self.DESVfr1_optMn = tk.OptionMenu(
            self.DESV_frame1, 
            self.clientesVar, 
            *list_client, 
            command=self.cargar_Modulos,
        )
        self.DESVfr1_optMn.config(
            background = bg_menu,
            foreground = fg_menu,
            font=_Font_Titulo_bold,
            activebackground = acfg_menu,
            activeforeground = bg_menu,
            relief="groove",
            borderwidth=2,
            width=20
        )
        self.DESVfr1_optMn["menu"].config(
            background=bg_menu,
            activebackground=acfg_menu,
            activeforeground=bg_menu,
            foreground=fg_menu,
            font=_Font_Texto,
        )
        self.DESVfr1_optMn.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=2)
# -----------------------------------------------------------------------------#
##TODO --- ENTRY DE BUSQUEDA
        self.var_entry_bsc = tk.StringVar(self)
        
        self.DESVfr1_entModulo = MyEntry(
            self.DESV_frame1,
            textvariable=self.var_entry_bsc,
        )
        
        self.DESVfr1_entModulo.configure(
            state='disabled',
            font=_Font_Texto,
            borderwidth=0,
            highlightcolor=active_color,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
            highlightthickness=2,
        )
        self.DESVfr1_entModulo.grid(row=1, column=0, pady=5, padx=(5,0), sticky='nsew')
        
##TODO --- BOTON BUSCAR DESVIACION
        self.DESVfr1_btnBuscar = ttk.Button(
            self.DESV_frame1, 
            image=self.BuscarModulo_icon,
            state='disabled',
            command=lambda: self.buscar_Modulos(self.DESVfr1_entModulo.get()),
        )
        self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
##TODO --- BOTON LIMPIAR BUSQUEDA
        self.DESVfr1_btnLimpiar = ttk.Button(
            self.DESV_frame1, 
            image=self.LimpiarModulo_icon,
            command=self.limpiar_busqueda,
        )
        # -----------------------------------------------------------------------------#
        self.DESVlist_yScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.VERTICAL)
        self.DESVlist_xScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.HORIZONTAL)
        self.DESVfr1_listbox = tk.Listbox(
            self.DESV_frame1,
            state='disabled',
            xscrollcommand=self.DESVlist_xScroll.set, 
            yscrollcommand=self.DESVlist_yScroll.set,
            font=_Font_Texto,
            foreground=color_fg_list,
            selectbackground=sel_bg_txt,
            selectforeground=sel_fg_txt,
            exportselection=False,
            highlightthickness=2,
            highlightcolor = active_color,
        )
        self.DESVfr1_listbox.grid(row=2, column=0, pady=(5,12), padx=(5,12), sticky='nsew', columnspan=2)
        self.DESVlist_yScroll.grid(row=2, column=0, pady=(5,15), sticky='nse', columnspan=2)
        self.DESVlist_xScroll.grid(row=2, column=0, padx=5, sticky='sew', columnspan=2)
        self.DESVlist_xScroll['command'] = self.DESVfr1_listbox.xview
        self.DESVlist_yScroll['command'] = self.DESVfr1_listbox.yview

## ======================== FRAME 2 ========================================= ##
## --- MODULO ----------------------------------------------------------------------------------------------------

        self.DESVfr2_lblModulo = ttk.Label(
            self.DESV_frame2,
            text='MODULO', 
            #width=10,
        )
        self.DESVfr2_lblModulo.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=5)
        ## --- Descripcion
        self.DESVfr2_lblDescripcion = ttk.Label(
            self.DESV_frame2,
            text='',
            font=_Font_Texto,
            width=10, 
            foreground='gray55'
        ) 
        self.DESVfr2_lblDescripcion.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=5)

## --- Comprobacion---------------------------------------------------------------------------------------------------------

        self.DESVfr2_lblComprobacion = ttk.Label(
            self.DESV_frame2, 
            text='COMPROBACIÓN',
            font=_Font_Titulo_bold
        ) 
        self.DESVfr2_lblComprobacion.grid(row=2, column=0, padx=5, pady=5, sticky='w' )
        
        self.DESV_btnDirectory = ttk.Button(
            self.DESV_frame2,
            text='Permissions',
            compound=tk.LEFT,
            image=self.Expandir_icon,
            state='disabled',
            command=self.abrir_DIRECTORY,
        )
        self.DESV_btnService = ttk.Button(
            self.DESV_frame2,
            text='Service',
            compound=tk.LEFT,
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_SERVICE,
        )
        self.DESV_btnAuthorized = ttk.Button(
            self.DESV_frame2,
            text='Authorized',
            compound=tk.LEFT,
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_AUTHORIZED,
        )
        self.DESV_btnRecortar = ttk.Button(
            self.DESV_frame2,
            text='Recortar',
            image=self.recortar_icon,
            state='enabled',
            command=self.RecortarMinMax,
        )
        self.DESV_btnAccount = ttk.Button(
            self.DESV_frame2,
            text='Account',
            compound=tk.LEFT,
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_ACCOUNT,
        )

        self.DESV_btnCommand = ttk.Button(
            self.DESV_frame2,
            text='Command',
            compound=tk.LEFT,
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_COMMAND,
        )

        self.DESV_btnIdrsa = ttk.Button(
            self.DESV_frame2,
            text='Id_Rsa',
            compound=tk.LEFT,
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_IDRSA,
        )
        
        self.DESVfr2_srcComprobacion = st.ScrolledText(self.DESV_frame2)
        self.DESVfr2_srcComprobacion.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=active_color,
            borderwidth=0, 
            highlightthickness=2,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
            state='disabled',
        )
        self.DESVfr2_srcComprobacion.grid(row=3, column=0, padx=5, pady=5, sticky='new', columnspan=5)
        self.varComprobacion = "COMPROBACION"
        
        self.DESV_btnRiskImpact = ttk.Button(
            self.DESV_frame2,
            image=self.risk_impacr_icon,
            state='disabled',
            command=self.Risk_Impact,
        )
        self.DESV_btnRiskImpact.grid(row=2, column=3, padx=(5,10), pady=5, sticky='ne')

        self.DESV_btn1Expandir = ttk.Button(
            self.DESV_frame2,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr2_srcComprobacion:self.expandir(x, self.varComprobacion),
        )
        self.DESV_btn1Expandir.grid(row=2, column=4, padx=(5,20), pady=5, sticky='ne')


## --- BACKUP ----------------------------------------------------------------------------------------------------
        self.DESVfr2_lblBackup = ttk.Label(
            self.DESV_frame2, 
            text='BACKUP', 
        ) 
        self.DESVfr2_lblBackup.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        
        self.DESVfr2_srcBackup = st.ScrolledText(
            self.DESV_frame2,
        )
        self.DESVfr2_srcBackup.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=active_color,
            borderwidth=0, 
            highlightthickness=2,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
            state='disabled',
        )
        self.DESVfr2_srcBackup.grid(row=5, column=0, padx=5, pady=5, sticky='new', columnspan=5)
        
        self.varBackup = "BACKUP"
        self.DESV_btn2Expandir = ttk.Button(
            self.DESV_frame2,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr2_srcBackup:self.expandir(x, self.varBackup),
        )
        self.DESV_btn2Expandir.grid(row=4, column=4, padx=(5,20), pady=5, sticky='nse', columnspan=3)
## ======================== FRAME 3 ========================================= ##
## --- EDITAR
        self.DESVfr3_lblEditar = ttk.Label(
            self.DESV_frame3, 
            text='EDITAR ✍'
        )
        self.DESVfr3_lblEditar.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.DESVfr3_srcEditar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcEditar.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=active_color,
            borderwidth=0, 
            highlightthickness=2,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
            state='disabled',
        )
        self.DESVfr3_srcEditar.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        
        self.varEditar = "EDITAR"
        self.DESV_btn3Expandir = ttk.Button(
            self.DESV_frame3,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr3_srcEditar:self.expandir(x, self.varEditar),
        )
        self.DESV_btn3Expandir.grid(row=0, column=1, padx=(5,20), pady=5, sticky='nse', columnspan=4)
        ## --- REFEESCAR
        self.DESVfr3_lblRefrescar = ttk.Label(
            self.DESV_frame3, 
            text='REFRESCAR'
        )
        self.DESVfr3_lblRefrescar.grid(row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.DESVfr3_srcRefrescar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcRefrescar.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=active_color,
            borderwidth=0, 
            highlightthickness=2,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
            state='disabled',
        )
        self.DESVfr3_srcRefrescar.grid(row=3, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        
        self.DESV_btn1CopyALL = ttk.Button(
            self.DESV_frame3,
            image=self.CopyALL_icon,
            state='disabled',
            command= lambda e=self.DESVfr3_srcRefrescar:self.copiarALL(e),
        )
        self.DESV_btn1CopyALL.grid(row=2, column=2, padx=5, pady=5, sticky='e')
        
        self.varRefrescar = "REFRESCAR"
        self.DESV_btn4Expandir = ttk.Button(
            self.DESV_frame3,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr3_srcRefrescar:self.expandir(x, self.varRefrescar),
        )
        self.DESV_btn4Expandir.grid(row=2, column=3, padx=(5,20), pady=5, sticky='e')
        
        ## --- EVIDENCIA
        self.DESVfr3_lblEvidencia = ttk.Label(
            self.DESV_frame3, 
            text='EVIDENCIA'
        )
        self.DESVfr3_lblEvidencia.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.DESVfr3_srcEvidencia = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcEvidencia.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=active_color,
            borderwidth=0, 
            highlightthickness=2,
            insertbackground=active_color,
            selectbackground=sel_bg_txt,
            state='disabled',
        )
        self.DESVfr3_srcEvidencia.grid(row=5, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        self.DESV_btnCopyALL = ttk.Button(
            self.DESV_frame3,
            image=self.CopyALL_icon,
            state='disabled',
            command=lambda e=self.DESVfr3_srcEvidencia:self.copiarALL(e),
        )
        self.DESV_btnCopyALL.grid(row=4, column=1, padx=(20,5), pady=5, sticky='ne')
        self.DESV_btnScreamEvidencia = ttk.Button(
            self.DESV_frame3,
            image=self.Captura_icon,
            state='disabled',
            command=self.ScreamEvidencia,
        )
        self.DESV_btnScreamEvidencia.grid(row=4, column=2, padx=5, pady=5, sticky='ne')
        
        self.varEvidencia = "EVIDENCIA"
        self.DESV_btn5Expandir = ttk.Button(
            self.DESV_frame3,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr3_srcEvidencia:self.expandir(x, self.varEvidencia),
        )
        self.DESV_btn5Expandir.grid(row=4, column=3, padx=(5,20), pady=5, sticky='ne')

## --- FUNCIONES PARA ABRIR VENTANAS EMERGENTE --------------- #    
    def _QuitarSeleccion_(self):
        global list_motion
        global txtWidget
        PST_DESV.DESV_frame2['text'] = 'SISTEMA OPERATIVO'
        PST_DESV.DESVfr2_lblDescripcion['text'] = ''
        PST_DESV.DESVfr2_srcComprobacion.delete('1.0',tk.END)
        PST_DESV.DESVfr2_srcBackup.delete('1.0',tk.END)
        PST_DESV.DESVfr3_srcEditar.delete('1.0',tk.END)
        PST_DESV.DESVfr3_srcRefrescar.delete('1.0',tk.END)
        PST_DESV.DESVfr3_srcEvidencia.delete('1.0',tk.END)
        PST_DESV.DESVfr2_lblModulo['text'] = 'MODULO'

        if list_motion:
            list_motion.selection_clear(0,tk.END)
            self.limpiar_Widgets()
    
    def abrir_DIRECTORY(self):
        from Ventanas import Ventana
        global asigne_Cliente
        global directory
        name_vtn = "PERMISSIONS"
        path = "Compliance/file/directory.json"
        directory = Ventana(self,name_vtn, asigne_Cliente, app,desviacion,path)
    
    def abrir_COMMAND(self):
        from Ventanas import Ventana
        global asigne_Cliente
        global command
        name_vtn = "COMMAND"
        path = "Compliance/file/command.json"
        command = Ventana(self,name_vtn, asigne_Cliente, app,desviacion,path)
    
    def abrir_AUTHORIZED(self):
        from Ventanas import Ventana
        global asigne_Cliente
        global authorized
        name_vtn = "AUTHORIZED"
        path = "Compliance/file/authorized_keys.json"
        authorized = Ventana(self,name_vtn, asigne_Cliente, app,desviacion,path)
    
    def abrir_ACCOUNT(self):
        from Ventanas import Ventana
        global asigne_Cliente
        global account
        name_vtn = "ACCOUNT"
        path = "Compliance/file/account.json"
        account = Ventana(self,name_vtn, asigne_Cliente, app,desviacion,path)
    
    def abrir_SERVICE(self):
        from Ventanas import Ventana
        global asigne_Cliente
        global service
        name_vtn = "SERVICE"
        path = "Compliance/file/service.json"
        service = Ventana(self,name_vtn, asigne_Cliente, app,desviacion,path)
    
    def abrir_IDRSA(self):
        from Ventanas import Ventana
        global asigne_Cliente
        global idrsa
        name_vtn = "ID_RSA"
        path = "Compliance/file/idrsa.json"
        idrsa = Ventana(self,name_vtn, asigne_Cliente, app,desviacion,path)
    
    def cambiar_NamePestaña(self, customer):
        app.cuaderno.tab(idOpenTab, option=None, text='DESVIACIONES : {} '.format(customer))
        app.cuaderno.notebookContent.tab(idOpenTab, option=None, text='DESVIACIONES : {} '.format(customer))

class Aplicacion():
    
    def __init__(self):
        self.root= tk.Tk()
        self.root.title("CONTINUOUS COMPLIANCE")
        window_width,window_height=1028,768
        screen_width = self.root.winfo_screenwidth()
        screen_height= self.root.winfo_screenheight()
        position_top = int(screen_height/2 - window_height/2)
        position_right = int(screen_width/2 - window_width/2)
        self.root.geometry(f'{window_width}x{window_height}+{position_top}+{position_right}')
        self.root.configure(background=fondo_app, borderwidth=0, border=0) 
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=path_icon+r'compliance.png'))
        self.open_client()
        self.iconos()
        self.cuaderno = ScrollableNotebook(self.root,wheelscroll=False,tabmenu=True, application=self)
        self.contenedor= ttk.Frame(self.cuaderno)
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        self.cuaderno.add(self.contenedor, text='WorkSpace  ', underline=0, image=self.WorkSpace_icon, compound=tk.LEFT)
        self.cuaderno.pack(fill="both",expand=True)
        self.cuaderno.bind_all("<<NotebookTabChanged>>",lambda e:self.alCambiar_Pestaña(e))
        self.cuaderno.enable_traversal()
        self.cuaderno.notebookTab.bind("<Button-3>", self.display_menu_clickDerecho)
        self.contenedor.bind("<Button-3>", self._display_menu_clickDerecho)
        self.root.bind_all("<Control-l>", lambda x : self.ocultar())
        self.root.focus_set()
        # Fuente MENU CLICK DERECHO APP
        # ----------------------------------------------------------
        self.sizegrid = ttk.Sizegrip(
            self.cuaderno,
        )
        self.sizegrid.pack(side="right", anchor='se')

        self.estilos()
        self.menu_clickDerecho()
        self._menu_clickDerecho()
        self.widgets_APP()

    def open_client(self):
        global list_client
        list_client = []
        with open(path_config.format("clientes")) as op:
            data = json.load(op)
            for clt in data:
                list_client.append(clt)

    def iconos(self):
        self.Desviaciones_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"openDesviaciones.png").resize((80, 80)))
        self.Extracion_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"openExtraciones.png").resize((80, 80)))
        self.Automatizar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"automatizar.png").resize((80, 80)))
        self.Abrir_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"abrir.png").resize((30, 30)))
        self.Client_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"clientes.png").resize((30, 30)))
        self.Salir_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"salir.png").resize((30, 30)))
        self.SelAllBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"selall.png").resize((30, 30)))
        self.BuscarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"buscar1.png").resize((30, 30)))
        self.CopiarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"copiarBarra.png").resize((30, 30)))
        self.PegarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"pegarBarra.png").resize((30, 30)))
        self.Ayuda_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"ayuda.png").resize((30, 30)))
        self.AcercaDe_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"acercaDe.png").resize((30, 30)))
        self.WorkSpace_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"workspace.png").resize((20, 20)))
    
    def estilos(self):
        self.style = Style()
        self.style.configure('TCombobox',
            background = bg_menu,
            selectbackground = sel_bg_txt,
            selectforeground = sel_fg_txt, 
        )
        self.style.map('TCombobox',
            background=[
                ("active", bg_menu)
            ]
        )
        
        self.style.configure('TSizegrip',
            background=fondo_app,
            borderwidth=0,
            border=0
        )
        
        self.style.configure('TFrame',
            background=fondo_app,
        )
        
        self.style.configure('TLabelframe',
            background=fondo_app,
        )
        self.style.configure('TLabelframe.Label',
            background=fondo_app,
            foreground=color_titulos,
            font=_Font_Titulo_bold,
        )
        # *===============================================================================
        self.style.configure(
            'APP.TButton',
            background = "#297F87",
            foreground = "#FFF7AE",
            font=_Font_Boton,
            padding=20,
            relief='sunke',
            borderwidth=5,
        )
        self.style.map(
            'APP.TButton',
            background = [("active","#F6D167")],
            foreground = [("active","#DF2E2E")],
            padding=[("active",20),("pressed",20)],
            relief=[("active",'ridge'),("pressed",'groove')],
            borderwidth=[("active",5)],
        )
        
        self.style.configure('TButton',
            background = "#D4ECDD",
            relief='sunke',
            borderwidth=1,
            padding=6,
            font=_Font_Boton
        )
        self.style.map('TButton',
            background=[("active","#F6D167")],
            foreground=[("active","#C64756")],
            padding=[("active",6),("pressed",6)],
            relief=[("active",'ridge'),("pressed",'groove')],
            borderwidth=[("active",1)],
        )

        self.style.configure('APP.TLabel',
            background = bg_menu,
            foreground = fg_menu,
            font=(fuente_titulos, 30, font.BOLD)
        )
        
        self.style.configure('TLabel',
            background = fondo_app,
            foreground = "gray17",
            font=_Font_Titulo_bold
        )
        
        self.style.configure('TEntry',
            background = fondo_app,
            foreground = sel_fg_txt,
            border=2,
            borderwidth=2,
            highlightthickness=2,
            highlightcolor=active_color,
            selectforeground=sel_fg_txt,
            selectbackground=sel_bg_txt,
        )

## --- MENU CONTEXTUAL --- ##
## --- MENU PARA EXPANDIR -----------------------------
    def menu_clickDerecho(self):  
        self.menu_Contextual = tk.Menu(self.root, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_menu)
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=self.cerrar_vtn_desviacion
        )
    
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)

    def _menu_clickDerecho_GLS(self):
        self.text_font = font.Font(family='Courier', size=14, font=font.BOLD)
        self.menu_Contextual_GLS = tk.Menu(self.root, tearoff=0)
        self.menu_Contextual_GLS.add_command(
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu, activeforeground=bg_menu,
            font=self.text_font,
            command=lambda e=self._list_clave : self._copiar_select_GLS_clave(e)
        )

    def _display_menu_clickDerecho_GLS(self, event):
        self.menu_Contextual_GLS.tk_popup(event.x_root, event.y_root)

    @beep_error
    def _copiar_select_GLS_clave(self, event):
        widget = event
        index = widget.curselection()
        value = widget.get(index[0])
        self.root.clipboard_clear()
        self.root.clipboard_append(value)

## --- MENU PARA SRC DE LOS MODULOS -------------------
    def _menu_clickDerecho(self):
        self._menu_Contextual = tk.Menu(self.root, tearoff=0)
        self._menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background=bg_menu)
        self._menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background=bg_menu)
        self._menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background=bg_menu)
        self._menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            state='disabled'
        )
        self._menu_Contextual.add_command(
            label="  Salir", 
            compound=tk.LEFT,
            background=bg_menu, foreground=fg_menu,
            activebackground=acfg_menu,activeforeground=bg_menu,
            font=_Font_Menu,
            command=self.root.quit
        )
    
    def _display_menu_clickDerecho(self, event):
        self._menu_Contextual.tk_popup(event.x_root, event.y_root)

    def cerrar_vtn_desviacion(self):
        if idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
        else:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
            self.cuaderno.forget(idOpenTab)
            self.cuaderno.notebookContent.forget(idOpenTab)

## ----------------------- ##
    def alCambiar_Pestaña(self, event):
        global idOpenTab
        global asigne_Cliente
        global value
        global PST_DESV
        # global automatizar
        # if automatizar in globals():
        #     automatizar.btn_lis_cli = []
        #     print("LISTA AL cambiar ", automatizar.btn_lis_cli)
        idOpenTab = event.widget.index('current')
        tab = event.widget.tab(idOpenTab)['text']
        self.root.update()
        if idOpenTab != 0:
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
        elif idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
            self.cuaderno._release_callback(e=None)
        else:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
        if idOpenTab == 1 or idOpenTab == 2 or idOpenTab == 3 or idOpenTab == 4:
            self.cuaderno.rightArrow.configure(foreground=active_color)
            Thread(target=self.cuaderno._tk.LEFTSlide, daemon=True).start()
            self.cuaderno._release_callback(e=None)
            self.cuaderno.rightArrow.configure(foreground=active_color)
## ---ASIGNAMOS A UNA VARIABLE CADA CLIENTE----------------------------
        if tab == 'WorkSpace  ':
            asigne_Cliente = ""
            self.fileMenu.entryconfig('  Clientes', state='disabled')
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
        elif tab == 'DESVIACIONES : AFB ':
            asigne_Cliente = 'AFB'
            # index = PST_DESV.DESVfr1_listbox.curselection()
            # VALOR_ACTUAL_LIST = PST_DESV.DESVfr1_listbox.get(index[0])
        elif tab == 'DESVIACIONES : ASISA ':
            asigne_Cliente = 'ASISA'
            # index = PST_DESV.DESVfr1_listbox.curselection()
            # VALOR_ACTUAL_LIST = PST_DESV.DESVfr1_listbox.get(index[0])
            # value = VALOR_ACTUAL_LIST
        elif tab == 'DESVIACIONES : CESCE ':
            asigne_Cliente = 'CESCE'
            # index = PST_DESV.DESVfr1_listbox.curselection()
            # VALOR_ACTUAL_LIST = PST_DESV.DESVfr1_listbox.get(index[0])
            # value = VALOR_ACTUAL_LIST
        elif tab == 'DESVIACIONES : CTTI ':
            asigne_Cliente = 'CTTI'
        elif tab == 'DESVIACIONES : ENEL ':
            asigne_Cliente = 'ENEL'
        elif tab == 'DESVIACIONES : EUROFRED ':
            asigne_Cliente = 'EUROFRED'
        elif tab == 'DESVIACIONES : FT ':
            asigne_Cliente = 'FT'
        elif tab == 'DESVIACIONES : INFRA ':
            asigne_Cliente = 'INFRA'
        elif tab == 'DESVIACIONES : IDISO ':
            asigne_Cliente = 'IDISO'
        elif tab == 'DESVIACIONES : LBK ':
            asigne_Cliente = 'LBK'
        elif tab == 'DESVIACIONES : PLANETA ':
            asigne_Cliente = 'PLANETA'
        elif tab == 'DESVIACIONES : SERVIHABITAT ':
            asigne_Cliente = 'SERVIHABITAT'
        else:
            self.fileMenu.entryconfig('  Clientes', state='normal')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
        if 'asigne_Cliente' in globals() and len(asigne_Cliente) != 0:
            with open(path_modulo.format(asigne_Cliente)) as g:
                global listClave
                global listModulo
                data = json.load(g)
                listModulo = []
                listClave = []
                for md in data:
                    listModulo.append(md['modulo'])
                    listClave.append(md['clave'])
        if tab == 'Issues EXTRACIONES':
            self.fileMenu.entryconfig('  Clientes', state='disabled')
            self.editMenu.entryconfig('  Buscar', state='normal')
        else:
            self.editMenu.entryconfig('  Buscar', state='disabled')
        try:
            self.valor_activo_list = desviacion.DESVfr1_listbox.get(tk.ANCHOR)
        except:
            pass
        try:
            expandir.cerrar_vtn_expandir()
        except:
            pass

        #self._QuitarSeleccion()
        self._cerrar_vtn_bsc()

    def _cerrar_vtn_bsc(self):
        global extracion
        try:
            extracion._on_closing_busca_top()
        except:
            pass

    def abrir_issues(self):
        idx = self.IssuesVar.get()
        itm = list_issues[idx]
        if str(itm) == "DESVIACIONES":
            self.abrir_issuesDesviacion()
        else:
            self.abrir_issuesExtracion()

    def abrir_issuesDesviacion(self):
        global idOpenTab
        global desviacion
        #self.root.after(1, self.open_client)
        self.open_client()
        desviacion = Desviacion(self.cuaderno)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES ')
        
    def abrir_issuesExtracion(self):
        from Extraciones import Extracion

        global idpTab
        global extracion
        try:
            extracion._on_closing_busca_top()
        except:
            pass

        extracion = Extracion(self.cuaderno, app, application=self)
        self.cuaderno.add(extracion, text='Issues EXTRACIONES')
        idpTab = self.cuaderno.index('current')
    
    def abrir_scripts(self):
        from Scripts import Automatizar
        global idpTab
        global automatizar
        automatizar = Automatizar(self.cuaderno, app, application=self)
        automatizar.fr_clt = ""
        self.cuaderno.add(automatizar, text='Automatizacion ')
        idpTab = self.cuaderno.index('current')

    def ocultar(self):
        extracion.hide()

    def bsc(self):
        extracion.panel_buscar()
    
    def cargar_modulos(self):
        desviacion._cargar_Modulos()
    
    def label_resize(self, event):
        event.widget['wraplength'] = event.width 
    
    def cerrar_vtn(self):
        self.vtn_acerca_de.destroy()

    def _acerca_de(self):
        self.vtn_acerca_de = tk.Toplevel(self.root)
        self.vtn_acerca_de.config(background=fondo_app)
        window_width=780
        window_height=370
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_acerca_de.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_acerca_de.tk.call('wm', 'iconphoto', self.vtn_acerca_de._w, tk.PhotoImage(file=path_icon+r'acercaDe.png'))       
        #self.vtn_acerca_de.transient(self.root)
        self.vtn_acerca_de.resizable(False,False)
        self.vtn_acerca_de.title("Continuous Compliance")

        self.icono_Acerca_de = ImageTk.PhotoImage(
            Image.open(path_icon+r"img_acerca_de.png").resize((200, 200)))

        self.AcercaDe_ico_frame = ttk.Frame(
                self.vtn_acerca_de,
                width=300,
            )
        self.AcercaDe_ico_frame.pack(fill='both', expand=1, side=tk.LEFT)
        self.AcercaDe_ico_frame.pack_propagate(False)

        self.ico_Acerca_de = ttk.Label(
            self.AcercaDe_ico_frame, 
            text='imagen',
            image=self.icono_Acerca_de,
        )
        self.ico_Acerca_de.place(x=50, y=50)

        self.AcercaDe_txt_frame = ttk.Frame(
                self.vtn_acerca_de, 
            )
        self.AcercaDe_txt_frame.pack(fill='both', expand=1, side=tk.LEFT)
        #self.AcercaDe_txt_frame.pack_propagate(False)

        self.lbl1 = ttk.Label(
            self.AcercaDe_txt_frame, 
            text='CONTINUOUS COMPLIANCE',
            anchor='center',
            font=(fuente_titulos, 16, "bold")
        )
        self.lbl1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.lbl5 = ttk.Label(
            self.AcercaDe_txt_frame,
            width=20,
            text='Herramienta para resolucion    de ISSUES Desviaciones / Extraciones',
            anchor='w',
            font=(fuente_titulos, 13)
        )
        self.lbl5.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.lbl5.bind("<Configure>", self.label_resize)

        self.lbl2 = ttk.Label(
            self.AcercaDe_txt_frame, 
            text='Versión:   2.0',
            anchor='w',
            font=(fuente_titulos, 13)
        )
        self.lbl2.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl2.bind("<Configure>", self.label_resize)

        self.lbl3 = ttk.Label(
            self.AcercaDe_txt_frame, 
            text='Fecha:   sabado marzo 12 CET 2022',
            anchor='w',
            font=(fuente_titulos, 11)
        )
        self.lbl3.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl3.bind("<Configure>", self.label_resize)

        self.lbl4 = ttk.Label(
            self.AcercaDe_txt_frame, 
            text='OS: x86_64 GNU/Linux',
            anchor='w',
            font=(fuente_titulos, 11)
        )
        self.lbl4.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl4.bind("<Configure>", self.label_resize)

        self.lbl6 = ttk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            foreground='gray',
            text='Documentado por el equipo de PHC - UNIX',
            anchor='w',
            font=(fuente_titulos, 11)
        )
        self.lbl6.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')

        self.lbl7 = ttk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            foreground='gray',
            text='Creado por Jose Alvaro Cedeño Panchana',
            anchor='w',
            font=(fuente_titulos, 11)
        )
        self.lbl7.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')

        self.lbl8 = ttk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            foreground='gray',
            text='Copyright © 2021 - 2022 Jose Alvaro Cedeño Panchana',
            anchor='w',
            font=(fuente_titulos, 11, 'bold')
        )
        self.lbl8.grid(row=7, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl8.bind("<Configure>", self.label_resize)

        self.boton = ttk.Button(
            self.AcercaDe_txt_frame,
            text='Close',
            command=self.cerrar_vtn
        )
        self.boton.grid(row=8, column=0, sticky='e', pady=20, padx=10)
    
    def _cargar_modulo_glosario(self, clt_modulo=None, *args):
        with open(path_modulo_clave.format('GLOSARIO')) as g:
            data = json.load(g)
            listModulo = []
            listClave = []
            for md in data:
                listModulo.append(md['modulo'])
                listClave.append(md['clave'])
        listModulo.sort()
        self._list_modulo.insert(tk.END,*listModulo)
        self._list_clave.insert(tk.END,*listClave)

    def on_select(self, event):
        global listbox_list
    
        widget = event.widget
        items = widget.curselection()
        for listbox in listbox_list:
            if listbox != widget:
                listbox.selection_clear(0, tk.END)
                for index in items:
                    listbox.selection_set(int(index))

    def _glosario(self):
        self.vtn_glosario = tk.Toplevel(self.root)
        self.vtn_glosario.config(background=fondo_app)
        window_width=800
        window_height=400
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_glosario.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_glosario.tk.call('wm', 'iconphoto', self.vtn_glosario._w, tk.PhotoImage(file=path_icon+r'acercaDe.png'))       
        #self.vtn_acerca_de.transient(self.root)
        self.vtn_glosario.resizable(False,False)
        self.vtn_glosario.title("Continuous Compliance")
        
        self.frame1 = ttk.Frame(
            self.vtn_glosario,
            height=40,
        )
        self.frame1.pack(fill='both', side='top', expand=0)

        self.titulo = ttk.Label(
            self.frame1,
            text='PALABRAS CLAVES DESVIACIONES',
            font=(fuente_titulos, 20, font.BOLD),
        )
        self.titulo.pack(expand=1)

        self.frame2 = ttk.Frame(
            self.vtn_glosario,
        )
        self.frame2.pack(fill='both', side=tk.LEFT, expand=0, pady=10)
        
        self.frame2.rowconfigure(1, weight=1)

        self.titulo_modulo = ttk.Label(
            self.frame2,
            text='MODULO',
            font=_Font_Titulo_bold,
            anchor='center',
            width=50
        )
        self.titulo_modulo.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

        self.ListModulo_yScroll = tk.Scrollbar(self.frame2, orient=tk.VERTICAL)
        
        ## LISTBOX MODULO
        self._list_modulo = tk.Listbox(
            self.frame2,
            font=_Font_Texto,
            foreground=color_fg_list,
            selectbackground=sel_bg_txt,
            selectforeground=sel_fg_txt,
            exportselection=False,
            highlightthickness=2,
            highlightcolor = active_color,
            yscrollcommand=self.ListModulo_yScroll.set,
        )
        self._list_modulo.grid(row=1, column=0, sticky='nsew', pady=10)
        listbox_list.append(self._list_modulo)
        
        self.frame3 = ttk.Frame(
            self.vtn_glosario,
            width=40
        )
        self.frame3.pack(fill='both', side='right', expand=1, pady=10,padx=10)
        self.frame3.columnconfigure(0, weight=1)
        self.frame3.rowconfigure(1, weight=1)

        self.titulo_clave = ttk.Label(
            self.frame3,
            text='CLAVE',
            font=_Font_Titulo_bold,
            anchor='center'
        )
        self.titulo_clave.grid(row=0, column=0, sticky='nsew', pady=5, padx=5, columnspan=2)

        self.ListClave_yScroll = tk.Scrollbar(self.frame3, orient=tk.VERTICAL)
        
        ## LISTBOX CLAVE
        self._list_clave = tk.Listbox(
            self.frame3,
            font=_Font_Texto,
            foreground=color_fg_list,
            selectbackground=sel_bg_txt,
            selectforeground=sel_fg_txt,
            exportselection=False,
            highlightthickness=2,
            highlightcolor = active_color,
            yscrollcommand=self.ListClave_yScroll.set,
        )
        self._list_clave.grid(row=1, column=0, sticky='nsew', pady=10,)
        listbox_list.append(self._list_clave)

        self.ListClave_yScroll.grid(row=1, column=1, pady=10, sticky='nse')
        self.ListModulo_yScroll.grid(row=1, column=1, pady=10, sticky='nse')

        self._list_modulo.bind('<<ListboxSelect>>', self.on_select)
        self._list_clave.bind('<<ListboxSelect>>', self.on_select)
        self._list_modulo.bind("<Button-3>", self._display_menu_clickDerecho_GLS)

        self._cargar_modulo_glosario()
        self._menu_clickDerecho_GLS()

    def widgets_APP(self):
            self.menuBar = tk.Menu(self.root, relief=tk.FLAT, border=0)
            self.root.config(menu=self.menuBar)
            self.menuBar.config(
                background=bg_menu,
                foreground=fg_menu,
                font=_Font_Menu,
                activebackground=acbg_menu,
                activeforeground=acfg_menu,
            )
            self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
            self.fileMenu.config(
                background=bg_submenu,
                foreground=fg_submenu,
                font=_Font_Menu,
                activebackground=acbg_menu,
                activeforeground=acfg_menu,
            )
            # --- INICIAMOS SUB MENU -------------------------- #
            self.clientMenu = tk.Menu(self.fileMenu, tearoff=0)
            self.issuesMenu = tk.Menu(self.fileMenu, tearoff=0)
            # -------------------------------------------------- #

            self.issuesMenu.config(
                background=bg_submenu,
                foreground=fg_submenu,
                font=_Font_Menu,
                activebackground=acbg_menu,
                activeforeground=acfg_menu,
                selectcolor=fg_menu
            )
            self.clientMenu.config(
                background=bg_submenu,
                foreground=fg_submenu,
                font=_Font_Menu,
                activebackground=acbg_menu,
                activeforeground=acfg_menu,
                selectcolor=fg_menu
            )

            self.fileMenu.add_cascade(
                label="  Abrir",
                compound=tk.LEFT,
                image=self.Abrir_icon,
                menu = self.issuesMenu
            )

            self.fileMenu.add_cascade(
                label="  Clientes",
                image=self.Client_icon,
                compound=tk.LEFT,
                menu=self.clientMenu
            )

            self.fileMenu.add_separator()

            #* MENU PREFERENCIAS
            self.fileMenu.add_command(
                label="  Preferencias",
                image=self.Client_icon,
                compound=tk.LEFT,
                command=self._fontchooser
                #menu=self.clientMenu
            )

            self.fileMenu.add_separator()

            self.fileMenu.add_command(
                label="  Salir",
                image=self.Salir_icon,
                compound=tk.LEFT,
                command=self.root.quit
            )

            self.ClientVar = tk.IntVar()
            for i, m in enumerate(list_client):
                self.clientMenu.add_radiobutton(
                    label=m,
                    variable=self.ClientVar,
                    value=i,
                    command=self.cargar_modulos,
                )

            self.IssuesVar = tk.IntVar()
            for i, m in enumerate(list_issues):
                self.issuesMenu.add_radiobutton(
                    label=m,
                    variable=self.IssuesVar,
                    value=i,
                    command=self.abrir_issues
                )

            self.editMenu = tk.Menu(self.menuBar, tearoff=0)
            self.editMenu.config(
                background=bg_submenu,
                foreground=fg_submenu,
                font=_Font_Menu,
                activebackground=acbg_menu,
                activeforeground=acfg_menu,
            )
            self.editMenu.add_command(
                label="  Buscar",
                accelerator='Ctrl+F',
                command=self.bsc,
                image=self.BuscarBar_icon,
                compound=tk.LEFT,
                state="disabled"
            )
            self.fileMenu.add_separator()
            self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
            self.helpMenu.config(
                background=bg_submenu,
                foreground=fg_submenu,
                font=_Font_Menu,
                activebackground=acbg_menu,
                activeforeground=acfg_menu,
            )
            self.helpMenu.add_command(
                label="  Ayuda",
                image=self.Ayuda_icon,
                compound=tk.LEFT,
                command=self._glosario
            )
            self.helpMenu.add_separator()
            self.helpMenu.add_command(
                label="  Acerca de...",
                image=self.AcercaDe_icon,
                compound=tk.LEFT,
                command=self._acerca_de
            )

            self.menuBar.add_cascade(label=" Archivo ", menu=self.fileMenu)
            self.menuBar.add_cascade(label=" Editar ", menu=self.editMenu)
            self.menuBar.add_cascade(label=" Ayuda ", menu=self.helpMenu)

# TODO BOTON DESVIACION

            self.frameButton = ttk.Frame(
                self.contenedor, 
            )

            self.frameButton.grid(row=0, column=0, sticky='nsew', pady=5, padx=5
            )
            
            self.btn_AbrirDesv = ttk.Button(
                self.frameButton, 
                text='DESVIACIONES',
                width=14,
                style='APP.TButton',
                image=self.Desviaciones_icon,
                compound='top',
                command=self.abrir_issuesDesviacion
            )
            self.btn_AbrirDesv.grid(
                padx=30, 
                pady=30, 
                row=0, 
                column=0, 
                ipady=20, 
            )

# TODO BOTON EXTRACION

            self.btn_AbrirExt = ttk.Button(
                self.frameButton, 
                text='EXTRACIONES',
                width=14,
                style='APP.TButton',
                image=self.Extracion_icon,
                compound='top',
                command=self.abrir_issuesExtracion
            )
            self.btn_AbrirExt.grid(
                pady=30,
                padx=(0,30),
                row=0, 
                column=1, 
                ipady=20, 
            )

# TODO BOTON AUTOMATIZAR

            self.btn_AbrirExt = ttk.Button(
                self.frameButton, 
                text='AUTOMATIZAR',
                width=14,
                style='APP.TButton',
                image=self.Automatizar_icon,
                compound='top',
                command=self.abrir_scripts,
            )

            self.btn_AbrirExt.grid(
                pady=30,
                padx=(0,30),
                ipady=20,
                row=0, 
                column=2, 
            )

# TODO RESTO BOTONES

            # self.btn_AbrirExt = ttk.Button(
            #     self.frameButton, 
            #     text='AUTOMATIZACION',
            #     width=14,
            #     style='APP.TButton',
            #     image=self.Automatizar_icon,
            #     compound='top',
            #     command=self.abrir_issuesExtracion,
            # )
            # self.btn_AbrirExt.grid(
            #     pady=30,
            #     padx=(0,30),
            #     ipady=20,
            #     row=0, 
            #     column=3, 
            # )

            # self.btn_AbrirExt = ttk.Button(
            #     self.frameButton, 
            #     text='AUTOMATIZACION',
            #     width=14,
            #     style='APP.TButton',
            #     image=self.Automatizar_icon,
            #     compound='top',
            #     command=self.abrir_issuesExtracion,
            # )
            # self.btn_AbrirExt.grid(
            #     pady=30,
            #     padx=(0,30),
            #     ipady=20,
            #     row=0, 
            #     column=4, 
            # )

# TODO BIENVANIDA
            
            self.frameLabel = ttk.Frame(
                self.contenedor, 
            )

            self.frameLabel.grid(row=1, column=0, sticky='sew', pady=5, padx=5, columnspan=2)
            
            self.frameLabel.columnconfigure(0, weight=1)
            self.frameLabel.rowconfigure(0, weight=1)

            self.lbl_Bienvenido = ttk.Label(
                self.frameLabel,
                style='APP.TLabel',
                text='Bienvenido : '+user,
                anchor='center',
            )
            self.lbl_Bienvenido.grid(
                row=0, 
                column=0, 
                sticky='nsew'
            )

    def _fontchooser(self):
        from Preferencias import SelectFont
        ventanafont = SelectFont(parent=None, titulo="Ventana")

        #ventanafont.grab_set()
    
    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
