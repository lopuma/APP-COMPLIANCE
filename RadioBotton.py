# -*- coding: utf-8 -*-
# Copyright (c) YOUTUBE : Tkinter Hub
# For license see LICENSE

import tkinter as tk
from tkinter import ttk

class RadioButton(ttk.Frame):
    def __init__(self, parent, alto, ancho, radio, *args, **kwargs):
        super().__init__(parent,  *args, **kwargs)
        from Compliance import fondo_app, color_bg_boton, color_outline
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
        
        round_rectangle(self.canvas, 5, 5, ancho - 5, alto - 5, radio, outline=color_outline, width=3, fill=color_bg_boton, activewidth=3,  activefill=color_bg_boton, activeoutline=color_outline,)
    
class BtnScripts(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        from Compliance import color_fg_boton, _Font_Boton, color_bg_boton, color_btn_actfg
        ttk.Button.configure(self,
            background=color_bg_boton,
            foreground=color_fg_boton,
            font=_Font_Boton,
            activeforeground=color_btn_actfg,
            activebackground=color_bg_boton,
            border=0,
            highlightthickness=0,
        )
