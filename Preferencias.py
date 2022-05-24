# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import font
from getpass import getuser
from Extraciones import MyEntry
from Compliance import default_bottom_app, hhtk

class SelectFont(tk.Toplevel):
    def __init__(self, parent, titulo, app, application=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.titulo = titulo
        self.app = app
        self.geometry('700x600')
        self.title("Apariencia para {} ".format(self.titulo))
        self.our_font = font.Font(family='Helvetica', size=32)
        self.config(background=default_bottom_app)
        self.widget_preferencia()

    def widget_preferencia(self):
        font_size = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 96]
        font_styles = ["Regular", "Bold", "Italic", "Bold/Italic", "Underline", "Strike"]
        self.fr1 =  ttk.Frame(
            self, 
            #height=210
        )
        self.fr1.pack(
            #expand=1, 
            fill=tk.BOTH,
            side=tk.TOP
        )
        
        self.frl_familia = tk.LabelFrame(
            self.fr1,
            text="Familia:",
            height=250,
            relief='groove'
        )
        self.frl_familia.pack(
            #expand=1,
            fill=tk.BOTH,
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        #self.frl_familia.configure(width=200)

        self.frl_estilo = tk.LabelFrame(
            self.fr1,
            text="Estilo:",
            relief='groove'
        )
        self.frl_estilo.pack(
            #expand=1,
            fill=tk.BOTH,
            side=tk.LEFT,
            #padx=5,
            pady=10
        )

        self.frl_tamaño = tk.LabelFrame(
            self.fr1,
            text="Tamaño:",
            relief='groove'
        )
        self.frl_tamaño.pack(
            #expand=1,
            fill=tk.BOTH,
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.txt_familia = MyEntry(
            self.frl_familia,
        )
        self.txt_familia.pack(
            expand=0, 
            fill=tk.X, 
            side=tk.TOP,
            padx=10,
            pady=10,
            ipady=5,
        )

        self.txt_estilo = MyEntry(
            self.frl_estilo,
        )        
        self.txt_estilo.pack(
            expand=0, 
            fill=tk.X, 
            side=tk.TOP,
            padx=10,
            pady=10,
            ipady=5,
        )
        self.txt_estilo.config(width=18)

        self.txt_tamaño = MyEntry(
            self.frl_tamaño,
        )
        self.txt_tamaño.pack(
            expand=0, 
            fill=tk.X, 
            side=tk.TOP,
            padx=10,
            pady=10,
            ipady=5,
        )
        self.txt_tamaño.config(width=14)

        self.list_familia = tk.Listbox(
            self.frl_familia,
            height=12,
            width=26,
            exportselection=False,
            selectmode=tk.SINGLE
        )

        list_family = font.families()
        list_family = list(list_family)
        list_family.sort()
        result = []
        for f in list_family:
            if f not in result:
                result.append(f)
        
        for fuente in result:
            self.list_familia.insert(tk.END, fuente)
        
        self.list_familia.pack(
            expand=0,
            fill=tk.BOTH,
            side=tk.TOP,
            padx=10,
            pady=(0, 10)
        )

        self.list_familia.config(
            foreground="black",
            selectbackground="#5584AC",
            selectforeground="white",
            font="Helvetica",
            highlightcolor="#297F87",
            borderwidth=0,
            highlightthickness=hhtk,
        )

        self.list_estilo = tk.Listbox(
            self.frl_estilo,
            height=12,
            width=18,
            exportselection=False,
            selectmode=tk.SINGLE
        )

        for e in font_styles:
            self.list_estilo.insert(tk.END, e)
        
        self.list_estilo.pack(
            expand=0,
            fill=tk.BOTH,
            side=tk.TOP,
            padx=10,
            pady=(0, 10)
        )

        self.list_estilo.config(
            foreground="black",
            selectbackground="#5584AC",
            selectforeground="white",
            font="Helvetica",
            highlightcolor = "#297F87",
            borderwidth=0, 
            highlightthickness=hhtk,
        )
        
        self.list_size = tk.Listbox(
            self.frl_tamaño,
            height=12,
            width=14,
            exportselection=False,
            selectmode=tk.SINGLE
        )

        for t in font_size:
            self.list_size.insert(tk.END, t)


        self.list_size.pack(
            expand=0,
            fill=tk.BOTH,
            side=tk.TOP,
            padx=10,
            pady=(0, 10)
        )
        self.list_size.config(
            foreground="black",
            selectbackground="#5584AC",
            selectforeground="white",
            font="Helvetica",
            highlightcolor = "#297F87",
            borderwidth=0, 
            highlightthickness=hhtk,
        )

        self.fr2 = ttk.Frame(
            self,
            #height=210
        )
        self.fr2.pack(
            expand=1, 
            fill=tk.BOTH,
            #side=tk.BOTTOM
        )
        self.fr2.pack_propagate(False)

        value = StringVar()
        value.set('Prueba')
        self.result = tk.Label(
            self.fr2,
            background='white',
            anchor='center',
            width=10,
            height=2,
            textvariable=value,
            justify=tk.CENTER,
            font=self.our_font,
        )
        self.result.pack_propagate(0)
        self.result.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)
        
        self.fr3 =  ttk.Frame(
            self,
            #height=210
        )
        self.fr3.pack(
            expand=1, 
            fill=tk.BOTH,
            side=tk.BOTTOM
        )

        self.list_familia.bind("<ButtonRelease-1>", self.font_family_chooser)
        self.list_estilo.bind("<ButtonRelease-1>", self.font_style_chooser)
        self.list_size.bind("<ButtonRelease-1>", self.font_size_chooser)
        self.result.bind("<Configure>", self.label_resize)
    
    def font_family_chooser(self, e):
        # self.our_font.config(
        #     family=self.list_familia.get(self.list_familia.curselection())
        # )
        self.app._Font_Titulo_bold.config(
            family=self.list_familia.get(self.list_familia.curselection())
        )

    def font_style_chooser(self, e):
        style=self.list_estilo.get(self.list_estilo.curselection()).lower()
        if style == "bold":
            # self.our_font.config(
            # weight=style,
            # slant='roman',
            # underline=0
            # )
            self.app._Font_Titulo_bold.config(
            weight=style,
            slant='roman',
            underline=0        
            )
        
        if style == "italic":
            # self.our_font.config(
            # slant=style,
            # weight='normal',
            # underline=0
            # )
            self.app._Font_Titulo_bold.config(
            slant=style,
            weight='normal',
            underline=0       
            )
        
        if style == "bold/italic":
            # self.our_font.config(
            # weight='bold',
            # slant='italic',
            # underline=0
            # )
            self.app._Font_Titulo_bold.config(
            weight='bold',
            slant='italic',
            underline=0       
            )

        if style == "regular":
            # self.our_font.config(
            # weight='normal',
            # slant='roman',
            # underline=0
            # )
            self.app._Font_Titulo_bold.config(
            weight='normal',
            slant='roman',
            underline=0       
            )

        if style == "underline":
            # self.our_font.config(
            # weight='normal',
            # slant='roman',
            # underline=1
            # )
            self.app._Font_Titulo_bold.config(
            weight='normal',
            slant='roman',
            underline=1      
            )

    def font_size_chooser(self, e):
        # self.our_font.config(
        #     size=self.list_size.get(self.list_size.curselection())
        # )
        self.app._Font_Titulo_bold.config(
            size=self.list_size.get(self.list_size.curselection())
        )
    
    def label_resize(self, event):
        event.widget['wraplength'] = event.width
