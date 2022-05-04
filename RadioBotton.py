# -*- coding: utf-8 -*-
# Copyright (c) YOUTUBE : Tkinter Hub
# For license see LICENSE

import tkinter as tk
from tkinter import ttk
from turtle import bgcolor

bg_cl = ''
class RadioButton(ttk.Frame):
    def __init__(self, *args,
                 alto, 
                 ancho, 
                 radio,
                 bg_color, 
                 **kwargs):
        super().__init__(*args, **kwargs)
        from Compliance import fondo_app, color_default_bgBT, color_default_outline
        
        global bg_cl

        bg_cl =  bg_color
        if bg_cl is None:
            bg_cl = color_default_bgBT
            print(bg_cl)
        else:
            bg_cl = bg_color
        
        print("llega :: ", bg_color)
        print("sale :: ", bg_cl)
        self.canvas = tk.Canvas(self,
        height=alto, 
        width=ancho,
        )
        self.canvas.pack( pady=10)
        self.canvas.configure(
            background=fondo_app,
            border=0,
            borderwidth=0,
            highlightthickness=0
        )
        

        def round_rectangle(obj, x1, y1, x2, y2, r=radio, border=2, **kwargs):    
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return obj.create_polygon(points, **kwargs, smooth=True)
        
        round_rectangle(self.canvas, 5, 5, ancho - 5, alto - 5, radio, outline=color_default_outline, width=3, fill=bg_cl, activewidth=3,  activefill=color_default_bgBT, activeoutline=color_default_outline,)
    
class BtnScripts(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        from Compliance import color_default_fgBT, _Font_Boton, color_default_abgBT, color_default_afgBT
        print(bg_cl)        
        ttk.Button.configure(self,
            background=bg_cl,
            foreground=color_default_fgBT,
            font=_Font_Boton,
            activeforeground=color_default_afgBT,
            activebackground=color_default_abgBT,
            border=0,
            highlightthickness=0,
        )
