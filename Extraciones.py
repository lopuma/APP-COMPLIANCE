# -*- coding: utf-8 -*-
import os
import re
import tkinter as tk
from os import listdir
from os.path import isdir, join, abspath
from tkinter import END, TclError, ttk
from tkinter import scrolledtext as st
from tkinter import font
from turtle import left
from PIL import Image, ImageTk
from threading import Thread
import time
from functools import partial
from Compliance import pathExtraction, hlh_def, pathIcon, pers_menu_bg, pers_scrText_bg, pathConfig, parse, pers_bottom_app, activar_modo, mypath, hhtk, default_scrText_bg, default_panelBg, bg_submenu, default_scrText_fg, default_menu_bg, fg_submenu, acdefault_panelBg, _Font_Menu, _Font_Texto, default_select_bg, default_select_fg, default_bottom_app, default_hglcolor, default_select_bg, default_select_fg, fuente_texto, tamñ_texto, _Font_Texto_bold, _Font_Texto_codigo

parar = False
_estado_actual = False
PST_EXT = ""
HIDDEN = 0
on = 1
def beep_error(f):
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    return applicator

class MyEntry(tk.Entry):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.changes = [""]
        self.steps = int()
        self.config(
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            selectforeground=default_select_fg,
            font=_Font_Texto,
            borderwidth=0,
            highlightcolor=default_hglcolor,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            highlightthickness=hhtk,        )
        self.mostrar_menu()
        self.bind('<Control-a>', self.seleccionar_todo)
        self.bind('<Control-A>', self.seleccionar_todo)
        self.bind('<Control-f>', self.seleccionar_todo)
        self.bind('<Control-F>', self.seleccionar_todo)
        self.bind('<Control-x>', self.cortar)
        self.bind('<Control-X>', self.cortar)
        self.bind('<Control-c>', self.copiar)
        self.bind('<Control-C>', self.copiar)
        self.bind('<Control-v>', self.pegar)
        self.bind('<Control-V>', self.pegar)
        self.bind('<Control-z>', self.deshacer)
        self.bind('<Control-Z>', self.deshacer)
        self.bind('<Control-y>', self.rehacer)
        self.bind('<Control-Y>', self.rehacer)
        self.bind("<Button-3><ButtonRelease-3>", self._display_menu_)
        self.bind("<Key>", self.add_changes)

    def mostrar_menu(self):
        self.menu_opciones = tk.Menu(self, tearoff=0)
        self.menu_opciones.add_command(# --- DESHACER
            label="  Deshacer",
            command=self.deshacer,
            accelerator='Ctrl+Z',
            background=bg_submenu,
            foreground=fg_submenu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled'
        )
        self.menu_opciones.add_command(# --- REHACER
            label="  Rehacer",
            command=self.rehacer,
            accelerator='Ctrl+Y',
            background=bg_submenu,
            foreground=fg_submenu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled'
        )
        self.menu_opciones.add_separator(background=bg_submenu)
        self.menu_opciones.add_command(# --- CORTAR
            label="  Cortar",
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disabled',
            command=self.cortar
        )
        self.menu_opciones.add_command(# --- COPIAR
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_submenu,
            foreground=fg_submenu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            font=_Font_Menu,
            state='disable',
            command=self.copiar
        )
        self.menu_opciones.add_command(# --- PEGAR
            label="  Pegar",
            accelerator='Ctrl+V',
            background=bg_submenu,
            foreground=fg_submenu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.pegar
        )
        self.menu_opciones.add_separator(background=bg_submenu)
        self.menu_opciones.add_command(# --- SELECT ALL
            label="  Selecionar todo",
            command=self.seleccionar_todo,
            accelerator='Ctrl+A',
            compound=tk.LEFT,
            background=bg_submenu,
            foreground=fg_submenu,
            activebackground=default_select_bg,
            activeforeground=default_select_fg,
            font=_Font_Menu,
        )

    def _display_menu_(self, event=None):
        self.menu_opciones.tk_popup(event.x_root, event.y_root)
        if self.select_present():
            self.menu_opciones.entryconfig("  Cortar", state="normal")
            self.menu_opciones.entryconfig("  Copiar", state="normal")
        else:
            self.menu_opciones.entryconfig("  Cortar", state="disabled")
            self.menu_opciones.entryconfig("  Copiar", state="disabled")

        if len(self.get()) > 0:
            self.menu_opciones.entryconfig("  Deshacer", state="normal")
            #self.menu_opciones.entryconfig("  Rehacer", state="disabled")
        else:
            self.menu_opciones.entryconfig("  Deshacer", state="disabled")

    def copiar(self, event=None):
        self.event_generate("<<Copy>>")
        #self.see("insert")
        return 'break'

    def cortar(self, event=None):
        self.event_generate("<<Cut>>")
        return 'break'

    def pegar(self, event=None):
        if self.select_present():
            self.delete(0, tk.END)
            self.event_generate("<<Paste>>")
        else:
            self.event_generate("<<Paste>>")
        return 'break'

    def seleccionar_todo(self, event=None):
        self.select_range(0, tk.END)
        self.focus_set()
        return 'break'

    #@beep_error
    def deshacer(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.delete(0, tk.END)
            self.insert(tk.END, self.changes[self.steps])
            self.menu_opciones.entryconfig("  Rehacer", state="normal")

    #@beep_error
    def rehacer(self, event=None):
        if self.steps < len(self.changes):
            self.delete(0, tk.END)
            self.insert(tk.END, self.changes[self.steps])
            self.steps += 1
            self.menu_opciones.entryconfig("  Rehacer", state="disabled")

    def add_changes(self, event=None):
        if self.get() != self.changes[-1]:
            self.changes.append(self.get())
            self.steps += 1

class Extracion(ttk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        global _estado_actual
        global PST_EXT
        self.navIcon = ImageTk.PhotoImage(Image.open(
            pathIcon+r"menu.png").resize((25, 25)))
        self.closeIcon = ImageTk.PhotoImage(Image.open(
            pathIcon+r"close.png").resize((25, 25)))
        PST_EXT = self
        self.wd = 50
        self.app = app
        self.iconos()
        self.createFrame()
        #self.bind("<Motion>", lambda e : self.EXT_motion(e))
        parent.bind_all('<Control-f>', lambda x: self.searchPanel(x))
        #self.app.root.bind('<Control-l>', lambda e : self.closeFrame(e))
        #PST_EXT.txt.bind('<Control-l>', lambda e : self.closeFrame(e))
        # # self.txt.bind('<Control-c>', lambda x: self._copiar_texto_seleccionado(x))
        # self.txt.bind('<Control-C>', lambda x: self._copiar_texto_seleccionado(x))
        # self.txt.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        # self.txt.bind('<Control-A>'_all('<Control-f>', lambda x: self.searchPanel(x))
        #self.app.root.bind('<Control-l>', lambda e: self._seleccionar_todo(e)
        # self.txt.bind('<Control-x>', lambda e: self._limpiar_busqueda(e))
        self._ocurrencias_encontradas = []
        self._numero_ocurrencia_actual = None
        _estado_actual = False
        self._menu_clickDerecho()


        

    # def EXT_motion(self, event):
    #     global PST_EXT
    #     PST_EXT = event.widget

    def iconos(self):
        self.flecha_up = ImageTk.PhotoImage(
            Image.open(pathIcon+r"flecha1.png").resize((20, 20)))
        self.btn_lmp = ImageTk.PhotoImage(
            Image.open(pathIcon+r"lmp.png").resize((22, 22)))
        self.flecha_down = ImageTk.PhotoImage(
            Image.open(pathIcon+r"flecha2.png").resize((20, 20)))
        self.btn_x = ImageTk.PhotoImage(
            Image.open(pathIcon+r"btn-x.png").resize((20, 20)))

    def closeFrame(self, event):
        global on
        if on:
            PST_EXT.frame1.pack_forget()
            PST_EXT.createFrameClose()
            on = 0
        else:
            PST_EXT.frameClose.pack_forget()
            PST_EXT.frame1.pack_forget()
            PST_EXT.frame2.pack_forget()
            PST_EXT.createFrame()
            on = 1

    def createFrameClose(self):
        parse.read(pathConfig.format("apariencia.ini"))
        modo_dark = parse.get('dark', 'modo_dark')
        self.frameClose = tk.Frame(self)
        self.frameClose.pack(before=self.frame2, side="left", expand=0, ipadx=1, anchor='ne')
        if modo_dark == 'False':
            self.frameClose.config(
                background=default_menu_bg,
            )
        else:
            self.frameClose.config(
                background=pers_menu_bg,
            )

        PST_EXT.frameClose.config(background=default_menu_bg)
        PST_EXT.btn_nav = ttk.Button(
                self.frameClose,
                image=self.navIcon,
                command=self.show_btn_nav,
            )
        PST_EXT.btn_nav.pack(side=tk.TOP, expand=0, fill=tk.BOTH)

    def createFrame(self):
        global on
        on = 1
        parse.read(pathConfig.format("apariencia.ini"))
        modo_dark = parse.get('dark', 'modo_dark')
        activar_modo = parse.get('dark', 'activar_modo')
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side="left", expand=0, fill=tk.BOTH, ipadx=self.wd)
        self.treeview = ttk.Treeview(
            self.frame1,
        )

        #? COLOR TEXT DE LAS CARPETAS DE EXTRACION
        self.treeview.heading("#0", text="FICHEROS de EXTRACIONES", anchor="center")
        self.treeview.pack(fill='both', expand=True, ipadx=50)

        self.treeview.tag_bind(
            "fstag", "<<TreeviewOpen>>", self.item_opened
        )
        self.treeview.tag_bind(
            "fstag", "<<TreeviewClose>>", self.item_closed
        )
        self.treeview.bind(
            "<<TreeviewSelect>>", lambda e: self.select_extraction(e)
        )
        self.fsobjects = {}

        self.file_image = tk.PhotoImage(file=pathIcon+r"files.png")
        self.folder_image = tk.PhotoImage(file=pathIcon+r"folder.png")

        self.btn_close = ttk.Button(
            self.frame1,
            image=self.closeIcon,
            command=self.hide_btn_nav,
        )

        self.btn_close.pack(before=self.treeview, expand=0, anchor='ne')

        self.max = ttk.Button(
            self.frame1,
            width=4,
            text="+",
        )
        self.max.pack(side="right", expand=0)

        self.min = ttk.Button(
            self.frame1,
            width=4,
            text="-",
        )
        self.min.pack(side="left", expand=0)

        #todo Cargar el directorio raíz.
        self.load_tree(abspath(pathExtraction))
        self.max.bind(
            "<Button-1>", lambda e: Thread(target=self.ampliar, daemon=True).start())
        self.max.bind("<ButtonRelease-1>", self._parar_)
        self.min.bind(
            "<Button-1>", lambda e: Thread(target=self.reducir, daemon=True).start())
        self.min.bind("<ButtonRelease-1>", self._parar_)

        self.frame2 = tk.Frame(self)
#         #self.frame2.grid(row=0, column=2, sticky="nsew", padx=5, pady=(10,0))
#         # self.frame2.columnconfigure(0, weight=1)
#         # self.frame2.rowconfigure(0, weight=1)
        self.frame2.pack(expand=True, fill=tk.BOTH)

        self.txt = st.ScrolledText(
            self.frame2,
            font=_Font_Texto,
        )

        self.txt.config(
            font=_Font_Texto,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            state='normal'
        )
        self.txt.pack(expand=1, fill=tk.BOTH)
        self.idx_gnral = tk.StringVar()
        pos_cursor = self.txt.index(tk.INSERT)
        self.idx_gnral.set(pos_cursor)
        self.txt.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.txt.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.txt.bind("<Motion>",lambda e: self.activar_Focus(e))
        self.frame1.bind_all('<Control-l>', lambda e : self.closeFrame(e))
        self.frame2.bind_all('<Control-l>', lambda e : self.closeFrame(e))
        if modo_dark == 'False':
            self.frame1.config(
            background=default_menu_bg,
            )
        else:
            self.frame1.config(
                background=pers_menu_bg,
            )
            # self.txt.config(
            #     background=pers_scrText_bg,
        if activar_modo == 'True':
            self.app.MODE_DARK()

    def ampliar(self):
        global parar
        parar = False
        print("FRAME 1 AMPLIAR¡", self.frame1, self.wd)
        while not parar:
            time.sleep(0.01)
            if self.wd < 300:
                self.wd += 0.5
                self.frame1.pack_configure(ipadx=self.wd)
                print(self.frame1)
            else:
                self._parar_(event=None)

    def _parar_(self, event):
        global parar
        parar = True

    def reducir(self):
        global parar
        parar = False
        while not parar:
            time.sleep(0.01)
            if self.wd > 2:
                self.wd -= 0.5
                self.frame1.pack_configure(ipadx=self.wd)
            else:
                self._parar_(event=None)

    def seleccionar_plantilla(self, plantilla):
        self.plantilla = plantilla
        with open(plantilla) as g:
            data = g.read()
            self.txt.delete('1.0', tk.END)
            for md in data:
                self.txt.insert(tk.END, md)

    def listdir(self, path):
        try:
            return listdir(path)
        except PermissionError:
            return []

    def get_icon(self, path):
        """
        Retorna la imagen correspondiente según se especifique
        un archivo o un directorio.
        """
        return self.folder_image if isdir(path) else self.file_image

    def insert_item(self, name, path, parent=""):
        iid = self.treeview.insert(parent,
            tk.END, text=name,
            tags=("fstag",)+(("folder",) if isdir(path) else ()),
            image=self.get_icon(path)
        )
        self.fsobjects[iid] = path
        return iid

    def load_tree(self, path, parent=""):
        for fsobj in listdir(path):
            fullpath = join(path, fsobj)
            child = self.insert_item(fsobj, fullpath, parent)
            if isdir(fullpath):
                for sub_fsobj in listdir(fullpath):
                    self.insert_item(sub_fsobj, join(fullpath, sub_fsobj),
                                     child)

    def load_subitems(self, iid):
        for child_iid in self.treeview.get_children(iid):
            if isdir(self.fsobjects[child_iid]):
                self.load_tree(self.fsobjects[child_iid],parent=child_iid)

    def item_opened(self, event):
        iid = self.treeview.selection()[0]
        self.load_subitems(iid)

    def item_closed(self, event):
        """
        Evento invocado cuando el contenido de una carpeta es abierto.
        """
        iid = self.treeview.selection()[0]
        records = self.treeview.get_children(iid)
        self.treeview.delete(*self.treeview.get_children())
        self.load_tree(abspath(pathExtraction))

    def select_extraction(self, event):
        treeSelect = event.widget
        iid = treeSelect.selection()[0]
        plantilla = treeSelect.item(iid, option="text")
        path = ''
        for root, _, files in os.walk(pathExtraction):
            if plantilla in files:
                path = os.path.join(root, plantilla)
                break
        if len(path) != 0:
            self.seleccionar_plantilla(path)
            self.colour_line()
            self.colour_line2()

    def cadena_valida(self, cadena):
        patron = "^\/*.*?\*/$"
        INTR = re.search(patron, cadena)
        print(INTR)


    def colour_line(self):
        indx = '1.0'
        indx3 = '1.0'
        indx4 = '1.0'
        indx5 = '1.0'
        indx6 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        line3 = "CONTESTAR NO"
        line4 = "CONTESTAR N/A"
        # patron = "^\/*.*?\*/$"
        # i = 0
        # texto = self.txt.get("1.0", END)
        # for i in texto:
        #     INTR = re.search(patron, texto)
        #     print(INTR)
        if line1:
            while True:
                indx = self.txt.search(line1, indx, nocase=1, stopindex=tk.END)
                if not indx:
                    break
                lastidx = '%s+%dc' % (indx, len(line1))
                self.txt.tag_add('found1', indx, lastidx)
                indx = lastidx
            self.txt.tag_config(
                'found1',
                foreground='dodgerblue',
                font=(fuente_texto, 17, font.BOLD)
            )
        if line3:
            while True:
                indx3 = self.txt.search(
                    line3, indx3, nocase=1, stopindex=tk.END)
                if not indx3:
                    break
                lastidx3 = '%s+%dc' % (indx3, len(line3))
                self.txt.tag_add('found3', indx3, lastidx3)
                indx3 = lastidx3

            #? COLOR CONTESTAR NO
            self.txt.tag_config(
                'found3',
                background='#FFE6E6',
                foreground='#FF2626',
                font=(fuente_texto, tamñ_texto, font.BOLD)
            )
        if line4:
            while True:
                indx4 = self.txt.search(
                    line4, indx4, nocase=1, stopindex=tk.END)
                if not indx4:
                    break
                lastidx4 = '%s+%dc' % (indx4, len(line4))
                self.txt.tag_add('found4', indx4, lastidx4)
                indx4 = lastidx4

            #? COLOR CONTESTAR N/A
            self.txt.tag_config(
                'found4',
                background='#FFCB91',
                foreground='#FF5F00',
                font=(fuente_texto, tamñ_texto, font.BOLD)
            )

        PST_EXT.txt.tag_configure(
            "titulo",
            background="#EDEDED",
            # foreground="#990033",
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )

        PST_EXT.txt.tag_configure(
            "coment",
            #background="#E9D5DA",
            foreground="#ECB365",
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )

        PST_EXT.txt.tag_configure(
            "coment2",
            #background="#E9D5DA",
            foreground="#064663",
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )

        PST_EXT.txt.tag_configure(
            "codigo",
            background="#FDEFF4",
            foreground="#990033",
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        end = PST_EXT.txt.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            # if not (PST_EXT.txt.search("#", startline, stopindex=f"{line}.1")) and not(PST_EXT.txt.search("//", startline, stopindex=f"{line}.1")) and not (PST_EXT.txt.search("\"", startline, stopindex=f"{line}.1")) and not (PST_EXT.txt.search("---", startline, stopindex=f"{line}.1")) and not (PST_EXT.txt.search("/*", startline, stopindex=f"{line}.1")) and not (PST_EXT.txt.search("+-", startline, stopindex=f"{line}.1")):
            #     endline = f"{line}.end"
            #     PST_EXT.txt.tag_add(
            #         "codigo", startline, endline)
            if (PST_EXT.txt.search("---", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXT.txt.tag_add(
                    "titulo", startline, endline)
            if (PST_EXT.txt.search("\"", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXT.txt.tag_add(
                    "coment", startline, endline)
            if (PST_EXT.txt.search("//", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                PST_EXT.txt.tag_add(
                    "coment2", startline, endline)

    def colour_line2(self):
        indx2 = '1.0'
        line2 = "CONTESTAR YES"
        while True:
            indx2 = self.txt.search(line2, indx2, nocase=1, stopindex=tk.END)
            if not indx2:
                break
            lastidx2 = '%s+%dc' % (indx2, len(line2))
            self.txt.tag_add('found2', indx2, lastidx2)
            indx2 = lastidx2

        #? COLOR CONTESTAR YES
        self.txt.tag_config(
            'found2',
            background='#000000',
            foreground='#357C3C',
            font=(fuente_texto, tamñ_texto, font.BOLD)
        )

    def widgets_SoloLectura(self, event):
        if(20 == event.state and event.keysym == 'c' or event.keysym == 'Down' or event.keysym == 'Up' or 20 == event.state and event.keysym == 'f' or 20 == event.state and event.keysym == 'a'):
            return
        else:
            return "break"

    def _menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=lambda e=self.txt: self.searchPanel(e)
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Copiar",
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state="disabled",
            command=self.copiar_texto_seleccionado
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo",
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.seleccionar_todo
        )
        self.menu_Contextual.add_command(
            label="  Limpiar Busqueda",
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            state="disabled",
            command=self.limpiar_busqueda
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Ocultar Panel",
            accelerator='Ctrl+L',
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=partial(self.hide_btn_nav)
        )
        self.menu_Contextual.add_command(
            label="  Mostrar Panel",
            state="disabled",
            accelerator='Ctrl+L',
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.show_btn_nav
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

    def _display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        txt_select = event.widget.tag_ranges(tk.SEL)
        if txt_select:
            self.menu_Contextual.entryconfig("  Copiar", state="normal")
        else:
            self.menu_Contextual.entryconfig("  Copiar", state="disabled")

    def limpiar_busqueda(self):
        self.var_entry_bsc.set("")
        self.menu_Contextual.entryconfig(
            '  Limpiar Busqueda', state='disabled')
        self.txt.tag_remove('found', '1.0', tk.END)
        self.txt.tag_remove('found_prev_next', '1.0', tk.END)

    def _limpiar_busqueda(self, event):
        txt_event = event.widget
        self.var_entry_bsc.set("")
        self.menu_Contextual.entryconfig(
            '  Limpiar Busqueda', state='disabled')
        txt_event.tag_remove('found', '1.0', tk.END)
        txt_event.tag_remove('found_prev_next', '1.0', tk.END)

    def copiar_texto_seleccionado(self):
        seleccion = self.txt.tag_ranges(tk.SEL)
        if seleccion:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(self.txt.get(*seleccion).strip())
            self.txt.tag_remove("sel", "1.0", "end")
            return 'break'

    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel", "1.0", "end")
            return 'break'
        else:
            pass

    def seleccionar_todo(self):
        self.txt.tag_add("sel", "1.0", "end")
        return 'break'

    def _seleccionar_todo(self, event):
        scr_Event = event.widget
        scr_Event.tag_add("sel", "1.0", "end")
        return 'break'

    def cerrar_vtn_desviacion(self):
        self.app.cerrar_vtn_desviacion()


    def hide_btn_nav(self):
        global parar
        global on
        self.menu_Contextual.entryconfig('  Ocultar Panel', state='disable')
        self.menu_Contextual.entryconfig('  Mostrar Panel', state='normal')
        self.closeFrame(event=None)
        #self.createFrameClose()
        # parar = False

    def show_btn_nav(self):
        global parar
        global on
        self.menu_Contextual.entryconfig('  Ocultar Panel', state='normal')
        self.menu_Contextual.entryconfig('  Mostrar Panel', state='disabled')
        self.closeFrame(event=None)
        # parar = False

    def elim_tags(self, l_tags):
        '''Eliminar etiqueta(s) pasada(s)'''
        for l_tag in l_tags:
            self.txt.tag_delete(l_tag)

    def buscar_prev(self):
        '''Buscar previa ocurrencia en el Entry de MainApp'''
        idx = self.indice_ocurrencia_actual[0] if self.indice_ocurrencia_actual else self.txt.index(
            tk.INSERT)
        self.indice_ocurrencia_actual = self.txt.tag_prevrange(
            'found', idx) or self.txt.tag_prevrange('found', self.txt.index(tk.END)) or None

    def buscar_next(self):
        '''Buscar siguiente ocurrencia en el Entry de MainApp'''
        idx = self.indice_ocurrencia_actual[1] if self.indice_ocurrencia_actual else self.txt.index(
            tk.INSERT)
        self.indice_ocurrencia_actual = self.txt.tag_nextrange(
            'found', idx) or self.txt.tag_nextrange('found', "0.0") or None

    @property
    def numero_ocurrencias(self):
        return len(self._ocurrencias_encontradas)

    @property
    def numero_ocurrencia_actual(self):
        return self._numero_ocurrencia_actual

    @property
    def indice_ocurrencia_actual(self):
        tags = self.txt.tag_ranges('found_prev_next')
        return tags[:2] if tags else None

    @indice_ocurrencia_actual.setter
    def indice_ocurrencia_actual(self, idx):
        self.elim_tags(['found_prev_next'])
        self.txt.tag_config('found_prev_next', background='orangered')

        if idx is not None:
            self.txt.tag_add('found_prev_next', *idx)
            self.txt.see(idx[0])
            self._numero_ocurrencia_actual = self._ocurrencias_encontradas.index(
                self.indice_ocurrencia_actual) + 1
        else:
            self._numero_ocurrencia_actual = None

    @property
    def ocurrencias_encontradas(self):
        return self._ocurrencias_encontradas


    def searchPanel(self, event=None):
        global _estado_actual
        if not _estado_actual:
            self.busca_top = tk.Toplevel(self.frame2)

            window_width = 680
            window_height = 100
            bus_reem_top_msg_w = 240
            self.busca_top.overrideredirect(True)
            screen_width = (self.app.root.winfo_x() + 640)
            screen_height = (self.app.root.winfo_y()+40)
            position_top = int(screen_height)
            position_right = int(screen_width)
            self.busca_top.geometry(
                f'{window_width}x{window_height}+{position_right}+{position_top}')
            #self.busca_top.transient(self)

            self.busca_top.config(
                bg=default_bottom_app,
                padx=5,
                pady=5
            )
             #self.busca_top.resizable(0, 0)

            self.busca_frm_tit = tk.Frame(
                self.busca_top,
            )
            self.busca_frm_tit.pack(fill='x', expand=1)

            self.busca_frm_content = tk.Frame(
                self.busca_top,
                bg=default_panelBg,
                padx=5,
                pady=10
            )
            self.busca_frm_content.pack(fill='x', expand=1)

            self.busca_top.title('Buscar')
            self.bus_reem_num_results = tk.StringVar()
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))

            self.buscar_01_msg = tk.Message(
                self.busca_frm_tit,
                textvariable=self.bus_reem_num_results,
                padx=10,
                pady=0
            )
            self.buscar_01_msg.pack(fill='both', expand=1)
            self.buscar_01_msg.config(
                width=bus_reem_top_msg_w,
                background=acdefault_panelBg,
                foreground="black",
                justify='center',
                font=(fuente_texto, 14, 'bold')
            )

            self.buscar_01_msg.bind("<ButtonPress-1>", self.start_move)
            self.buscar_01_msg.bind("<ButtonRelease-1>", self.stop_move)
            self.buscar_01_msg.bind("<B1-Motion>", self.on_move)

            self.var_entry_bsc = tk.StringVar(self)

            self.entr_str = MyEntry(
                self.busca_frm_content,
                textvariable=self.var_entry_bsc,
            )
            self.entr_str.grid(row=0, column=0, padx=5, sticky="nsew")

            self.entr_str.configure(
                width=43,
                highlightcolor=default_hglcolor,
                insertbackground=default_hglcolor,
                insertwidth=5,
                selectbackground=default_select_bg,
                highlightthickness=hhtk,
                font=(fuente_texto, 14)
            )

            self.btn_cerrar_buscar = tk.Button(
                self.busca_frm_content,
                text='X',
                image=self.btn_x,
                command=self._on_closing_busca_top
            )
            self.btn_cerrar_buscar.config(
                background=default_panelBg,
                highlightcolor=default_hglcolor,
                activebackground=acdefault_panelBg,
                border=0,
                highlightbackground=default_panelBg,
            )
            self.btn_cerrar_buscar.grid(row=0, column=4, padx=5, pady=5)

## --- Botom Limpiar
            self.btn_limpiar = tk.Button(
                self.busca_frm_content,
                text='<<',
                image=self.btn_lmp,
                command=self.limpiar_busqueda
            )

            self.btn_limpiar.config(
                background=default_panelBg,
                highlightcolor=default_hglcolor,
                activebackground=acdefault_panelBg,
                border=0,
                highlightbackground=default_panelBg,
            )

            self.btn_limpiar.grid(
                row=0, column=1, padx=(5, 0), pady=5, sticky="nsew")

## --- Botom anterior
            self.btn_buscar_prev = tk.Button(
                self.busca_frm_content,
                text='<|',
                image=self.flecha_up,
                command=self._buscar_anterior
            )

            self.btn_buscar_prev.config(
                background=default_panelBg,
                highlightcolor=default_hglcolor,
                activebackground=acdefault_panelBg,
                border=0,
                highlightbackground=default_panelBg,
            )

            self.btn_buscar_prev.grid(
                row=0, column=2, padx=(5, 0), pady=5, sticky="nsew")

## --- Botom siguiente
            self.btn_buscar_next = tk.Button(
                self.busca_frm_content,
                text='|>',
                image=self.flecha_down,
                command=self._buscar_siguiente
            )

            self.btn_buscar_next.config(
                background=default_panelBg,
                highlightcolor=default_hglcolor,
                activebackground=acdefault_panelBg,
                border=0,
                highlightbackground=default_panelBg,
            )

            self.btn_buscar_next.grid(
                row=0, column=3, padx=(5, 0), pady=5, sticky="nsew")

## --- Activa el focu en el ENTRY
            self.entr_str.focus_set()

## --- Busca palabras al escribir, y activa el panel
            self.entr_str.bind('<Any-KeyRelease>', self.on_entr_str_busca_key_release)
            _estado_actual = True
        else:
            self._buscar_focus(self.entr_str)
            _estado_actual = True
            return 'break'

## --- Activa el motion en cada widget del panel
        self.busca_top.bind("<Motion>", lambda e: self._activar_Focus(e))

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        self._x = None
        self._y = None

    def on_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        new_pos = "+{}+{}".format(self.busca_top.winfo_x() + deltax, self.busca_top.winfo_y() + deltay)
        #self.app.root.geometry(new_pos)
        self.busca_top.geometry(new_pos)

    def _buscar_focus(self, event):
        MyEntry.seleccionar_todo(event)

    def _on_closing_busca_top(self):
        global PST_EXT
        global _estado_actual
        _estado_actual = False
        PST_EXT.busca_top.destroy()

## --- Activa el focu de los widgets del PANEL
    def _activar_Focus(self, event):
        pnl_buscar = event.widget
        pnl_buscar.focus()

## --- Activa el FOCU del TXT principal
    def activar_Focus(self, event):
        txt_active = event.widget
        txt_active.focus()

## --- Al escribir en el ENTRY del PANEL, busca concurrencias
    def on_entr_str_busca_key_release(self, event):
        if event.keysym != "F2" and event.keysym != "F3":  # F2 y F3
            self._buscar()
            return "break"

    def _buscar(self, event=None):
        self.buscar_todo(self.entr_str.get().strip())
        if self.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(
                self.numero_ocurrencia_actual, self.numero_ocurrencias))
            self.entr_str.configure(
                highlightthickness=hhtk,
                highlightcolor='blue')
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))
            self.entr_str.configure(
                highlightthickness=hhtk,
                highlightcolor='red')

    def buscar_todo(self, txt_buscar=None):
        '''Buscar todas las ocurrencias en el Entry de MainApp'''
        # eliminar toda marca establecida, si existiera, antes de plasmar nuevos resultados
        self.txt.tag_remove('found', '1.0', tk.END)
        self.txt.tag_remove('found_prev_next', '1.0', tk.END)
        if txt_buscar:
            # empezar desde el principio (y parar al llegar al final [stopindex >> END])
            idx = '1.0'
            while True:
                # encontrar siguiente ocurrencia, salir del loop si no hay más
                idx = self.txt.search(
                    txt_buscar, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                # index justo después del final de la ocurrencia
                lastidx = '%s+%dc' % (idx, len(txt_buscar))
                # etiquetando toda la ocurrencia (incluyendo el start, excluyendo el stop)
                self.txt.tag_add('found', idx, lastidx)
                # preparar para buscar la siguiente ocurrencia
                idx = lastidx
                self.txt.see(idx)
            # configurando la forma de etiquetar las ocurrencias encontradas
            self.txt.tag_config('found', background='dodgerblue')
            # FUNCIONA

            # self.buscar_next(self.entr_str.get().strip())
            self.menu_Contextual.entryconfig(
                '  Limpiar Busqueda', state='normal')
        else:
            self.menu_Contextual.entryconfig(
                '  Limpiar Busqueda', state='disabled')
            #MessageBox.showinfo('Info', 'Establecer algún criterior de búsqueda.')
        tags = self.txt.tag_ranges('found')
        self._ocurrencias_encontradas = list(zip(*[iter(tags)] * 2))
        self.buscar_next()

    def _buscar_siguiente(self, event=None):
        self.buscar_next()
        if self.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(
                self.numero_ocurrencia_actual, self.numero_ocurrencias))
            self.entr_str.configure(
                highlightthickness=hhtk,
                highlightcolor='blue')
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))
            self.entr_str.configure(
                highlightthickness=hhtk,
                highlightcolor='red')

    def _buscar_anterior(self, event=None):
        self.buscar_prev()
        if self.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(
                self.numero_ocurrencia_actual, self.numero_ocurrencias))
            self.entr_str.configure(
                highlightthickness=hhtk,
                highlightcolor='blue')
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))
            self.entr_str.configure(
                highlightthickness=hhtk,
                highlightcolor='red')