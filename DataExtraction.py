# -*- coding: utf-8 -*-
from functools import partial
import os
import time
import tkinter as tk
from os import listdir
from os.path import isdir, join, abspath
from tkinter import  TclError, ttk
from tkinter import scrolledtext as st
from tkinter import font
from threading import Thread
from Compliance import pathExtractions, default_color_line_fg, default_Framework, default_select_fg, hlh_def, pers_menu_bg, pers_scrText_bg, pathConfig, parse, pers_bottom_app, activar_modo, mypath, hhtk, default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg, default_bottom_app, bg_submenu, default_scrText_fg, default_menu_bg, fg_submenu, _Font_Menu, _Font_Texto, default_select_bg, default_bottom_app, default_hglcolor, fuente_texto, tamñ_texto, _Font_Texto_bold, _Font_Texto_codigo
parar = False
_estado_actual = False
PST_EXT = ""
HIDDEN = 0
_activeFocus = False

def beep_error(f):
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    return applicator

class MyScrollText(st.ScrolledText):
    def __init__(self, parent, app, *args, **kwargs):
        st.ScrolledText.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.app = app
        self.configr()

    def configr(self):
        self.config( 
            font=_Font_Texto,
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
    
    def colourText(self, bg_color, bg_codigo, fg_codigo, fg_nota):
        self.tag_configure(
            "codigo",
            background=bg_codigo,
            foreground=fg_codigo,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_codigo
        )

        self.tag_configure(
            "line",
            background=bg_color,
            foreground=default_color_line_fg,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto_bold
        )

        self.tag_configure(
            "nota",
            background='#D4EFEE',
            foreground='#000000',
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto
        )

        self.tag_configure(
            "server",
            background='#7BB3A4',
            foreground='#000000',
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto
        )
        self.tag_configure(
            "coment",
            background=pers_scrText_bg,
            foreground='#EFB810',
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto
        )

        end = self.index("end")
        line_count = int(end.split(".", 1)[0])
        for line in range(1, line_count+1):
            startline = f"{line}.0"
            if not (self.search("##", startline, stopindex=f"{line}.1")) and not (self.search("// NOTA", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                self.tag_add(
                    "codigo", startline, endline)
            if (self.search("+-", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                self.tag_add(
                    "line", startline, endline)
            if (self.search("//", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                self.tag_add(
                    "nota", startline, endline)
            if (self.search("[", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                self.tag_add(
                    "server", startline, endline)
            if (self.search("\"", startline, stopindex=f"{line}.1")):
                endline = f"{line}.end"
                self.tag_add(
                    "coment", startline, endline)

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
            highlightthickness=hhtk,        
            )
        self.mostrar_menu()

        self.bind('<Control-a>', self.selectedAll)
        self.bind('<Control-A>', self.selectedAll)
        self.bind('<Control-f>', self.selectedAll)
        self.bind('<Control-F>', self.selectedAll)
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
            command=self.selectedAll,
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
        return 'break'

    def cortar(self, event=None):
        self.select_range(0, tk.END)
        self.event_generate("<<Cut>>")
        try:
            PST_EXT.defaultEntry()
        except:
            pass
        return 'break'

    def pegar(self, event=None):
        if self.select_present():
            self.delete(0, tk.END)
            self.event_generate("<<Paste>>")
        else:
            self.event_generate("<<Paste>>")
        return 'break'

    def selectedAll(self, event=None):
        self.select_range(0, tk.END)
        self.focus_set()
        return 'break'

    @beep_error
    def deshacer(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.delete(0, tk.END)
            self.insert(tk.END, self.changes[self.steps])
            self.menu_opciones.entryconfig("  Rehacer", state="normal")

    @beep_error
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
        PST_EXT = self
        self.wd = 300
        self.app = app
        self.hidden = 0
        self.menu()
        self.text()
        self.columnconfigure(2, weight=5)
        self.rowconfigure(0, weight=1)
        PST_EXT.bind("<Motion>", lambda e : self.EXT_motion(e))
        self.txt.bind('<Control-f>', lambda x: self.searchPanel(x))
        self.txt.bind('<Control-F>', lambda x: self.searchPanel(x))
        self.txt.bind('<Control-l>', lambda x: self.hide_btn_nav(x))
        self.txt.bind('<Control-c>', lambda x: self.copyTextSelected(x))
        self.txt.bind('<Control-C>', lambda x: self.copyTextSelected(x))
        self.txt.bind('<Control-a>', lambda e: self.selectedAll(e))
        self.txt.bind('<Control-x>', lambda e: self._limpiar_busqueda(e))
        self.txt.bind('<Control-X>', lambda e: self._limpiar_busqueda(e))
        self._ocurrencias_encontradas = []
        self._numero_ocurrencia_actual = None
        _estado_actual = False
        self._menu_clickDerecho()

        self.btn_nav = ttk.Button(
            self,
            image=self.app.iconoMenu,
            command=self.show_btn_nav,
        )
        self.btn_nav.bind("<Motion>", partial(self.app.openTooltip, self.btn_nav, "Show Panel"))
        self.btn_nav.bind("<Leave>", self.app._hide_event)
        
    def EXT_motion(self, event):
        global PST_EXT
        PST_EXT = event.widget
        PST_EXT.app.MODE_DARK()
        PST_EXT.app.EXT_motion()

    def menu(self):
        parse.read(pathConfig.format("apariencia.ini"))
        modo_dark = parse.get('dark', 'modo_dark')
        self.text_font = font.Font(family='Consolas', size=14, weight="bold")
        self.frameMain = tk.Frame(
            self,
            width=self.wd
        )
        if modo_dark == 'False':
            self.frameMain.config(
            background=default_menu_bg,
            )
        else:
            self.frameMain.config(
                background=pers_menu_bg,
            )
            #self.txt.config(background=pers_scrText_bg,)
        self.frameMain.grid_propagate(False)
        self.frameMain.grid(row=0, column=0, sticky="nsew", pady=(10,0))
        self.frameMain.columnconfigure(0, weight=1)
        self.frameMain.rowconfigure(1, weight=1)

        self.buttonCloseMenu = ttk.Button(
            self.frameMain,
            image=self.app.iconoCloseMenu,
            command=self.hide_btn_nav,
        )
        self.buttonCloseMenu.grid(row=0, column=0, sticky="e")
        
        self.treeview = ttk.Treeview(
            self.frameMain,
        )
        self.treeview.heading("#0", text="FICHEROS de EXTRACIONES", anchor="center")
        self.treeview.grid(row=1, column=0, sticky="nsew")

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
        self.max = ttk.Button(
            self.frameMain,
            width=4,
            text="+",
        )
        self.max.grid(row=2, column=0, sticky="e")

        self.min = ttk.Button(
            self.frameMain,
            width=4,
            text="-",
        )
        self.min.grid(row=2, column=0, sticky="w")

        # Cargar el directorio raíz.
        self.load_tree(abspath(pathExtractions))
        self.max.bind(
            "<Button-1>", lambda e: Thread(target=self.ampliar, daemon=True).start())
        self.max.bind("<ButtonRelease-1>", self._parar_)
        self.min.bind(
            "<Button-1>", lambda e: Thread(target=self.reducir, daemon=True).start())
        self.min.bind("<ButtonRelease-1>", self._parar_)

    def text(self):
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=0, column=2, sticky="nsew", padx=5, pady=(10,0))
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)
        self.txt = MyScrollText(
            self.frame2,
            self.app
        )
        self.txt.grid(row=0, column=0, sticky="nsew")
        self.txt.bind("<Key>", lambda e: self.app.widgets_SoloLectura(e))
        self.txt.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.txt.bind("<Motion>", lambda e: self.desactiveFocus(e))

    def ampliar(self):
        global parar
        parar = False
        while not parar:
            time.sleep(0.01)
            if self.wd < 1000:
                self.wd += 3
                self.frameMain.config(width=self.wd)
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
            if self.wd > 240:
                self.wd -= 3
                self.frameMain.config(width=self.wd)
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
        return self.app.iconoFolder if isdir(path) else self.app.iconoFile

    def insert_item(self, name, path, parent=""):
        """
        Añade un archivo o carpeta a la lista y retorna el identificador
        del ítem.
        """
        iid = self.treeview.insert(parent,
            tk.END, text=name,
            tags=("fstag",)+(("folder",) if isdir(path) else ()),
            image=self.get_icon(path)
        )
        self.fsobjects[iid] = path
        return iid

    def load_tree(self, path, parent=""):
        """
        Carga el contenido del directorio especificado y lo añade
        a la lista como ítemes hijos del ítem "parent".
        """
        for fsobj in listdir(path):
            fullpath = join(path, fsobj)
            child = self.insert_item(fsobj, fullpath, parent)
            if isdir(fullpath):
                for sub_fsobj in listdir(fullpath):
                    self.insert_item(sub_fsobj, join(fullpath, sub_fsobj),
                                     child)

    def load_subitems(self, iid):
        """
        Cargar el contenido de todas las carpetas hijas del directorio
        que se corresponde con el ítem especificado.
        """

        for child_iid in self.treeview.get_children(iid):
            if isdir(self.fsobjects[child_iid]):
                self.load_tree(self.fsobjects[child_iid],
                               parent=child_iid)

    def item_opened(self, event):
        """
        Evento invocado cuando el contenido de una carpeta es abierto.
        """
        iid = self.treeview.selection()[0]
        self.load_subitems(iid)

    def item_closed(self, event):
        """
        Evento invocado cuando el contenido de una carpeta es abierto.
        """
        iid = self.treeview.selection()[0]
        records = self.treeview.get_children(iid)
        self.treeview.delete(*self.treeview.get_children())
        self.load_tree(abspath(pathExtractions))

    def select_extraction(self, event):
        treeSelect = event.widget
        iid = treeSelect.selection()[0]
        plantilla = treeSelect.item(iid, option="text")
        path = ''
        for root, _, files in os.walk(pathExtractions):
            if plantilla in files:
                path = os.path.join(root, plantilla)
                break
        if len(path) != 0:
            self.seleccionar_plantilla(path)
            #todo LLMADA A COLORES
            #PST_EXT.txt.colourText(default_scrText_bg, default_colourCodeBg, default_colourCodeFg, default_colourNoteFg)
            self.colour_line()
            self.colour_line2()

    def colour_line(self):
        indx3 = '1.0'
        indx4 = '1.0'
        line3 = "CONTESTAR NO"
        line4 = "CONTESTAR N/A"
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
            command=self.copyTextSelected,
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo",
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.selectedAll
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
            command=self.hide_btn_nav
        )
        self.menu_Contextual.add_command(
            label="  Mostrar Panel",
            state="disabled",
            accelerator='Ctrl+L',
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_select_bg, activeforeground=default_select_fg,
            font=_Font_Menu,
            command=self.hide_btn_nav
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
        PST_EXT.txt.tag_remove('found', '1.0', tk.END)
        PST_EXT.txt.tag_remove('found_prev_next', '1.0', tk.END)
        self.defaultEntry()

    def _limpiar_busqueda(self, event):
        txt_event = event.widget
        self.var_entry_bsc.set("")
        self.menu_Contextual.entryconfig(
            '  Limpiar Busqueda', state='disabled')
        txt_event.tag_remove('found', '1.0', tk.END)
        txt_event.tag_remove('found_prev_next', '1.0', tk.END)
        self.defaultEntry()

    def copyTextSelected(self, *args):
        scrText = PST_EXT.txt
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel", "1.0", "end")
            return 'break'
        else:
            pass

    def selectedAll(self, *args):
        scrText = PST_EXT.txt
        scrText.tag_add("sel", "1.0", "end")
        return 'break'

    def cerrar_vtn_desviacion(self):
        self.app.cerrar_vtn_desviacion()

    def hide_btn_nav(self, *args):
        global parar
        if self.hidden == 0:
            self.frameMain.destroy()
            self.btn_nav.grid(row=0, column=0, sticky="nw", pady=10)
            self.menu_Contextual.entryconfig(
                "  Ocultar Panel", state="disabled")
            self.menu_Contextual.entryconfig("  Mostrar Panel", state="normal")
            self.hidden = 1
            parar = False
        elif self.hidden == 1:
            self.menu()
            self.menu_Contextual.entryconfig("  Ocultar Panel", state="normal")
            self.menu_Contextual.entryconfig(
                "  Mostrar Panel", state="disabled")
            self.btn_nav.grid_forget()
            self.hidden = 0
            parar = False

    def show_btn_nav(self):
        global parar
        if self.hidden == 1:
            self.menu()
            self.btn_nav.grid_forget()
            self.menu_Contextual.entryconfig("  Ocultar Panel", state="normal")
            self.menu_Contextual.entryconfig(
                "  Mostrar Panel", state="disabled")
            self.hidden = 0
        parar = False

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
        # establecer la marca distintiva para la ocurrencia a etiquetar
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
        self.y_alto_btn = 115
        self.x_ancho_btn = 680
        self.hg_btn = int(self.y_alto_btn-30)
        self.wd_btn = int(self.x_ancho_btn-30)
        from RadioBotton import RadioFrame
        global _estado_actual
        global _activeFocus
        _activeFocus = True
        if not _estado_actual:
            self.busca_top = tk.Toplevel(self.frame2)
            window_width =  self.x_ancho_btn
            window_height = self.y_alto_btn
            bus_reem_top_msg_w = 240
            self.busca_top.attributes('-type', 'splash')            #self.busca_top.overrideredirect(True)
            screen_width = (self.app.root.winfo_x() + 640)
            screen_height = (self.app.root.winfo_y()+40)
            position_top = int(screen_height)
            position_right = int(screen_width)
            self.busca_top.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
            self.busca_top.transient(self)

            self.busca_top.config(
                bg=default_bottom_app,
            )
            self.busca_top.resizable(0, 0)
            self.frameRadio = RadioFrame(
                self.busca_top,
                alto=self.y_alto_btn,
                ancho=self.x_ancho_btn,
                radio=25,
                width=3,
                bg_color=None
            )
            self.frameRadio.pack()

            self.framePanel = tk.Frame(
                self.frameRadio,
                background=default_bottom_app
            )
            self.framePanel.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            height=self.hg_btn,
            width=self.wd_btn
            )
            self.busca_frm_tit = tk.Frame(
                self.framePanel,
            )
            self.busca_frm_tit.pack(fill='x', expand=1)

            self.busca_frm_content = tk.Frame(
                self.framePanel,
                bg=default_bottom_app,
                #padx=5,
                pady=10
            )
            self.busca_frm_content.pack(fill='x', expand=1)

            self.busca_top.title('Buscar')
            self.bus_reem_num_results = tk.StringVar()
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))

            self.buscar_01_msg = tk.Message(
                self.busca_frm_tit,
                textvariable=self.bus_reem_num_results,
                # padx=10,
                # pady=0
            )
            self.buscar_01_msg.pack(fill='both', expand=1)
            self.buscar_01_msg.config(
                width=bus_reem_top_msg_w,
                background=default_bottom_app,
                foreground="black",
                justify='center',
                font=(fuente_texto, 14, 'bold')
            )

            self.buscar_01_msg.bind("<ButtonPress-1>", self.start_move)
            self.buscar_01_msg.bind("<ButtonRelease-1>", self.stop_move)
            self.buscar_01_msg.bind("<B1-Motion>", self.on_move)

            self.var_entry_bsc = tk.StringVar(self)

            self.EXT_entry = MyEntry(
                self.busca_frm_content,
                textvariable=self.var_entry_bsc,
            )

            self.EXT_entry.configure(
                width=40,
                highlightcolor=default_hglcolor,
                insertbackground=default_hglcolor,
                insertwidth=1,
                selectbackground=default_select_bg,
                highlightthickness=1,
                font=(fuente_texto, 14)
            )

            self.EXT_entry.grid(row=0, column=0, ipady=8, sticky="nsew")

            self.buttonClosePanel = tk.Button(
                self.busca_frm_content,
                text='X',
                image=self.app.iconoClose,
                command=self._on_closing_busca_top
            )
            self.buttonClosePanel.config(
                background=default_bottom_app,
                highlightcolor=default_hglcolor,
                activebackground=default_bottom_app,
                border=0,
                highlightbackground=default_bottom_app,
            )
            self.buttonClosePanel.grid(row=0, column=4, padx=10, pady=5)

#--- Botom Limpiar
            self.buttonClosePanel = tk.Button(
                self.busca_frm_content,
                text='<<',
                image=self.app.iconoClear,
                command=self.limpiar_busqueda
            )

            self.buttonClosePanel.config(
                background=default_bottom_app,
                highlightcolor=default_hglcolor,
                activebackground=default_bottom_app,
                border=0,
                highlightbackground=default_bottom_app,
            )

            self.buttonClosePanel.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")

#--- Botom anterior
            self.btn_buscar_prev = tk.Button(
                self.busca_frm_content,
                text='<|',
                image=self.app.iconoArrowUp,
                command=self._buscar_anterior
            )

            self.btn_buscar_prev.config(
                background=default_bottom_app,
                highlightcolor=default_hglcolor,
                activebackground=default_bottom_app,
                border=0,
                highlightbackground=default_bottom_app,
            )

            self.btn_buscar_prev.grid(
                row=0, column=2, padx=5, pady=5, sticky="nsew")

#--- Botom siguiente
            self.btn_buscar_next = tk.Button(
                self.busca_frm_content,
                text='|>',
                image=self.app.iconoArrowDown,
                command=self._buscar_siguiente
            )

            self.btn_buscar_next.config(
                background=default_bottom_app,
                highlightcolor=default_hglcolor,
                activebackground=default_bottom_app,
                border=0,
                highlightbackground=default_bottom_app,
            )

            self.btn_buscar_next.grid(
                row=0, column=3, padx=(5, 10), pady=5, sticky="nsew")

#--- Activa el focu en el ENTRY
            self.EXT_entry.focus_set()

#--- Busca palabras al escribir, y activa el panel
            self.EXT_entry.bind('<Any-KeyRelease>', self.on_EXT_entry_busca_key_release)
            self.txt.bind("<Button-1>", lambda e: self.activeFocus(e))
            self.txt.bind("<Motion>", lambda e: self.desactiveFocus(e))
            self.EXT_entry.bind("<Motion>", lambda e: self.desactiveFocus(e))
            self.EXT_entry.bind("<Button-1>", lambda e: self._Focus(e))
            
            self.app.MODE_DARK()

            _estado_actual = True
        else:
            self._buscar_focus(self.EXT_entry)
            _estado_actual = True
            return 'break'

    def start_move(self, event):
        self._a = event.x
        self._b = event.y

    def stop_move(self, event):
        self._a = None
        self._b = None

    def on_move(self, event):
        deltax = event.x - self._a
        deltay = event.y - self._b
        new_pos = "+{}+{}".format(self.busca_top.winfo_x() + deltax, self.busca_top.winfo_y() + deltay)
        self.app.root.geometry(new_pos)
        self.busca_top.geometry(new_pos)

    def _buscar_focus(self, event):
        self.EXT_entry.selectedAll(event)

    def _on_closing_busca_top(self):
        global PST_EXT
        global _estado_actual
        #self.menu_Contextual.entryconfig(    "  Limpiar Busqueda", state="disabled")
        #self.limpiar_busqueda()
        _estado_actual = False
        PST_EXT.busca_top.destroy()

## --- Activa el focu de los widgets del PANEL
    def activeFocus(self, event):
        global _activeFocus
        _activeFocus = False

    def _Focus(self, event):
        global _activeFocus
        _activeFocus = True

    def desactiveFocus(self, event):
        global _activeFocus
        if _activeFocus ==  True:
            try:
                PST_EXT.EXT_entry.focus()
            except TclError:
                _activeFocus = False
            except AttributeError:
                _activeFocus = False
        else:
            self.txt.focus()

## --- Al escribir en el ENTRY del PANEL, busca concurrencias
    def on_EXT_entry_busca_key_release(self, event):
        if event.keysym != "F2" and event.keysym != "F3":  # F2 y F3
            self._buscar()
            return "break"

    def _buscar(self, event=None):
        self.buscar_todo(self.EXT_entry.get().strip())
        if self.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(
                self.numero_ocurrencia_actual, self.numero_ocurrencias))
            self.foundEntry()
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))
            if self.var_entry_bsc.get() == "":
                self.defaultEntry()
            else:
                self.noFoundEntry()

    def foundEntry(self):
        self.EXT_entry.configure(
                highlightthickness=2,
                highlightcolor='#003482')

    def noFoundEntry(self):
        self.EXT_entry.configure(
                    highlightthickness=2,
                    highlightcolor='orange red')

    def defaultEntry(self):
        self.EXT_entry.configure(
                highlightthickness=1,
                highlightcolor=default_hglcolor)
        self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))
    
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

            # self.buscar_next(self.EXT_entry.get().strip())
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
            # self.EXT_entry.configure(
            #     highlightthickness=2,
            #     highlightcolor='blue')
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))

    def _buscar_anterior(self, event=None):
        self.buscar_prev()
        if self.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(
                self.numero_ocurrencia_actual, self.numero_ocurrencias))
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))