#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Jose Alvaro Cedeño 2022
# For license see LICENSE
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import json
import os
import time
import subprocess
import sys
from getpass import getuser
from tkinter import TclError, scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font
from PIL import Image, ImageTk
from ScrollableNotebook import *
from RadioBotton import RadioButton
from functools import partial
from configparser import ConfigParser
from Tooltip import CustomHovertip
#-----------------------------------------------------------#
user = getuser()
mypath = os.path.expanduser("~/")

#? ROUTERS
pathExtraction = mypath+"Compliance/extracion/"
pathIcon = mypath+"Compliance/image/"
pathFiles = mypath+"Compliance/file/desviaciones_{}.json"
pathFilesGl = mypath+"Compliance/file/{}.json"
pathConfig = mypath+"Compliance/.conf/{}"
pathRisk = mypath+"Compliance/file/Riesgo_Impacto/{}"

#? Arrays
listClient = []
listButton = [
    "DESVIACIONES",
    "EXTRACIONES",
    #"AUTOMATIZACION"
]
# --- VARIABLE GLOBAL ---
idOpenTab = 0
tooltip = False
listModulo = []
listKeys = []
txtWidget_focus = False
txtWidget = ""
sis_oper = ""
idpTab = 0
varNum = 0
text_aExpandir = ""
value = ""
list_motion = ""
automatizar = ""
# TODO VARIABLES DE VENTANAS
PST_DESV = ""
PST_EXP = ""
PST_AUT = ""
APP_EXT = ""
PST_VTN = ""
# TODO------------------------
_tt_Desv = ""
listbox_list = []
no_exist = False
extracion = ""
act_rbtn_ = False
act_rbtn_auto = False

# * Configuracion de APARIENCIA INICIAL
parse = ConfigParser()
parse.read(pathConfig.format("apariencia.ini"))

# COLOR MENU
default_menu_bg = parse.get('menu', 'background')
default_menu_fg = parse.get('menu', 'foreground')
default_select_bg = parse.get('menu', 'activebackground')
default_select_fg = parse.get('menu', 'activeforeground')
fg_submenu = parse.get('menu', 'foreground_submenu')
bg_submenu = parse.get('menu', 'background_submenu')

# COLOR BOTONES
default_boton_bg = parse.get('boton', 'background')
default_boton_fg = parse.get('boton', 'foreground')
default_boton_acbg = parse.get('boton', 'activebackground')
default_boton_acfg = parse.get('boton', 'activeforeground')
default_Outline = parse.get('boton', 'outline')

# * COLOR TREEVIEW
oddrow = parse.get('treeview', 'oddrow')
evenrow = parse.get('treeview', 'evenrow')

# COLOR FONDO APP
default_bottom_app = parse.get('app', 'fondo')

# * COLOR TAB
color_out_bg_pestaña = parse.get('tab', 'tab_outselect_bg')
color_out_fg_pestaña = parse.get('tab', 'tab_outselect_fg')
color_act_bg_pestaña = parse.get('tab', 'tab_actselect_bg')
color_act_fg_pestaña = parse.get('tab', 'tab_actselect_fg')
color_sel_fg_pestaña = parse.get('tab', 'tab_select_fg')

# COLOR WIDGETS / DESV #? POR DEFECTO
hlh_def = 2
hhtk = 3
default_color_titulos = parse.get('app', 'titulo')
default_color_subtitulos = parse.get('app', 'subtitulo')
default_scrText_fg = parse.get('app', 'colour_text')
default_hglcolor = parse.get('app', 'color_widget_activo')
default_scrText_bg = parse.get('app', 'colour_scroll') #? COLOR FONDO PARA WIDGETS
default_color_descripcion = '#838389'
default_colourCodeFg = '#FF5E5E'
#default_colourCodeBg = '#FFE7E7'
default_colourCodeBg = '#fedee1'
default_color_line_fg = '#1E90FF'
default_colourNoteFg = '#7A7A7A'
default_Framework = '#838389'

# FUENTES
fuente_titulos = parse.get('app', 'fuente_titulo')
tamñ_titulo = parse.get('app', 'tamano_titulo')
weight_DF = parse.get('app', 'weight')
fuente_texto = parse.get('app', 'fuente_texto')
fuente_texto_cdg = 'Courier New'
tamñ_texto = parse.get('app', 'tamano_texto')
fuente_menu = parse.get('menu', 'fuente_menu')
tamñ_menu = parse.get('menu', 'tamano_menu')
fuente_boton = parse.get('boton', 'fuente_boton')
tamñ_boton = parse.get('boton', 'tamano_boton')
tamñ_texto_exp = parse.get('expand', 'tamano_text_expand')
tamñ_pestaña = parse.get('pestana', 'tamano_pestana')
fuente_pestañas = parse.get('pestana', 'fuente_pestana')

# COMBINACIONES DE FUENTES
_Font_Menu = (fuente_menu, tamñ_menu)
_Font_Menu_bold = (fuente_menu, tamñ_menu)
_Font_Texto = (fuente_texto, tamñ_texto)
_Font_Texto_codigo = (fuente_texto_cdg, tamñ_texto)
_Font_Texto_bold = (fuente_texto, tamñ_texto, weight_DF)
_Font_pestañas = (fuente_pestañas, tamñ_pestaña)
_Font_txt_exp = (fuente_texto, tamñ_texto_exp)
_Font_txt_exp_cdg = (fuente_texto_cdg, tamñ_texto_exp)
_Font_text_exp_bold = (fuente_titulos, tamñ_texto_exp, weight_DF)
_Font_Boton = (fuente_boton, tamñ_boton, weight_DF)

#todo MODO DARK
modo_dark = parse.get('dark', 'modo_dark')
activar_modo = parse.get('dark', 'activar_modo')
text_btnMode = "Dark Mode ON"
# * COLOR PERSONALIZADO
pers_scrText_fg = '#f4f4f4'
pers_scrText_bg = '#555555'  # ? PARA CUADRO DE TEXTO
pers_color_titulo = '#FF8080'
pers_menu_bg = '#353535'  # ? COLOR PRIMARIO
pers_bottom_app = '#454545'  # ? SECUNDARIO
pers_hglcolor = '#E7E7E7'
pers_OutlineDark = '#E95858' #? color rojo outline
pers_Outline = '#4A8CCA' #? color azul outline
pers_colourCodeFg = '#E68080'
pers_colourNoteFg = '#BABABA'
pers_Framework = '#545454'
pers_colourCodeBg = '#555555'

def beep_error(f):
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    return applicator

class Expandir(ttk.Frame):
    y_alto_btn = 55
    x_ancho_btn = 200
    hg_btn = int(y_alto_btn-15)
    wd_btn = int(x_ancho_btn-20)
    def __init__(self, parent, text_EXP, widget_EXP, customer, titulo, so, st_btnDIR, st_btnAUTH, st_btnSER, st_btnACC, st_btnCMD, st_btnIDR, varNum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global PST_EXP
        PST_EXP = self
        self.parent = parent
        self.customer = customer
        self.titulo = titulo
        self.so = so
        # Recibe el text del SRC a expandir
        self.txt_Expan = text_EXP
        self.widget_EXP = widget_EXP
        # -----------------------------------
        self.st_btnDIR = st_btnDIR
        self.st_btnAUTH = st_btnAUTH
        self.st_btnSER = st_btnSER
        self.st_btnACC = st_btnACC
        self.st_btnCMD = st_btnCMD
        self.st_btnIDR = st_btnIDR
        self.varNum = varNum
        self.vtn_expandir = tk.Toplevel(self)
        self.vtn_expandir.config(background=default_bottom_app)
        parse.read(pathConfig.format("apariencia.ini"))
        window_width = parse.get('medidas_expandir', 'width')
        window_height = parse.get('medidas_expandir', 'height')
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_expandir.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        #self.vtn_expandir.tk.call('wm', 'iconphoto', self.vtn_expandir._w, tk.PhotoImage(file=pathIcon+r'expandir1.png'))
        self.vtn_expandir.transient(self.parent)
        self.vtn_expandir.title(
            "DESVIACIONES : {} - {}".format(self.customer, self.so))
        self.vtn_expandir.columnconfigure(0, weight=1)
        self.vtn_expandir.rowconfigure(1, weight=1)
        self.vtn_expandir.resizable(False, False)
        # ----------------------------------------------------------------
        self.menu_clickDerecho()
        self.WIDGETS_EXPANDIR()

        self.bind("<Motion>", lambda e: self.EXP_motion(e))
        self.EXP_scrExpandir.bind(
            "<Button-3><ButtonRelease-3>", self.display_menu_clickDerecho)
        self.EXP_scrExpandir.bind(
            "<Motion>", lambda e: desviacion.activar_Focus(e))
        self.EXP_scrExpandir.bind(
            "<Key>", lambda e: app.widgets_SoloLectura(e))
        self.EXP_scrExpandir.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.EXP_scrExpandir.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
    ## --- MENU CONTEXTUAL --------------------------- ##

    def EXP_motion(self, event):
        global PST_EXP
        PST_EXP = event.widget

    def cerrar_vtn_expandir(self):
        # if txtWidget_focus:
        self.vtn_expandir.destroy()

    def menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self.vtn_expandir, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Copiar",
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=desviacion.copiar_texto_seleccionado,
            state="disabled"
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo",
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda: desviacion.seleccionar_todo(event=None),
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña",
            # image=self.cerrar_icon,
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
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

    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel", "1.0", "end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel", "1.0", "end")

    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel", "1.0", "end")
            return 'break'
        else:
            pass

    def _siguiente(self, customer):
        global _tt_Desv
        self.EXP_btnScreamEvidencia.config(state="disabled")
        self.EXP_btnCopyALL.config(state="disabled")
        if self.varNum == 1:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['copia']
                            if self._txt_Desv is None:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, md['editar'])
                                self.varNum = 3
                                self.descativar_botones()
                            else:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 2
                                self.descativar_botones()
        elif self.varNum == 2:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['editar']
                            if self._txt_Desv is None:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(
                                    tk.END, md['refrescar'])
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 4
                                self.descativar_botones()
                            else:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 3
                                self.descativar_botones()
        elif self.varNum == 3:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['refrescar']
                            if self._txt_Desv is None:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(
                                    tk.END, md['evidencia'])
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                                self.descativar_botones()
                            else:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 4
        elif self.varNum == 4:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['evidencia']
                            if self._txt_Desv is None:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(
                                    tk.END, md['comprobacion'])
                                self.varNum = 1
                                self.activar_botones()
                            else:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                            self.descativar_botones()
        elif self.varNum == 5:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['comprobacion']
                            if self._txt_Desv is None:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, md['copia'])
                                self.varNum = 2
                                self.descativar_botones()
                            else:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 1
                                self.activar_botones()
        if modo_dark == 'False':
            self.colourLineExpandir(
                default_scrText_bg,
                default_colourCodeBg,
                default_colourCodeFg,
                default_colourNoteFg
            )
        else:
            PST_EXP.colourLineExpandir(
                pers_scrText_bg,
                pers_scrText_bg,
                pers_colourCodeFg,
                pers_colourNoteFg
            )

    def _anterior(self, customer):
        global _tt_Desv
        self.EXP_btnScreamEvidencia.config(state="disabled")
        self.EXP_btnCopyALL.config(state="disabled")
        if self.varNum == 1:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['evidencia']
                            if self._txt_Desv is None:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(
                                    tk.END, md['refrescar'])
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 4
                                self.descativar_botones()
                            else:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                                self.descativar_botones()
        elif self.varNum == 2:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['comprobacion']
                            if self._txt_Desv is None:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(
                                    tk.END, md['evidencia'])
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                                self.descativar_botones()
                            else:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 1
                                self.activar_botones()
        elif self.varNum == 3:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['copia']
                            if self._txt_Desv is None:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(
                                    tk.END, md['evidencia'])
                                self.varNum = 1
                                self.activar_botones()
                            else:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 2
                                self.descativar_botones()
        elif self.varNum == 4:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['editar']
                            if self._txt_Desv is None:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, md['copia'])
                                self.varNum = 2
                                self.descativar_botones()
                            else:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 3
                                self.descativar_botones()
        elif self.varNum == 5:
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['refrescar']
                            if self._txt_Desv is None:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, md['editar'])
                                self.varNum = 2
                                self.descativar_botones()
                            else:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_scrExpandir.delete('1.0', tk.END)
                                self.EXP_scrExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 1
        if modo_dark == 'False':
            self.colourLineExpandir(
                default_scrText_bg,
                default_colourCodeBg,
                default_colourCodeFg,
                default_colourNoteFg
            )
        else:
            PST_EXP.colourLineExpandir(
                pers_scrText_bg,
                pers_scrText_bg,
                pers_colourCodeFg,
                pers_colourNoteFg
            )

    def activar_botones(self):
        global PST_EXP
        if PST_EXP.st_btnDIR:
            PST_EXP.EXP_btnDirectory.grid(row=0, column=0, sticky='ne')
        elif PST_EXP.st_btnAUTH:
            PST_EXP.EXP_btnAuthorized.grid(row=0, column=0, sticky='ne')
        elif PST_EXP.st_btnSER:
            PST_EXP.EXP_btnService.grid(row=0, column=0, sticky='ne')
        elif PST_EXP.st_btnACC:
            PST_EXP.EXP_btnAccount.grid(row=0, column=0, sticky='ne')
        elif PST_EXP.st_btnCMD:
            PST_EXP.EXP_btnCommand.grid(row=0, column=0, sticky='ne')
        elif PST_EXP.st_btnIDR:
            PST_EXP.EXP_btnIdrsa.grid(row=0, column=0, sticky='ne')

    def WIDGETS_EXPANDIR(self):
        from DataExtraction import MyScrollText
        self.EXP_lblWidget = ttk.Label(
            self.vtn_expandir,
            text=self.titulo,
            foreground=default_color_titulos,
        )
        self.EXP_lblWidget.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        self.EXP_scrExpandir = MyScrollText(
            self.vtn_expandir,
            app
        )

        self.EXP_scrExpandir.insert('1.0', self.txt_Expan)

        self.EXP_btnDirectory = RadioButton(
            self.vtn_expandir,
            alto=Expandir.y_alto_btn,
            ancho=Expandir.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btn_expDIR_ = ttk.Button(
            self.EXP_btnDirectory,
            text='Permissions  ',
            compound=tk.RIGHT,
            image=app.icono_account,
            style='APP.TButton',
            command=desviacion.abrir_DIRECTORY
        )
        self._btn_expDIR_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Expandir.hg_btn,
            width=Expandir.wd_btn
        )

        self.EXP_btnAuthorized = RadioButton(
            self.vtn_expandir,
            alto=Expandir.y_alto_btn,
            ancho=Expandir.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btn_expAUT_ = ttk.Button(
            self.EXP_btnAuthorized,
            text='Authorized',
            compound=tk.RIGHT,
            image=app.icono_account,
            style='APP.TButton',
            command=desviacion.abrir_AUTHORIZED,
            state="normal"
        )
        self._btn_expAUT_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Expandir.hg_btn,
            width=Expandir.wd_btn
        )

        self.EXP_btnService = RadioButton(
            self.vtn_expandir,
            alto=Expandir.y_alto_btn,
            ancho=Expandir.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btn_expSER_ = ttk.Button(
            self.EXP_btnService,
            text='Service',
            compound=tk.RIGHT,
            image=app.icono_account,
            command=desviacion.abrir_SERVICE,
            style='APP.TButton',
            state="normal"
        )
        self._btn_expSER_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Expandir.hg_btn,
            width=Expandir.wd_btn
        )

        self.EXP_btnAccount = RadioButton(
            self.vtn_expandir,
            alto=Expandir.y_alto_btn,
            ancho=Expandir.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btn_expACC_ = ttk.Button(
            self.EXP_btnAccount,
            text='Account',
            compound=tk.RIGHT,
            image=app.icono_account,
            command=desviacion.abrir_ACCOUNT,
            style='APP.TButton',
            state="normal"
        )
        self._btn_expACC_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Expandir.hg_btn,
            width=Expandir.wd_btn
        )

        self.EXP_btnCommand = RadioButton(
            self.vtn_expandir,
            alto=Expandir.y_alto_btn,
            ancho=Expandir.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btn_expCMD_ = ttk.Button(
            self.EXP_btnCommand,
            text='Command',
            compound=tk.RIGHT,
            image=app.icono_account,
            command=desviacion.abrir_COMMAND,
            style='APP.TButton',
            state="normal"
        )
        self._btn_expCMD_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Expandir.hg_btn,
            width=Expandir.wd_btn
        )

        self.EXP_btnIdrsa = RadioButton(
            self.vtn_expandir,
            alto=Expandir.y_alto_btn,
            ancho=Expandir.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btn_expIDR_ = ttk.Button(
            self.EXP_btnIdrsa,
            text='Id_Rsa',
            compound=tk.RIGHT,
            image=app.icono_account,
            command=desviacion.abrir_IDRSA,
            style='APP.TButton',
            state="normal"
        )
        self._btn_expIDR_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Expandir.hg_btn,
            width=Expandir.wd_btn
        )

        self.EXP_btn_Siguiente = tk.Button(
            self.vtn_expandir,
            text='SIGUIENTE',
            image=app.next_icon,
            command=partial(self._siguiente, PST_EXP.customer),
            border=0,
            borderwidth=0,
            highlightthickness=0,
            background=default_bottom_app,
            relief="flat",
            highlightbackground=default_bottom_app,
            activebackground=default_bottom_app,
        )
        self.EXP_btn_Siguiente.grid(row=0, column=2, pady=15, padx=(0,10), sticky='ne')

        self.EXP_btn_Anterior = tk.Button(
            self.vtn_expandir,
            text='ANTERIOR',
            image=app.previous_icon,
            command=partial(self._anterior, PST_EXP.customer),
            border=0,
            borderwidth=0,
            highlightthickness=0,
            background=default_bottom_app,
            relief="flat",
            highlightbackground=default_bottom_app,
            activebackground=default_bottom_app,
        )
        self.EXP_btn_Anterior.grid(row=0, column=1, pady=15, padx=10, sticky='ne')

        self.EXP_btnCopyALL = ttk.Button(
            self.vtn_expandir,
            image=desviacion.icono_copiar,
            style='APP.TButton',
            state="disabled",
            command=lambda e=self.EXP_scrExpandir: self.copiarALL(e),
        )
        self.EXP_btnCopyALL.grid(row=0, column=4, pady=15, sticky='ne')

        self.EXP_btnScreamEvidencia = ttk.Button(
            self.vtn_expandir,
            image=desviacion.icono_captura,
            command=desviacion.ScreamEvidencia,
            style='APP.TButton',
            state="disabled",
        )
        self.EXP_btnScreamEvidencia.grid(row=0, column=5, padx=10, pady=15, sticky='ne')

        self.EXP_btnReducir = ttk.Button(
            self.vtn_expandir,
            image=app.iconoCloseExpand,
            style='APP.TButton',
            command=self.cerrar_vtn_expandir,
        )
        # self.EXP_btnReducir.config(
        #         background=default_bottom_app,
        #         highlightcolor=default_hglcolor,
        #         activebackground=default_bottom_app,
        #         border=0,
        #         highlightbackground=default_bottom_app,
        #     )
        self.EXP_btnReducir.grid(row=0, column=6, padx=(0,20), pady=15, sticky='ne')

        self.EXP_scrExpandir.grid(
            row=1, column=0, padx=5, pady=5, sticky='nsew', columnspan=7)

        self.activar_botones()

    def descativar_botones(self):
        self.EXP_btnDirectory.grid_forget()
        self.EXP_btnAuthorized.grid_forget()
        self.EXP_btnService.grid_forget()
        self.EXP_btnAccount.grid_forget()
        self.EXP_btnCommand.grid_forget()
        self.EXP_btnIdrsa.grid_forget()

    def colourLineExpandir(self,
        bg_color,
        bg_codigo,
        fg_codigo,
        fg_nota):
        PST_EXP.EXP_scrExpandir.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_txt_exp_cdg
        )
        PST_EXP.EXP_scrExpandir.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=font.Font(family=_Font_Texto, size=20, weight='bold')
        )
        PST_EXP.EXP_scrExpandir.tag_configure(
            "nota",
            background='#D4EFEE',
            foreground='#000000',
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_txt_exp
        )
        PST_EXP.EXP_scrExpandir.tag_configure(
            "server",
            background='#7BB3A4',
            foreground='#000000',
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_txt_exp
        )
        PST_EXP.EXP_scrExpandir.tag_configure(
            "coment",
            background=pers_scrText_bg,
            foreground='#EFB810',
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_txt_exp
        )
        end = PST_EXP.EXP_scrExpandir.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_EXP.EXP_scrExpandir.search("##", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_scrExpandir.tag_add(
                    "codigo", startline, endline)
            if (PST_EXP.EXP_scrExpandir.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_scrExpandir.tag_add(
                    "line", startline, endline)
            if (PST_EXP.EXP_scrExpandir.search("//", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_scrExpandir.tag_add(
                    "nota", startline, endline)
            if (PST_EXP.EXP_scrExpandir.search("[", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_scrExpandir.tag_add(
                    "server", startline, endline)
            if (PST_EXP.EXP_scrExpandir.search("\"", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_scrExpandir.tag_add(
                    "coment", startline, endline)

class TextSimilar(ttk.Frame):
    def __init__(self, parent, titulo, modulo_clave, cliente, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global no_exist
        self.titulo = titulo
        self.cliente = cliente
# ---- TOP LEVEL-----
        self.vtn_modulos = tk.Toplevel(self)
        self.vtn_modulos.config(background=default_bottom_app)
        window_width = 1000
        window_height = 300
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height)
        position_right = int(screen_width+150)
        self.vtn_modulos.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_modulos.resizable(0, 0)
        self.vtn_modulos.transient(self)
        self.vtn_modulos.grab_set()
        self.vtn_modulos.focus_set()
        self.vtn_modulos.config(background=default_bottom_app)


# --- FRAME TITULO
        self.frame1 = ttk.Frame(
            self.vtn_modulos,
        )
        self.frame1.pack(fill='both', side='top', expand=0)

        self.titulo = ttk.Label(
            self.frame1,
            text=self.titulo,
        )
        self.titulo.pack(pady=10)

# --- FRAME LISTBOX
        self.frame2 = ttk.Frame(
            self.vtn_modulos,
        )
        self.frame2.pack(fill='both', side=tk.LEFT, expand=1, pady=5, padx=5)
        self.frame2.pack_propagate(1)
        self.frame2.rowconfigure(0, weight=5)
        self.frame2.columnconfigure(0, weight=5)


# --- LISTBOX MODULO - FRAME2
        self._list_modulo = tk.Listbox(
            self.frame2,
            font=_Font_Texto,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            exportselection=False,
            highlightthickness=hhtk,

            highlightcolor=default_hglcolor,
        )

        self._list_modulo.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

# --- FUNCIONES LIST MODULO A SCROLL
        self._list_modulo.bind("<Down>", lambda e: self._OnVsb_down(e))
        self._list_modulo.bind("<Up>", lambda e: self._OnVsb_up(e))

# --- FRAME 3
        self.frame3 = ttk.Frame(
            self.vtn_modulos,
        )
        self.frame3.pack(fill='both', side='right', expand=0, pady=5, padx=5)
        self.frame3.rowconfigure(0, weight=1)

# --- LISTBOX CLAVE - FRAME 3
        self._list_clave = tk.Listbox(
            self.frame3,
            font=_Font_Texto,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            exportselection=False,
            highlightthickness=hhtk,
            highlightcolor=default_hglcolor,
            width=18,
            height=18,
        )
        self._list_clave.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

# --- LISTBOX SO - FRAME 2
        self._list_SO = tk.Listbox(
            self.frame3,
            font=_Font_Texto,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            exportselection=False,
            highlightthickness=hhtk,
            highlightcolor=default_hglcolor,
            width=12,
            height=12,
        )
        self._list_SO.grid(row=0, column=1, sticky='nsew', pady=5, padx=(0, 5))

# - CREAR SCROLL
        self.vsb_scroll = tk.Scrollbar(
            self.frame3,
            orient="vertical",
            command=self.yview
        )

        self.vsb_scroll.grid(row=0, column=2, sticky='nsew')

# --- list asociados a los SCROLL
        self._list_modulo.configure(yscrollcommand=self.yscroll_modulo)
        self._list_clave.configure(yscrollcommand=self.yscroll_clave)
        self._list_SO.configure(yscrollcommand=self.yscroll_so)

# --------------------------------------------------------------------
# --- INSERTAR MODULO Y CLAVE A LIST BOX
        # TRUE
        if no_exist:
            for m, c in modulo_clave.items():
                self._list_modulo.insert(tk.END, m)
                self._list_clave.insert(tk.END, c[0])
                self._list_SO.insert(tk.END, c[1])
            self._list_modulo.bind('<<ListboxSelect>>',
                                   lambda e: self.on_SelectList(e))
            self._list_modulo.bind('<Double-Button-1>',
                                   lambda e: self.onDoubleSelectList(e))
        else:
            for m, c in modulo_clave.items():
                self._list_modulo.insert(tk.END, m)
                self._list_clave.insert(tk.END, c[0])
                self._list_SO.insert(tk.END, c[1])
            self._list_modulo.bind('<<ListboxSelect>>',
                                   lambda e: self.on_SelectList(e))
            self._list_modulo.bind('<Double-Button-1>',
                                   partial(self._on_select_list))

# TODO --- Bloquear select listbox
        self._list_clave.bindtags((self._list_clave, app, "all"))
        self._list_SO.bindtags((self._list_clave, app, "all"))

# --- FUNCIONES PARA SCROLLBAR

    def yscroll_modulo(self, *args):
        wyview = self._list_modulo.yview()
        if self._list_clave.yview() != wyview:
            self._list_clave.yview_moveto(args[0])
        if self._list_SO.yview() != wyview:
            self._list_SO.yview_moveto(args[0])
        self.vsb_scroll.set(*args)

    def yscroll_clave(self, *args):
        wyview = self._list_SO.yview()
        if self._list_clave.yview() != wyview:
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

# --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_down(self, event):
        list_event = event.widget
        list_event.yview_scroll(1, "units")
        self._list_clave.yview_scroll(1, "units")
        self._list_SO.yview_scroll(1, "units")

# --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_up(self, event):
        list_event = event.widget
        list_event.yview_scroll(-1, "units")
        self._list_clave.yview_scroll(-1, "units")
        self._list_SO.yview_scroll(-1, "units")

# --- ACCION AL SELECIONAR
    def on_SelectList(self, event):
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

# --- ACCION DOBLE CLICK
    def onDoubleSelectList(self, event):
        global value
        global listModulo
        global listKeys
        listbox_list_all = []
        widget = event.widget
        index = widget.curselection()
        listbox_list_all.append(self._list_modulo)
        listbox_list_all.append(self._list_clave)
        listbox_list_all.append(self._list_SO)
        customer = self._list_SO.get(index[0])
        moduleFound = self._list_modulo.get(index[0])
        desviacion = Desviacion(app.cuaderno)
        app.cuaderno.add(desviacion, text='DESVIACIONES : {} '.format(customer))
        desviacion.enabled_Widgets()
        desviacion.varClient.set(customer)
        with open(pathFiles.format(customer)) as g:
            data = json.load(g)
            listModulo = []
            listKeys = []
            for md in data:
                if 'modulo' in md:
                    listModulo.append(md['modulo'])
                    listKeys.append(md['clave'])
        listModulo.sort()
        desviacion.DESV_ListBox.insert(tk.END, *listModulo)
        moduleFound = str(moduleFound).replace("[", "").replace("]", "").replace("'", "")
        data = []
        with open(pathFiles.format(customer)) as g:
            data = json.load(g)
            for md in data:
                if 'modulo' in md:
                    if moduleFound in md['modulo']:
                        value = md['modulo']
                        # --- LIMPIAR ------------------------------------- ##
                        desviacion.limpiar_Widgets()
                        ## ------------------------------------------------- ##
                        desviacion.asignarValor_aWidgets(md)
            desviacion.showButtonsModule(moduleFound)
            desviacion.DESV_ListBox.selection_clear(0, tk.END)
            moduleLoaded = desviacion.DESV_ListBox.get(0, tk.END)
            index = moduleLoaded.index(value)
            desviacion.DESV_ListBox.selection_set(index)
        self.vtn_modulos.destroy()

    #@beep_error
    def _on_select_list(self, event):
        global value
        global PST_DESV
        listbox = event.widget
        index = listbox.curselection()
        value = listbox.get(index[0])
        customer = PST_DESV.varClient.get()
        moduleLoaded = PST_DESV.DESV_ListBox.get(0, tk.END)
        index = moduleLoaded.index(value)
        PST_DESV.DESV_ListBox.selection_set(index)
        self.vtn_modulos.destroy()
        desviacion._loadSelectItem(value, customer)

class Desviacion(ttk.Frame):
    y_alto_btn = 55
    x_ancho_btn = 200
    hg_btn = int(y_alto_btn-15)
    wd_btn = int(x_ancho_btn-20)

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        global PST_DESV
        self.parent = parent
        PST_DESV = self
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        PST_DESV.bind("<Motion>", lambda e: self.DESV_motion(e))
# --- FUENTE PARA DESVIACIONES
# --- Fuente Menu click derecho
        self.iconos()
        self.WIDGETS_DESVIACION()
        self._menu_clickDerecho()
        if activar_modo == 'True':
            app.MODE_DARK()
## --- SELECCIONAR ELEMENTO DEL LISTBOX. --- #
        self.DESV_ListBox.bind("<<ListboxSelect>>", self.selectModule)

## --- ADJUTAR EL TEXT DE LOS LABEL --- #
        self.DESVfr2_lblModulo.bind("<Configure>", self.label_resize)
        self.DESVfr2_lblDescripcion.bind("<Configure>", self.label_resize)

## --- ACTIVAR WIDGET. --- #
        #self.DESVfr2_lblModulo.bind("<Motion>",lambda e:self.activar_Focus(e))
        #self.DESV_frame2.bind("<Motion>",lambda e:self.activar_Focus(e))
        #self.DESVfr2_lblDescripcion.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESV_scrCheck.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_scrBackup.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_scrEdit.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_scrRefresh.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_scrEvidencia.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_entry.bind(
            "<Motion>", lambda e: self._act_focus_ent(e))
        #*app.cuaderno.bind("<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_ListBox.bind("<Motion>", lambda e: self._activar_Focus(e))

## --- MOSTRAR MENU DERECHO  --- ##
        self.DESV_scrCheck.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESV_scrBackup.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESV_scrEdit.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESV_scrRefresh.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESV_scrEvidencia.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)

## --- ACTIVAR MODO SOLO LECTURA --- ##
        self.DESV_scrCheck.bind(
            "<Key>", lambda e: app.widgets_SoloLectura(e))
        self.DESV_scrBackup.bind(
            "<Key>", lambda e: app.widgets_SoloLectura(e))
        self.DESV_scrEdit.bind(
            "<Key>", lambda e: app.widgets_SoloLectura(e))
        self.DESV_scrRefresh.bind(
            "<Key>", lambda e: app.widgets_SoloLectura(e))
        self.DESV_scrEvidencia.bind(
            "<Key>", lambda e: app.widgets_SoloLectura(e))


## --- SELECCIONAR TOD --- ##
        self.DESV_scrCheck.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESV_scrBackup.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))

## --- BIND --- ##
        self.DESV_entry.bind(
            "<Return>", lambda event=None: self.findModule(self.DESV_entry.get()))
        self.DESV_entry.bind(
            "<KeyPress>", lambda e: self.clear_bsq_buttom(e))
        self.DESV_ListBox.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESV_ListBox.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_ListBox.bind("<Down>", lambda e: self.ListDown(e))
        self.DESV_ListBox.bind("<Up>", lambda e: self.ListUp(e))
        self.DESV_entry.bind(
            '<Control-x>', lambda e: self._clear_busqueda(e))
        self.DESV_entry.bind(
            "<FocusIn>", lambda e: self.clear_busqueda(e))
        self.DESV_entry.bind(
            "<FocusOut>", lambda e: self.clear_busqueda(e))

        self.DESV_scrCheck.bind(
            '<Control-f>', lambda e: self.buscar(e))
        self.DESV_scrBackup.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESV_scrCheck.bind(
            '<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrBackup.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrCheck.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrBackup.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrCheck.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrBackup.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEdit.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESV_scrRefresh.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESV_scrEvidencia.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESV_scrEdit.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrRefresh.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrEvidencia.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrEdit.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrRefresh.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEvidencia.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEdit.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrRefresh.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEvidencia.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEdit.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESV_scrRefresh.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESV_scrEvidencia.bind('<Control-f>', lambda e: self.buscar(e))

## --- DESHABILITAR BOTONES --- ##
        self.activeBtnDir = False
        self.activeBtnAuth = False
        self.activeBtnSer = False
        self.activeBtnAcc = False
        self.activeBtnCmd = False
        self.activeBtnIdr = False

    def DESV_motion(self, event):
        global PST_DESV
        PST_DESV = event.widget
        if activar_modo == 'True':
            app.MODE_DARK()

    def iconos(self):  # TODO ICONOS DE VENTANA DESVIACION
        self.BuscarModulo_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"buscar.png").resize((25, 25)))
        self.LimpiarModulo_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"limpiar.png").resize((25, 25)))
        self.icono_expandir = ImageTk.PhotoImage(
            Image.open(pathIcon+r"expandir.png").resize((40, 40)))
        self.icono_expandir1 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"expandir1.png").resize((40, 40)))
        self.icono_expandir2 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"expandir2.png").resize((40, 40)))
        self.icono_recortar = ImageTk.PhotoImage(
            Image.open(pathIcon+r"recortar.png").resize((40, 40)))
        self.icono_recortar1 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"recortar1.png").resize((40, 40)))
        self.icono_recortar2 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"recortar2.png").resize((40, 40)))
        self.icono_captura = ImageTk.PhotoImage(
            Image.open(pathIcon+r"captura.png").resize((40, 40)))
        self.icono_captura1 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"captura1.png").resize((40, 40)))
        self.icono_captura2 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"captura2.png").resize((40, 40)))
        self.icono_reducir = ImageTk.PhotoImage(
            Image.open(pathIcon+r"reduce.png").resize((30, 30)))
        self.icono_copiar = ImageTk.PhotoImage(
            Image.open(pathIcon+r"copiar.png").resize((40, 40)))
        self.icono_copiar1 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"copiar1.png").resize((40, 40)))
        self.icono_copiar2 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"copiar2.png").resize((40, 40)))
        self.icono_riesgos = ImageTk.PhotoImage(
            Image.open(pathIcon+r"riesgos.png").resize((40, 40)))
        self.icono_riesgos1 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"riesgos1.png").resize((40, 40)))
        self.icono_riesgos2 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"riesgos2.png").resize((40, 40)))

## --- ADJUTAR EL TEXT DE LOS LABEL -------------------------- ##
    def label_resize(self, event):
        event.widget['wraplength'] = event.width

## --- ACTIVAR WIDGET ---------------------------------------- ##
    def _act_focus_ent(self, event):
        self.txtWidget = event.widget
        # self.txtWidget.select_range(0,tk.END)
        self.txtWidget.focus_set()
        self.DESV_scrCheck.tag_remove("sel", "1.0", "end")
        self.DESV_scrBackup.tag_remove("sel", "1.0", "end")
        self.DESV_scrEdit.tag_remove("sel", "1.0", "end")
        self.DESV_scrRefresh.tag_remove("sel", "1.0", "end")
        self.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        return 'break'

    def activar_Focus(self, event):
        global txtWidget
        global txtWidget_focus
        global PST_DESV
        txtWidget = event.widget
        if txtWidget == PST_DESV.DESV_entry:
            txtWidget.focus()
            PST_DESV.DESV_scrCheck.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrBackup.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrEdit.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrRefresh.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        elif txtWidget == PST_DESV.DESV_scrCheck:
            # srcCom = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            PST_DESV.DESV_scrBackup.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrEdit.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrRefresh.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        elif txtWidget == PST_DESV.DESV_scrBackup:
            # srcBac = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == PST_DESV.DESV_scrEdit:
            # srcEdi = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            PST_DESV.DESV_scrCheck.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrBackup.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrRefresh.tag_remove("sel", "1.0", "end")
            PST_DESV.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        elif txtWidget == PST_DESV.DESV_scrRefresh:
            # srcRes = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == PST_DESV.DESV_scrEvidencia:
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

    def cambiar_icono(self, btn, icono1, *args):
        btn['image'] = icono1
        name = btn['text']
        app.openTooltip(btn, name)
        btn.bind('<Leave>', app._hide_event)

## ------ VENTANAS TOP EXPANDIR ------------------------------ ##
    def expandir(self, scrolltext, titulo):  # TODO comprobando expandir
        global expandir
        global sis_oper
        global varNum
        global text_aExpandir
        global value
        global PST_DESV
        global PST_EXP

        index = PST_DESV.DESV_ListBox.curselection()
        VALOR_ACTUAL_LIST = PST_DESV.DESV_ListBox.get(index[0])
        value = VALOR_ACTUAL_LIST
        self.widget_Expan = scrolltext
        tittleExpand = titulo
        customer = PST_DESV.varClient.get()
        self.widget_Expan.focus()
        text_aExpandir = self.widget_Expan.get('1.0', tk.END)
        if tittleExpand == "COMPROBACION":
            varNum = 1
        elif tittleExpand == "BACKUP":
            varNum = 2
        elif tittleExpand == "EDITAR":
            varNum = 3
        elif tittleExpand == "REFRESCAR":
            varNum = 4
        elif tittleExpand == "EVIDENCIA":
            varNum = 5

        # --------- LLAMADA A LA VENTANA EXPANDIR
        expandir = Expandir(self, text_aExpandir, self.widget_Expan, customer, tittleExpand, sis_oper,
                            self.activeBtnDir, self.activeBtnAuth, self.activeBtnSer, self.activeBtnAcc, self.activeBtnCmd, self.activeBtnIdr, varNum)
        #PST_EXP = extracion
        if modo_dark == 'True':
            app.expandirModeDark()
        elif modo_dark == 'False':
            app.expandirModeDefault()

        # ---------------------------------------

        if tittleExpand == "REFRESCAR":
            expandir.EXP_btnCopyALL.config(state="normal")
        elif tittleExpand == "EVIDENCIA":
            varNum = 5
            expandir.EXP_btnScreamEvidencia.config(state="normal")
            expandir.EXP_btnCopyALL.config(state="normal")
        #expandir.vtn_expandir.bind('<Motion>', app.activeDefault)

    def _menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda e=self.DESV_entry: self._buscar(e),
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.copiar_texto_seleccionado,
            state='disabled',
        )

        self.menu_Contextual.add_command(
            label="  Pegar",
            accelerator='Ctrl+V',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            #command=lambda e=self.DESV_entry:self.pegar_texto_seleccionado(e),
        )

        self.menu_Contextual.add_separator(background=bg_submenu)

        self.menu_Contextual.add_command(
            label="  Seleccionar todo",
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda: self.seleccionar_todo(event=None),
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar",
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda e=None: self._clear_busqueda(e),
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña",
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=app.cerrar_vtn_desviacion
        )

    def _display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.scrEvent = event.widget
        self.scrEvent.focus()
        if str(self.scrEvent) == str(self.DESV_entry):
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='normal')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig(
                '  Seleccionar todo', state='disabled')
            if len(self.DESV_entry.get()) > 0:
                self.menu_Contextual.entryconfig('  Limpiar', state='normal')
            else:
                self.menu_Contextual.entryconfig('  Limpiar', state='disabled')
        else:
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Buscar', state='normal')
            self.menu_Contextual.entryconfig(
                '  Seleccionar todo', state='normal')
            self.menu_Contextual.entryconfig(
                '  Cerrar pestaña', state='normal')
            self.menu_Contextual.entryconfig('  Limpiar', state='disabled')
            txt_select = event.widget.tag_ranges(tk.SEL)
            if txt_select:
                self.menu_Contextual.entryconfig("  Copiar", state="normal")
            else:
                self.menu_Contextual.entryconfig("  Copiar", state="disabled")

    def seleccionar_todo(self, event):
        if txtWidget_focus:
            txtWidget.tag_add("sel", "1.0", "end")
            return 'break'

    def _seleccionar_todo(self, event):
        scr_Event = event.widget
        scr_Event.tag_add("sel", "1.0", "end")
        return 'break'

    def copiar_texto_seleccionado(self):
        global txtWidget_focus
        global txtWidget
        if txtWidget_focus:
            seleccion = txtWidget.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(txtWidget.get(*seleccion).strip())
                txtWidget.tag_remove("sel", "1.0", "end")
                return 'break'

    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel", "1.0", "end")
            return 'break'
        else:
            pass

    def buscar(self, event):
        self.DESV_entry.focus()
        self._buscar_Ativate_focus()

    def _buscar_focus(self, event):
        entry_event = event.widget
        entry_event.select_range(0, tk.END)
        entry_event.focus_set()
        return 'break'

    def _buscar_Ativate_focus(self):
        self.DESV_entry.select_range(0, tk.END)
        self.DESV_entry.focus_set()
        return 'break'

    def _buscar(self, event):
        self._buscar_Ativate_focus()

## ------------------------------------- ##
## --- FUNCIONES AL SELECIONAR MODULO, O BUSCAR MODULO ------- ##
    def limpiar_Widgets(self):
        #self.DESV_ListBox.selection_clear(0, tk.END)
        self.DESV_frame2['text'] = 'SISTEMA OPERATIVO'
        self.DESVfr2_lblModulo['text'] = 'MODULO'
        self.DESVfr2_lblDescripcion['text'] = ''
        self.DESV_scrCheck.delete('1.0', tk.END)
        self.DESV_scrBackup.delete('1.0', tk.END)
        self.DESV_scrEdit.delete('1.0', tk.END)
        self.DESV_scrRefresh.delete('1.0', tk.END)
        self.DESV_scrEvidencia.delete('1.0', tk.END)

# --- SELECIONA UN ELEMNETO DEL LIST BOX ACTUAL
    def selectModule(self, event):
        global value
        #PST_DESV.DESV_scrCheck.colourText(PST_DESV.DESV_scrCheck)
        customer = PST_DESV.varClient.get()
        list_event = event.widget
        index = list_event.curselection()
        value = list_event.get(index[0])
        self.loadSelectItem(value, customer)

# --- CARGA ELEMENTO SELECIONADO
    def loadSelectItem(self, selectionValue, customer):  # TODO CARGAR MODULO
        data = []
        with open(pathFiles.format(customer)) as g:
            data = json.load(g)
            for md in data:
                if 'modulo' in md:
                    if selectionValue in md['modulo']:
                        self.limpiar_Widgets()
                        self._asignarValor_aWidgets(md)
                        self.showButtonsModule(selectionValue)

    def _loadSelectItem(self, selectionValue, customer):  # TODO CARGAR MODULO
        data = []
        with open(pathFiles.format(customer)) as g:
            data = json.load(g)
            for md in data:
                if 'modulo'in md:
                    if selectionValue in md['modulo']:
                        self.limpiar_Widgets()
                        self.asignarValor_aWidgets(md)
            self.showButtonsModule(selectionValue)

#  --- ASIGNACION DE VALORES A WIDGETS SRC, AL CAMBIAR DE PESTAÑA
#  --- Y al buscar mas de un modulo en el mismo cliente
    def asignarValor_aWidgets(self, md):
        global sis_oper
        global PST_DESV
        if md['SO'] is not None:
            sis_oper = md['SO']
            PST_DESV.DESV_frame2['text'] = md['SO']
        if md['modulo'] is not None:
            PST_DESV.DESVfr2_lblModulo['text'] = md['modulo']

        if md['descripcion'] is not None:
            PST_DESV.DESVfr2_lblDescripcion['text'] = md['descripcion']

        if md['comprobacion'] is not None:
            PST_DESV.DESV_scrCheck.insert(tk.END, md['comprobacion'])
            PST_DESV.DESV_btn1Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn1Expandir.config(state='disabled')

        if md['copia'] is not None:
            PST_DESV.DESV_scrBackup.insert(tk.END, md['copia'])
            PST_DESV.DESV_btn2Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn2Expandir.config(state='disabled')

        if md['editar'] is not None:
            PST_DESV.DESV_scrEdit.insert(tk.END, md['editar'])
            PST_DESV.DESV_btn3Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn3Expandir.config(state='disabled')

        if md['refrescar'] is not None:
            PST_DESV.DESV_scrRefresh.insert(tk.END, md['refrescar'])
            PST_DESV.DESV_btn4Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn4Expandir.config(state='disabled')

        if md['evidencia'] is not None:
            PST_DESV.DESV_scrEvidencia.insert(tk.END, md['evidencia'])
            PST_DESV.DESV_btn5Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn5Expandir.config(state='disabled')

        #? llamada a colores
        self.llamada_colores()

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
            self.DESV_scrCheck.insert(tk.END, md['comprobacion'])
            self.DESV_btn1Expandir.config(state='normal')
        else:
            self.DESV_btn1Expandir.config(state='disabled')

        if md['copia'] is not None:
            self.DESV_scrBackup.insert(tk.END, md['copia'])
            self.DESV_btn2Expandir.config(state='normal')
        else:
            self.DESV_btn2Expandir.config(state='disabled')

        if md['editar'] is not None:
            self.DESV_scrEdit.insert(tk.END, md['editar'])
            self.DESV_btn3Expandir.config(state='normal')
        else:
            self.DESV_btn3Expandir.config(state='disabled')

        if md['refrescar'] is not None:
            self.DESV_btn4Expandir.config(state='normal')
            self.DESV_scrRefresh.insert(tk.END, md['refrescar'])
        else:
            self.DESV_btn4Expandir.config(state='disabled')

        if md['evidencia'] is not None:
            self.DESV_scrEvidencia.insert(tk.END, md['evidencia'])
            self.DESV_btn5Expandir.config(state='normal')
        else:
            self.DESV_btn5Expandir.config(state='disabled')

        self.llamada_colores()

    def llamada_colores(self):
        if modo_dark == 'False':
            PST_DESV.DESV_scrCheck.colourText(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
            PST_DESV.DESV_scrBackup.colourText(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
            PST_DESV.DESV_scrEdit.colourText(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
            PST_DESV.DESV_scrRefresh.colourText(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
            PST_DESV.DESV_scrEvidencia.colourText(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
        elif modo_dark == 'True':
            PST_DESV.DESV_scrCheck.colourText(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg, pers_colourNoteFg)
            PST_DESV.DESV_scrBackup.colourText(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg, pers_colourNoteFg)
            PST_DESV.DESV_scrEdit.colourText(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg, pers_colourNoteFg)
            PST_DESV.DESV_scrRefresh.colourText(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg, pers_colourNoteFg)
            PST_DESV.DESV_scrEvidencia.colourText(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg, pers_colourNoteFg)

    def showButtonsModule(self, modulo_selecionado):  # TODO añadir demas botones
        global PST_DESV
# --- DIRECTORY ---------------------------------
        if str(modulo_selecionado) == "Protecting Resources-mixed/Ensure sticky bit is set on all world-writable directories" or str(modulo_selecionado) == "Protecting Resources-OSRs/CRON Command WW Permissions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /TMP Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /VAR Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /OPT Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /ETC Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /USR Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/CRON Command Group Permissions":
            self.activeBtnDir = True
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnDirectory.grid(row=2, column=1, padx=5)
# --- AUTHORIZED
        elif str(modulo_selecionado) == "Password Requirements/Private Key File Restriction" or str(modulo_selecionado) == "Identify and Authenticate Users/Public Key Authentication" or str(modulo_selecionado) == "AV.1.1.6 Password Requirements" or str(modulo_selecionado) == "Identify and Authenticate Users/Public Key Label" or str(modulo_selecionado) == "AV.1.1.7 Password Requirements":
            self.activeBtnDir = False
            self.activeBtnAuth = True
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid(row=2, column=1, padx=5)
# --- SERVICE
        elif str(modulo_selecionado) == "Network Settings/Ensure LDAP Server is not enabled" or str(modulo_selecionado) == "Network Settings/NFS root restrictions" or str(modulo_selecionado) == "E.1.5.22.3 Network Settings" or str(modulo_selecionado) == "Password Requirements/SSH PermitRootLogin Restriction" or str(modulo_selecionado) == "Network Settings/Prohibited Processes" or str(modulo_selecionado) == "Identify and Authenticate Users/PermitRootLogin Restriction" or str(modulo_selecionado) == "Network Settings/Disable NFS server":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = True
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnService.grid(row=2, column=1, padx=5)
# --- ACCOUNT
        elif str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow" or str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow - Linux" or str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow - Aix" or str(modulo_selecionado) == "Password Requirements/Password MAX Age" or str(modulo_selecionado) == "AD.1.1.1.2 Password Requirements":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = True
            self.activeBtnCmd = False
            self.activeBtnIdr = False

            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnAccount.grid(row=2, column=1, padx=5)
            PST_DESV.DESV_btnRecortar.grid(row=2, column=2, padx=5)
# --- COMMAND
        elif str(modulo_selecionado) == "protecting Resources-OSRs/SUDO Command WW Permissions":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = True
            self.activeBtnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnCommand.grid(row=2, column=1, padx=5)
# --- ID RSA
        elif str(modulo_selecionado) == "Password Requirements/NULL Passphrase" or str(modulo_selecionado) == "Password Requirements/Private Key Passphrase":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = True
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid(row=2, column=1, padx=5)
# --- MINAGE
        elif str(modulo_selecionado) == "Password Requirements/Password MIN Age Shadow":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = True
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid(
                row=2, column=2, padx=5, pady=10, sticky='ne')
# --- DISABLED ALL
        else:
            self._disabled_buttons()

    def mostrar_buttons_clave(self, keyFound):
        global PST_DESV
# --- DIRECTORY ---------------------------------
        if keyFound == "STICKY" or keyFound == "OSRsCRON" or keyFound == "OSRTMP" or keyFound == "OSRCRON" or keyFound == "OSRVAR" or keyFound == "OSROPT" or keyFound == "OSRETC" or keyFound == "OSRUSR":
            self.activeBtnDir = True
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnDirectory.grid(row=2, column=1, padx=5)
# --- COMMAND
        elif keyFound == "COMMAND":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = True
            self.activeBtnIdr = False
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnCommand.grid(row=2, column=1, padx=5)
# --- ID RSA
        elif keyFound == "IDRSA" or keyFound == "NOT PASSPHRASE":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = True
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid(row=2, column=1, padx=5)
# --- SERVICE
        elif keyFound == "PERMITROOTLOGIN" or keyFound == "LDAP" or keyFound == "PROCESSES" or keyFound == "NFS":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = True
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnService.grid(row=2, column=1, padx=5)
# --- AUTHORIZED
        elif keyFound == "AUTHORIZED_KEY" or keyFound == "PUBLICKEY" or keyFound == "LABEL":
            self.activeBtnDir = False
            self.activeBtnAuth = True
            self.activeBtnSer = False
            self.activeBtnAcc = False
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnRecortar.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid(row=2, column=1, padx=5)
# --- MAXAGE
        elif keyFound == "MAXAGE":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = True
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnAccount.grid(row=2, column=1, padx=5)
            PST_DESV.DESV_btnRecortar.grid(
                row=2, column=2, padx=5, pady=10, sticky='ne')
# --- MINAGE
        elif keyFound == "MINAGE":
            self.activeBtnDir = False
            self.activeBtnAuth = False
            self.activeBtnSer = False
            self.activeBtnAcc = True
            self.activeBtnCmd = False
            self.activeBtnIdr = False
            PST_DESV.DESV_btnDirectory.grid_forget()
            PST_DESV.DESV_btnAuthorized.grid_forget()
            PST_DESV.DESV_btnService.grid_forget()
            PST_DESV.DESV_btnCommand.grid_forget()
            PST_DESV.DESV_btnIdrsa.grid_forget()
            PST_DESV.DESV_btnAccount.grid_forget()
            self.DESV_btnRecortar.grid(
                row=2, column=2, padx=5, pady=10, sticky='ne')
# --- DISABLED ALL
        else:
            self._disabled_buttons()

    def solve(self, moduloBuscado):
        words = moduloBuscado.split()
        if len(words) <= 1:
            full_moduloBuscado = [w.capitalize(
            ) if '/' not in w and w[1:-1].upper() not in w else w[0].upper()+w[1:] for w in words]
        elif len(words) > 1:
            full_moduloBuscado = words
        return ' '.join(full_moduloBuscado)

    def findModule(self, event=None):
        global value
        global no_exist
        global listModulo
        global listKeys
        customer = PST_DESV.varClient.get()
        with open(pathFiles.format(customer)) as g:
            data = json.load(g)
            listModulo = []
            listKeys = []
            for md in data:
                if 'CUSTOMER' in md:
                    pass
                else:
                    listModulo.append(md['modulo'])
                    listKeys.append(md['clave'])
        listModulo.sort()
        #self.moduleLoaded(customer)
        dict_clave_modulo = {}
        valor_aBuscar = event
        keyFound = [n for n in listKeys if valor_aBuscar.upper().strip() in n]

        moduleFound = self.solve(valor_aBuscar)
        moduleFound = [n for n in listModulo if moduleFound.strip().replace("\\", "/") in n]

        self.DESVfr1_btnBuscar.grid_forget()
        self.DESVfr1_btnLimpiar.grid(
            row=1, column=1, pady=5, padx=5, sticky='nsw')

## --- LIMPIAR ------------------------------------- ##
        self.limpiar_Widgets()
        self.enabled_Widgets()
# --------- OBTENER MODULO POR CLAVE O MODULO -------------- ## //TODO "definir si buscar por clave o modulo"
# TODO --- SI NO EXISTE, MODULO O CLAVE
        if len(keyFound) == 0 and len(moduleFound) == 0:
            self.DESV_ListBox.select_clear(tk.ANCHOR)
            self.DESV_entry.focus()
            self._disabled_buttons()
            self.disabled_btn_expandir()
            self.DESV_ListBox.selection_clear(0, tk.END)
            listModuleFound = []
            listKeysFound = []
            MsgBox = mb.askyesno(
                "ERROR", "El modulo no existe en este cliente.\n¿ Deseas buscar en otro cliente ?")
            if MsgBox:
                no_exist = True
                dict_clave_modulo = {}
                listPathCustomer = []
                for client in listClient:
                    listPathCustomer.append(pathFiles.format(client))
                moduleToFind = PST_DESV.DESV_entry.get()
                moduleToFind = self.solve(moduleToFind)
# --- ABRIR TODOS LOS JSON" DE LOS CLIENTESmd_a_buscar
                for openFile in listPathCustomer:
                    try:
                        with open(openFile, 'r', encoding='UTF-8') as fileCustomer:
                            fileJsonCustomer = json.load(fileCustomer)
                        for dataCustomer in fileJsonCustomer:
                            if 'modulo' in dataCustomer:
                                listModuleFound.append(dataCustomer['modulo'])
                                listKeysFound.append(dataCustomer['clave'])
                                moduleFound = [n for n in listModuleFound if moduleToFind.strip().replace("\\", "/") in n]
                                keysFound = [n for n in listKeysFound if moduleToFind.upper() in n]
                                self.addNewModuleFound(dict_clave_modulo, moduleFound, dataCustomer,openFile)
                                self.addNewKeysFound(dict_clave_modulo, keysFound, dataCustomer,openFile)
                    except FileNotFoundError:
                        mb.showerror("No such file or directory!.\nPlease create a new CUST file")
# SI EL MODULO EXISTE EN ALGUN CLIENTE QUE NOS MUESTRE EN UNA VENTANA
                if len(dict_clave_modulo) == 0:
                    mb.showinfo("INFORMACION", "No existe el modulo, en ningun cliente !!")
                else:
                    titulo = 'LISTA DE MODULOS ENCONTRADOS, EN LOS SIGUIENTES CLIENTES'
                    textsimilar = TextSimilar(
                        self, titulo, dict_clave_modulo, customer)
            else:
                no_exist = False
            return 'break'
# TODO --- POR CLAVE UNICA
        elif len(keyFound) == 1 and len(moduleFound) == 0:
            data = []
            no_exist = False
            keyFound = str(keyFound).replace(
                "[", "").replace("]", "").replace("'", "")
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'clave' in md:
                        if keyFound in md['clave']:
                            self.limpiar_Widgets()
                            # self.enabled_Widgets()
                            value = md['modulo']
                            self.asignarValor_aWidgets(md)
                            self.mostrar_buttons_clave(keyFound)
                self.DESV_ListBox.selection_clear(0, tk.END)
                moduleLoaded = self.DESV_ListBox.get(0, tk.END)
                index = moduleLoaded.index(value)
                self.DESV_ListBox.selection_set(index)
                return 'break'
# TODO --- SI EXISTEN MAS DE UNA CLAVE
        elif len(keyFound) > 1 and len(moduleFound) == 0:
            data = []
            no_exist = False
            self.DESV_ListBox.selection_clear(0, tk.END)
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    for n in keyFound:
                        if 'clave' in md:
                            if n in md['clave']:
                                dict_clave_modulo[md['modulo']
                                                ] = md['clave'], md['SO']
                titulo = 'LISTA DE MODULOS ENCONTRADOS, SEGUN SU CRITERIO DE BUSQUEDA, en {}'.format(
                    customer)
                textsimilar = TextSimilar(
                    self, titulo, dict_clave_modulo, customer)
                return 'break'
# TODO --- SI ES MODULO UNICO
        elif len(moduleFound) == 1 and len(keyFound) == 0:
            data = []
            no_exist = False
            moduleFound = str(moduleFound).replace(
                "[", "").replace("]", "").replace("'", "")
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if moduleFound in md['modulo']:
                            value = md['modulo']
                            self.asignarValor_aWidgets(md)
                self.showButtonsModule(moduleFound)
                self.DESV_ListBox.selection_clear(0, tk.END)
                moduleLoaded = self.DESV_ListBox.get(0, tk.END)
                index = moduleLoaded.index(value)
                self.DESV_ListBox.selection_set(index)
                return 'break'
# TODO --- SI HAY MAS DE UN MODULO
        elif len(moduleFound) > 1 and len(keyFound) == 0:
            data = []
            no_exist = False
            self.DESV_ListBox.selection_clear(0, tk.END)
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    for n in moduleFound:
                        if 'modulo' in md:
                            if n in md['modulo']:
                                dict_clave_modulo[md['modulo']
                                                ] = md['clave'], md['SO']
                titulo = 'LISTA DE MODULOS ENCONTRADOS, SEGUN SU CRITERIO DE BUSQUEDA, en {}'.format(
                    customer)
                textsimilar = TextSimilar(
                    self, titulo, dict_clave_modulo, customer)
                return 'break'
# TODO --- SI EXISTE UN MODULO Y UNA CLAVE
        else:
            data = []
            no_exist = False
            self.DESV_ListBox.selection_clear(0, tk.END)
            with open(pathFiles.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    for n in moduleFound:
                        if 'modulo' in md:
                            if n in md['modulo']:
                                dict_clave_modulo[md['modulo']
                                                ] = md['clave'], md['SO']
                    for n in keyFound:
                        if 'clave' in md:
                            if n in md['clave']:
                                dict_clave_modulo[md['modulo']
                                                ] = md['clave'], md['SO']
                titulo = 'LISTA DE MODULOS ENCONTRADOS, SEGUN SU CRITERIO DE BUSQUEDA, en {}'.format(
                    customer)
                textsimilar = TextSimilar(
                    self, titulo, dict_clave_modulo, customer)
                return 'break'

    def _add_newList_clt(self, dict_clave_modulo, _md_Buscado, ln_clt, CUST):
        for n in _md_Buscado:
            if n in ln_clt['modulo']:
                dict_clave_modulo[ln_clt['modulo']] = ln_clt['clave'], CUST

    def addNewModuleFound(self, dict_clave_modulo, _md_Buscado, ln_clt, file):
        CUST = ""
        for n in _md_Buscado:
            if 'CUSTOMER' in ln_clt:
                pass
            else:
                if n in ln_clt['modulo']:
                    with open(file, 'r') as fileopen:
                        data = json.load(fileopen)
                        for md in data:
                            if 'CUSTOMER' in md:
                                CUST = md['CUSTOMER']
                    dict_clave_modulo[ln_clt['modulo']] = ln_clt['clave'], CUST

    def addNewKeysFound(self, dict_clave_, _clv_Buscado, ln_clt, file):
        CUST = ""
        for n in _clv_Buscado:
            if 'CUSTOMER' in ln_clt:
                pass
            else:
                if n in ln_clt['clave']:
                    with open(file, 'r') as fileopen:
                        data = json.load(fileopen)
                        for md in data:
                            if 'CUSTOMER' in md:
                                CUST = md['CUSTOMER']
                    dict_clave_[ln_clt['modulo']] = ln_clt['clave'], CUST

    def _add_newList_clt_clv(self, dict_clave_modulo, _clv_Buscado, ln_clt, CUST):
        for n in _clv_Buscado:
            if n in ln_clt['clave']:
                dict_clave_modulo[ln_clt['modulo']] = ln_clt['clave'], CUST

    def _clear_busqueda(self, event):
        self.var_entry_bsc.set("")
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(
            row=1, column=1, pady=5, padx=5, sticky='nsw')

    def clear_busqueda(self, event):
        text_widget = event.widget
        entry = self.var_entry_bsc.get()
        if entry == "":
            text_widget.icursor(0)
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(
                row=1, column=1, pady=5, padx=5, sticky='nsw')

    def clear_bsq_buttom(self, event):
        entry = self.var_entry_bsc.get()
        long_entry = len(entry)
        if long_entry <= 1:
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(
                row=1, column=1, pady=5, padx=5, sticky='nsw')

    def limpiar_busqueda(self):
        widget_event = self.DESV_entry
        widget_event.delete(0, tk.END)
        widget_event.focus()
        widget_event.icursor(0)
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(
            row=1, column=1, pady=5, padx=5, sticky='nsw')

    def ListDown(self, event):
        list_event = event.widget
        list_event.yview_scroll(1, "units")
        selecion = list_event.curselection()[0]+1
        modulo_selecionado = list_event.get(selecion)
        customer =  PST_DESV.varClient.get()
        self.loadSelectItem(modulo_selecionado, customer)

    def ListUp(self, event):
        list_event = event.widget
        list_event.yview_scroll(-1, "units")
        selecion = list_event.curselection()[0]-1
        modulo_selecionado = list_event.get(selecion)
        customer =  PST_DESV.varClient.get()
        self.loadSelectItem(modulo_selecionado, customer)

    def enabled_Widgets(self):
        self.DESV_ListBox.config(state="normal")
        self.DESV_entry.config(state="normal")
        self.DESV_entry.focus()
        self.DESVfr1_btnBuscar.config(state="normal")
        self.DESV_scrCheck.config(state="normal")
        self.DESV_scrBackup.config(state="normal")
        self.DESV_scrEdit.config(state="normal")
        self.DESV_scrRefresh.config(state="normal")
        self.DESV_scrEvidencia.config(state="normal")
        self.DESV_btnRiskImpact.config(state='normal')
        self.DESV_btn1Expandir.config(state='normal')
        self.DESV_btn2Expandir.config(state='normal')
        self.DESV_btn3Expandir.config(state='normal')
        self.DESV_btn4Expandir.config(state='normal')
        self.DESV_btn5Expandir.config(state='normal')
        self.DESV_btnScreamEvidencia.config(state='normal')
        self.DESV_btnCopyALL.config(state='normal')
        self.DESV_btn1CopyALL.config(state='normal')

    def loadModule(self, clt_modulo=None, *args):
        global listModulo
        global listKeys
        self.enabled_Widgets()
        customer = clt_modulo
        self.varClient.set(customer)
        self.renameNameTab(customer)
        # --- LIMPIAR -----------------------------
        self.DESV_entry.delete(0, tk.END)
        self.DESV_ListBox.delete(0, tk.END)
        self.limpiar_Widgets()
        self._disabled_buttons()
        self.disabled_btn_expandir()
        ## ----------------------------------------- ##
        with open(pathFiles.format(customer)) as g:
            data = json.load(g)
            listModulo = []
            listKeys = []
            for md in data:
                if 'CUSTOMER' in md:
                    pass
                else:
                    listModulo.append(md['modulo'])
                    listKeys.append(md['clave'])
        listModulo.sort()
        self.DESV_ListBox.insert(tk.END, *listModulo)

    def _disabled_buttons(self):
        global PST_DESV
        self.activeBtnDir = False
        self.activeBtnAuth = False
        self.activeBtnSer = False
        self.activeBtnAcc = False
        self.activeBtnCmd = False
        self.activeBtnIdr = False
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

    def ScreamEvidencia(self):
        #app.root.withdraw()
        os.popen('gtk-launch capture.desktop')
        time.sleep(2)
        #app.root.deiconify()

    def Risk_Impact(self):
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, pathRisk.format("RISK_IMPACT.ods")])

    def RecortarMinMax(self):
        recortar = mypath+"Compliance/recortar.sh"
        os.popen("gnome-terminal -e "+recortar)

    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel", "1.0", "end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel", "1.0", "end")

    def WIDGETS_DESVIACION(self):
        from DataExtraction import MyEntry, MyScrollText

# --- DEFINIMOS LOS LABEL FRAMEs, QUE CONTENDRAN LOS WIDGETS --------------------------#
        self.DESV_frame1 = ttk.LabelFrame(
            self,
            text="CLIENTE / MODULO",
            relief='groove'
        )
        self.DESV_frame1.grid_propagate(False)
        self.DESV_frame1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        self.DESV_frame2 = ttk.LabelFrame(
            self,
            text="SISTEMA OPERATIVO",
            relief='groove'
        )
        self.DESV_frame2.grid_propagate(False)
        self.DESV_frame2.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')

        self.DESV_frame3 = ttk.LabelFrame(
            self,
            text="EDITAR / EVIDENCIA",
            relief='groove'
        )
        self.DESV_frame3.grid_propagate(False)
        self.DESV_frame3.grid(column=2, row=0, padx=10, pady=10, sticky='nsew')

# -----------------------------------------------------------------------------#
        self.DESV_frame2.columnconfigure(0, weight=1)
        self.DESV_frame2.rowconfigure(3, weight=1)
        self.DESV_frame2.rowconfigure(5, weight=1)

        self.DESV_frame1.columnconfigure(0, weight=1)
        self.DESV_frame3.columnconfigure(0, weight=1)

        self.DESV_frame1.rowconfigure(2, weight=1)
        self.DESV_frame3.rowconfigure(1, weight=1)
        self.DESV_frame3.rowconfigure(3, weight=1)
        self.DESV_frame3.rowconfigure(5, weight=1)
        # --- Variable del OptionMenu, lista de clientes ------------------------------#
        self.varClient = tk.StringVar(self)
        self.varClient.set('CLIENTES')
        #-----------------------------------------------------------------------------#
        ## ======================== FRAME 1 ========================================= ##
        # ---------------- OptionMenu, lista de clientes ---------------------------- ##
        self.DESV_OptionMenu = tk.OptionMenu(
            self.DESV_frame1,
            self.varClient,
            *listClient,
            command=self.loadModule,
        )
        self.DESV_OptionMenu.config(
            justify=tk.CENTER,
            anchor=tk.CENTER,
            background=default_menu_bg,
            foreground=default_menu_fg,
            font=app._Font_Titulo_bold,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            relief="groove",
            borderwidth=0,
            width=20
        )
        self.DESV_OptionMenu["menu"].config(
            background=bg_submenu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            foreground=fg_submenu,
            font=_Font_Texto,
        )
        self.DESV_OptionMenu.grid(row=0, column=0, padx=5,
                                pady=5, sticky='new', columnspan=2)

# -----------------------------------------------------------------------------#
# TODO --- ENTRY DE BUSQUEDA
        self.var_entry_bsc = tk.StringVar(self)
        self.DESV_entry = MyEntry(
            self.DESV_frame1,
            textvariable=self.var_entry_bsc,
        )
        self.DESV_entry.configure(
            state='disabled'
        )
        self.DESV_entry.grid(
            row=1, column=0, pady=5, ipady=8, padx=(5, 0), sticky='nsew')

# TODO --- BOTON BUSCAR DESVIACION
        self.DESVfr1_btnBuscar = ttk.Button(
            self.DESV_frame1,
            image=self.BuscarModulo_icon,
            state='disabled',
            command=lambda: self.findModule(self.DESV_entry.get()),
        )
        self.DESVfr1_btnBuscar.grid(
            row=1, column=1, pady=5, padx=5, sticky='nsw')

# TODO --- BOTON LIMPIAR BUSQUEDA
        self.DESVfr1_btnLimpiar = ttk.Button(
            self.DESV_frame1,
            image=self.LimpiarModulo_icon,
            command=self.limpiar_busqueda,
        )
        # -----------------------------------------------------------------------------#

# TODO --- LISTA DE CLIENTE, EN LISTBOX
        self.DESVlist_yScroll = tk.Scrollbar(
            self.DESV_frame1,
            orient=tk.VERTICAL)
        self.DESVlist_xScroll = tk.Scrollbar(
            self.DESV_frame1, orient=tk.HORIZONTAL)

        self.DESV_ListBox = tk.Listbox(
            self.DESV_frame1,
            state='disabled',
            xscrollcommand=self.DESVlist_xScroll.set,
            yscrollcommand=self.DESVlist_yScroll.set,
            font=_Font_Texto,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            exportselection=False,
            highlightthickness=hhtk,
            highlightcolor=default_hglcolor,
        )
        self.DESV_ListBox.grid(row=2, column=0, pady=(
            5, 12), padx=(5, 12), sticky='nsew', columnspan=2)

        self.DESVlist_yScroll.grid(row=2, column=0, pady=(
            5, 15), sticky='nse', columnspan=2)
        self.DESVlist_xScroll.grid(
            row=2, column=0, padx=5, sticky='sew', columnspan=2)

        self.DESVlist_xScroll['command'] = self.DESV_ListBox.xview
        self.DESVlist_yScroll['command'] = self.DESV_ListBox.yview
## ======================== FRAME 2 ========================================= #
        # --- MODULO ----------------------------------------------------------------------------------------------------
        self.DESVfr2_lblModulo = ttk.Label(
            self.DESV_frame2,
            text='MODULO',
        )
        self.DESVfr2_lblModulo.grid(
            row=0, column=0, padx=10, pady=5, sticky='ew', columnspan=5)

        # --- Descripcion ----------------------------------------------------------------------------------------------------
        self.DESVfr2_lblDescripcion = ttk.Label(
            self.DESV_frame2,
            foreground='gray60',
            font=_Font_Texto,
        )
        self.DESVfr2_lblDescripcion.grid(
            row=1, column=0, padx=10, pady=5, sticky='new', columnspan=5)

        # --- Comprobacion---------------------------------------------------------------------------------------------------------
        self.DESVfr2_lblComprobacion = ttk.Label(
            self.DESV_frame2,
            text='COMPROBACIÓN',
        )
        self.DESVfr2_lblComprobacion.grid(
            row=2, column=0, padx=5, pady=5, sticky='ew')

        self.DESV_btnDirectory = RadioButton(
            self.DESV_frame2,
            alto=Desviacion.y_alto_btn,
            ancho=Desviacion.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btnDir_ = ttk.Button(
            self.DESV_btnDirectory,
            text='Permissions  ',
            compound=tk.RIGHT,
            image=self.icono_expandir,
            style='APP.TButton',
            command=self.abrir_DIRECTORY,
        )
        self._btnDir_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Desviacion.hg_btn,
            width=Desviacion.wd_btn
        )

        self.DESV_btnService = RadioButton(
            self.DESV_frame2,
            alto=Desviacion.y_alto_btn,
            ancho=Desviacion.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btnSer_ = ttk.Button(
            self.DESV_btnService,
            text='Service  ',
            compound=tk.RIGHT,
            image=self.icono_expandir,
            style='APP.TButton',
            command=self.abrir_SERVICE,
        )
        self._btnSer_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Desviacion.hg_btn,
            width=Desviacion.wd_btn
        )

        self.DESV_btnAuthorized = RadioButton(
            self.DESV_frame2,
            alto=Desviacion.y_alto_btn,
            ancho=Desviacion.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btnAuth_ = ttk.Button(
            self.DESV_btnAuthorized,
            text='Authorized  ',
            compound=tk.RIGHT,
            image=self.icono_expandir,
            style='APP.TButton',
            command=self.abrir_AUTHORIZED,
        )
        self._btnAuth_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Desviacion.hg_btn,
            width=Desviacion.wd_btn
        )

        self.DESV_btnAccount = RadioButton(
            self.DESV_frame2,
            alto=Desviacion.y_alto_btn,
            ancho=Desviacion.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btnAcc_ = ttk.Button(
            self.DESV_btnAccount,
            text='Account  ',
            compound=tk.RIGHT,
            image=app.icono_account,
            style='APP.TButton',
            command=self.abrir_ACCOUNT,
        )
        self._btnAcc_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Desviacion.hg_btn,
            width=Desviacion.wd_btn
        )

        self.DESV_btnCommand = RadioButton(
            self.DESV_frame2,
            alto=Desviacion.y_alto_btn,
            ancho=Desviacion.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=default_bottom_app,
        )
        self._btnComm_ = ttk.Button(
            self.DESV_btnCommand,
            text='Command  ',
            compound=tk.RIGHT,
            image=self.icono_expandir,
            style='APP.TButton',
            command=self.abrir_COMMAND,
        )
        self._btnComm_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Desviacion.hg_btn,
            width=Desviacion.wd_btn
        )

        self.DESV_btnIdrsa = RadioButton(
            self.DESV_frame2,
            alto=Desviacion.y_alto_btn,
            ancho=Desviacion.x_ancho_btn,
            radio=25,
            width=3,
            bg_color=None,
        )
        self._btnIdr_ = ttk.Button(
            self.DESV_btnIdrsa,
            text='Id_Rsa  ',
            compound=tk.RIGHT,
            image=self.icono_expandir,
            style='APP.TButton',
            command=self.abrir_IDRSA,
        )
        self._btnIdr_.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Desviacion.hg_btn,
            width=Desviacion.wd_btn
        )

        self.DESV_btnRecortar = ttk.Button(
            self.DESV_frame2,
            text='Script Cut Text',
            image=self.icono_recortar,
            style='APP.TButton',
            command=self.RecortarMinMax,
        )

        self.DESV_scrCheck = MyScrollText(self.DESV_frame2, app)
        # self.DESV_scrCheck.config(
        #     font=_Font_Texto,
        #     wrap=tk.WORD,
        #     highlightcolor=default_hglcolor,
        #     borderwidth=0,
        #     highlightbackground=default_Framework,
        #     highlightthickness=hhtk,
        #     insertbackground=default_hglcolor,
        #     insertwidth=hlh_def,
        #     selectbackground=default_select_bg,
        #     selectforeground=default_select_fg,
        #     background=default_scrText_bg,
        #     foreground=default_scrText_fg,
        #     state='disabled',
        # )
        self.DESV_scrCheck.grid(
            row=3, column=0, padx=5, pady=5, sticky='new', columnspan=5)
        self.DESV_btnRiskImpact = ttk.Button(
            self.DESV_frame2,
            text="Risk e Impact",
            image=self.icono_riesgos,
            state='disabled',
            style='APP.TButton',
            command=self.Risk_Impact,
        )
        self.DESV_btnRiskImpact.grid(
            row=2, column=3, padx=5, pady=10, sticky='ne')

        self.varComprobacion = "COMPROBACION"
        self.DESV_btn1Expandir = ttk.Button(
            self.DESV_frame2,
            text="Expand CHECK",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=partial(self.expandir, self.DESV_scrCheck, self.varComprobacion),
            #command=lambda x=self.DESV_scrCheck: self.expandir(x, self.varComprobacion),
        )
        self.DESV_btn1Expandir.grid(
            row=2, column=4, padx=(0, 20), pady=10, sticky='ne')

# --- BACKUP ----------------------------------------------------------------------------------------------------
        self.DESVfr2_lblBackup = ttk.Label(
            self.DESV_frame2,
            text='BACKUP',
        )
        self.DESVfr2_lblBackup.grid(
            row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=4)

        self.DESV_scrBackup = MyScrollText(
            self.DESV_frame2,
            app
        )
        
        self.DESV_scrBackup.grid(
            row=5, column=0, padx=5, pady=5, sticky='new', columnspan=5)

        self.varBackup = "BACKUP"
        self.DESV_btn2Expandir = ttk.Button(
            self.DESV_frame2,
            text="Expand BACKUP",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=lambda x=self.DESV_scrBackup: self.expandir(
                x, self.varBackup),
        )
        self.DESV_btn2Expandir.grid(row=4, column=4, padx=(
            5, 20), pady=5)


## ======================== FRAME 3 ========================================= ##
## --- EDITAR
        self.DESVfr3_lblEditar = ttk.Label(
            self.DESV_frame3,
            text='EDITAR ✍'
        )
        self.DESVfr3_lblEditar.grid(
            row=0, column=0, padx=5, pady=5, sticky='w')

        self.DESV_scrEdit = MyScrollText(self.DESV_frame3, app)
            
        self.DESV_scrEdit.grid(
            row=1, column=0, padx=5, pady=5, sticky='new', columnspan=4)

        self.varEditar = "EDITAR"
        self.DESV_btn3Expandir = ttk.Button(
            self.DESV_frame3,
            text="Expand EDIT",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=lambda x=self.DESV_scrEdit: self.expandir(
                x, self.varEditar),
        )
        self.DESV_btn3Expandir.grid(row=0, column=1, padx=(
            5, 20), pady=5, sticky='ne', columnspan=4)

        ## --- REFEESCAR
        self.DESVfr3_lblRefrescar = ttk.Label(
            self.DESV_frame3,
            text='REFRESCAR'
        )
        self.DESVfr3_lblRefrescar.grid(
            row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)

        self.DESV_scrRefresh = MyScrollText(self.DESV_frame3, app)
        self.DESV_scrRefresh.grid(
            row=3, column=0, padx=5, pady=5, sticky='new', columnspan=4)

        self.DESV_btn1CopyALL = ttk.Button(
            self.DESV_frame3,
            text="Copy All Refresh",
            image=self.icono_copiar,
            style='APP.TButton',
            state='disabled',
            command=lambda e=self.DESV_scrRefresh: self.copiarALL(e),
        )
        self.DESV_btn1CopyALL.grid(row=2, column=2, padx=5, pady=5, sticky='e')

        self.varRefrescar = "REFRESCAR"
        self.DESV_btn4Expandir = ttk.Button(
            self.DESV_frame3,
            text="Expand Refresh",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=lambda x=self.DESV_scrRefresh: self.expandir(
                x, self.varRefrescar),
        )
        self.DESV_btn4Expandir.grid(
            row=2, column=3, padx=(5, 20), pady=5, sticky='e')

        ## --- EVIDENCIA
        self.DESVfr3_lblEvidencia = ttk.Label(
            self.DESV_frame3,
            text='EVIDENCIA'
        )
        self.DESVfr3_lblEvidencia.grid(
            row=4, column=0, padx=5, pady=5, sticky='w')

        self.DESV_scrEvidencia = MyScrollText(self.DESV_frame3, app)
        self.DESV_scrEvidencia.grid(
            row=5, column=0, padx=5, pady=5, sticky='new', columnspan=4)

        self.DESV_btnCopyALL = ttk.Button(
            self.DESV_frame3,
            text="Copy All Evidence",
            image=self.icono_copiar,
            style='APP.TButton',
            state='disabled',
            command=lambda e=self.DESV_scrEvidencia: self.copiarALL(e),
        )
        self.DESV_btnCopyALL.grid(
            row=4, column=1, padx=(20, 5), pady=5, sticky='ne')

        self.DESV_btnScreamEvidencia = ttk.Button(
            self.DESV_frame3,
            text="Screem Shot",
            image=self.icono_captura,
            style='APP.TButton',
            state='disabled',
            command=self.ScreamEvidencia,
        )
        self.DESV_btnScreamEvidencia.grid(
            row=4, column=2, padx=5, pady=5, sticky='ne')

        self.varEvidencia = "EVIDENCIA"
        self.DESV_btn5Expandir = ttk.Button(
            self.DESV_frame3,
            text="Expand EVIDENCE",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=lambda x=self.DESV_scrEvidencia: self.expandir(
                x, self.varEvidencia),
        )
        self.DESV_btn5Expandir.grid(
            row=4, column=3, padx=(5, 20), pady=5, sticky='ne')

        # self.DESVfr2_lblDescripcion.bind('<Motion>', app.activeDefault)
        # self.DESVfr2_lblComprobacion.bind('<Motion>', app.activeDefault)
        # self.DESVfr2_lblBackup.bind('<Motion>', app.activeDefault)
        # self.DESV_scrCheck.bind('<Motion>', app.activeDefault)
        # self.DESV_scrBackup.bind('<Motion>', app.activeDefault)
        # self.DESVfr3_lblEditar.bind('<Motion>', app.activeDefault)
        # self.DESVfr3_lblEvidencia.bind('<Motion>', app.activeDefault)
        # self.DESVfr3_lblRefrescar.bind('<Motion>', app.activeDefault)
        # self.DESV_scrEdit.bind('<Motion>', app.activeDefault)
        # self.DESV_scrEvidencia.bind('<Motion>', app.activeDefault)
        # self.DESV_scrRefresh.bind('<Motion>', app.activeDefault)

        # self.DESV_frame1.bind('<Motion>', app.activeDefault)
        # self.DESV_frame2.bind('<Motion>', app.activeDefault)
        # self.DESV_frame3.bind('<Motion>', app.activeDefault)

        self.DESV_btnRecortar.bind("<Leave>", app._hide_event)
        self.DESV_btnRiskImpact.bind("<Leave>", app._hide_event)
        self.DESV_btnCopyALL.bind("<Leave>", app._hide_event)
        self.DESV_btn1CopyALL.bind("<Leave>", app._hide_event)
        self.DESV_btnScreamEvidencia.bind("<Leave>", app._hide_event)
        self.DESV_btn1Expandir.bind("<Leave>", app._hide_event)
        self.DESV_btn2Expandir.bind("<Leave>", app._hide_event)
        self.DESV_btn3Expandir.bind("<Leave>", app._hide_event)
        self.DESV_btn4Expandir.bind("<Leave>", app._hide_event)
        self.DESV_btn5Expandir.bind("<Leave>", app._hide_event)
        self._btnAcc_.bind("<Leave>", app._hide_event)
        self._btnAuth_.bind("<Leave>", app._hide_event)
        self._btnDir_.bind("<Leave>", app._hide_event)
        self._btnIdr_.bind("<Leave>", app._hide_event)
        self._btnComm_.bind("<Leave>", app._hide_event)
        self._btnSer_.bind("<Leave>", app._hide_event)

        self.asignar_iconos()
        self.changeColorActiveToolTipRB()

    def _QuitarSeleccion_(self):
        global list_motion
        global txtWidget
        PST_DESV.DESV_frame2['text'] = 'SISTEMA OPERATIVO'
        PST_DESV.DESVfr2_lblDescripcion['text'] = ''
        PST_DESV.DESV_scrCheck.delete('1.0', tk.END)
        PST_DESV.DESV_scrBackup.delete('1.0', tk.END)
        PST_DESV.DESV_scrEdit.delete('1.0', tk.END)
        PST_DESV.DESV_scrRefresh.delete('1.0', tk.END)
        PST_DESV.DESV_scrEvidencia.delete('1.0', tk.END)
        PST_DESV.DESVfr2_lblModulo['text'] = 'MODULO'

        if list_motion:
            list_motion.selection_clear(0, tk.END)
            self.limpiar_Widgets()

    def abrir_DIRECTORY(self):
        from Ventanas import Ventana
        global PST_VTN
        name_vtn = "PERMISSIONS"
        path = "Compliance/file/directory.json"
        customer = PST_DESV.varClient.get()
        PST_VTN = Ventana(
            self,
            name_vtn, customer,
            app,
            desviacion,
            path
        )
        if modo_dark == 'True':
            app.windowModeDark()
        else:
            app.windowModeDefault()

    def abrir_COMMAND(self):
        from Ventanas import Ventana
        global PST_VTN
        name_vtn = "COMMAND"
        path = "Compliance/file/command.json"
        customer = PST_DESV.varClient.get()
        PST_VTN = Ventana(
            self,
            name_vtn,
            customer,
            app,
            desviacion,
            path
        )
        if modo_dark == 'True':
            app.windowModeDark()
        else:
            app.windowModeDefault()

    def abrir_AUTHORIZED(self):
        from Ventanas import Ventana
        global PST_VTN
        name_vtn = "AUTHORIZED"
        path = "Compliance/file/authorized_keys.json"
        customer = PST_DESV.varClient.get()
        PST_VTN = Ventana(
            self,
            name_vtn,
            customer,
            app,
            desviacion,
            path
        )
        if modo_dark == 'True':
            app.windowModeDark()
        else:
            app.windowModeDefault()

    def abrir_ACCOUNT(self):
        from Ventanas import Ventana
        global PST_VTN
        name_vtn = "ACCOUNT"
        path = "Compliance/file/account.json"
        customer = PST_DESV.varClient.get()
        PST_VTN = Ventana(
            self,
            name_vtn,
            customer,
            app,
            desviacion,
            path
        )
        if modo_dark == 'True':
            app.windowModeDark()
        else:
            app.windowModeDefault()

    def abrir_SERVICE(self):
        from Ventanas import Ventana
        global PST_VTN
        name_vtn = "SERVICE"
        path = "Compliance/file/service.json"
        customer = PST_DESV.varClient.get()
        PST_VTN = Ventana(
            self,
            name_vtn,
            customer,
            app,
            desviacion,
            path
        )
        if modo_dark == 'True':
            app.windowModeDark()
        else:
            app.windowModeDefault()

    def abrir_IDRSA(self):
        from Ventanas import Ventana
        global PST_VTN
        name_vtn = "ID_RSA"
        path = "Compliance/file/idrsa.json"
        customer = PST_DESV.varClient.get()
        PST_VTN = Ventana(
            self,
            name_vtn,
            customer,
            app,
            desviacion,
            path
        )
        if modo_dark == 'True':
            app.windowModeDark()
        else:
            app.windowModeDefault()

    def renameNameTab(self, customer):
        app.cuaderno.tab(idOpenTab, option=None, text='DESVIACIONES : {} '.format(customer))
        app.cuaderno.notebookContent.tab(idOpenTab, option=None, text='DESVIACIONES : {} '.format(customer))

    def asignar_iconos(self):
        if modo_dark == 'False':
            icon_rec = self.icono_recortar1
            icon_risk = self.icono_riesgos1
            icon_exp = self.icono_expandir1
            icon_cap = self.icono_captura1
            icon_copy = self.icono_copiar1
        elif modo_dark == 'True':
            icon_rec = self.icono_recortar2
            icon_risk = self.icono_riesgos2
            icon_exp = self.icono_expandir2
            icon_cap = self.icono_captura2
            icon_copy = self.icono_copiar2

        self.DESV_btnRecortar.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btnRecortar, icon_rec, self.icono_recortar2))
        self.DESV_btnRiskImpact.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btnRiskImpact, icon_risk))
        self.DESV_btn1Expandir.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btn1Expandir, icon_exp))
        self.DESV_btn2Expandir.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btn2Expandir, icon_exp))
        self.DESV_btn3Expandir.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btn3Expandir, icon_exp))
        self.DESV_btn4Expandir.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btn4Expandir, icon_exp))
        self.DESV_btn5Expandir.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btn5Expandir, icon_exp))
        self.DESV_btnScreamEvidencia.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btnScreamEvidencia, icon_cap))
        self.DESV_btnCopyALL.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btnCopyALL, icon_copy))
        self.DESV_btn1CopyALL.bind('<Motion>', partial(
            self.cambiar_icono, self.DESV_btn1CopyALL, icon_copy))

    def changeColorActiveToolTipRB(self):
        self._btnDir_.bind('<Motion>', partial(
            app.active_radio_botton, self.DESV_btnDirectory, self._btnDir_))
        self._btnSer_.bind('<Motion>', partial(
            app.active_radio_botton, self.DESV_btnService, self._btnSer_))
        self._btnAuth_.bind('<Motion>', partial(
            app.active_radio_botton, self.DESV_btnAuthorized, self._btnAuth_))
        self._btnAcc_.bind('<Motion>', partial(
            app.active_radio_botton, self.DESV_btnAccount, self._btnAcc_))
        self._btnComm_.bind('<Motion>', partial(
            app.active_radio_botton, self.DESV_btnCommand, self._btnComm_))
        self._btnIdr_.bind('<Motion>', partial(
            app.active_radio_botton, self.DESV_btnIdrsa, self._btnIdr_))

class Aplicacion():
    #Ancho y Alto de la APP
    WIDTH = 1360
    HEIGHT = 650

    #Tamaño del borde y boton para los radios button
    y_alto_btn = 200
    x_ancho_btn = 250
    hg_btn = int(y_alto_btn-30)
    wd_btn = int(x_ancho_btn-30)
    def __init__(self):
        self.root = tk.Tk()
        self._Font_Titulo_bold = font.Font(family=fuente_titulos, size=tamñ_titulo, weight=weight_DF)
        self.root.title("CONTINUOUS COMPLIANCE")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height/2 - Aplicacion.HEIGHT/2)
        position_right = int(screen_width/2 - Aplicacion.WIDTH/2)
        self.root.geometry(
            f'{Aplicacion.WIDTH}x{Aplicacion.HEIGHT}+{position_top}+{position_right}')
        #self.root.minsize(Aplicacion.WIDTH, Aplicacion.HEIGHT)
        self.root.configure(background=default_bottom_app, borderwidth=0, border=0)
        self.root.tk.call('wm', 'iconphoto', self.root._w,tk.PhotoImage(file=pathIcon+r'compliance.png'))
        self.openCustomer()
        self.iconos()
        self.cuaderno = ScrollableNotebook(self.root, wheelscroll=False, tabmenu=True, application=self)
        self.contenedor = ttk.Frame(self.cuaderno)
        self.contenedor.config(borderwidth=1,border=1)
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        self.cuaderno.add(self.contenedor, text='WorkSpace  ', underline=0, image=self.iconoWorkSpace, compound=tk.LEFT)
        self.cuaderno.grid(row=0, column=0, sticky='nsew')
        self.cuaderno.bind_all("<<NotebookTabChanged>>",lambda e: self.toChangeTab(e))
        self.cuaderno.enable_traversal()
        self.cuaderno.notebookTab.bind("<Button-3>", self.display_menu_clickDerecho)
        self.cuaderno.bind("<Button-3>", self._display_menu_clickDerecho)
        self.root.focus_set()
        self.estilos()
        self.menu_clickDerecho()
        self._menu_clickDerecho()
        self.widgets_APP()
        self.menuBar()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.sizegrid = ttk.Sizegrip(
            self.root,
        )
        #self.sizegrid.pack(fill='both')
        self.sizegrid.grid(row=1, column=0, pady=5, sticky='nsew')
        self.changeTextButton(text_btnMode)

    def changeTextButton(self, text_btnMode):
        self.cuaderno.btnMode.bind("<Motion>", partial(self.openTooltip, self.cuaderno.btnMode, text_btnMode))
        self.cuaderno.btnMode.bind("<Leave>", self._hide_event)

    def activeDefault(self):
        if modo_dark == 'True':
            self.rbOpenAuto.canvas.itemconfig(
                1, fill=pers_bottom_app, outline=default_Outline)
            self.rbOpenExt.canvas.itemconfig(
                1, fill=pers_bottom_app, outline=default_Outline)
            self.rbOpenDesv.canvas.itemconfig(
                1, fill=pers_bottom_app, outline=default_Outline)
        else:
            self.rbOpenAuto.canvas.itemconfig(
                1, fill=default_bottom_app, outline=default_Outline)
            self.rbOpenExt.canvas.itemconfig(
                1, fill=default_bottom_app, outline=default_Outline)
            self.rbOpenDesv.canvas.itemconfig(
                1, fill=default_bottom_app, outline=default_Outline)
        if 'desviacion' in globals():
            if modo_dark == 'True':
                PST_DESV.DESV_btnAccount.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                #PST_DESV.DESV_btnAccount.bind("<Leave>", self._hide_event)
                PST_DESV.DESV_btnCommand.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnIdrsa.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnDirectory.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnAuthorized.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnService.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
            elif modo_dark == 'False':
                PST_DESV.DESV_btnAccount.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnCommand.canvas.itemconfig(
                    1, fill=default_bottom_app, outline=default_Outline)
                PST_DESV.DESV_btnIdrsa.canvas.itemconfig(
                    1, fill=default_boton_bg, outline=default_Outline)
                PST_DESV.DESV_btnDirectory.canvas.itemconfig(
                1, fill=default_bottom_app, outline=default_Outline)
                PST_DESV.DESV_btnService.canvas.itemconfig(
                    1, fill=default_bottom_app, outline=default_Outline)
                PST_DESV.DESV_btnAuthorized.canvas.itemconfig(
                    1, fill=default_bottom_app, outline=default_Outline)

            if PST_DESV.DESV_btnRiskImpact:
                PST_DESV.DESV_btnRiskImpact['image'] = PST_DESV.icono_riesgos
            if PST_DESV.DESV_btn1Expandir:
                PST_DESV.DESV_btn1Expandir['image'] = PST_DESV.icono_expandir
            if PST_DESV.DESV_btnRecortar:
                PST_DESV.DESV_btnRecortar['image'] = PST_DESV.icono_recortar
            if PST_DESV.DESV_btn2Expandir:
                PST_DESV.DESV_btn2Expandir['image'] = PST_DESV.icono_expandir
            if PST_DESV.DESV_btn3Expandir:
                PST_DESV.DESV_btn3Expandir['image'] = PST_DESV.icono_expandir
            if PST_DESV.DESV_btn4Expandir:
                PST_DESV.DESV_btn4Expandir['image'] = PST_DESV.icono_expandir
            if PST_DESV.DESV_btn5Expandir:
                PST_DESV.DESV_btn5Expandir['image'] = PST_DESV.icono_expandir
            if PST_DESV.DESV_btnScreamEvidencia:
                PST_DESV.DESV_btnScreamEvidencia['image'] = PST_DESV.icono_captura
            if PST_DESV.DESV_btnCopyALL:
                PST_DESV.DESV_btnCopyALL['image'] = PST_DESV.icono_copiar
            if PST_DESV.DESV_btn1CopyALL:
                PST_DESV.DESV_btn1CopyALL['image'] = PST_DESV.icono_copiar

    def openCustomer(self):
        global listClient
        listClient = []
        pathFiles = mypath+"Compliance/file/"
        os.chdir(pathFiles)
        listPathCustomer = []
        for file in os.listdir():
            if file.startswith("desviaciones_"):
                file_path = f"{pathFiles}{file}"
                listPathCustomer.append(file_path)
                for openFile in listPathCustomer:
                    with open(openFile, 'r', encoding='UTF-8') as fileCustomer:
                        fileJsonCustomer = json.load(fileCustomer)
                    for dataCustomer in fileJsonCustomer:
                        if 'CUSTOMER' in dataCustomer:
                            listClient.append(dataCustomer['CUSTOMER'])
        listClient = set(listClient)
        listClient = list(listClient)
        listClient.sort()

    def iconos(self):
        self.Desviaciones_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"openDesviaciones.png").resize((80, 80)))
        self.Extracion_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"openExtraciones.png").resize((80, 80)))
        self.Automatizar_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"automatizar.png").resize((80, 80)))
        self.iconoNew = (
        tk.PhotoImage("iconoNew", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAACQ0lEQVRIieWWTUhUURSAv/swtDEyZIyXC9+zDGkSgiJIwoVUkGJgbYPBAqPaBP1Rs65NW8EWbqIiqCRLC6oJgiyhiMAwNcHxmdmMmjY6TvOjz9eiHHR09M2fEn6rd88793yXey6XC2sNER3wer2FQINhGEWGYSz4vwTToVDosSzLl4UQ+nLJGdEBSZJuTE4GDrS2doJhmLZuyrFQut92fmRkxGoYRo0QYsnJC8S6rhd1dvTT8uQDO/fsMC3+3PiOr53fqKk9bPd4PH7gbFzi2e0tLFY4duKIafGPfjdPW96zLjOD4/aDZzRN86uqeilWvmS68jJIkiAcmqKpsY3mR23k5uZe7OnpuZZ28SzhUJjbt5y8fP4RWZYd7e3tV1dE/Fc+RUP9M96+6RCqql53Op210TkLepwo+eoWBvvdkfGMrnOzrhlF2SwKCgrOAQ+A8ZSLq+1VVNur5sXu1t3H7R5j2/Y8C2CdK07LVsdg3mWUsNjV1Yerqy/hVSQs7u3W6O3WVl6cLHEdrgmvj3AwDIDf9xuAn55RANZbssjemJ0e8b36h4wOjwHg++UD4MunLgDyZCunrtSkR3zacTLy7Wx6DcCho+XxlIjwf/R4LkLE80ZIoXhf+d7VEW/IMX+CF2PVerz2xDF7POAa5EXjq6SKD7gGoXSrObGu65qtRNlVUemP63m7GBWVu7GVKLjd34eBmSXFgUDgQjAYVMrKivOTsv5jfHxsyOFw3AGG5sZj3QJZgApkpsA9DQwAEymolTx/AAVIwo5raMlVAAAAAElFTkSuQmCC
        ''')) 
        self.iconoCustomer = (
        tk.PhotoImage("iconoCustomer", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAEhUlEQVRIieXWb0wbZRwH8O/1etfrtVcopToKFOi2Am4F3QbO/UtwKIsv1DdTE9SYDF+Q7I+OOXXGGP+9GUSzLCEZm5mLiX9CBjRm/zo0JvxnGSwIcTCgpaMtlpZxbUe767XnC6NxY6xd6xvj7+Xl+/w+z3N5nnsO+L8Vkcogu92+mWGYbQAQDAa7zGbzwL87rXtqbm7uyOLi4i2e56VAICAFAgGJ53nJ4/EE7Hb7Rw/TK+kV+3y+Tpqmd/p9AVw+P4ipCScAYE2xEc88VwltFgen03nFYrFUJtNPlkzI6/V+RdP0zt7uUbz/VjMyQnbs2a7Enu1KcMFpvHegGf3dYzAajRWdnZ0XkulJJgr4fL5cmqa/nrzhlp06dhbH6tegolgDnYaCTkNhfaEaVeUZaDw5iFLLahSZ8k0Mw/zc1dXlTGvFsVjsCEEQ5HenL2L/CwboNNSyjE5DY//zBnx7+gJUKpXMbDZ/lqhvQpiiqI3xuAS7fQ4b1nIr5jaaOUxNeRCPS9Dr9ebGxkZVWjAApSBEoVTIQRAr70WCIMAo5IgKIiiKovr7+x9NF/YwDA1BlBC5E18xFBZiEGMSFAwFr9d7W6vVCmnBS0tL7QDw1NZ1aO+ZXzHX3uPDlm3rAQDd3d3Xa2tr59KC8/LyToTD4cDLr1fj4rUgLg8tLMvYri7g0nAQL71WDYfDccdqtbZWVVWJD+qb1AfE7XbvUigU50PBCHG8qRW8fwFPmP7cO0NTIWj12dh3aDcUDCnV19e3hUKht2022820YQCYmZl5VaFQnGFZVuZ2+TE54QIArC3OQ44hC5FIRGpoaLg0Ojr6yfDwcF+ifknBDodjS0ZGxvckSebH4xImJ1zwuP0QxRh02RqUPlYABUOB53khHA5/msw5TgjPzs4e5DjuqCjGyLbWHpz7cRCMSgO5QgUQMkjRCAK35vH4htXY8+azyNSq4XQ6e8vKyramDHu93gMMw3zpm+eJD949A5LJhDbXDJKi78pJkoRbvzvBu27gQMOL2FRpxvj4+HBFRcWGh4bdbvcmtVrdN+/l5e8cPAVtbik43aoHzRNC+DY841dQv3cXKjeXYGBg4IeamppX7pdd8TgplcrWaFSUf/zhN8g0lCREAYBWqpBT8iSaj5+Da9aP8vLy3S0tLdVJwx6PZy9JkoXWtj6IMg6a7JyE6N84o4TOuA7HvrCCZVlZUVFRiyRJy97sfWGGYQ5FIgI6zvZCl1+SNPpXcbpVWAxEcW1oEhaLpbCuru7phPD09HQBSZLGrl9+hUZvAClffg0mU2p9Iazt/WBZltixY8eRhDDHcfsBED91joDNNKSEAgCX9Qiu/3YTghBFQUFB+eHDh++6U+X3DiBJcrMkSZhxzMG43gQhfDtlnFVnYHLCDYPBoOnt7TUDuLoiDIATBBEmUw7uLN5IGQWALC0NggAYhiFdLlfuA+FYLHacIIgTnx99I6V/7ntLkiR0dHQ4WZYN/vP5Mliv159samryq1SqfaIoqtOFR0ZGpm02m7WmpqZ7bGws3Xb/4foDR4WzhPac9+4AAAAASUVORK5CYII=
        ''')) 
        self.iconoExit = (
        tk.PhotoImage("iconoExit", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAFJ0lEQVRIiaWWW4wTZRSAv39m2k673W3ZG+Ju2wXKkgArGuQSQAgCicQECYlvJCoQ1Cgm+IB4QWNIiIIYMEafcE2M0SejL4JBSQy35bKbrbjIZUEuwV0oe2m7baedzvw+7EV2C7MFz9PMOec/3znJ+c/5BQ4ipVTOnj0bcPIpVZLJZGHx4sWp4X/h5PzSxlcPdd+Kr1BU9X+DrUKBRfPnr9q+fetBAM3J2TStYOP0KJOnNCCEQFEG85w7bwG6Vyc1kCKfMx2BihBMqJzArp27pWnma4b1juBhuXTxMtev36C6qhpV0+jtzaB7ddrb2sjnc45nDcNg46YNRfqSwEjJmrXPEagI8Ne5c8Ta2xBCRdVc+MsDuN36fY8mEz0UCoWHBAMuTSPaGCXaGGXDpg10/9NNa2srJ1tOcav7BrpehuZy4/X6UBRl3Hglg8dKXaiOulAdq9esJpFI0N4W42TLKTovdVLmL0dRNLy+MmdwLBYrE0K47zb09PSk9n/9XUlJBAIBli5bwtJlS7AKBc6dO8/eT/c5gzs6Ovzbtm5PCSRSDHatLaE6WP43mqenJPJdomoas5pmFumXr1ye7e3O/zICzmazukDyvjuFqWkoqsKfpsIxq1Bp3QPccuwEy1YsIxgMPlBCyURCTWsZP3AbYKQLhMfFjoyXfWld/pZ3S133Xr5XgNYjR/jqsy+QUt4XIoQgFA6P0p0+dcZt96UXDf+PgF2Kil9TrUXPLH/UXfPIxxnFdcjI5SalBzKkMxm6um7RebETI5+n9+oVDv180LHCpqYmR3tRV1+92vVkdc/NbdiSSS5NKn0ZBILMmeOcPXOc6VisC+R454cfmT5rBpFIpCiolJKDBw4w8ZFQ6eCKCs/luS6TaitP4wSfcKvWkGX0hNrsy/Dlnr18uPsjPB4P+Xye1tNtTI1Ooaa2Btu2HSsuuunXbnZv+DU/mE+/wxx+Qod5hSTf7W8G4Nvmz2k5/Ak7d3wwLhTGGSDx9OCoC3pcqKJ4kd3dX5ZlIfI5BFaR3wODJZLbaZPb6eLKL9kqLXo5O9a/CMC69ZvZ/naczVteebiRqQjNvmorfC99gwoxtLSHKlaRPC0MfsLPm+++ha4PLghd1/GW+QgESns3FIFnTJ+8pz1nWneQYiCTWRcMBuqijVOJRqcB8OM33/CtobDq+bVFHf36G69RVV3leMeLwKpiM1Cw1OOHj94EqKyqPFrweLrK/L66VDKFruvUh+vRXRr+qnoWLH2qKFhtbU2RblywZZjsCipY5FUAs3FSbO/5roUA/X399Pb2UB+u58kVK2ma3UQ2a6DrOXTdUzJsFNjr9RogeC/rh+x/hqlXulcBibEHFixcMPLd399HZWUlbrd7rNv44JkzZw7EYjH/fdbiCafDUkJPbx+BinJ8Pt+DgQFmz56dBtJjjete2DR+BClJJJJkMlnK/X48ntKqf+gXyFgxTZPevj4UIXC53Yjh3W7bXL92Ddu2R02gksGnT7WSy+WJRMLUTKwdCTxWbCkxDIOCaXIn3kUuZ5BKJpBy9BgtCTxl2mTit+P80R7jyO9HSaaShEIhIg0hQpEIkXAY3Tv6palpLubMeQyEIBCoKIrpDBYic7nzCtev3RillpbkwvkLXDh/YchNUDuxhoaGBsKRMOFIeHBbnWkfOWNkDdxuT/9IaCduc3OzHo/H5zsmNySJRDZ8M979rCrUFdlsrtLIGSya9/hyy7JsAJcrkNqy5eW2UmL9L+no6HBs738BCEj1jbPumaUAAAAASUVORK5CYII=
        '''))
        self.iconoModeDark = (
        tk.PhotoImage("iconoModeDark", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAFC0lEQVRIidWWXWxTZRjHn/f0nNOP0dOvbe26IXNbGVlkKtV90Gw0aiDojSESwREFrwhxN174gUNPGCEDE8FAYrzxAyYIg00unKjA6iLJMiLOAYWMgYUO6Nat6057+nF6znm9sdUtp11piIn/q+Z5/+f/O2/6PO95Af5vam5mzc3NrLnQ51EhD7ndLLmiSnsZEOAbt+JOj4cVHzaDKAQcj4POVq6z2uw6WzwOukIyCgI/CpFKxfU17eqyJvs3oiRPHjmeagdg5YeLZYnXN1OHSBVhfTB0v+2H8UPJhQ7FHXNWraVimc61utW6fWsbfRSAnecjiLlUMiEmkwkxSRBzqYXQrW300dWt1u3lS3Uuzqq1KDFUSkW//2KkotTFGc20y1FraChmkk84VphPe71eDAAwMTEklpe4kpE5cbD/p71D83dKdze1lG6KcsLcjatzu78/23leiZGzq7ds3PNWvdO8mzHShgtn779/yz9xoM5hO6DWyC8CpjVcJMojJN+M88TAvWD4YHVF+dvPrS/fy4WFudHfQh9293QczpatuOO0Rr0Xhq3GpvDsbEofjaYuPVah6S8pS7nrVi41Gc1F+lg8aDYVyw7GKL1AE7q1qSQ1wPOi2X878mn3qV2f5crOa443rNtZZrTBDUtpiqmpqQGKomA2lISxsTHQ6nDGF5ggRwPTS573eNjpxTLzGiemhDylN8YYu90OFEVl9VnLxXrTktj+fDIXBbvdrIaiBSdFkWAwGHJ6EQIo0ktr1te0qxfLzczxyy/tcpbZ9e+qaUSna+GQEAiHU72UOqXW6YoWywIAgCWM/PiUnWnc+uzeLUYzVZquJwUsTN6NdfX+yF6eB9aqyc3OBstGQvXP3+738eGRS5N/IkIClSpnH2akIjGScaq+yqF/paKyyJSuyxKGc6HEHQCYD34QwuzP/femtVpV5uzlOfFahBfHRIHoEsX8vgNCAglSAg2MjszuuD3O1WXqAvChm1xmvDJgj4eNAkCXQhZaVvUBx/M8I8syEETutohyKu/ApX1eALiWy5dPV+NUUnVcEDAEg8GcRjEFcpRDPQCAcxrzBMP18TgbmdVfDQSCEIlEFD2SBPj+HfWZQAi+yCdzkY5hiW1t646setqyf+qB+IkoqKhwOFxJ0jKBEA2hUAgoCoCbJYKBCfIrDa0fbmwoOVa9bM1TI1dazgB4su48B5gltrXR3Y0tpZsRAumujzt2/HTnzmKD60QsKpungzwfDkm/h6ao06EpzY7+c13Hah0tj1UvN2yoWs48U2JI1I5caenLBs8KfuO1tUebWks3pQ/8E30ffQ0AMO67ODN6dbC3vm6tm6Y0iZPfdbbfujMYBgC4PvbLdaupmTea6dXVtYzTwiQcf1w535s32N30XqWzsXi/JGJB6Svjcr2jX+UsOWg0q6tFaeXnfv9FIb026r0wnIYzBqoaJ5486Zv4NbyQoXgD8Qx1+WxlnR9jQLdP9HX0LFwXRR0iEELp3wvXu3s6Dr8q7plEgKs8Q10+JYYiGADg275d+7Kt5SOlF/63CrrskWQMyzIGWcZAkrFFZ1ZJCIAlWhuS2xDC+R3Gf8ti0bwJgGBmJp7X3KaFMZIGh9VfIgBArQ0dlTIWUVzWBPQEz4igKuiunE0kSLGIXMRpiYSNQCQeHN7jIwEAMCGbKAxII8dnZFldRJGi8VGCkahGJojHJQKZRCRjAFBsuP9EfwEG3xj4PwITUQAAAABJRU5ErkJggg==
        '''))
        self.iconoIncident = (
        tk.PhotoImage("iconoIncident", data='''
            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
        '''))
        self.iconoFindBar = (
        tk.PhotoImage("iconoFindBar", data='''
            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
        '''))
        self.iconoHelp = (
        tk.PhotoImage("iconoHelp", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAE9UlEQVRIieWWW3ATVRjH/5vsbnaTbpKmpSktoS0X24ECrYwXxjIgl9HhQaAIlOqDPHB5gFFUFIbCgx2dcRSvYL2h46WA+MSM4ogODHSAwSnlNlMLtJReoJA2bZLNZu+7PrSpCUlJOo7jg9/TyXe+7//b75yT8x3gPzJinPEkAG5kzAPQ/jUwS5LzSrLY1z02eko2TXEcRVopC4GQqpm6iWhE0ZSIpsqCbvQHJfnXO6LcCCDwT8DuUhd3aKXP+8iWspKcXBv9QKGopuN8IKh/29HTdyUY7rgVkV4SVPXSeMGFsz3O3w5VPVw2lXOMdzvgl2S8fKHV39I/9PVNQdyRKsaawsfNynadPLbosZmTHGwSVDVMXA3yaA4Ewas6chkaViIxzEGSqJ480cFR1OzrvFAckJWf0oJLndyRxvkVVUVZ9gQ1E8B7XX58IhgIzJ0HPPkULrEcGi63QYxGMYezJ1Uwx+O0BWV1SkdIuB3WtKvxcwniOQyzZPP0yYd3z56ec7/Ituu9mLF+IxYvX5EEOLjvY+SePYnNk3KT5gzTxMLj59r/GBiqACDE/Jb4oALW9vb2mVOToKf7g2Afn4/Fy1dAEkXs27Mbe1ZXY1dtDXq7ulC7ZSvOMU6E1eR/l4Ug8FZlWUlRln1ngj82oIC5C/M9JYzVkpTcJMhYsmYtIjyPXc+tQ23fDXxfkouGPBZf1A3rzVu5Ck3+waRcAKjK81i9DLMacVtLxgbT3NyL66f6slMlPu22480dr0HXNLzjdeAhzgEAcNMUaCkIALCxLGTDTAkGgJri/PwrwfACSdNOJFScRZIzZ7i4lElz3Rw+n5iFAz73KBQABmQFOucCAPx5pgmV2anzAWDV5AJnscO+IaliF02OnQUg/gIxAeztuoeLlANb976PCM+jt6UZJaWFY+Z7WRs4yjL9fjDlsJK2B4Hj7cuefjDV61C/tgayLKN+4wbU5bvS5rloyhkbx5ZaFQ1dzRR8VtKwbG0NIjyPuudrsZ3RMMOVlTbPYSUZjBQ7useyrouZgk16eHFO/XIMm1gTlRlAAcBJkwDgSAAHFS2aKThmxaVluChl3hmHZNXEyCXyd8WGecMvyRkJaMpwXFl5OTpUI2Mwr2kiRnr46Kn2S+KJy4Ph2qUFE9J2owragob6NyBFo1jKMRlBBU1Hnyh1x36Pggcl9fTxuwP+pQUTvOlEXi3y4kp3KwgCmJXvyQh8oL0rFBDF/UlgAO1n7g36DdP0WogHF31+iMfeQQmkYWA7YUl7uMKqhm86bt8IKPrRmC/hYvZL0kff3ewVklMTbf+AgPrDP6Lu4A941x9JF45tza19nYK4Kd6XAO6NSgc+bLvVmu6QkaaB7s5OCJEIWIx9PwNAY2dv5Iw/8FlUVVvi/anW1Dffm9P086JHi2hLcqcCgICs4NM7Q7itaNjpy4HPnvqANQdC2gtnL//eHuaXAYlfmHIzJ7BsVYWHO9z4RGWhkyJThaS1dl4wnz11oaUtxFcBkO6fT/XmQlTTuv2yevxoz70qwLSXu5020pL5m+9amDfWnG652BbiFyPu1RFv6dSIPJau9jLMK+VuzldTVFA4K9tJFIyxtIph4Kv2Hr7h+q0L10KRZzD86E8tnGkVAPLcDLUsn2YWWK3ENBdJspTV4qAtFpuVIIigomiCrvf3i9IHd0XlyDh0/yf2F7A64c4RDz8sAAAAAElFTkSuQmCC        
        '''))
        self.iconoAbout = (
        tk.PhotoImage("iconoAbout", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAEjUlEQVRIibWXXWwUVRTHf3NnZj/KIgW67XZhSSmh8mFSvh/ASBTkIz6IYIySoBE1EaPxwRiVxGJ4wECMMQhiJIA+ANGY4ovC8pVojCEY+ajQ0kopsuxu6xJgYbu7nZ251we2tZbtdgX7T+Zl5pzzm3vPybnnwr3LzD/DKhNYbArxmc802ty6uAFIQLp1ccNnGm2mENuBRYBRSkCtBOBLLiE2GUIbsTzo15ZW+83QCC9VHhcAXVmLSHeGcDyR+yGawFHqtiXlemAXYN8LeIZHF9+NNIzAxvo693M14zBF8f+0pGT/5RgNZ9t6UrYdzzpyBXD2v4BXGZq299XJE4wP6ut0r64XBQ5U2nFoONPq7LwYsW2lVgONA20KRVyla9rX2+c9ZL41rVaYQtxl8PWfMVafbGZHe5Sxhs708pH/+m4KwZKgX4wr8xiHYomnFZwDWvrbDFzxDEPTTnwyZ5r7xUmhgqvpSKWZHf6F7Ts+RynF6+vWcWr5AmpGeAva7+2I8trJc5at1Hzgt0Jg06OLP16eFBq/edbUQfc2HEvwZutVrnR2AhAKVLH1wRBLg/7BXHj7VIuzuz1yJevIOvIF17/0X/EZRmBDfV3RhM4dW0737WZeWLMGpRSZVIp5FeXFXNhYX6d/eyUezDrWWuAL+CfHpkuIg1tmTfHNGVs8iNfQWRao4ERTE1oswraZUwgNss29MoVgtMs0jsWvzbeV+hiQvVv9uFfXv4+tWmS6ChRTIVlSAlCqfU4qgo1HrbTtLAeOCwBd8NQT4ypVqUG2tHRQ1XiMQONxPrpwuSQfU2gsC1ZophArAQSAVzcWL6mucJUSoDmZYnPLJQ4fPcahI0f4sLmdlmSqJPiS6krTrYvFkC+unCOrhspTr1qSKWpDE1i4cCEAtaEJNCdTTB3lG9I3VOYhJ2UV3FmxaUk5strrLgksUYh+rVMIDYkqybfa68Zy5CjA7EuqKs33vtQPoQSQcwlxK57JDjs4nunBpYskYAsAUxd/RdLDD450ZzCF6IJ8VWcc+3A4nrCGGxyOJ3JZxw73gR3JgYPRhNbbFIZDlpSEY9ewJQf6wMBPSqnb+y/Hhg28ryOGUuoW8HN/cC4r5fr3z7b2pB3nf4dmHIcNTW3ZrJTvkj+d+vfIXd22E28401qUHPC4iXZ2kUwmuXnzJtHOLgKe4j1g/elWJ2XbMeDL3nf9wXbWkSt2XozYe9ojgwaZ7x/NzFE+JtfUMHliDbPLfSzwjx7Ufm9HlN2XInZ+/uob/grNXCt1Tftm29zp+vO14wsGc5Tix67raBo8UjkGXSs8un116Spv/HredpR6Bu4UVa8KHfotCs6FY4knr1sWD1eOuWvuEprGRF8ZE31liALQtOPwzukLzqbzF3OOUs8OhA624l7Ve3RxwGcYwTvjbXDIs9eSkn0dMRqaWnu6bSea397fC9kONdAbwFqPEJs0TXtgWdCvlgb9rlCZh0D+UOnM9BBJZzkUS1jhWEJTSt3KSvkesIciA32pMoDHdMGnPtNoLXCFuaALtgKPUuIV5n50X5e2vwFPYsaDeTmdkwAAAABJRU5ErkJggg==
        '''))
        self.iconoWorkSpace = (
        tk.PhotoImage("iconoWorkSpace", data='''
            iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAACcUlEQVRYhe2XP0/bQBjGn/tj34kmCIYylFC1SJmsIA8BJDY2Pkf5AN2qbp1LZpayMfIlMlTKkoiIAYEwYmm7NVVArUMud74ObSwrwbGluqJS80ivZOm95/y7e33vycBc/5I2NzffSinvKaVRWgghhr7vv5/0+r5/IIQYzvJKKQdbW1tvUgGklPcAbFZwznWn03HGvvPzc5dzrvN4pZSD5Dvp+CEIAqGUcvPslNaa3dzcVBIAq1prlserlBJBEIgpgMfSHGAO8OgAsay1RAgxRI6zzBgzyaPUbDYlY8zk8QohhtZa8iCE7/sHWQ2FMWZqtdqHSa/neUdZEJxzPdlFp0g6nY5jrV1L26mlpaUv1Wp1+FAuCALR7/dX07yEkE/1en2Ulv8/VWgJkjo9PX1qjClHUXS7vb3dy0WT9yP0PO9o1jyHh4drlNIIgHUcRydPzKTiPmCtJRcXF6+zbjVjDL28vHw1a9IwDJejKCLAr5tTKeWkjY0Brq+v3dFolDpwEqLb7T7LMzZLvIhJAODs7GxFKVUCgKurq0oyF4bhi3a7HQIAIeSuXq9/nZogCAIxrlueODk5eTn2Hh8fr+T1uq6rm81mvPBC7gIp5ZNxzbOktaaVSiX+zgopweLi4q3rukZrHS8oCUQptQlY1e12daEAe3t731qtVrlUKkkAaLfb3v7+/kcAIISg1Wo9X1hY+AEAvV5vsLu7awoFAICdnZ0BgAEANBqNu2SuXC73Pc/7/pAv3rJqtTp0XTezwwEA59ysr69//gPeaQAA2NjYePf7x8SmhRBC1Wq1xqxbjTHWcxzHUEqtlFIBUEXAzvVX9BMO31I+Sxc/aAAAAABJRU5ErkJggg==
        '''))
        self.icono_account = ImageTk.PhotoImage(
            Image.open(pathIcon+r"account.png").resize((20, 20)))
        self.icono_account1 = ImageTk.PhotoImage(
            Image.open(pathIcon+r"account1.png").resize((20, 20)))
        self.previous_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"previous.png").resize((40, 40)))
        self.next_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"next.png").resize((40, 40)))
        self.iconoSwitchOn = (
        tk.PhotoImage("switchOn", data='''
            iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAACEklEQVRYhe3XT4sSYQDH8d88/sknbRZWFAtUOtXBYA9jdvDspYO3Yk/bJXoLQS+ge69glaDDQp0EoYOXhQgNLFcECaVWqWlx1bWZR9TneTrEym65i+CfOex8b888Dw8fhnmYGcDOzs7uaqecHRSLxTsA7hNCqBUYIQQTQnxMJBL102tTYKVSeRUIBJ55PB4XAEVKaYVRmqbJu93ubiwWezoFlkqle+Fw+BOl1GWF6t/a7Tav1+vb6XR6zwkAiqI8oJS6JhOOne2XGJwMLYGpKsXum+cIhUKOXC73qFAovHMCgJSSAoDgAoOTIZI7Q9ANsVYc6xPsZ/4a3Ndc0HXd5/f7bzhnLd64KeDdXC/Qff38WEqpMMbITOCibdIwbql351p7ZDSh//564fxKgEHvbWyFHs619kB/fymQLAu1qmzgotnARbOBi2YDF20lb5JfRhPln7m51h4ZzUvnVwI8Zoc4ZodL2WsmsP+DYGQuZf+5Y/3ZT9vpByuTUoI4CFSVYj+zVts0VaVwOB3gnENKOZoChRAfDMOY+Hw+5+u9F9boztRoNESv1/s2Ho9HTgCIx+MH1Wo10+l0ngSDQQch1hxuIQRarZbIZrNfotHo52QyOTj325nP59O1Wu2xrutezrly0UarinM+Mk3zeyQSqaRSqbeapvX/Q0gpSblcVhljltxGt9s91DRtzUfUzs7uCvcH1IDLM1dhnewAAAAASUVORK5CYII=
        '''))
        self.iconoAdd = (
        tk.PhotoImage("iconoAdd", data='''
            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
        '''))
        self.iconoSwitchOff = (
        tk.PhotoImage("switchOff", data='''
            iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAB80lEQVRYhe3XsWsTYRzG8ef3Jj2OcKEoObQQkCgIOVA6BYQ46lBaEVw6xEGn4JDVRbcu/QdcXbIFGqgNCI4RXCKESJIKVhQSiWkIChmO673v6+LF0IQYOZt36PuZ7l6O977H3XHvAZqmaecbTe60Wq0rhmHcA2Ao6vE8z9t3HOdrMDAO7PV6e7FY7D5ORS+blFIOh8PXqVRqA0FMt9vdsixrn4hw3P8BIaSSuEiEIWGvwvd9FIvF54VCYScKAES0QURo1I/w7OlLJXGBnd1HuLl+DUKIB7VabTcINADAdU9w0YzgxdWBkrgnnxNw3RMAAOfcKJfLl6OnD2IMsCJqbjFjf7allADApgInyVu3gUtrC01O9ffAl6MQebPNDcSNdcjr6YUmon7vTALZ3w9RSweGpQPD0oFh6cCw5n9JPtRB/e+LzfSt+x9yps0NpHfVMznpv5gKFAIYcTWLaiGmx6IAIKX0AMA0VzB0ObZbF5ZbNsZhmisAAN/3OfB7yd/pdDYty3rFGMPg+Cc4n3EpSzC55M/lcgfZbPZxFACSyeRBu91+Y9v2nYS9qiQu4HkeSqXSp0aj8bZSqQzGz2A6nb6bz+e34/H4Q9d1YyrifN8X1Wr142g0OsxkMntEJGe+Dc1mU9V/MRzH4UTEVZ1f07Rz5xfaiKHAztUwZwAAAABJRU5ErkJggg==
        '''))
        self.preference = (
        tk.PhotoImage("preference", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAFN0lEQVRIie1WX0xTVxz+zr2lFRRKgfK3tBQQlAKCEwXENA7FgBqWLNP5L9l8Me5hmmx7mC7bki2LL0v2smW+6BI3F6dDQUCYEqdDLBNkghUE2tJW+VdEb0EKLfecPRTRjusCxvjk93Rzft/5ffl+57snB3iNVwSy0A1HGto/M/e5D/HeCQ+jzAfGfOkqduDQrtKKhfSRLYTMGCOln5/6auKeEwCCn6wPR6vPAOBemvDJlrvL6ttHWzmArc1RGJqamjxTLhey31wHrXENhrxAf+N19F9rJiaTKawD0cHNHbZmNukjqzKCCvcXF99fsPCxhp6Vv9abWwVLLwiAkcHUvj5DgplO+xASLIeP+nmcXA6IImosE8fNzn/KR3qsPGGAyxVvP3qxMXnfxiKHVH/JM/7tpjnjxIUes9tqQdn2zfD4RFyuqAOjFLLFofjy0z2o8oSAAfCNjcN87AR8449BeB7J5WVglMFaVYPwhHix1Bijk3Iu6bimTWh1W3pR9u4WxGWnwz0NfLw0DnedIyjM0uJPjwJshhsUugRZ+/bC7XAiJEYNhVI528daWc2bOkJNABLnJcwIm/32UcA2Cdg4FYhOhd/dc/n8IgVUaalSrQCOZ5LLUotbcsLfCEtJRe2pGihHhyGbORDJDhJ43D8IW2UtVDqNmG9QFMxbeNtKw523C1M+ASG4bnYi/D9zmRIEuNra4Wprx5QgzNk/ZneAEYYtOfHbnpfsgHB9U9ux/6/mrh8mhwbBqAhGKQ58tBsmuRrijN2RW7dhr7sERv2xJhwHXelGRGUbnjoeGELnT7+A8Dw4nkdIVAQrWJW69XD5mponnAAv7ffd30447TAYCxEUJINxRRJcSjXEiRmnjwTY6y4hMnM5tCXFAABHfQPsdRcRptVAHu4P1uK4GCx/bxfG7A7QaRH3rzSS7vioowA0kqMWfaIMHIeD7xQgsSgPzYvU6J54Wnfb7ABj0JYUgwuSgQuSQbupGKAMgs0eMMrFcTGIzc9DfFE+QADRRxc9W5dMtUcEBrxSlRcEmXtdBAjLeEJBKX6suA6B8AiOjkJ4avJsPSxZBxACR32D3yn8owYh/tozEKx9mBgcBhgFYQDPkwArAcI5acovHt7THOkytQKMQZyaQlJZCdS52QAAhVIJXekG2C9cwkiH2W9mJlzPXhwj7bdhO18HXqEAIQRL4mNZVmzkhwFDeN50jv9hWnryQnt3qFYD/dbSgNqUIMBt9Z+pUq+bDdUT2M7XYczuwM6yFWnvl+T3SPWX/I+/v3w5tuqGs9MrjCEyyzCnrlAqoc7Nhjo3e44oAERmZsDrHkfV347Oo1evxs1buKXL2/LA0scnv1WGsCStFOV/EabXQl9ehgdWO2/q8NyQ4kimmjACAhKQxkc9Fgw0NSMkJhqJG9eD43kAABVFOBuuwDM4hNiC1QhfmuLvwXMgICCc9E0r6bjIEFeg0idS69kajHbexeidLvSergT1eeG6eQuj5q5ZrtDdC1dLG6jXi97TlX5+VzesFdVQ6RNpUUZ84byF9xqznNuL0lJU+gRqOVcNS2UNIpK14gclqzN5hQK+8cez3MmHAji5HHs2ZS6PSNaKlnPVsJw9D5VeQ3fmZabvNWY5pTSe+wLZsT6379iVjqRr0RGNoAwrl8nXhGL4EQCA0adERkEIQZLCa9+wNkpzMzLcRHiCwvSYdduMBklR4AVemZsP/0zH+gcC9i1JiGO1X+9+eY89KRjzknaY70V+Nz3pUwCATBE0makJPVi70Eav8arwL6DRDYzgtzsxAAAAAElFTkSuQmCC
        '''))
        self.iconoFolder = (
        tk.PhotoImage("iconoFolder", data='''
            iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAABmJLR0QA/wD/AP+gvaeTAAACZklEQVRIie2UvWtTURiHn5vcJDc3H6RpEtLaaKgV0SK6lFIHB0Gwm9DBSQQH3dRdcFGsf4AgCIK4ORTcxMVFCh2MDurQ2to26YdtvEmaj5vPe46DbWzaDG1NwcFneofD+5zf+x4O/GcfKFtFQNOOnezveRgJ+L2VWs2lKIriVO2a06E61rL5jcnPc1eB4l9JLg2dmpx4cPO87nLuOjS3lBZj9589+TK/cucgEnWriIW7utoJAI73hW3jt67cePFmasQGRQvpBtA1h71uSYdmtwtFUXQhJV7dRb1h8XEm+TYxnbzbIpHKn1TtGB0e9I4ODw7t9fbXH70kMZ0EwNaUCCn22mAveDSni811NJMIIUWmUGJh1SCdK7JibJBaz1JvWNgUBUsIHKodISRCypaGQkgcqg1dc9KwBD5dAwUX4AUKTUliZjH09PV7BuM9BP06F86eIBYJ4FRV9ktyPcOrdx8CuyTxaHfm3rXL0X13bMPRSJDbYxetqa/Po8Bqcyc+j9vshGCLoF/3AgHYtnhAtj9+MCwhBCB2SjqK/P06dkhkZ5MIKQWb0zm0JA1LSMA6VEmpUqkD5UOVFMu1OmC2SqTs6E7MSq0BVFokDUtYnZQUzOruJPOrxuLccrpjotRapgxkgZbv3XVuIPY43ts9Eo8EoyNn+sPRLr/udbvImxV+GPnS0s9suVa3rL5wQI9FunyhgBfN6SBfLFMsV/m2lM59mk3l0rmi8T2VnkjMJsd3SrbjAU4HfHqPz+MOGtlc2qxaa4ABVIGQx6X2HgmHBlS74i+WKkbWrC4XTHMBmAFqnZrIv8Uv6Nbzf3j4jCEAAAAASUVORK5CYII=
        '''))
        self.iconoFile = (
        tk.PhotoImage("iconoFile", data='''
            iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAABmJLR0QA/wD/AP+gvaeTAAACCElEQVRIid3VzYrTUBQH8H96ncREQ2tF2iLRVJyNUPoGLv1YdiO+gMtuhNn4DDIOLpW8QECpWn0CGZgZXQkFwTi6KA4ltfloe2+TO4kbhWmcJqRZ6dndc8L93RMu5wL/Swin5DQAdyRJuqEoikgIIX8KjDHOGAs451MAPgAXgARA+f3JAMCb5IZnEuu77XZ7q9vtXtN1/eqqkwVBwHzfn1JKqaqqqiAIEASBGIbxsd/vHwE4WNlJtVp9Zprmg9WNpweldNbpdJ5yzh+dzJdOLuI4Pl4XAABZls81Go1GMr+EMMZoEQQAyuXypVSEUupyznkRpF6vKwAqKxEAPz3P84sgzWZzA8CVNGTiOE4hRNf181mI5zjOrAiiadrFLMSfTCasCFKr1eoALmchiyIIIWRDluWzqYjruoVuFwBIkiSmIVPGWFwUiaJoaZIkERYEQSHENM33nueNs5C1AcuyrOeGoQF4kYowtt7lsizLeri9/Z1c3/wM4FMacuz7fu4hSSmdbe3sHMqPn9yMjn4MASz98iSCIAhytzIYDL7Et26r/PDrt8h1PyTrfyGj0cjOi7RarU2+uztj794OAbzKRGzb7vd6vf08iCiKSlsS48X+ng1gmKyf9saDEHJf07R7lUrlQhiGEEVxQSmNS6XS0jTgnCMMwwXnnI3H43g+n78G8DLPAf+t+AVAT+A0KJvU5QAAAABJRU5ErkJggg==
        '''))
        self.iconoArrowUp = (
        tk.PhotoImage("iconoArrowUp", data='''
            iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABuklEQVRIie2PsWsaURzHf/d7d++4e/dAJCD2gWY5TjKIyAmF4g0toma5oYtIBpFwS+ngUGf/g6zdOnSTjt1d2qlOHQrFpYNDKJRCgzGanNfpBxLaYBIJGfzCG977fX6f7x3ALrs8WKIo2pNSTqWU0yiK9rYq73a7T4QQPwEgAYDEtu1f7XY7vxV5q9XatyzrN8npmKb5p9FoePeSh2F4wDk/I6njOKeO45zSnXN+FobhwZ3k9Xq9zDmfkUxKOe10Oql+vy9TqdQPejcM47zZbD69lbxWqz0zDONiTf691+tZNB8MBjydTn+jua7ri2q1+mIjeRAEz3VdX9ByJpP5OhqN9OvccDhkSqnPxDHGlkEQHN4o933/EBEvaSmbzX5JkgT/xydJoimlPhGPiFfFYvHlP+FKpXKEiFcE5/P50Ua/DABKqY9rJXGpVDq+/uVdRIwJUkp92FROyeVy72lf07S4XC6/AgCAQqHwWtO0FQ1d1313WznF87y3ayUr13XfgBBihogrxljsed7JXeVrJSeMsRgRV0KImTaZTMz5fG4vl8uF7/vn9y0AABiPxzbn3LQsayu+XR55/gLZIoqjalg5SAAAAABJRU5ErkJggg==
        '''))
        self.iconoArrowUpDark = (
        tk.PhotoImage("iconoArrowUpDark", data='''
            iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABuklEQVRIie2PsWsaURzHf/d7d++4e/dAJCD2gWY5TjKIyAmF4g0toma5oYtIBpFwS+ngUGf/g6zdOnSTjt1d2qlOHQrFpYNDKJRCgzGanNfpBxLaYBIJGfzCG977fX6f7x3ALrs8WKIo2pNSTqWU0yiK9rYq73a7T4QQPwEgAYDEtu1f7XY7vxV5q9XatyzrN8npmKb5p9FoePeSh2F4wDk/I6njOKeO45zSnXN+FobhwZ3k9Xq9zDmfkUxKOe10Oql+vy9TqdQPejcM47zZbD69lbxWqz0zDONiTf691+tZNB8MBjydTn+jua7ri2q1+mIjeRAEz3VdX9ByJpP5OhqN9OvccDhkSqnPxDHGlkEQHN4o933/EBEvaSmbzX5JkgT/xydJoimlPhGPiFfFYvHlP+FKpXKEiFcE5/P50Ua/DABKqY9rJXGpVDq+/uVdRIwJUkp92FROyeVy72lf07S4XC6/AgCAQqHwWtO0FQ1d1313WznF87y3ayUr13XfgBBihogrxljsed7JXeVrJSeMsRgRV0KImTaZTMz5fG4vl8uF7/vn9y0AABiPxzbn3LQsayu+XR55/gLZIoqjalg5SAAAAABJRU5ErkJggg==        
        '''))
        self.iconoArrowDown = (
        tk.PhotoImage("iconoArrowDown", data='''
            iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAA+ElEQVRIie3OsSuFYRTH8c+V4SYZDJKUwaAYDBaDxXA3k8lmM7Hd8i8YjCajwWg3yGC7k4FSlitRUkoGEV7LeetJXd7rfcf3W2d4zvmd73moqamCG2R4RqsCXytcGbqwlDTesFpCvoLXcL1gOR8s4DEGH1j/h3wN7+F4wuLPwCzuIvCFrT7kG/iM3QfM9wrO4DY50i4g34xshnvM/bUwhetYyLDzS3Y7yXUxXeBDYBwXyfIeGsm8gd1kfoXJovKcMZwnkgMMYgD7Sf8SE/3Kc0bRSWSHUfm7E5lSDOMkkeZ1hpGy8pwhHCfy0zhcKU0cRTWrltfU9OYbwP9Ih9s4LiMAAAAASUVORK5CYII=
        '''))
        self.iconoArrowDownDark = (
        tk.PhotoImage("iconoArrowDownDark", data='''
            iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAA+ElEQVRIie3OsSuFYRTH8c+V4SYZDJKUwaAYDBaDxXA3k8lmM7Hd8i8YjCajwWg3yGC7k4FSlitRUkoGEV7LeetJXd7rfcf3W2d4zvmd73moqamCG2R4RqsCXytcGbqwlDTesFpCvoLXcL1gOR8s4DEGH1j/h3wN7+F4wuLPwCzuIvCFrT7kG/iM3QfM9wrO4DY50i4g34xshnvM/bUwhetYyLDzS3Y7yXUxXeBDYBwXyfIeGsm8gd1kfoXJovKcMZwnkgMMYgD7Sf8SE/3Kc0bRSWSHUfm7E5lSDOMkkeZ1hpGy8pwhHCfy0zhcKU0cRTWrltfU9OYbwP9Ih9s4LiMAAAAASUVORK5CYII=        
        '''))
        self.iconoClear = (
        tk.PhotoImage("iconoClear", data='''
            iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABWElEQVRIie2UMUvDQBTH/3e+NKVDu2RxC7mlDXbRKBoIDoUr+RA6dshaEASHfpFObhnE+AGS3X4FF/cgCAqpYM9BCkebCtWmOPQPD44H937v/nf3gJ3+nTzPuzBN851zPvttGIYxbbfb10vFB4PBPhF9AFB/DcMwCgBgOsCyrMc8z4+JaDoej09c131b14HJZHIQRVHCGFNpmtZ0ay7n9G63ezPPK6WYECKRUvqLxaSUvhAi0XPD4fAIgGKMzbIsIwDAaDSq1ev1VwCq1Wo96Rscx3kAoIio0CFSSp+ICgBKCHH/I8C27TsAinP+2e/3D3VAr9c7mxciomkQBOdluZWAMAxPGWMzAMpxnNsyX/VuiajQ14vWLQGazeYzANVoNF7iON4rAyxCyjpfBeCrCm5MlVsEVHzJwBaeKfA9g1DBR9veqACqGXZL2tC4LjqdztW6p9+pGn0Bd9gT7+RfTD8AAAAASUVORK5CYII=
        '''))
        self.iconoClose = (
        tk.PhotoImage("iconoClose", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAD2ElEQVRIie2WXUxbZRzGf2/POYW2lB7aInSsAyl0HzBHwgAD2USco4kxakxmJNli4hKMi4kYo4m6XcyPm8WYmMUbp15oXFzM/GTJoiMCCtiBw6kkkODcWBEYUJzQQr+OF3gSgistH97tuXzO8z5P/u/7f8//hdtIjh2AmkKTDdRuVKAKvJ1rlHqBN1JojwD9gLzeUG+mJHre25XfF/R5NFWR/EB+Eq3BKIT/4GZrG/DcekItZoPov1xfOBb0ebSgz6Od2e26BJxKon+gMdfSMdXoieUoUg+wZSVzwwrf5uYT2rmPRm4O68T9TnNFsVnZCty1XCwJjpwoc3gNAumLKleOJHgXkNYSTAKOnhgOTnw+Ntuvc59UutyS4PVl0u0lFqPqzlTyAHZmZ3ifKVKNwNE1BQNxDQ42/zwR/j0UDQCUWJTCPQ6TBfDpIgHHT5bf4Vy68MVSe7UsaCJJo6UKBpiNaNqhe7uuj4diWhjgg4r8CkXwMotbeXeZ1bhpt5pRunRRQ1egN6bRAsRuZZr0DJZheiGhjbZOzJYc3mJzZxqEaTKaGO77a8EoCZ4+X1PgVRXJqotbBibbvr0x9w3wfjLDdIMBhqYiiTtjGvJeh8l9j9NUcPLKjLfBaYkcLrSV66Ivx+d6jw9OBTR4diUzsYpgAIMs+Lq1pqC0Ws0s6Q6GB7ZnZbhVxWAFuBKKjNR0jlyLaviA2Y0MBsgzy6L1t/qiUlU2ZOtkRNMWtrVd7Q9G44eAoVQmq9lqHXPRBBlXQzHHw/lZhTr5kP/PzqG5yDtAezoma/mnFlhk8cSbO3I9OjETi093BcMycDpdk3Su01IYZSE+bK0qUO1Gg00nVVmy1+aYYsBj/1fwW69tc1h22TKKATRI7O8JtA+HooGzVa5auyK1sDg+NzT4+cZcy87mQlu1Tjx1efy7izPzffu6A2OAoaN2s9soxClSz+208WS51fjDtM+T0CfV6UrXTwI+ZfFmPH6f09IR9Hm0M5WuSwI+S1VUqq4WwAslWUpTR527WhJCApiIxG/s/zEwHdc4AISBX/8IRR/ZYzeJeqe57Fo4NvrL35Ei0uzwW6H1UVdWx2SjJ65XOu3zJDZlyl1A9TKtJ88o+//VJerspgtAUzLjVGf81cBsRIpqWlQnjg1OtY/Ox84B/mXa4fFI7PzHgZu9gDhb5aqTBS2rKPI/OJBrlP2j+4pDgw1FE7IQ7SS//9k2Rbo41ehJvLrV3gm8sp5ggAc9ZuX7BqfpArA3hfalY15Ht9kg+lh8da4b+gsyFawCrgPNGxGqIytNXSlrmwO3sfH4B6pPOCB2MOAbAAAAAElFTkSuQmCC
        '''))
        self.iconoCloseExpand = (
        tk.PhotoImage("iconoCloseExpand", data='''
            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
        '''))
        self.iconoMenu = (
        tk.PhotoImage("iconoMenu", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAADR0lEQVRIie2WTUgUYRjHn33bd2Zidmed3DE2WGdJVxTHiLAuq7WgbuSlPSwZhCCrdaguHaTrXJc+bmFZaEVEBxE8lCdbtpNgRISBlMpuC3nYdATdj9x1posr77zTiER48g97eJ7n93zM7LwfAIc6IDlox+Dg4Ll0On0RAAAhlA+FQqOqqm6STCwWu6Zp2kkAAI/HszQ5OfmajCcSCXcymbxeLpd5AABZlqfHxsY+2k4xMDBwFiGkA4BR/Xm93kWSURRlhIwDgKEoyiOS8Xq9y2QcIaT39/e3kwwijXQ6fV7XddNb2NjY8JF2Lpc7TQ+cy+XOUDnHSVvXdUc2m71g23ifsvw9Nr49ZWrsdDp/Wyo6HIYpAaEtSxHKR+cAADAMU7Rt3NHR8VySpCWGYYoY4yLLsvmGhoaXJNPY2PiA53kNY1zEGBd5nteamprukUwgEHjFsmweY1xkGKYoSdJST0/PC+tzH+oAZPkaFUUZ0TTtlMPhAACoBIPBh8lkcqoaj8fjJ2ZmZp5tb297AACcTud6JBIZGh0dXaky4XA4uri4eAcAnIZhgCiKn+fn52/ZThGNRq8AtTm4XK41kpFleZpmZFl+RzI8z6/RzE7tXZm+6vX1dT89TLlcZkm7VCqJNFMqlY6RdqVSYWmGrv0vG8h/kalxTU1NlgYwxiXS5jhujWY4jvtF5Vg2IlEUf5D2EdJYWFj42tbWJmGMKx6PJysIwnJra+vdTCbzrcr09fW9X11dbXG5XDlBELK1tbVfent7h+bm5nZPsFAotFCpVHyCIPx0u93ZQCAwlUql7ts//6EOSolEwi1J0jLDMAWMcYFl2c3m5ubHJBMOh6M7h0QBY1zgeX6ts7PzMsm0tLQ8ZVl2E2NcYBimIEnSkqqqLtvG3d3dt4Fa+BzHma49Pp/vA83s+Ha1k2NiIpHITZIxLae/LXzDMEzbqq7rDM3QPjoHAGBra+uobeN9ynLI2/j2lKmx3+9PIYRMRQRBWCFtSZI+0UXq6upMN0g6ByGk+/3+FOmzvJJ4PN6eyWQuAQBgjPNdXV1PhoeH8yQTi8WuapoWBAAQRfH7xMTEGzKuqqprdnb2RvV6W19f/3Z8fNwy8KEORH8AASkseKBxpNIAAAAASUVORK5CYII=
        '''))
        self.iconoCloseMenu = (
        tk.PhotoImage("iconoCloseMenu", data='''
            iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAADbUlEQVRIie2WPWgbZxjH//d9OZ/udJaceqgDhQPhgtFyvtLIn6nBHSxTo+EokjoI00nGoKFjehQEylIwGQxFeMiWd/PkrV7s4kGeVJMuGYKb4rp1bCEpij+Ut4suVVylsj7IlD+8wz33PO/vfZ7n5eEFPug9iWn+SCaTnxwcHHz1fwGKolR3dnZ+6uspJicnvwNA2625ublUryy+lZFl2bosy8fX7fV63Xd+fq7u7++7ADZ6hb+Rl7HP5ztq9X95eXmUZdk6+pB1y4zfpXw+/2RkZOSXw8PDid3d3R8DgcA3N421bfuHra2tn7sCA8D8/Py3Gxsbv9ZqNb1Wq03fNK5SqVgAugfn8/knY2Nj2ePj47Gb+J+enn55cXEhX7d3DAaAYrF4/6a+Pp/vqBWY7QbcD30A90WUUqZQKOjvBey6rt80zceqqp7wPH81Pj5+JgjCZaVSud02uN3kepempqbioii+QmOWMwxDeZ6/YhjmzXxXFKW0uLg42zfwzMxMwhujiqKUbNt+sL6+fhsAcrncnXA4/FCSpCoAynHcZTQanegZ7Lqu38t0eHj4N0LILUII1+xDCOFc1w0ahnEIgKqqerq9vf32/OgUbJrmYwB0YGCgRAi5ZVnW97quv3AcZxQAYrHYZ5qmnUUikfTq6upH3iFt2872BFZV9aSx0QNCCKfr+gsAVJblsuM4cVEUawBoMBh8DgChUOgRAOr3+591DaaUshzH1RmGoV5PHccZlWW5jKZHg6qqJysrKx8DQCaTuQuASpL0smvw3t6e1ri99Wa74zhx/Hu7X6dSqdl2MR2XWhCES4ZhaC6XuwMAS0tLn3vlZRjmNRplj8fjnwJAOp2+B4A2ev1fMMuyV4qi/NFueZuHw+GHlFJW07QzNMqbSqVmvbIHAoEjADBNkwCghmE8bQnudEmSVHVdNxiJRNJDQ0PPvZ46jjMaDAaPpqenv04kEibP8xcAqGVZ2Y6ft80SRZEpFov3q9WqPjg4+HsymbTW1tb+vO6XSCTMzc3NvXK5HNA07e9SqdR+jLbTwsLCFxzHXaLRu1Ao9CiTydwtFAp6Op2+Z5om8TIVBOE8FotZPUM9RaPRCVVVz9BU/uY5DYBqmvZXX6GeCCGcbdtZv9//TJKklzzP10VRfGUYxlPLsrKU0rfa+g/fZXcfiGBcQQAAAABJRU5ErkJggg==        
        '''))

    def estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            font=_Font_Texto,
            rowheight=30,
            fieldbackground=default_scrText_bg
        )
        self.style.map("Treeview",
            background=[('selected', default_select_bg)],
            foreground=[('selected', default_select_fg)]
        )
        self.style.configure('TCombobox',
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
        )
        self.style.map('TCombobox',
            background=[
                ("active", default_select_fg)
            ]
        )

        self.style.configure('TSizegrip',
            background=default_menu_bg,
            borderwidth=0,
            border=0
        )

        self.style.configure('TFrame',
            background=default_bottom_app,
        )

        self.style.configure('TLabelframe',
            background=default_bottom_app,
        )
        self.style.configure('TLabelframe.Label',
            background=default_bottom_app,
            foreground=default_color_titulos,
            font=self._Font_Titulo_bold,
        )
        self.style.configure(
            'APP.TButton',
            background=default_bottom_app,
            foreground=default_boton_fg,
            relief="flat",
            border=0,
            highlightthickness=0,
            highlightbackground=default_bottom_app,
            activebackground=default_bottom_app,
            #font=(fuente_boton, tamñ_boton, weight_DF),
            borderwidth=0,
        )
        self.style.map(
            'APP.TButton',
            background=[("active", default_bottom_app)],
            foreground=[("active", default_boton_fg)],
            borderwidth=[("active", 0)],
            highlightbackground=[("active", default_bottom_app)],
            relief=[("active", "flat")],
            activebackground=[("active", default_boton_fg)],
            border=[("active", 0)],
            highlightthickness=[("active", 0)],
        )

        self.style.configure('TButton',
            font=_Font_Boton,
            background=default_boton_bg,
            borderwidth=1,
            relief='groove',
            #padding=5,
        )
        self.style.map('TButton',
            background=[("active", default_boton_acbg)],
            relief=[("active", 'ridge')],
            borderwidth=[("active", 1)],
        )

        self.style.configure('APP.TLabel',
            background=default_menu_bg,
            foreground=default_menu_fg,
            font=(fuente_titulos, 25, weight_DF)
        )

        self.style.configure('TLabel',
            background=default_bottom_app,
            foreground=default_color_subtitulos,
            font=self._Font_Titulo_bold
        )

    def menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self.root, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Pegar",
            accelerator='Ctrl+V',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo",
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar",
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña",
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.cerrar_vtn_desviacion
        )

    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)

    def _menu_clickDerecho_GLS(self):
        self.menu_Contextual_GLS = tk.Menu(self.root, tearoff=0)
        self.menu_Contextual_GLS.add_command(
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda e=self._list_clave: self._copiar_select_GLS_clave(e)
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

    def _menu_clickDerecho(self):
        self._menu_Contextual = tk.Menu(self.root, tearoff=0)
        self._menu_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background=bg_submenu)
        self._menu_Contextual.add_command(
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_command(
            label="  Pegar",
            accelerator='Ctrl+V',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background=bg_submenu)
        self._menu_Contextual.add_command(
            label="  Seleccionar todo",
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_command(
            label="  Limpiar",
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background=bg_submenu)
        self._menu_Contextual.add_command(
            label="  Cerrar pestaña",
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled'
        )
        self._menu_Contextual.add_command(
            label="  Salir",
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.root.quit
        )

    def _display_menu_clickDerecho(self, event):
        self._menu_Contextual.tk_popup(event.x_root, event.y_root)

    def cerrar_vtn_desviacion(self):
        if idOpenTab == 0:
            self.menu_Contextual.entryconfig(
                '  Cerrar pestaña', state='disabled')
        else:
            self.menu_Contextual.entryconfig(
                '  Cerrar pestaña', state='normal')
            self.cuaderno.forget(idOpenTab)
            self.cuaderno.notebookContent.forget(idOpenTab)

    def toChangeTab(self, event):
        global idOpenTab
        global value
        global modo_dark
        global PST_DESV
        # if activar_modo == 'True':
        idOpenTab = event.widget.index('current')
        tab = event.widget.tab(idOpenTab)['text']

        if idOpenTab != 0:
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
        elif idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
            self.cuaderno._release_callback(e=None)
        else:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')

        if tab == 'WorkSpace  ':
            self.fileMenu.entryconfig('  Clientes', state='disabled')
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
        else:
            self.fileMenu.entryconfig('  Clientes', state='normal')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')

        if tab == 'Issues EXTRACIONES':
            self.fileMenu.entryconfig('  Clientes', state='disabled')
            self.editMenu.entryconfig('  Buscar', state='normal')
        else:
            self.editMenu.entryconfig('  Buscar', state='disabled')

        try:
            expandir.cerrar_vtn_expandir()
        except:
            pass
        modo_dark = parse.get('dark', 'modo_dark')
        if activar_modo == 'True':
            self.MODE_DARK()
        self._cerrar_vtn_bsc()
        self.EXT_motion()

    def _cerrar_vtn_bsc(self):
        try:
            extracion._on_closing_busca_top()
        except AttributeError:
            pass

    def nameOpenButton(self):
        idx = self.IssuesVar.get()
        itm = listButton[idx]
        self.openButton(itm)

    def openButton(self, button):
        if button == "DESVIACIONES":
            self.openButtonDesviacion()
        elif button ==  "EXTRACIONES":
            self.openButtonExtracion()
        else:
            self.openButtonAutomatizacion()

    def openButtonDesviacion(self):
        global idOpenTab
        global desviacion
        desviacion = Desviacion(self.cuaderno)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES ')

    def openButtonExtracion(self):
        global APP_EXT
        from DataExtraction import Extracion, PST_EXT
        global idpTab
        global extracion
        try:
            APP_EXT._on_closing_busca_top()
        except:
            pass
        #extracion = Extracion(self.cuaderno, app, application=self)
        extracion = Extracion(self.cuaderno, app)
        APP_EXT = extracion
        self.cuaderno.add(extracion, text='Issues EXTRACIONES')
        #APP_EXT.bind("<Motion>", lambda e : self.EXT_motion(e))
        idpTab = self.cuaderno.index('current')
    
    def EXT_motion(self):
        from DataExtraction import PST_EXT
        global APP_EXT
        APP_EXT = PST_EXT
        self.MODE_DARK()
        

    def openButtonAutomatizacion(self):
        from Scripts import Automatizar
        global idpTab
        global automatizar
        automatizar = Automatizar(self.cuaderno, app, application=self)
        automatizar.fr_clt = ""
        self.cuaderno.add(automatizar, text='Automatizacion ')
        idpTab = self.cuaderno.index('current')

    def ocultar(self):
        partial(extracion.close_frame, even=None)

    def bsc(self):
        extracion.searchPanel()

    def loadClient(self):
        index = self.varClientMenu.get()
        customer = listClient[int(index)]
        desviacion.loadModule(customer)

    def label_resize(self, event):
        event.widget['wraplength'] = event.width

    def cerrar_vtn(self):
        self.vtn_acerca_de.destroy()

    def cerrar_vtn_gls(self):
        self.vtn_glosario.destroy()

    def _acerca_de(self):
        self.vtn_acerca_de = tk.Toplevel(self.root)
        self.vtn_acerca_de.config(background=default_bottom_app)
        window_wh = 780
        window_hg = 400
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_acerca_de.geometry(
            f'{window_wh}x{window_hg}+{position_right}+{position_top}')
        self.vtn_acerca_de.tk.call('wm', 'iconphoto', self.vtn_acerca_de._w, tk.PhotoImage(
            file=pathIcon+r'acercaDe.png'))
        self.vtn_acerca_de.transient(self.root)
        self.vtn_acerca_de.resizable(False, False)
        self.vtn_acerca_de.title("Acerca de")

        self.close_icon = ImageTk.PhotoImage(
            Image.open(pathIcon+r"close1.png").resize((80, 60)))

        self.icono_Acerca_de = ImageTk.PhotoImage(
            Image.open(pathIcon+r"img_acerca_de.png").resize((200, 200)))

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
        # self.AcercaDe_txt_frame.pack_propagate(False)

        # ? FONT ACERCA DE...
        self.lbl1 = ttk.Label(
            self.AcercaDe_txt_frame,
            foreground=default_color_titulos,
            text='CONTINUOUS COMPLIANCE',
            anchor='center',
            font=(fuente_titulos, 16, "bold")
        )
        self.lbl1.grid(row=0, column=0, padx=10, pady=20, sticky='nsew')

        self.lbl5 = ttk.Label(
            self.AcercaDe_txt_frame,
            width=40,
            text='Herramienta para resolucion de ISSUES Desviaciones / Extraciones\n',
            anchor='w',
            font=(fuente_titulos, 13)
        )
        self.lbl5.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.lbl5.bind("<Configure>", self.label_resize)

        self.lbl2 = ttk.Label(
            self.AcercaDe_txt_frame,
            text='Versión:   2.5',
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
            # width=20,
            foreground='gray',
            text='Documentado por el equipo de PHC - UNIX',
            anchor='w',
            font=(fuente_titulos, 11)
        )
        self.lbl6.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')

        self.lbl7 = ttk.Label(
            self.AcercaDe_txt_frame,
            # width=20,
            foreground='gray',
            text='Creado por Jose Alvaro Cedeño Panchana',
            anchor='w',
            font=(fuente_titulos, 11)
        )
        self.lbl7.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')

        self.lbl8 = ttk.Label(
            self.AcercaDe_txt_frame,
            # width=20,
            foreground='gray',
            text='Copyright © 2021 - 2022 Jose Alvaro Cedeño Panchana',
            anchor='w',
            font=(fuente_titulos, 11, 'bold')
        )
        self.lbl8.grid(row=7, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl8.bind("<Configure>", self.label_resize)

        self.boton = tk.Button(
            self.AcercaDe_txt_frame,
            text='Close',
            image=self.close_icon,
            command=self.cerrar_vtn
        )
        self.boton.grid(row=8, column=0, sticky='e', pady=10, padx=10)
        self.boton.config(
            background=default_bottom_app,
            activebackground=default_bottom_app,
            borderwidth=0,
            highlightbackground=default_bottom_app
        )

    def _cargar_modulo_glosario(self, *args):
        with open(pathFilesGl.format('GLOSARIO')) as g:
            data = json.load(g)
            listModulo = []
            listClave = []
            for md in data:
                listModulo.append(md['modulo'])
                listClave.append(md['clave'])
        #listModulo.sort()
        self._list_modulo.insert(tk.END, *listModulo)
        self._list_clave.insert(tk.END, *listClave)

    def on_select(self, event):
        global listbox_list
        print("select")
        widget = event.widget
        items = widget.curselection()
        for listbox in listbox_list:
            if listbox != widget:
                listbox.selection_clear(0, tk.END)
                for index in items:
                    listbox.selection_set(int(index))

    def _glosario(self):
        self.vtn_glosario = tk.Toplevel(self.root)
        self.vtn_glosario.config(background=default_bottom_app)
        window_width = 1000
        window_height = 500
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_glosario.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_glosario.tk.call('wm', 'iconphoto', self.vtn_glosario._w, tk.PhotoImage(
            file=pathIcon+r'acercaDe.png'))
        self.vtn_glosario.transient(self.root)
        self.vtn_glosario.resizable(False, False)
        self.vtn_glosario.title("Ayuda")

        self.close_icon_gls = ImageTk.PhotoImage(
            Image.open(pathIcon+r"close1.png").resize((80, 60)))

        self.fr1_gls = ttk.Frame(
            self.vtn_glosario,
            height=20,
        )
        self.fr1_gls.pack(fill='both', side='top', expand=0)

        # ? FONt AYUDA
        self.titulo = ttk.Label(
            self.fr1_gls,
            text='PALABRAS CLAVES DESVIACIONES',
            font=(fuente_titulos, 20, weight_DF),
        )
        self.titulo.pack(expand=1, pady=10)

        self.fr2_gls = ttk.Frame(
            self.vtn_glosario,
        )
        self.fr2_gls.pack(fill='both', side=tk.TOP, expand=1)

        self.frame2 = ttk.Frame(
            self.fr2_gls,
        )
        self.frame2.pack(fill='both', side=tk.LEFT, expand=1, pady=10)

        self.frame2.rowconfigure(1, weight=1)

        # ? FONt AYUDA
        self.titulo_modulo = ttk.Label(
            self.frame2,
            text='MODULO',
            foreground=default_color_titulos,
            font=font.Font(family=fuente_titulos, size=16, weight='bold'),
            anchor='center',
            width=45
        )
        self.titulo_modulo.grid(
            row=0, column=0, sticky='nsew', pady=10, padx=5)

        self.ListModulo_yScroll = tk.Scrollbar(self.frame2, orient=tk.VERTICAL)

        # LISTBOX MODULO
        self._list_modulo = tk.Listbox(
            self.frame2,
            font=_Font_Texto,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            exportselection=False,
            highlightthickness=hhtk,
            highlightcolor=default_hglcolor,
            yscrollcommand=self.ListModulo_yScroll.set,
        )
        self._list_modulo.grid(
            row=1, column=0, sticky='nsew', pady=10, padx=(10, 0))
        listbox_list.append(self._list_modulo)

        self.frame3 = ttk.Frame(
            self.fr2_gls,
            width=30
        )
        self.frame3.pack(fill='both', side='right', expand=1, pady=10, padx=10)
        self.frame3.columnconfigure(0, weight=1)
        self.frame3.rowconfigure(1, weight=1)

        self.titulo_clave = ttk.Label(
            self.frame3,
            text='CLAVE',
            foreground=default_color_titulos,
            font=font.Font(family=fuente_titulos, size=16, weight='bold'),
            anchor='center'
        )
        self.titulo_clave.grid(
            row=0, column=0, sticky='nsew', pady=10, padx=5, columnspan=2)

        self.ListClave_yScroll = tk.Scrollbar(self.frame3, orient=tk.VERTICAL)

        # LISTBOX CLAVE
        self._list_clave = tk.Listbox(
            self.frame3,
            font=_Font_Texto,
            foreground=default_scrText_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            exportselection=False,
            highlightthickness=hhtk,
            highlightcolor=default_hglcolor,
            yscrollcommand=self.ListClave_yScroll.set,
        )
        self._list_clave.grid(row=1, column=0, sticky='nsew', pady=10,)

        self.fr3_gls = ttk.Frame(
            self.vtn_glosario,
            height=30
        )
        self.fr3_gls.pack(fill='both', side=tk.BOTTOM, expand=0, padx=10)

        self.boton_gls = tk.Button(
            self.fr3_gls,
            text='Close',
            image=self.close_icon_gls,
            command=self.cerrar_vtn_gls
        )
        self.boton_gls.pack(side=tk.RIGHT, padx=10, pady=10)
        self.boton_gls.config(
            background=default_bottom_app,
            activebackground=default_bottom_app,
            borderwidth=0,
            highlightbackground=default_bottom_app
        )

        listbox_list.append(self._list_clave)

        self.ListClave_yScroll.grid(row=1, column=1, pady=10, sticky='nse')
        self.ListModulo_yScroll.grid(row=1, column=1, pady=10, sticky='nse')

        self._list_modulo.bind('<<ListboxSelect>>', self.on_select)
        self._list_clave.bind('<<ListboxSelect>>', self.on_select)
        self._list_modulo.bind(
            "<Button-3>", self._display_menu_clickDerecho_GLS)

        self._cargar_modulo_glosario()
        self._menu_clickDerecho_GLS()

    def widgets_APP(self):

    #TODO FRAME PARA BUTTONS

        self.frameButtons = ttk.Frame(
            self.contenedor,
            #style='TFrame'
        )
        self.frameButtons.grid(row=0, column=0, pady=5, padx=5)

    # TODO BOTON DESVIACION
        self.rbOpenDesv = RadioButton(
            self.frameButtons,
            alto=Aplicacion.y_alto_btn,
            ancho=Aplicacion.x_ancho_btn,
            radio=50,
            width=5,
            bg_color=default_bottom_app,
        )
        self.btnOpenDesv = ttk.Button(
            self.rbOpenDesv,
            text='\nDESVIACIONES',
            style='APP.TButton',
            image=self.Automatizar_icon,
            compound='top',
            command=self.openButtonDesviacion,
        )
        self.btnOpenDesv.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Aplicacion.hg_btn,
            width=Aplicacion.wd_btn
        )
        self.rbOpenDesv.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

# TODO BOTON EXTRACION
        self.rbOpenExt = RadioButton(
            self.frameButtons,
            alto=Aplicacion.y_alto_btn,
            ancho=Aplicacion.x_ancho_btn,
            radio=50,
            width = 5,
            bg_color=default_bottom_app,
        )
        self.btnOpenExt = ttk.Button(
            self.rbOpenExt,
            text='\nEXTRACIONES',
            style='APP.TButton',
            image=self.Extracion_icon,
            compound='top',
            command=self.openButtonExtracion,
        )
        self.btnOpenExt.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Aplicacion.hg_btn,
            width=Aplicacion.wd_btn
        )
        self.rbOpenExt.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )

# TODO BOTON AUTOMATIZAR
        self.rbOpenAuto = RadioButton(
            self.frameButtons,
            alto=Aplicacion.y_alto_btn,
            ancho=Aplicacion.x_ancho_btn,
            radio=50,
            width = 5,
            bg_color=default_bottom_app,
        )
        self.btnOpenAuto = ttk.Button(
            self.rbOpenAuto,
            text='\nAUTOMATIZACION',
            style='APP.TButton',
            image=self.Automatizar_icon,
            compound='top',
            command=self.openButtonAutomatizacion,
        )
        self.btnOpenAuto.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=Aplicacion.hg_btn,
            width=Aplicacion.wd_btn
        )
        # self.rbOpenAuto.grid(
        #     row=0,
        #     column=2,
        #     padx=20,
        #     pady=20
        # )

        self.btnOpenDesv.bind('<Motion>', partial(
            self.active_radio_botton, self.rbOpenDesv, self.btnOpenDesv))
        self.btnOpenExt.bind('<Motion>', partial(
            self.active_radio_botton, self.rbOpenExt, self.btnOpenExt))
        self.btnOpenAuto.bind('<Motion>', partial(
            self.active_radio_botton, self.rbOpenAuto, self.btnOpenAuto))

        self.btnOpenDesv.bind("<Leave>", self._hide_event)
        self.btnOpenExt.bind("<Leave>", self._hide_event)
        self.btnOpenAuto.bind("<Leave>", self._hide_event)

        # # Aqui activamos los colores por defecto del radio button
        # # Tambien hay que llamar a la funcion en ='WorkSpace'
        # self.rbOpenDesv.canvas.bind('<Motion>', self.activeDefault)
        # self.rbOpenExt.canvas.bind('<Motion>', self.activeDefault)
        # self.rbOpenAuto.canvas.bind('<Motion>', self.activeDefault)
        #self.frameButtons.bind('<Motion>', self.activeDefault)
        #self.contenedor.bind("<Motion>", self.activeDefault)

# TODO BIENVANIDA

        self.frameLabel = ttk.Frame(
            self.contenedor,
        )

        self.frameLabel.grid(row=1, column=0, sticky='sew', columnspan=2)

        self.frameLabel.columnconfigure(0, weight=1)
        self.frameLabel.rowconfigure(0, weight=1)

        self.lbl_Bienvenido = ttk.Label(
            self.frameLabel,
            style='APP.TLabel',
            text='Bienvenido : '+user.upper(),
            anchor='center',
        )
        self.lbl_Bienvenido.grid(
            row=0,
            column=0,
            sticky='nsew',
            ipady=20
        )

    def menuBar(self):
        #* MENU
        self.bar = tk.Menu(self.root, relief=tk.FLAT, border=0)
        self.root.config(menu=self.bar)
        self.bar.config(
            background=default_menu_bg,
            foreground=default_menu_fg,
            font=_Font_Menu_bold,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
        )
        self.fileMenu = tk.Menu(self.bar, tearoff=0)
        self.fileMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
        )

        #* --- INICIAMOS SUB MENU de SUB MENU -------------------------- #
        self.clientMenu = tk.Menu(self.fileMenu, tearoff=0)
        self.issuesMenu = tk.Menu(self.fileMenu, tearoff=0)
        self.preferenceMenu = tk.Menu(self.fileMenu, tearoff=0)
        #* -------------------------------------------------- #
        
        #* AÑADIMOS SUB MENU A FILE
        self.fileMenu.add_cascade(
            label="  Abrir",
            compound=tk.LEFT,
            image=self.iconoNew,
            menu=self.issuesMenu
        )
        self.fileMenu.add_cascade(
            label="  Clientes",
            image=self.iconoCustomer,
            compound=tk.LEFT,
            menu=self.clientMenu
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_cascade(
            label="  Preferencias",
            image=self.preference,
            compound=tk.LEFT,
            menu=self.preferenceMenu,
            #command=self._fontchooser
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label="  Salir",
            image=self.iconoExit,
            compound=tk.LEFT,
            command=self.root.quit
        )
        self.fileMenu.add_separator()
        #? CONFIGURAMOS SUBMENU
        #?---------------------------------------------
        self.issuesMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            selectcolor=default_menu_fg
        )
        self.clientMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            selectcolor=default_menu_fg
        )
        self.preferenceMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            selectcolor=default_menu_fg
        )
        #?---------------------------------------------
        #todo AÑADIR ITEM AL SUBMENU
        #todo -----------------------------------------
        self.varClientMenu = tk.StringVar()
        for i, m in enumerate(listClient):
            self.clientMenu.add_radiobutton(
                label=m,
                variable=self.varClientMenu,
                value=i,
                command=self.loadClient
            )
        self.IssuesVar = tk.IntVar()
        for i, m in enumerate(listButton):
            self.issuesMenu.add_radiobutton(
                label=m,
                variable=self.IssuesVar,
                value=i,
                command=self.nameOpenButton
            )
        self.preferenceMenu.add_command(
            label="  Titulo",
            #image=self.preference,
            compound=tk.LEFT,
            command=self._fontchooser
        )
        self.preferenceMenu.add_separator()
        self.preferenceMenu.add_command(
            label="  Modo Dark",
            image=self.iconoModeDark,
            #state='disable',
            compound=tk.LEFT,
            command=self.activeModeDark
        )
        #todo -----------------------------------------

        #* MENU VER
        self.verMenu = tk.Menu(self.bar, tearoff=0)
        self.verMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
        )
        self.verMenu.add_command(
            label="  Incidencias Criticas",
            command=self.bsc,
            image=self.iconoIncident,
            compound=tk.LEFT,
            state="normal"
        )

        #* MENU EDIT
        self.editMenu = tk.Menu(self.bar, tearoff=0)
        self.editMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
        )
        self.editMenu.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            command=self.bsc,
            image=self.iconoFindBar,
            compound=tk.LEFT,
            state="disabled"
        )
        
        #* MENU HELP
        self.helpMenu = tk.Menu(self.bar, tearoff=0)
        self.helpMenu.config(
            background=bg_submenu,
            foreground=fg_submenu,
            font=_Font_Menu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
        )
        self.helpMenu.add_command(
            label="  Ayuda",
            image=self.iconoHelp,
            compound=tk.LEFT,
            command=self._glosario
        )
        self.helpMenu.add_separator()
        self.helpMenu.add_command(
            label="  Acerca de...",
            image=self.iconoAbout,
            compound=tk.LEFT,
            command=self._acerca_de
        )

        self.bar.add_cascade(label=" Archivo ", menu=self.fileMenu)
        self.bar.add_cascade(label=" Editar ", menu=self.editMenu)
        self.bar.add_cascade(label=" Ver ", menu=self.verMenu)
        self.bar.add_cascade(label=" Ayuda ", menu=self.helpMenu)

    def active_radio_botton(self, canva, button, *args):
        if modo_dark == 'True':
            canva.canvas.itemconfig(
                1, outline=pers_OutlineDark)
        elif modo_dark == 'False':
            canva.canvas.itemconfig(
                1, outline=pers_Outline)
        name = button['text']
        if name == "Account  ":
            name = "Open Window Account"
        elif name == "Command  ":
            name = "Open Window Command"
        elif name == "Id_Rsa  ":
            name = "Open Window Id_Rsa"
        elif name == "Service  ":
            name = "Open Window Service"
        elif name == "Authorized  ":
            name = "Open Window Authorized"
        elif name == "Permissions  ":
            name = "Open Window Permissions"
        self.openTooltip(button, name)

    def _fontchooser(self):
        from Preferencias import SelectFont
        ventanafont = SelectFont(None, "Ventana", app, application=self)

        #? REINCIIAR
        # python = sys.executable
        # os.execl(python, python, * sys.argv)

    def activeModeDark(self):
        global activar_modo
        global modo_dark
        if activar_modo == 'False':
            modo_dark = 'True'
            activar_modo = 'True'
            parse['dark'] = {"activar_modo": activar_modo, "modo_dark": modo_dark}
            with open(pathConfig.format("apariencia.ini"), 'w') as configfile:
                parse.write(configfile)
        elif activar_modo == 'True':
            modo_dark = 'False'
            activar_modo = 'False'
            parse['dark'] = {"activar_modo": activar_modo, "modo_dark": modo_dark}
            with open(pathConfig.format("apariencia.ini"), 'w') as configfile:
                parse.write(configfile)
        if 'desviacion' in globals():
            desviacion.llamada_colores()
        self.MODE_DARK()

    #@beep_error
    def MODE_DARK(self):
        global modo_dark
        global text_btnMode
        
        modo_dark = parse.get('dark', 'modo_dark')
        if modo_dark == 'True':
            text_btnMode = "Dark Mode OFF"
            self.cuaderno.btnMode['image'] = self.iconoSwitchOn
            self.cuaderno.btnMode.config(background=pers_bottom_app, highlightbackground=pers_bottom_app, activebackground=pers_bottom_app)
            self.root.configure(
                background=pers_bottom_app,
            )
            self.cuaderno.buttonTab_novo.config(background=pers_bottom_app)
            self.cuaderno.leftArrow.config(background=pers_bottom_app)
            self.cuaderno.rightArrow.config(background=pers_bottom_app)
            self.rbOpenExt.canvas.config(background=pers_bottom_app)
            self.rbOpenDesv.canvas.config(background=pers_bottom_app)
            self.rbOpenAuto.canvas.config(background=pers_bottom_app)
            self.rbOpenExt.canvas.itemconfig(1, fill=pers_bottom_app)
            self.rbOpenDesv.canvas.itemconfig(1 ,fill=pers_bottom_app)
            self.rbOpenAuto.canvas.itemconfig(1, fill=pers_bottom_app)
            self.bar.config(
                background=pers_menu_bg,
                foreground=pers_scrText_fg,
            )
            self.style.configure('ScrollableNotebook',
                                background=pers_menu_bg,
                                )
            self.style.configure("Treeview",
                    background=pers_scrText_bg,
                    foreground=pers_scrText_fg,
                    rowheight=30,
                    fieldbackground=pers_scrText_bg
            )
            self.style.map("Treeview",
                background=[('selected', default_select_bg)],
                foreground=[('selected', default_select_fg)]
            )
            self.style.configure('TFrame',
                    background=pers_bottom_app,
            )
            self.style.configure('TLabelframe',
                    background=pers_bottom_app,
            )
            self.style.configure('TLabelframe.Label',
                        background=pers_bottom_app
            )
            self.style.configure('APP.TLabel',
                        background=pers_menu_bg,
                        foreground=pers_scrText_fg,
            )
            self.style.configure('TLabel',
                        background=pers_bottom_app,
                        foreground='gray70',
            )
            self.style.configure('APP.TButton',
                        background=pers_bottom_app,
                        foreground=pers_scrText_fg,
            )
            self.style.map("APP.TButton",
                        background=[
                            ("active", pers_bottom_app),
                        ],
                        foreground=[("active", pers_scrText_fg)],
            )
            self.style.map("TButton",
                background=[
                    ("active", pers_OutlineDark),
                ]
            )
            self.style.map("ScrollableNotebook.Tab",
                        background=[
                            ("selected", pers_bottom_app),
                            ("active", color_act_bg_pestaña)
                        ],
                        foreground=[
                            ("selected", pers_scrText_fg),
                            ("active", pers_scrText_fg)
                        ]
                        )
            self.style.configure('TCombobox',
                background=pers_bottom_app,
                foreground=default_scrText_fg,
            )
            if APP_EXT != "":
                try:
                    APP_EXT.frameMain.config(background=pers_menu_bg)
                    APP_EXT.txt.config(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                    )
                    try:
                        APP_EXT.frameRadio.canvas.config(background=pers_scrText_bg)
                        APP_EXT.frameRadio.canvas.itemconfig(
                        1,
                        outline=pers_Outline
                        )
                    except AttributeError:
                        pass
                except TclError:
                    pass

            if PST_DESV != "":
                if PST_VTN != "":
                    try:
                        self.windowModeDark()
                    except TclError:
                        pass
                if PST_EXP != "":
                    try:
                        self.expandirModeDark()
                    except TclError:
                        pass
                PST_DESV.cambiar_icono(PST_DESV._btnAuth_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnAcc_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnComm_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnDir_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnIdr_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnSer_, app.icono_account1)
                app._hide_event()
                PST_DESV.DESV_btnAccount.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnAccount.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnCommand.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnCommand.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnDirectory.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnDirectory.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnAuthorized.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnAuthorized.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnIdrsa.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnIdrsa.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                    )
                PST_DESV.DESV_btnService.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnService.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                    )
                PST_DESV.DESV_entry.config(
                    background=pers_scrText_bg,
                    foreground=pers_scrText_fg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.DESV_ListBox.config(
                    background=pers_scrText_bg,
                    foreground=pers_scrText_fg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                )
                PST_DESV.DESV_OptionMenu.config(
                    background=pers_menu_bg,
                    foreground=pers_scrText_fg,
                    highlightbackground=pers_menu_bg,
                    highlightcolor=pers_hglcolor,
                )
                PST_DESV.DESVfr2_lblDescripcion.configure(
                    foreground='gray60',
                    background=pers_scrText_bg,
                )
                PST_DESV.DESV_scrCheck.configure(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.DESV_scrBackup.configure(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.DESV_scrEdit.configure(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.DESV_scrEvidencia.configure(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.DESV_scrRefresh.configure(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.asignar_iconos()
        elif modo_dark == 'False':
            text_btnMode = "Dark Mode ON"
            self.cuaderno.btnMode['image'] = self.iconoSwitchOff
            self.cuaderno.btnMode.config(background=default_bottom_app, highlightbackground=default_bottom_app, activebackground=default_bottom_app)
            self.root.configure(
                background=default_bottom_app,
            )
            self.cuaderno.buttonTab_novo.config(background=default_bottom_app)
            self.cuaderno.leftArrow.config(background=default_bottom_app)
            self.cuaderno.rightArrow.config(background=default_bottom_app)
            self.rbOpenExt.canvas.config(background=default_bottom_app)
            self.rbOpenDesv.canvas.config(background=default_bottom_app)
            self.rbOpenAuto.canvas.config(background=default_bottom_app)
            self.rbOpenExt.canvas.itemconfig(1, fill=default_bottom_app)
            self.rbOpenDesv.canvas.itemconfig(1 ,fill=default_bottom_app)
            self.rbOpenAuto.canvas.itemconfig(1, fill=default_bottom_app)
            self.bar.config(
                background=default_menu_bg,
                foreground=default_scrText_fg,
            )
            self.style.configure('ScrollableNotebook',
                        background=default_menu_bg,
            )
            app.estilos()
            self.style.configure("Treeview",
                background=default_scrText_bg,
                foreground=default_scrText_fg,
                font=_Font_Texto,
                rowheight=30,
                fieldbackground=default_scrText_bg
            )
            self.style.map("Treeview",
                background=[('selected', default_select_bg)],
                foreground=[('selected', default_select_fg)]
            )
            self.style.map("ScrollableNotebook.Tab",
                        background=[
                            ("selected", default_bottom_app),
                            ("active", color_act_bg_pestaña)
                        ],
                        foreground=[
                            ("selected", default_scrText_fg),
                            ("active", default_scrText_fg)
                        ]
                        )
            self.style.configure('TCombobox',
                                background=default_bottom_app,
                                foreground=default_scrText_fg,
                                #electbackground=default_scrText_fg,
                                #selectforeground=default_select_fg,
                                )
            if APP_EXT != "":
                try:
                    APP_EXT.frameMain.config(background=default_menu_bg)
                    APP_EXT.txt.config(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )
                    try:
                        APP_EXT.frameRadio.canvas.config(background="gray90")
                        APP_EXT.frameRadio.canvas.itemconfig(
                        1,
                        outline=default_scrText_fg
                        )
                    except AttributeError:
                        pass
                except TclError:
                    pass
            if PST_DESV != "":
                if PST_VTN != "":
                    try:
                        self.windowModeDefault()
                    except TclError:
                        pass
                if PST_EXP != "":
                    try:
                        self.expandirModeDefault()
                    except TclError:
                        pass
                PST_DESV.cambiar_icono(PST_DESV._btnAcc_, app.icono_account)
                PST_DESV.cambiar_icono(PST_DESV._btnAuth_, app.icono_account)
                PST_DESV.cambiar_icono(PST_DESV._btnComm_, app.icono_account)
                PST_DESV.cambiar_icono(PST_DESV._btnDir_, app.icono_account)
                PST_DESV.cambiar_icono(PST_DESV._btnIdr_, app.icono_account)
                PST_DESV.cambiar_icono(PST_DESV._btnSer_, app.icono_account)
                app._hide_event()
                PST_DESV.DESV_btnAccount.canvas.config(
                    background=default_bottom_app,
                )
                PST_DESV.DESV_btnAccount.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnCommand.canvas.config(
                    background=default_bottom_app,
                )
                PST_DESV.DESV_btnCommand.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnDirectory.canvas.config(
                    background=default_bottom_app,
                )
                PST_DESV.DESV_btnDirectory.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnAuthorized.canvas.config(
                    background=default_bottom_app,
                )
                PST_DESV.DESV_btnAuthorized.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnIdrsa.canvas.config(
                    background=default_bottom_app,
                )
                PST_DESV.DESV_btnIdrsa.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_btnService.canvas.config(
                    background=default_bottom_app,
                )
                PST_DESV.DESV_btnService.canvas.itemconfig(
                    1,
                    fill=default_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.DESV_entry.config(
                    background=default_scrText_bg,
                    foreground=default_scrText_fg,
                    highlightbackground=default_Framework,
                    highlightcolor=default_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=default_hglcolor
                )
                PST_DESV.DESV_ListBox.config(
                    background=default_scrText_bg,
                    foreground=default_scrText_fg,
                    highlightbackground=default_Framework,
                    highlightcolor=default_hglcolor,
                    highlightthickness=hhtk,
                )
                PST_DESV.DESV_OptionMenu.config(
                    background=default_menu_bg,
                    foreground=default_scrText_fg,
                    highlightbackground=default_Framework,
                    highlightcolor=default_hglcolor,
                )
                PST_DESV.DESVfr2_lblDescripcion.configure(
                    foreground='gray60',
                    background=default_bottom_app,
                )
                PST_DESV.DESV_scrCheck.configr()
                PST_DESV.DESV_scrBackup.configr()
                PST_DESV.DESV_scrEdit.configr()
                PST_DESV.DESV_scrRefresh.configr()
                PST_DESV.DESV_scrEvidencia.configr()
                PST_DESV.asignar_iconos()
        self.changeTextButton(text_btnMode)

    #todo MODO PARA LA CLASE EXPANDIR
    def expandirModeDefault(self):
        PST_EXP.colourLineExpandir(
                default_scrText_bg,
                default_colourCodeBg,
                default_colourCodeFg,
                default_colourNoteFg
        )
        PST_EXP.vtn_expandir.config(
                                    background=default_bottom_app,
                            )
        PST_EXP.EXP_btn_Siguiente.config(
                                background=default_bottom_app,
                                activebackground=default_bottom_app
                            )
        PST_EXP.EXP_btn_Anterior.config(
                                background=default_bottom_app,
                                activebackground=default_bottom_app
                            )
        PST_EXP.EXP_scrExpandir.config(
                            foreground=default_scrText_fg,
                            background=default_scrText_bg,
                            highlightbackground=default_Framework,
                            highlightcolor=default_hglcolor,
                            highlightthickness=hhtk,
                            insertbackground=default_hglcolor
                            )
        PST_EXP.EXP_btnDirectory.canvas.itemconfig(1,
                        fill=default_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnAuthorized.canvas.itemconfig(1,
                        fill=default_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnService.canvas.itemconfig(1,
                        fill=default_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnAccount.canvas.itemconfig(1,
                        fill=default_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnCommand.canvas.itemconfig(1,
                        fill=default_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnIdrsa.canvas.itemconfig(1,
                        fill=default_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnDirectory.canvas.config(background=default_bottom_app)
        PST_EXP.EXP_btnAuthorized.canvas.config(background=default_bottom_app)
        PST_EXP.EXP_btnService.canvas.config(background=default_bottom_app)
        PST_EXP.EXP_btnAccount.canvas.config(background=default_bottom_app)
        PST_EXP.EXP_btnCommand.canvas.config(background=default_bottom_app)
        PST_EXP.EXP_btnIdrsa.canvas.config(background=default_bottom_app)

    def expandirModeDark(self):
        PST_EXP.colourLineExpandir(
                pers_scrText_bg,
                pers_colourCodeBg,
                pers_colourCodeFg,
                pers_colourNoteFg
        )
        PST_EXP.vtn_expandir.config(
                                    background=pers_bottom_app,
                            )
        PST_EXP.EXP_btn_Siguiente.config(
                                background=pers_bottom_app,
                                activebackground=pers_bottom_app
                            )
        PST_EXP.EXP_btn_Anterior.config(
                                background=pers_bottom_app,
                                activebackground=pers_bottom_app
                            )
        PST_EXP.EXP_scrExpandir.config(
                            foreground=pers_scrText_fg,
                            background=pers_scrText_bg,
                            highlightbackground=pers_Framework,
                            highlightcolor=pers_hglcolor,
                            highlightthickness=hhtk,
                            insertbackground=pers_hglcolor
                            )
        PST_EXP.EXP_btnDirectory.canvas.itemconfig(1,
                        fill=pers_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnAuthorized.canvas.itemconfig(1,
                        fill=pers_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnService.canvas.itemconfig(1,
                        fill=pers_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnAccount.canvas.itemconfig(1,
                        fill=pers_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnCommand.canvas.itemconfig(1,
                        fill=pers_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnIdrsa.canvas.itemconfig(1,
                        fill=pers_bottom_app,
                        outline=default_Outline)
        PST_EXP.EXP_btnDirectory.canvas.config(background=pers_bottom_app)
        PST_EXP.EXP_btnAuthorized.canvas.config(background=pers_bottom_app)
        PST_EXP.EXP_btnService.canvas.config(background=pers_bottom_app)
        PST_EXP.EXP_btnAccount.canvas.config(background=pers_bottom_app)
        PST_EXP.EXP_btnCommand.canvas.config(background=pers_bottom_app)
        PST_EXP.EXP_btnIdrsa.canvas.config(background=pers_bottom_app)

    #todo MODO PARA LA CLASE VENTANA
    def windowModeDark(self):
        PST_VTN.vtn_ventanas.config(
            background=pers_bottom_app,
        )
        PST_VTN.srcRisk.configure(
            foreground=pers_scrText_fg,
            background=pers_scrText_bg,
            highlightbackground=pers_Framework,
            highlightcolor=pers_hglcolor,
            highlightthickness=hhtk,
            insertbackground=pers_hglcolor
        )
        PST_VTN.srcImpact.configure(
            foreground=pers_scrText_fg,
            background=pers_scrText_bg,
            highlightbackground=pers_Framework,
            highlightcolor=pers_hglcolor,
            highlightthickness=hhtk,
            insertbackground=pers_hglcolor
        )
        PST_VTN.srcVariable.configure(
            foreground=pers_scrText_fg,
            background=pers_scrText_bg,
            highlightbackground=pers_Framework,
            highlightcolor=pers_hglcolor,
            highlightthickness=hhtk,
            insertbackground=pers_hglcolor
        )
        PST_VTN.srcRisk.configure(
            foreground=pers_scrText_fg,
            background=pers_scrText_bg,
            highlightbackground=pers_Framework,
            highlightcolor=pers_hglcolor,
            highlightthickness=hhtk,
            insertbackground=pers_hglcolor
        )
        PST_VTN.listServer.config(
            background=pers_scrText_bg,
            foreground=pers_scrText_fg,
            highlightbackground=pers_Framework,
            highlightcolor=pers_hglcolor,
            highlightthickness=hhtk,
        )
        PST_VTN.VTN_entry.config(
            background=pers_scrText_bg,
            foreground='gray75',
            highlightbackground=pers_Framework,
            highlightcolor=pers_hglcolor,
            highlightthickness=hhtk,
            insertbackground=pers_hglcolor
        )

    def windowModeDefault(self):
        PST_VTN.vtn_ventanas.config(
            background=default_bottom_app,
        )
        PST_VTN.srcRisk.configure(
            foreground=default_scrText_fg,
            background=default_scrText_bg,
            highlightbackground=default_Framework,
            highlightcolor=default_hglcolor,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor
        )
        PST_VTN.srcImpact.configure(
            foreground=default_scrText_fg,
            background=default_scrText_bg,
            highlightbackground=default_Framework,
            highlightcolor=default_hglcolor,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor
        )
        PST_VTN.srcVariable.configure(
            foreground=default_scrText_fg,
            background=default_scrText_bg,
            highlightbackground=default_Framework,
            highlightcolor=default_hglcolor,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor
        )
        PST_VTN.listServer.config(
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            highlightbackground=default_Framework,
            highlightcolor=default_hglcolor,
            highlightthickness=hhtk,
        )
        PST_VTN.VTN_entry.config(
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            highlightbackground=default_Framework,
            highlightcolor=default_hglcolor,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor
        )

    def _hide_event(self, event=None):
        self.hidetip()

    def hidetip(self):
        global tooltip
        try:
            custom.destroy()
            tooltip = False
        except TclError:
            pass
        self.activeDefault()

    def openTooltip(self, object, text, *args):
        global custom
        global tooltip
        if tooltip == False:
            custom = CustomHovertip(object, text=text)
            tooltip = True

    ## --- ACTIVAR MODO SOLO LECTURA ----------------------------- ##
    def widgets_SoloLectura(self, event):
        if(20 == event.state and event.keysym == 'c' or event.keysym == 'Down' or event.keysym == 'Up' or 20 == event.state and event.keysym == 'f' or 20 == event.state and event.keysym == 'a'):
            return
        else:
            return "break"
    
    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()