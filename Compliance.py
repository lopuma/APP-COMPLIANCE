#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Jose Alvaro Cedeño 2022
# For license see LICENSE
import json
import os
import time
import subprocess
import sys
from getpass import getuser
from tkinter import TclError, scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font
import tkinter as tk
from PIL import Image, ImageTk
from ScrollableNotebook import *
from RadioBotton import RadioButton
from functools import partial
from configparser import ConfigParser
from Tooltip import CustomHovertip
#-----------------------------------------------------------#
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
pathFileCustomer = mypath+"Compliance/file/desviaciones_{}.json"
pathFileCustomer_clave = mypath+"Compliance/file/{}.json"
path_config = mypath+"Compliance/.conf/{}.json"
path_config_ini = mypath+"Compliance/.conf/{}"

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
PST_EXT = ""
PST_VTN = ""
# TODO----------------------
_tt_Desv = ""
listbox_list = []
no_exist = False
extracion = ""
act_rbtn_ = False
act_rbtn_auto = False

# * Configuracion de APARIENCIA INICIAL
parse = ConfigParser()
parse.read(path_config_ini.format("apariencia.ini"))

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
default_colourCodeBg = '#FFE7E7'
default_color_line_fg = '#1E90FF'
default_colourNoteFg = '#7A7A7A'
default_Framework = '#838389'
default_panelBg = 'red'
acdefault_panelBg = 'blue'

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

# * COLOR PERSONALIZADO
pers_scrText_fg = '#f4f4f4'
pers_color_titulo = '#FF8080'
pers_menu_bg = '#353535'  # ? COLOR PRIMARIO
pers_bottom_app = '#454545'  # ? SECUNDARIO
pers_scrText_bg = '#555555'  # ? PARA CUADRO DE TEXTO
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
        window_width = 1010
        window_height = 650
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_expandir.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        #self.vtn_expandir.tk.call('wm', 'iconphoto', self.vtn_expandir._w, tk.PhotoImage(file=path_icon+r'expandir1.png'))
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
        self.EXP_srcExpandir.bind(
            "<Button-3><ButtonRelease-3>", self.display_menu_clickDerecho)
        self.EXP_srcExpandir.bind(
            "<Motion>", lambda e: desviacion.activar_Focus(e))
        self.EXP_srcExpandir.bind(
            "<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.EXP_srcExpandir.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.EXP_srcExpandir.bind(
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
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['copia']
                            if self._txt_Desv is None:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, md['editar'])
                                self.varNum = 3
                                self.descativar_botones()
                            else:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 2
                                self.descativar_botones()
        elif self.varNum == 2:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['editar']
                            if self._txt_Desv is None:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(
                                    tk.END, md['refrescar'])
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 4
                                self.descativar_botones()
                            else:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 3
                                self.descativar_botones()
        elif self.varNum == 3:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['refrescar']
                            if self._txt_Desv is None:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(
                                    tk.END, md['evidencia'])
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                                self.descativar_botones()
                            else:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 4
        elif self.varNum == 4:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['evidencia']
                            if self._txt_Desv is None:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(
                                    tk.END, md['comprobacion'])
                                self.varNum = 1
                                self.activar_botones()
                            else:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                            self.descativar_botones()
        elif self.varNum == 5:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['comprobacion']
                            if self._txt_Desv is None:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, md['copia'])
                                self.varNum = 2
                                self.descativar_botones()
                            else:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 1
                                self.activar_botones()
        if modo_dark == 'False':
            self.expandirColourLine(
                default_scrText_bg,
                default_colourCodeBg,
                default_colourCodeFg,
                default_colourNoteFg
            )
        else:
            PST_EXP.expandirColourLine(
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
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['evidencia']
                            if self._txt_Desv is None:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(
                                    tk.END, md['refrescar'])
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 4
                                self.descativar_botones()
                            else:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                                self.descativar_botones()
        elif self.varNum == 2:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['comprobacion']
                            if self._txt_Desv is None:
                                _tt_Desv = "EVIDENCIA"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(
                                    tk.END, md['evidencia'])
                                self.EXP_btnScreamEvidencia.config(state="normal")
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 5
                                self.descativar_botones()
                            else:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 1
                                self.activar_botones()
        elif self.varNum == 3:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['copia']
                            if self._txt_Desv is None:
                                _tt_Desv = "COMPROBACION"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(
                                    tk.END, md['evidencia'])
                                self.varNum = 1
                                self.activar_botones()
                            else:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 2
                                self.descativar_botones()
        elif self.varNum == 4:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['editar']
                            if self._txt_Desv is None:
                                _tt_Desv = "BACKUP"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, md['copia'])
                                self.varNum = 2
                                self.descativar_botones()
                            else:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.varNum = 3
                                self.descativar_botones()
        elif self.varNum == 5:
            with open(pathFileCustomer.format(customer)) as g:
                data = json.load(g)
                for md in data:
                    if 'modulo' in md:
                        if value in md['modulo']:
                            self._txt_Desv = md['refrescar']
                            if self._txt_Desv is None:
                                _tt_Desv = "EDITAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, md['editar'])
                                self.varNum = 2
                                self.descativar_botones()
                            else:
                                _tt_Desv = "REFRESCAR"
                                self.EXP_lblWidget['text'] = _tt_Desv
                                self.EXP_srcExpandir.delete('1.0', tk.END)
                                self.EXP_srcExpandir.insert(tk.END, self._txt_Desv)
                                self.EXP_btnCopyALL.config(state="normal")
                                self.varNum = 1
        if modo_dark == 'False':
            self.expandirColourLine(
                default_scrText_bg, 
                default_colourCodeBg, 
                default_colourCodeFg, 
                default_colourNoteFg
            )
        else:
            PST_EXP.expandirColourLine(
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
        self.EXP_lblWidget = ttk.Label(
            self.vtn_expandir,
            text=self.titulo,
            foreground=default_color_titulos,
        )
        self.EXP_lblWidget.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        self.EXP_srcExpandir = st.ScrolledText(
            self.vtn_expandir,
        )
        self.EXP_srcExpandir.config(
            font=_Font_txt_exp,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightthickness=hhtk,
            highlightbackground=default_Framework,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
        )
        self.EXP_srcExpandir.insert('1.0', self.txt_Expan)
        
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
        self.EXP_btn_Siguiente.grid(row=0, column=2, pady=10, padx=(0,10), sticky='ns')

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
        self.EXP_btn_Anterior.grid(row=0, column=1, pady=10, padx=10, sticky='ns')

        self.EXP_btnCopyALL = ttk.Button(
            self.vtn_expandir,
            image=desviacion.icono_copiar,
            style='APP.TButton',
            state="disabled",
            command=lambda e=self.EXP_srcExpandir: self.copiarALL(e),
        )
        self.EXP_btnCopyALL.grid(row=0, column=4, pady=15, sticky='ns')
        
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
            image=desviacion.icono_reducir,
            #style='APP.TButton',
            command=self.cerrar_vtn_expandir,
        )
        self.EXP_btnReducir.grid(row=0, column=6, padx=20, pady=17, sticky='ne')
        
        self.EXP_srcExpandir.grid(
            row=1, column=0, padx=5, pady=5, sticky='nsew', columnspan=7)

        self.activar_botones()

    def descativar_botones(self):
        self.EXP_btnDirectory.grid_forget()
        self.EXP_btnAuthorized.grid_forget()
        self.EXP_btnService.grid_forget()
        self.EXP_btnAccount.grid_forget()
        self.EXP_btnCommand.grid_forget()
        self.EXP_btnIdrsa.grid_forget()

    def expandirColourLine(self, 
        bg_color, 
        bg_codigo, 
        fg_codigo, 
        fg_nota):
        PST_EXP.EXP_srcExpandir.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_txt_exp_cdg
        )
        PST_EXP.EXP_srcExpandir.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=font.Font(family=_Font_Texto, size=20, weight='bold')
        )
        PST_EXP.EXP_srcExpandir.tag_configure(
            "nota",
            background=bg_color,
            foreground=fg_nota,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_txt_exp
        )

        end = PST_EXP.EXP_srcExpandir.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_EXP.EXP_srcExpandir.search("##", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_srcExpandir.tag_add(
                    "codigo", startline, endline)
            if (PST_EXP.EXP_srcExpandir.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_srcExpandir.tag_add(
                    "line", startline, endline)
            if (PST_EXP.EXP_srcExpandir.search("//", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXP.EXP_srcExpandir.tag_add(
                    "nota", startline, endline)

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
        with open(pathFileCustomer.format(customer)) as g:
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
        with open(pathFileCustomer.format(customer)) as g:
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
        self.bind("<Motion>", lambda e: self.DESV_motion(e))
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
        self.DESVfr2_srcBackup.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_scrEdit.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESVfr3_srcRefrescar.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_scrEvidencia.bind(
            "<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_entryModule.bind(
            "<Motion>", lambda e: self._act_focus_ent(e))
        app.cuaderno.bind("<Motion>", lambda e: self.activar_Focus(e))
        self.DESV_ListBox.bind("<Motion>", lambda e: self._activar_Focus(e))

## --- MOSTRAR MENU DERECHO  --- ##
        self.DESV_scrCheck.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESVfr2_srcBackup.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESV_scrEdit.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESVfr3_srcRefrescar.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)
        self.DESV_scrEvidencia.bind(
            "<Button-3><ButtonRelease-3>", self._display_menu_clickDerecho)

## --- ACTIVAR MODO SOLO LECTURA --- ##
        self.DESV_scrCheck.bind(
            "<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr2_srcBackup.bind(
            "<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESV_scrEdit.bind(
            "<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcRefrescar.bind(
            "<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESV_scrEvidencia.bind(
            "<Key>", lambda e: self.widgets_SoloLectura(e))


## --- SELECCIONAR TOD --- ##
        self.DESV_scrCheck.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr2_srcBackup.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))

## --- BIND --- ##
        self.DESV_entryModule.bind(
            "<Return>", lambda event=None: self.findModule(self.DESV_entryModule.get()))
        self.DESV_entryModule.bind(
            "<KeyPress>", lambda e: self.clear_bsq_buttom(e))
        self.DESV_ListBox.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESV_ListBox.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_ListBox.bind("<Down>", lambda e: self.ListDown(e))
        self.DESV_ListBox.bind("<Up>", lambda e: self.ListUp(e))
        self.DESV_entryModule.bind(
            '<Control-x>', lambda e: self._clear_busqueda(e))
        self.DESV_entryModule.bind(
            "<FocusIn>", lambda e: self.clear_busqueda(e))
        self.DESV_entryModule.bind(
            "<FocusOut>", lambda e: self.clear_busqueda(e))

        self.DESV_scrCheck.bind(
            '<Control-f>', lambda e: self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESV_scrCheck.bind(
            '<Control-F>', lambda e: self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrCheck.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESVfr2_srcBackup.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrCheck.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESVfr2_srcBackup.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEdit.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcRefrescar.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESV_scrEvidencia.bind(
            '<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESV_scrEdit.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrEvidencia.bind('<Control-F>', lambda e: self.buscar(e))
        self.DESV_scrEdit.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcRefrescar.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEvidencia.bind(
            '<Control-c>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEdit.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcRefrescar.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEvidencia.bind(
            '<Control-C>', lambda e: self._copiar_texto_seleccionado(e))
        self.DESV_scrEdit.bind('<Control-f>', lambda e: self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-f>', lambda e: self.buscar(e))
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
            Image.open(path_icon+r"buscar.png").resize((25, 25)))
        self.LimpiarModulo_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"limpiar.png").resize((25, 25)))
        self.icono_expandir = ImageTk.PhotoImage(
            Image.open(path_icon+r"expandir.png").resize((40, 40)))
        self.icono_expandir1 = ImageTk.PhotoImage(
            Image.open(path_icon+r"expandir1.png").resize((40, 40)))
        self.icono_expandir2 = ImageTk.PhotoImage(
            Image.open(path_icon+r"expandir2.png").resize((40, 40)))
        self.icono_recortar = ImageTk.PhotoImage(
            Image.open(path_icon+r"recortar.png").resize((40, 40)))
        self.icono_recortar1 = ImageTk.PhotoImage(
            Image.open(path_icon+r"recortar1.png").resize((40, 40)))
        self.icono_recortar2 = ImageTk.PhotoImage(
            Image.open(path_icon+r"recortar2.png").resize((40, 40)))
        self.icono_captura = ImageTk.PhotoImage(
            Image.open(path_icon+r"captura.png").resize((40, 40)))
        self.icono_captura1 = ImageTk.PhotoImage(
            Image.open(path_icon+r"captura1.png").resize((40, 40)))
        self.icono_captura2 = ImageTk.PhotoImage(
            Image.open(path_icon+r"captura2.png").resize((40, 40)))
        self.icono_reducir = ImageTk.PhotoImage(
            Image.open(path_icon+r"reduce.png").resize((30, 30)))
        self.icono_copiar = ImageTk.PhotoImage(
            Image.open(path_icon+r"copiar.png").resize((40, 40)))
        self.icono_copiar1 = ImageTk.PhotoImage(
            Image.open(path_icon+r"copiar1.png").resize((40, 40)))
        self.icono_copiar2 = ImageTk.PhotoImage(
            Image.open(path_icon+r"copiar2.png").resize((40, 40)))
        self.icono_riesgos = ImageTk.PhotoImage(
            Image.open(path_icon+r"riesgos.png").resize((40, 40)))
        self.icono_riesgos1 = ImageTk.PhotoImage(
            Image.open(path_icon+r"riesgos1.png").resize((40, 40)))
        self.icono_riesgos2 = ImageTk.PhotoImage(
            Image.open(path_icon+r"riesgos2.png").resize((40, 40)))

## --- ADJUTAR EL TEXT DE LOS LABEL -------------------------- ##
    def label_resize(self, event):
        event.widget['wraplength'] = event.width

## --- ACTIVAR MODO SOLO LECTURA ----------------------------- ##
    def widgets_SoloLectura(self, event):
        if(20 == event.state and event.keysym == 'c' or event.keysym == 'Down' or event.keysym == 'Up' or 20 == event.state and event.keysym == 'f' or 20 == event.state and event.keysym == 'a'):
            return
        else:
            return "break"

## --- ACTIVAR WIDGET ---------------------------------------- ##
    def _act_focus_ent(self, event):
        self.txtWidget = event.widget
        # self.txtWidget.select_range(0,tk.END)
        self.txtWidget.focus_set()
        self.DESV_scrCheck.tag_remove("sel", "1.0", "end")
        self.DESVfr2_srcBackup.tag_remove("sel", "1.0", "end")
        self.DESV_scrEdit.tag_remove("sel", "1.0", "end")
        self.DESVfr3_srcRefrescar.tag_remove("sel", "1.0", "end")
        self.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        return 'break'

    def activar_Focus(self, event):
        global txtWidget
        global txtWidget_focus
        global PST_DESV
        txtWidget = event.widget
        if txtWidget == self.DESV_entryModule:
            txtWidget.focus()
            self.DESV_scrCheck.tag_remove("sel", "1.0", "end")
            self.DESVfr2_srcBackup.tag_remove("sel", "1.0", "end")
            self.DESV_scrEdit.tag_remove("sel", "1.0", "end")
            self.DESVfr3_srcRefrescar.tag_remove("sel", "1.0", "end")
            self.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        elif txtWidget == self.DESV_scrCheck:
            # srcCom = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESVfr2_srcBackup.tag_remove("sel", "1.0", "end")
            self.DESV_scrEdit.tag_remove("sel", "1.0", "end")
            self.DESVfr3_srcRefrescar.tag_remove("sel", "1.0", "end")
            self.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        elif txtWidget == self.DESVfr2_srcBackup:
            # srcBac = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == self.DESV_scrEdit:
            # srcEdi = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESV_scrCheck.tag_remove("sel", "1.0", "end")
            self.DESVfr2_srcBackup.tag_remove("sel", "1.0", "end")
            self.DESVfr3_srcRefrescar.tag_remove("sel", "1.0", "end")
            self.DESV_scrEvidencia.tag_remove("sel", "1.0", "end")
        elif txtWidget == self.DESVfr3_srcRefrescar:
            # srcRes = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == self.DESV_scrEvidencia:
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

    def cambiar_icono(self, btn, icono1, *arg):
        btn['image'] = icono1
        name = btn['text']
        app.openTooltip(btn, name)

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
            print("EJECUTA TRUE")
            app.expandirModeDark()
        elif modo_dark == 'False':
            print("EJECUTA FALSE")
            app.expandirModeDefault()
        
        # ---------------------------------------

        if tittleExpand == "REFRESCAR":
            expandir.EXP_btnCopyALL.config(state="normal")
        elif tittleExpand == "EVIDENCIA":
            varNum = 5
            expandir.EXP_btnScreamEvidencia.config(state="normal")
            expandir.EXP_btnCopyALL.config(state="normal")
        expandir.vtn_expandir.bind('<Motion>', app.activeDefault)

    def _menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda e=self.DESV_entryModule: self._buscar(e),
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
            #command=lambda e=self.DESV_entryModule:self.pegar_texto_seleccionado(e),
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
        if str(self.scrEvent) == str(self.DESV_entryModule):
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='normal')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig(
                '  Seleccionar todo', state='disabled')
            if len(self.DESV_entryModule.get()) > 0:
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
        self.DESV_entryModule.focus()
        self._buscar_Ativate_focus()

    def _buscar_focus(self, event):
        entry_event = event.widget
        entry_event.select_range(0, tk.END)
        entry_event.focus_set()
        return 'break'

    def _buscar_Ativate_focus(self):
        self.DESV_entryModule.select_range(0, tk.END)
        self.DESV_entryModule.focus_set()
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
        self.DESVfr2_srcBackup.delete('1.0', tk.END)
        self.DESV_scrEdit.delete('1.0', tk.END)
        self.DESVfr3_srcRefrescar.delete('1.0', tk.END)
        self.DESV_scrEvidencia.delete('1.0', tk.END)

# --- SELECIONA UN ELEMNETO DEL LIST BOX ACTUAL
    def selectModule(self, event):
        global value
        customer = PST_DESV.varClient.get()
        list_event = event.widget
        index = list_event.curselection()
        value = list_event.get(index[0])
        self.loadSelectItem(value, customer)

# --- CARGA ELEMENTO SELECIONADO
    def loadSelectItem(self, selectionValue, customer):  # TODO CARGAR MODULO
        data = []
        with open(pathFileCustomer.format(customer)) as g:
            data = json.load(g)
            for md in data:
                if 'modulo' in md:
                    if selectionValue in md['modulo']:
                        self.limpiar_Widgets()
                        self._asignarValor_aWidgets(md)
                        self.showButtonsModule(selectionValue)

    def _loadSelectItem(self, selectionValue, customer):  # TODO CARGAR MODULO
        data = []
        with open(pathFileCustomer.format(customer)) as g:
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
            PST_DESV.DESVfr2_srcBackup.insert(tk.END, md['copia'])
            PST_DESV.DESV_btn2Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn2Expandir.config(state='disabled')

        if md['editar'] is not None:
            PST_DESV.DESV_scrEdit.insert(tk.END, md['editar'])
            PST_DESV.DESV_btn3Expandir.config(state='normal')
        else:
            PST_DESV.DESV_btn3Expandir.config(state='disabled')

        if md['refrescar'] is not None:
            PST_DESV.DESVfr3_srcRefrescar.insert(tk.END, md['refrescar'])
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
            self.DESVfr2_srcBackup.insert(tk.END, md['copia'])
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
            self.DESVfr3_srcRefrescar.insert(tk.END, md['refrescar'])
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
            PST_DESV.colour_line_com(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
            PST_DESV.colour_line_bak(default_scrText_bg, default_colourCodeBg, default_colourCodeFg)
            PST_DESV.colour_line_edi(default_scrText_bg, default_colourCodeBg, default_colourCodeFg)
            PST_DESV.colour_line_ref(default_scrText_bg, default_colourCodeBg, default_colourCodeFg)
            PST_DESV.colour_line_evi(default_scrText_bg, default_colourCodeBg, default_colourCodeFg)
        elif modo_dark == 'True':
            PST_DESV.colour_line_com(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg, pers_colourNoteFg)
            PST_DESV.colour_line_bak(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg)
            PST_DESV.colour_line_edi(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg)
            PST_DESV.colour_line_ref(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg)
            PST_DESV.colour_line_evi(pers_scrText_bg, pers_scrText_bg, pers_colourCodeFg)

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
                row=2, column=2, padx=5, pady=15, sticky='ne')
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
                row=2, column=2, padx=5, pady=15, sticky='ne')
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
                row=2, column=2, padx=5, pady=15, sticky='ne')
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
        with open(pathFileCustomer.format(customer)) as g:
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
            self.DESV_entryModule.focus()
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
                    listPathCustomer.append(pathFileCustomer.format(client))
                moduleToFind = PST_DESV.DESV_entryModule.get()
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
            with open(pathFileCustomer.format(customer)) as g:
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
            with open(pathFileCustomer.format(customer)) as g:
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
            with open(pathFileCustomer.format(customer)) as g:
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
            with open(pathFileCustomer.format(customer)) as g:
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
            with open(pathFileCustomer.format(customer)) as g:
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
        widget_event = self.DESV_entryModule
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
        self.loadSelectItem(modulo_selecionado)

    def ListUp(self, event):
        list_event = event.widget
        list_event.yview_scroll(-1, "units")
        selecion = list_event.curselection()[0]-1
        modulo_selecionado = list_event.get(selecion)
        self.loadSelectItem(modulo_selecionado)

    def enabled_Widgets(self):
        self.DESV_ListBox.config(state="normal")
        self.DESV_entryModule.config(state="normal")
        self.DESV_entryModule.focus()
        self.DESVfr1_btnBuscar.config(state="normal")
        self.DESV_scrCheck.config(state="normal")
        self.DESVfr2_srcBackup.config(state="normal")
        self.DESV_scrEdit.config(state="normal")
        self.DESVfr3_srcRefrescar.config(state="normal")
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
        self.DESV_entryModule.delete(0, tk.END)
        self.DESV_ListBox.delete(0, tk.END)
        self.limpiar_Widgets()
        self._disabled_buttons()
        self.disabled_btn_expandir()
        ## ----------------------------------------- ##
        with open(pathFileCustomer.format(customer)) as g:
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

    def colour_line_com(self, bg_color, bg_codigo, fg_codigo, fg_nota):
        PST_DESV.DESV_scrCheck.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        PST_DESV.DESV_scrCheck.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )

        PST_DESV.DESV_scrCheck.tag_configure(
            "nota",
            background=bg_color,
            foreground=fg_nota,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )

        end = PST_DESV.DESV_scrCheck.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_DESV.DESV_scrCheck.search("##", startline, stopindex=f"{line}.1")) and not (PST_DESV.DESV_scrCheck.search("// NOTA", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrCheck.tag_add(
                    "codigo", startline, endline)
            if (PST_DESV.DESV_scrCheck.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrCheck.tag_add(
                    "line", startline, endline)
            if (PST_DESV.DESV_scrCheck.search("//", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrCheck.tag_add(
                    "nota", startline, endline)

    def colour_line_bak(self, bg_color, bg_codigo, fg_codigo):
        PST_DESV.DESVfr2_srcBackup.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        PST_DESV.DESVfr2_srcBackup.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )
        end = PST_DESV.DESVfr2_srcBackup.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_DESV.DESVfr2_srcBackup.search("##", startline, stopindex=f"{line}.1")) or not (PST_DESV.DESVfr2_srcBackup.search("##", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"

                PST_DESV.DESVfr2_srcBackup.tag_add(
                    "codigo", startline, endline)

            if (PST_DESV.DESVfr2_srcBackup.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESVfr2_srcBackup.tag_add(
                    "line", startline, endline)

    def colour_line_ref(self, bg_color, bg_codigo, fg_codigo):
        PST_DESV.DESVfr3_srcRefrescar.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        PST_DESV.DESVfr3_srcRefrescar.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )
        end = PST_DESV.DESVfr3_srcRefrescar.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_DESV.DESVfr3_srcRefrescar.search("##", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESVfr3_srcRefrescar.tag_add(
                    "codigo", startline, endline)
            if (PST_DESV.DESVfr3_srcRefrescar.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESVfr3_srcRefrescar.tag_add(
                    "line", startline, endline)

    def colour_line_edi(self, bg_color, bg_codigo, fg_codigo):
        PST_DESV.DESV_scrEdit.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        PST_DESV.DESV_scrEdit.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )
        end = PST_DESV.DESV_scrEdit.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_DESV.DESV_scrEdit.search("##", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrEdit.tag_add(
                    "codigo", startline, endline)
            if (PST_DESV.DESV_scrEdit.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrEdit.tag_add(
                    "line", startline, endline)

    def colour_line_evi(self, bg_color, bg_codigo, fg_codigo):
        PST_DESV.DESV_scrEvidencia.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        PST_DESV.DESV_scrEvidencia.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )
        end = PST_DESV.DESV_scrEvidencia.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (PST_DESV.DESV_scrEvidencia.search("##", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrEvidencia.tag_add(
                    "codigo", startline, endline)
            if (PST_DESV.DESV_scrEvidencia.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_DESV.DESV_scrEvidencia.tag_add(
                    "line", startline, endline)

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
            event.tag_add("sel", "1.0", "end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel", "1.0", "end")

    def WIDGETS_DESVIACION(self):
        from Extraciones import MyEntry

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
        self.DESV_entryModule = MyEntry(
            self.DESV_frame1,
            textvariable=self.var_entry_bsc,
        )
        self.DESV_entryModule.configure(
            state='disabled',
        )
        self.DESV_entryModule.grid(
            row=1, column=0, pady=5, padx=(5, 0), sticky='nsew')

# TODO --- BOTON BUSCAR DESVIACION
        self.DESVfr1_btnBuscar = ttk.Button(
            self.DESV_frame1,
            image=self.BuscarModulo_icon,
            state='disabled',
            command=lambda: self.findModule(self.DESV_entryModule.get()),
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

        self.DESV_scrCheck = st.ScrolledText(self.DESV_frame2)
        self.DESV_scrCheck.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightbackground=default_Framework,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            state='disabled',
        )
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
            row=2, column=3, padx=5, pady=15, sticky='ne')

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
            row=2, column=4, padx=(0, 20), pady=15, sticky='ne')

# --- BACKUP ----------------------------------------------------------------------------------------------------
        self.DESVfr2_lblBackup = ttk.Label(
            self.DESV_frame2,
            text='BACKUP',
        )
        self.DESVfr2_lblBackup.grid(
            row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=4)

        self.DESVfr2_srcBackup = st.ScrolledText(
            self.DESV_frame2,
        )
        self.DESVfr2_srcBackup.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            highlightbackground=default_Framework,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            state='disabled',
        )
        self.DESVfr2_srcBackup.grid(
            row=5, column=0, padx=5, pady=5, sticky='new', columnspan=5)

        self.varBackup = "BACKUP"
        self.DESV_btn2Expandir = ttk.Button(
            self.DESV_frame2,
            text="Expand BACKUP",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=lambda x=self.DESVfr2_srcBackup: self.expandir(
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

        self.DESV_scrEdit = st.ScrolledText(self.DESV_frame3)
        self.DESV_scrEdit.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            highlightbackground=default_Framework,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            state='disabled',
        )
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

        self.DESVfr3_srcRefrescar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcRefrescar.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            highlightbackground=default_Framework,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            state='disabled',
        )
        self.DESVfr3_srcRefrescar.grid(
            row=3, column=0, padx=5, pady=5, sticky='new', columnspan=4)

        self.DESV_btn1CopyALL = ttk.Button(
            self.DESV_frame3,
            text="Copy All Refresh",
            image=self.icono_copiar,
            style='APP.TButton',
            state='disabled',
            command=lambda e=self.DESVfr3_srcRefrescar: self.copiarALL(e),
        )
        self.DESV_btn1CopyALL.grid(row=2, column=2, padx=5, pady=5, sticky='e')

        self.varRefrescar = "REFRESCAR"
        self.DESV_btn4Expandir = ttk.Button(
            self.DESV_frame3,
            text="Expand Refresh",
            image=self.icono_expandir,
            style='APP.TButton',
            state='disabled',
            command=lambda x=self.DESVfr3_srcRefrescar: self.expandir(
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

        self.DESV_scrEvidencia = st.ScrolledText(self.DESV_frame3)
        self.DESV_scrEvidencia.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            highlightbackground=default_Framework,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            state='disabled',
        )
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

        self.DESVfr2_lblDescripcion.bind('<Motion>', app.activeDefault)
        self.DESVfr2_lblComprobacion.bind('<Motion>', app.activeDefault)
        self.DESVfr2_lblBackup.bind('<Motion>', app.activeDefault)
        self.DESV_scrCheck.bind('<Motion>', app.activeDefault)
        self.DESVfr2_srcBackup.bind('<Motion>', app.activeDefault)
        self.DESVfr3_lblEditar.bind('<Motion>', app.activeDefault)
        self.DESVfr3_lblEvidencia.bind('<Motion>', app.activeDefault)
        self.DESVfr3_lblRefrescar.bind('<Motion>', app.activeDefault)
        self.DESV_scrEdit.bind('<Motion>', app.activeDefault)
        self.DESV_scrEvidencia.bind('<Motion>', app.activeDefault)
        self.DESVfr3_srcRefrescar.bind('<Motion>', app.activeDefault)

        self.DESV_frame1.bind('<Motion>', app.activeDefault)
        self.DESV_frame2.bind('<Motion>', app.activeDefault)
        self.DESV_frame3.bind('<Motion>', app.activeDefault)

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
        self.cambiar_color_RD()

    def _QuitarSeleccion_(self):
        global list_motion
        global txtWidget
        PST_DESV.DESV_frame2['text'] = 'SISTEMA OPERATIVO'
        PST_DESV.DESVfr2_lblDescripcion['text'] = ''
        PST_DESV.DESV_scrCheck.delete('1.0', tk.END)
        PST_DESV.DESVfr2_srcBackup.delete('1.0', tk.END)
        PST_DESV.DESV_scrEdit.delete('1.0', tk.END)
        PST_DESV.DESVfr3_srcRefrescar.delete('1.0', tk.END)
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

    def cambiar_color_RD(self):
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
        self._Font_Titulo_bold = font.Font(
            family=fuente_titulos, size=tamñ_titulo, weight=weight_DF)
        self.root.title("CONTINUOUS COMPLIANCE")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height/2 - Aplicacion.HEIGHT/2)
        position_right = int(screen_width/2 - Aplicacion.WIDTH/2)
        self.root.geometry(
            f'{Aplicacion.WIDTH}x{Aplicacion.HEIGHT}+{position_top}+{position_right}')
        #self.root.minsize(Aplicacion.WIDTH, Aplicacion.HEIGHT)
        #self.root.configure(background=default_bottom_app, borderwidth=0, border=0)
        self.root.tk.call('wm', 'iconphoto', self.root._w,tk.PhotoImage(file=path_icon+r'compliance.png'))
        self.open_client()
        self.iconos()
        
        self.cuaderno = ScrollableNotebook(self.root, wheelscroll=False, tabmenu=True, application=self)

        self.contenedor = ttk.Frame(self.cuaderno)
        self.contenedor.config(
            borderwidth=1,
            border=1,
        )
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        #self.contenedor.rowconfigure(2, weight=1)

        self.cuaderno.add(self.contenedor, text='WorkSpace  ', underline=0, image=self.WorkSpace_icon, compound=tk.LEFT)
        self.cuaderno.grid(row=0, column=0, sticky='nsew')
        #self.cuaderno.pack(fill="both", expand=True)
        
        self.cuaderno.bind_all("<<NotebookTabChanged>>",lambda e: self.toChangeTab(e))
        self.cuaderno.enable_traversal()
        self.cuaderno.notebookTab.bind("<Button-3>", self.display_menu_clickDerecho)
        self.cuaderno.bind("<Button-3>", self._display_menu_clickDerecho)

        self.root.bind_all("<Control-l>", lambda x: self.ocultar())
        self.root.focus_set()
        #self.contenedor.bind('<Motion>', self.activeDefault)
        # Fuente MENU CLICK DERECHO APP
        # ----------------------------------------------------------
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
        self.sizegrid.grid(row=1, column=0, sticky='nsew')

    def activeDefault(self, e):
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

    def open_client(self):
        global listClient
        listClient = []
        pathFiles = mypath+"Compliance/file/"
        os.chdir(pathFiles)
        listPathCustomer = []
        for file in os.listdir():
            if file.startswith("desviaciones_"):
                file_path = f"{pathFiles}{file}"
                listPathCustomer.append(file_path)
                print(listPathCustomer)
                for openFile in listPathCustomer:
                #     #try:
                #     print(*openFile)
                    with open(openFile, 'r', encoding='UTF-8') as fileCustomer:
                        fileJsonCustomer = json.load(fileCustomer)
                    for dataCustomer in fileJsonCustomer:
                        if 'CUSTOMER' in dataCustomer:
                            print(dataCustomer)
                            listClient.append(dataCustomer['CUSTOMER'])
        listClient = set(listClient)
        listClient = list(listClient)
        listClient.sort()
        print(listClient)
                    # except FileNotFoundError:
                    #     pass
                        #mb.showerror("No such file or directory!.\nPlease create a new CUST file")
        # for client in pathFileCustomer:
        #     listPathCustomer.append(pathFileCustomer.format(client))
        # with open(path_config.format("clientes")) as op:
        #     data = json.load(op)
        #     for clt in data:
        #         listClient.append(clt['name'])

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
        self.BuscarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"buscar1.png").resize((30, 30)))
        self.PegarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"pegarBarra.png").resize((30, 30)))
        self.Ayuda_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"ayuda.png").resize((30, 30)))
        self.AcercaDe_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"acercaDe.png").resize((30, 30)))
        self.WorkSpace_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"workspace.png").resize((20, 20)))
        self.icono_account = ImageTk.PhotoImage(
            Image.open(path_icon+r"account.png").resize((20, 20)))
        self.icono_account1 = ImageTk.PhotoImage(
            Image.open(path_icon+r"account1.png").resize((20, 20)))
        self.previous_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"previous.png").resize((40, 40)))
        self.next_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"next.png").resize((40, 40)))

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
            font=(fuente_boton, tamñ_boton, weight_DF),
            borderwidth=0,
        )
        self.style.map(
            'APP.TButton',
            background=[("active", default_bottom_app)],
            foreground=[("active", default_boton_fg)],
            borderwidth=[("active", 0)],
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
        global PST_DESV
        if activar_modo == 'True':
            self.MODE_DARK()
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

        self._cerrar_vtn_bsc()

    def _cerrar_vtn_bsc(self):
        global extracion
        try:
            extracion._on_closing_busca_top()
        except:
            pass
    
    def nameOpenButton(self):
        idx = self.IssuesVar.get()
        itm = listButton[idx]
        self.openButton(itm)

    def openButton(self, button):
        print("desde SCROLL", button)
        if button == "DESVIACIONES":
            self.openButtonDesviacion()
        elif button ==  "EXTRACIONES":
            self.openButtonExtracion()
        else:
            self.openButtonAutomatizacion()

    def openButtonDesviacion(self):
        global idOpenTab
        global desviacion
        #self.root.after(1, self.open_client)
        self.open_client()
        desviacion = Desviacion(self.cuaderno)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES ')

    def openButtonExtracion(self):
        global PST_EXT
        from Extraciones import Extracion

        global idpTab
        global extracion
        try:
            extracion._on_closing_busca_top()
        except:
            pass

        extracion = Extracion(self.cuaderno, app, application=self)
        PST_EXT = extracion
        self.cuaderno.add(extracion, text='Issues EXTRACIONES')
        idpTab = self.cuaderno.index('current')

    def openButtonAutomatizacion(self):
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
        window_width = 720
        window_height = 380
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_acerca_de.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_acerca_de.tk.call('wm', 'iconphoto', self.vtn_acerca_de._w, tk.PhotoImage(
            file=path_icon+r'acercaDe.png'))
        self.vtn_acerca_de.transient(self.root)
        self.vtn_acerca_de.resizable(False, False)
        self.vtn_acerca_de.title("Acerca de")

        self.close_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"close1.png").resize((80, 60)))

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

    def _cargar_modulo_glosario(self, clt_modulo=None, *args):
        with open(pathFileCustomer_clave.format('GLOSARIO')) as g:
            data = json.load(g)
            listModulo = []
            listClave = []
            for md in data:
                listModulo.append(md['modulo'])
                listClave.append(md['clave'])
        listModulo.sort()
        self._list_modulo.insert(tk.END, *listModulo)
        self._list_clave.insert(tk.END, *listClave)

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
        self.vtn_glosario.config(background=default_bottom_app)
        window_width = 800
        window_height = 500
        screen_width = app.root.winfo_x()
        screen_height = app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_glosario.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_glosario.tk.call('wm', 'iconphoto', self.vtn_glosario._w, tk.PhotoImage(
            file=path_icon+r'acercaDe.png'))
        self.vtn_glosario.transient(self.root)
        self.vtn_glosario.resizable(False, False)
        self.vtn_glosario.title("Ayuda")

        self.close_icon_gls = ImageTk.PhotoImage(
            Image.open(path_icon+r"close1.png").resize((80, 60)))

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
        self.boton_gls.pack(side=tk.RIGHT, padx=20, pady=10)
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
        self.rbOpenAuto.grid(
            row=0,
            column=2,
            padx=20,
            pady=20
        )
        
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
        self.frameButtons.bind('<Motion>', self.activeDefault)
        self.contenedor.bind("<Motion>", self.activeDefault)

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
        # --- INICIAMOS SUB MENU -------------------------- #
        self.clientMenu = tk.Menu(self.fileMenu, tearoff=0)
        self.issuesMenu = tk.Menu(self.fileMenu, tearoff=0)
        # -------------------------------------------------- #

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

        self.fileMenu.add_cascade(
            label="  Abrir",
            compound=tk.LEFT,
            image=self.Abrir_icon,
            menu=self.issuesMenu
        )
        self.fileMenu.add_cascade(
            label="  Clientes",
            image=self.Client_icon,
            compound=tk.LEFT,
            menu=self.clientMenu
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label="  Preferencias",
            image=self.Client_icon,
            compound=tk.LEFT,
            command=self._fontchooser
        )
        self.fileMenu.add_command(
            label="  Modo Dark",
            image=self.Client_icon,
            compound=tk.LEFT,
            command=self.activar_modo_noche
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label="  Salir",
            image=self.Salir_icon,
            compound=tk.LEFT,
            command=self.root.quit
        )
        self.fileMenu.add_separator()

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
            image=self.BuscarBar_icon,
            compound=tk.LEFT,
            state="disabled"
        )
        
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

        self.bar.add_cascade(label=" Archivo ", menu=self.fileMenu)
        self.bar.add_cascade(label=" Editar ", menu=self.editMenu)
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

    def activar_modo_noche(self):
        global activar_modo
        global modo_dark
        if activar_modo == 'False':
            modo_dark = 'True'
            activar_modo = 'True'
            parse['dark'] = {"activar_modo": activar_modo, "modo_dark": modo_dark}
            with open(path_config_ini.format("apariencia.ini"), 'w') as configfile:
                parse.write(configfile)
        elif activar_modo == 'True':
            modo_dark = 'False'
            activar_modo = 'False'
            parse['dark'] = {"activar_modo": activar_modo, "modo_dark": modo_dark}
            with open(path_config_ini.format("apariencia.ini"), 'w') as configfile:
                parse.write(configfile)
        if 'desviacion' in globals():
            desviacion.llamada_colores()
        self.MODE_DARK()

    #@beep_error
    def MODE_DARK(self):
        global modo_dark
        if modo_dark == 'True':
            self.root.configure(
                background=pers_bottom_app,
            )
            self.cuaderno.bottomTab_novo.config(background=pers_bottom_app)
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
            if PST_EXT != "":
                PST_EXT.frame1.config(background=pers_menu_bg)            
                PST_EXT.txt.configure(
                foreground=pers_scrText_fg,
                background=pers_scrText_bg,
                highlightbackground=pers_Framework,
                highlightcolor=pers_hglcolor,
                highlightthickness=hhtk,
                insertbackground=pers_hglcolor
            )            
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
                PST_DESV.DESV_btnAccount.canvas.config(
                    background=pers_bottom_app,
                )
                PST_DESV.DESV_btnAccount.canvas.itemconfig(
                    1,
                    fill=pers_bottom_app,
                    outline=default_Outline
                )
                PST_DESV.cambiar_icono(PST_DESV._btnAcc_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnAuth_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnComm_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnDir_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnIdr_, app.icono_account1)
                PST_DESV.cambiar_icono(PST_DESV._btnSer_, app.icono_account1)
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
                PST_DESV.DESV_entryModule.config(
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
                PST_DESV.DESVfr2_srcBackup.configure(
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
                PST_DESV.DESVfr3_srcRefrescar.configure(
                    foreground=pers_scrText_fg,
                    background=pers_scrText_bg,
                    highlightbackground=pers_Framework,
                    highlightcolor=pers_hglcolor,
                    highlightthickness=hhtk,
                    insertbackground=pers_hglcolor
                )
                PST_DESV.asignar_iconos()
        elif modo_dark == 'False':
                self.root.configure(
                    background=default_bottom_app,
                )
                self.cuaderno.bottomTab_novo.config(background=default_bottom_app)
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
                
                if PST_EXT != "":
                    PST_EXT.frame1.config(background=default_menu_bg)            
                    PST_EXT.txt.config(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )            

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
                    PST_DESV.DESV_entryModule.config(
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
                        # highlightthickness=0,
                    )
                    PST_DESV.DESVfr2_lblDescripcion.configure(
                        foreground='gray60',
                        background=default_bottom_app,
                    )
                    PST_DESV.DESV_scrCheck.configure(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )
                    PST_DESV.DESVfr2_srcBackup.configure(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )
                    PST_DESV.DESV_scrEdit.configure(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )
                    PST_DESV.DESV_scrEvidencia.configure(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )
                    PST_DESV.DESVfr3_srcRefrescar.configure(
                        foreground=default_scrText_fg,
                        background=default_scrText_bg,
                        highlightbackground=default_Framework,
                        highlightcolor=default_hglcolor,
                        highlightthickness=hhtk,
                        insertbackground=default_hglcolor
                    )
                    PST_DESV.asignar_iconos()

    def expandirModeDefault(self):
        PST_EXP.expandirColourLine(
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
        PST_EXP.EXP_srcExpandir.config(
                            foreground=default_scrText_fg,
                            background=default_scrText_bg,
                            highlightbackground=default_Framework,
                            highlightcolor=default_hglcolor,
                            highlightthickness=hhtk,
                            insertbackground=default_hglcolor
                            )
        PST_DESV.cambiar_icono(PST_EXP._btn_expDIR_, app.icono_account)
        PST_DESV.cambiar_icono(PST_EXP._btn_expAUT_, app.icono_account)
        PST_DESV.cambiar_icono(PST_EXP._btn_expACC_, app.icono_account)
        PST_DESV.cambiar_icono(PST_EXP._btn_expSER_, app.icono_account)
        PST_DESV.cambiar_icono(PST_EXP._btn_expCMD_, app.icono_account)
        PST_DESV.cambiar_icono(PST_EXP._btn_expIDR_, app.icono_account)
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
        print("DESPUES DE TRUE ----- AQI")
        PST_EXP.expandirColourLine(
                pers_scrText_bg,
                pers_colourCodeBg,
                pers_colourCodeFg,
                pers_colourNoteFg
        )
        print("----------------------->>>>>")
        PST_EXP.vtn_expandir.config(
                                    background=pers_bottom_app,
                            )
        print("<<<<-----------------------")
        PST_EXP.EXP_btn_Siguiente.config(
                                background=pers_bottom_app,
                                activebackground=pers_bottom_app
                            )
        PST_EXP.EXP_btn_Anterior.config(
                                background=pers_bottom_app,
                                activebackground=pers_bottom_app
                            )
        PST_EXP.EXP_srcExpandir.config(
                            foreground=pers_scrText_fg,
                            background=pers_scrText_bg,
                            highlightbackground=pers_Framework,
                            highlightcolor=pers_hglcolor,
                            highlightthickness=hhtk,
                            insertbackground=pers_hglcolor
                            )
        PST_DESV.cambiar_icono(PST_EXP._btn_expDIR_, app.icono_account1)
        PST_DESV.cambiar_icono(PST_EXP._btn_expAUT_, app.icono_account1)
        PST_DESV.cambiar_icono(PST_EXP._btn_expACC_, app.icono_account1)
        PST_DESV.cambiar_icono(PST_EXP._btn_expSER_, app.icono_account1)
        PST_DESV.cambiar_icono(PST_EXP._btn_expCMD_, app.icono_account1)
        PST_DESV.cambiar_icono(PST_EXP._btn_expIDR_, app.icono_account1)
        
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
        PST_VTN.textBuscar.config(
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
        PST_VTN.textBuscar.config(
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

    def openTooltip(self, boton, text, *args):
        global custom
        global tooltip
        if tooltip == False:
            custom = CustomHovertip(boton, text=text)
            tooltip = True

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()