# -*- coding: utf-8 -*-
# Copyright (c) YOUTUBE : Tkinter Hub
# For license see LICENSE

import tkinter as tk
from tkinter import ttk

class RadioButton(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        from Compliance import fondo_app, color_bg_boton, color_outline
        self.btn_frame = ttk.Frame(self)
        self.canvas = tk.Canvas(self, 
        height=185, 
        width=185
        )
        self.canvas.pack( pady=10)
        self.canvas.configure(
            background=fondo_app,
            border=0,
            borderwidth=0,
            highlightthickness=0
        )
        self.btn_frame.pack(side=tk.LEFT)

        
        def round_rectangle(obj, x1, y1, x2, y2, r=50, border=2, **kwargs):    
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return obj.create_polygon(points, **kwargs, smooth=True)
        
        round_rectangle(self.canvas, 5, 5, 180, 180, 50, outline=color_outline, width=3, fill=color_bg_boton, activewidth=3,  activefill=color_bg_boton, activeoutline=color_outline,)

class RB_Automatizacion_clt(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        from Compliance import fondo_app, color_bg_boton, color_outline
        self.btn_frame = ttk.Frame(self)
        self.canvas = tk.Canvas(self, 
        height=75, 
        width=205
        )
        self.canvas.pack(pady=5)
        self.canvas.configure(
            background=fondo_app,
            border=0,
            borderwidth=0,
            highlightthickness=0
        )
        self.btn_frame.pack(side=tk.LEFT)

        
        def round_rectangle(obj, x1, y1, x2, y2, r=25, border=2, **kwargs):    
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return obj.create_polygon(points, **kwargs, smooth=True)
        
        round_rectangle(self.canvas, 5, 5, 200, 70, 25, outline=color_outline, width=3, fill=color_bg_boton, activewidth=3,  activefill=color_bg_boton, activeoutline=color_outline,)

class RadioButton_venta(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        from Compliance import fondo_app, color_bg_boton, color_outline
        self.btn_frame = ttk.Frame(self)
        self.canvas = tk.Canvas(self, 
        height=55,
        width=155
        )
        self.canvas.pack()
        self.canvas.configure(
            background=fondo_app,
            border=0,
            borderwidth=0,
            highlightthickness=0
        )
        self.btn_frame.pack(side=tk.LEFT)

        
        def round_rectangle(obj, x1, y1, x2, y2, r=20, border=2, **kwargs):    
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return obj.create_polygon(points, **kwargs, smooth=True)
        
        round_rectangle(self.canvas, 5, 5, 150, 50, 20, outline=color_outline, width=3, fill=color_bg_boton, activewidth=3,  activefill=color_bg_boton, activeoutline=color_outline,)