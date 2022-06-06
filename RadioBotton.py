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
            width,
            bg_color, 
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        from Compliance import default_bottom_app, default_Outline
        
        global bg_cl

        bg_cl =  bg_color
        if bg_cl is None:
            bg_cl = 'red'
        else:
            bg_cl = bg_color
        
        self.canvas = tk.Canvas(self,
        height=alto, 
        width=ancho,
        )
        self.canvas.pack( pady=10)
        self.canvas.configure(
            background=default_bottom_app,
            border=0,
            borderwidth=0,
            highlightthickness=0
        )
        

        def round_rectangle(obj, x1, y1, x2, y2, r=radio, border=2, **kwargs):    
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return obj.create_polygon(points, **kwargs, smooth=True)
        
        round_rectangle(self.canvas, 5, 5, ancho - 5, alto - 5, radio, outline=default_Outline, width=width, fill=bg_cl, activewidth=width)

class RadioFrame(ttk.Frame):
    def __init__(self, *args,
            alto, 
            ancho, 
            radio,
            width,
            bg_color, 
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        from Compliance import default_bottom_app, default_scrText_fg
        global bg_cl
        bg_cl =  bg_color
        if bg_cl is None:
            bg_cl = default_bottom_app
        else:
            bg_cl = bg_color
        
        self.canvas = tk.Canvas(self,
        height=alto, 
        width=ancho,
        )
        self.canvas.pack()
        self.canvas.configure(
            background="gray90",
            border=0,
            borderwidth=0,
            highlightthickness=0
        )

        def round_rectangle(obj, x1, y1, x2, y2, r=radio, border=2, **kwargs):    
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return obj.create_polygon(points, **kwargs, smooth=True)
        
        round_rectangle(self.canvas, 1, 1, ancho - 2 , alto - 2, radio, outline=default_scrText_fg, width=width, fill=bg_cl, activewidth=width)

class BtnScripts(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        from Compliance import default_boton_fg, _Font_Boton, default_boton_acbg, default_boton_acfg
        tk.Button.configure(self,
            background=bg_cl,
            foreground=default_boton_fg,
            font=_Font_Boton,
            activeforeground=default_boton_acfg,
            activebackground=default_boton_acbg,
            border=0,
            highlightthickness=0,
        )
