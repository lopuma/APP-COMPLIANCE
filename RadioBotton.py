# -*- coding: utf-8 -*-
# Copyright (c) YOUTUBE : Tkinter Hub
# For license see LICENSE

import tkinter as tk
from tkinter import ttk

class RadioButton(ttk.Frame):
    def __init__(self, parent, alto, ancho, radio, *args, **kwargs):
        super().__init__(parent,  *args, **kwargs)
        from Compliance import fondo_app, color_default_bgBT, color_default_outline
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
        
        round_rectangle(self.canvas, 5, 5, ancho - 5, alto - 5, radio, outline=color_default_outline, width=3, fill=color_default_bgBT, activewidth=3,  activefill=color_default_bgBT, activeoutline=color_default_outline,)
    
class BtnScripts(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        from Compliance import color_default_fgBT, _Font_Boton, color_default_bgBT, color_default_afgBT
        ttk.Button.configure(self,
            background=color_default_bgBT,
            foreground=color_default_fgBT,
            font=_Font_Boton,
            activeforeground=color_default_afgBT,
            activebackground=color_default_bgBT,
            border=0,
            highlightthickness=0,
        )
