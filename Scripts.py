# -*- coding: utf-8 -*-
import os
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from getpass import getuser
import subprocess
from functools import partial
from ScrollableNotebook  import *
from Compliance import default_bottom_app, default_boton_acfg, default_boton_fg, hhtk, default_boton_bg
from RadioBotton import RadioButton, BtnScripts
#* variable para actualizar la ventana
PST_AUT = ""
FR_POL = ""
FR_SCR = ""
fr_clt = False
framescript = ""
#* PATH
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
path_config = mypath+"Compliance/.conf/{}.json"
btn_cerrar = ""
# * COLORES INICIALES
# ? -------------------------------------------------------------
color_bd_fr = '#383838'
colour_fr_pie = '#C65D7B'
colour_fr_tittle = '#F68989'
cl_btn_actbg = '#8FBDD3'
# ? -------------------------------------------------------------
class FramesPoliticas(ttk.Frame):
    def __init__(self, parent, cliente, frame, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        global FR_POL
        self.btn_lis_pol = []
        self.btn_rb_pol = []
        self.frame = frame
        FR_POL = self
        self.cliente = cliente
        self.bind("<Motion>", self.FR_POL_motion)
        self.fr_md2 = ttk.Frame(
            self.frame,
        )

        self.fr_md2.pack(
            fill=tk.BOTH,
            side='left',
            padx=(10,0)
        )

        self.fr_md2.config(
            borderwidth=0,
            border=0
        )

        self.canvas = tk.Canvas(
            self.fr_md2,
            background=default_bottom_app,
            width=400,
            borderwidth=0,
            border=0,
            highlightthickness=0
        )
        
        self.h = tk.Scrollbar(
            self.fr_md2,
            orient='vertical',
            command=self.canvas.yview
        )

        self.lb_frame_politica = ttk.LabelFrame(
            self.canvas,
            text='POLICY : {}'.format(cliente),
            relief='groove'
        )

        self.lb_frame_politica.bind("<Configure>", lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0,0), window=self.lb_frame_politica, anchor="nw", width=400, height=675)

        self.canvas.config(yscrollcommand=self.h.set)
#
        self.canvas.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=0,
            pady=10
        )

        self.h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(20,0)
        )

        self.canvas.bind("<Button-5>", self.OnVsb_down)
        self.canvas.bind("<Button-4>", self.OnVsb_up)
        self.lb_frame_politica.bind("<Button-5>", self.OnVsb_down)
        self.lb_frame_politica.bind("<Button-4>", self.OnVsb_up)

        # * ----------- BOTOTNES DE POLITICAS ------------
        self.asignar_name_clt(cliente)

    def format_response(self, data):
        url = path_icon+"{}"
        y_alto_btn = 80
        x_ancho_btn = 300
        hg_btn = int(y_alto_btn - 22)
        wd_btn = int(x_ancho_btn - 22)
        for pl in data['politica']:
            politica_icon = pl['icon']
            logo_script_ico = ImageTk.PhotoImage(
                Image.open(url.format(politica_icon)).resize((80, 60)))
            
            self.buttons_POLITICA = RadioButton(
                self.lb_frame_politica,
                alto=y_alto_btn,
                ancho=x_ancho_btn,
                radio=25,
                bg_color=default_bottom_app,
                width=3
            )
            self.buttons_POLITICA.pack(
                expand=0,
                padx=10,
                pady=10,
                fill='both',
            )
            self.botones_politica = BtnScripts(
                self.buttons_POLITICA,
                text=pl['main'],
                compound='left',
                #image=self.goclient_ico,
            )

            self.botones_politica["command"] = partial(
                self.abrir_frames_scripts_, self.botones_politica, self.cliente, data, self.frame, logo_script_ico, self.buttons_POLITICA)

            self.botones_politica.place(
                relx=0.5,
                rely=0.5,
                anchor=tk.CENTER,
                height=hg_btn,
                width=wd_btn
            )
            self.buttons_POLITICA.bind("<Button-5>", self.OnVsb_down)
            self.buttons_POLITICA.bind("<Button-4>", self.OnVsb_up)
            self.botones_politica.bind("<Button-5>", self.OnVsb_down)
            self.botones_politica.bind("<Button-4>", self.OnVsb_up)
            self.botones_politica.bind("<Button-1>", partial(self.on_enter_politica, self.botones_politica, self.buttons_POLITICA))

    def asignar_name_clt(self, name):
        with open(path_config.format('clientes')) as pr_clt:
            data = json.load(pr_clt)
            for dt in data:
                if dt['name'] == name:
                    self.format_response(dt)
    
    def FR_POL_motion(self, event):
        global FR_POL
        FR_POL = event.widget

    def borrar(self):
        self.canvas.destroy()
        self.canvas.pack_forget()
        self.h.destroy()
        self.h.pack_forget()
        self.lb_frame_politica.pack_forget()
        self.lb_frame_politica.destroy()
        self.fr_md2.pack_forget()
        self.fr_md2.destroy()

    def abrir_frames_scripts_(self, btn, cliente, data, frame, icon, canvas):
        global framescript
        global btn_cerrar
        lt_scr = ""
        self.lista_scripts = []
        self.fr_cv_politicas = []
        self.fr_cv_politicas.append(canvas)
        btn.focus_set()
        self.frame =  frame
        btn_cerrar['image'] = icon
        scr_pol = btn['text']
        for pl in data['politica']:
            if scr_pol in pl['main']:
                self.lista_scripts.append(pl['script'])
                lt_scr = pl['script']

        ## Al hacer click se cambiar de color.
        if btn:
            # #* aqui si quieres poner fondo al boton
            btn.configure(
                #bg=cl_btn_actbg,
                fg=default_boton_acfg
            )

            # #* aqui si quieres poner fondo al canvas
            for rb in self.fr_cv_politicas:
                rb.canvas.itemconfig(1, fill=default_boton_bg, outline=default_boton_acfg)


        if type(framescript) == str:
            self.framescript = FramesScripts(
                self, cliente, self.frame, lt_scr, scr_pol)
            framescript =  self.framescript
        else:
            self.framescript.borrar_script()
            self.framescript = FramesScripts(
                self, cliente, self.frame, lt_scr, scr_pol)

    def OnVsb_down(self, event):
        FR_POL.canvas.yview_scroll(1, "units")

    def OnVsb_up(self, event):
        FR_POL.canvas.yview_scroll(-1, "units")

    def on_enter_politica(self, btn, canvas, *arg):
        self.btn_rb_pol.append(canvas)
        self.btn_lis_pol.append(btn)

        for i in self.btn_lis_pol:
            i['background'] = default_boton_bg
            i['foreground'] = default_boton_fg

        for rb in self.btn_rb_pol:
            rb.canvas.itemconfig(1, fill=default_boton_bg, outline=default_outline)

class FramesScripts(ttk.Frame):
    def __init__(self, parent, cliente, frame, lt_scr, scr_pol, * args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        global FR_SCR
        global framescript
        self.btn_rb_scr = []
        self.btn_lis_scr = []
        self.frame = frame
        self.cliente = cliente
        FR_SCR = self
        
        self.bind("<Motion>", self.FR_SCR_motion)
        
        self.fr_md3 = ttk.Frame(
            self.frame,
        )

        self.fr_md3.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=1,
            padx=10
        )

        self.fr_md3.config(
            borderwidth=0,
            border=0
        )

        self.canvas3 = tk.Canvas(
            self.fr_md3,
            background=default_bottom_app,
            borderwidth=0,
            border=0,
            highlightthickness=0
        )
        
        self.scr3 = tk.Scrollbar(
            self.fr_md3,
            orient='vertical',
            command=self.canvas3.yview
        )

        self.lb_frame_script = ttk.LabelFrame(
            self.canvas3,
            text='{} - SCRIPTS - {}'.format(cliente, scr_pol),
            relief='groove'
        )

        self.lb_frame_script.bind("<Configure>", lambda e:self.canvas3.configure(scrollregion=self.canvas3.bbox("all")))

        self.canvas3.create_window((0,0), window=self.lb_frame_script, anchor="nw")

        self.canvas3.config(yscrollcommand=self.scr3.set)
#
        self.canvas3.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=1,
            pady=10
        )

        self.scr3.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(20,0),
        )
        self.canvas3.bind("<Button-5>", self.OnVsb_down)
        self.canvas3.bind("<Button-4>", self.OnVsb_up)
        self.lb_frame_script.bind("<Button-5>", self.OnVsb_down)
        self.lb_frame_script.bind("<Button-4>", self.OnVsb_up)

        # * ----------- BOTOTNES DE SCRIPTS ------------
        def ceildiv(dividendo, divisor):
            # divmod nos devuelve una tupla con el cociente y el resto, desempaquetamos eso.
            cociente, resto = divmod(dividendo, divisor)

            # sumamos al cociente el resto convertido en booleano. Recuerda que True vale 1 y False 0.
            # Por lo que si hay resto se sumará 1.
            return cociente + bool(resto)

        def grid_by_column(frame, columns, spacex=10, spacey=10):
            # obtenemos todos los widgets del frame
            widgets = frame.winfo_children()
            rows = ceildiv(len(widgets), columns)

            row = 0
            column = 0

            for widget in widgets:
                # ubicamos el widget en la esquina noroeste de la celda.
                widget.grid(row=row, column=column, sticky="nw", padx=10, pady=10)

                # el siguiente widget será ubicado en la siguiente columna.
                column += 1

                # si alcanzamos la cantidad maxima de columnas...
                if(column >= columns):
                    column = 0
                
                    row += 1

            # le agregamos un espacio (en este caso a la derecha) a cada fila menos la ultima.
            # La ultima se omite para evitar que el frame tenga espacio vacío en el borde derecho.
            for row in range(rows-1):
                frame.rowconfigure(row, pad=spacex)

            # se hace lo mismo con las columnas. Se omite la ultima para evitar que haya espacio vacío en el borde inferior.
            for column in range(columns-1):
                frame.columnconfigure(column, pad=spacey)

        #* Tmaño de los botones
        y_alto_btn = 150
        x_ancho_btn = 150
        hg_btn = int(y_alto_btn - 22)
        wd_btn = int(x_ancho_btn - 22)

        for l in lt_scr:
            self.buttons_SCRIPT = RadioButton(
                self.lb_frame_script,
                alto=y_alto_btn,
                ancho=x_ancho_btn,
                radio=25,
                bg_color=default_bottom_app,
                width=3
            )

            grid_by_column(self.lb_frame_script, 4)

            self.btn_scr = BtnScripts(
                self.buttons_SCRIPT,
                text=l,
            )

            self.btn_scr["command"] = partial(
                self.ejecutar_script, self.btn_scr, self.cliente, l, self.frame, self.buttons_SCRIPT)

            self.btn_scr.place(
                relx=0.5,
                rely=0.5,
                anchor=tk.CENTER,
                height=hg_btn,
                width=wd_btn
            )

            self.buttons_SCRIPT.bind("<Button-5>", self.OnVsb_down)
            self.buttons_SCRIPT.bind("<Button-4>", self.OnVsb_up)
            self.btn_scr.bind("<Button-5>", self.OnVsb_down)
            self.btn_scr.bind("<Button-4>", self.OnVsb_up)
            self.btn_scr.bind("<Button-1>", partial(self.on_enter_script,
                        self.btn_scr, self.buttons_SCRIPT))

    def FR_SCR_motion(self, event):
        global FR_SCR
        FR_SCR = event.widget

    def borrar_script(self):
        self.canvas3.destroy()
        self.canvas3.pack_forget()
        self.scr3.destroy()
        self.scr3.pack_forget()
        self.lb_frame_script.pack_forget()
        self.lb_frame_script.destroy()
        self.fr_md3.pack_forget()
        self.fr_md3.destroy()

## --- FUNCIONES PARA SCROLLBAR
    def OnVsb_down(self, event):
        self.canvas3.yview_scroll(1, "units")

    def OnVsb_up(self, event):
        self.canvas3.yview_scroll(-1, "units")

    def on_enter_script(self, btn, canvas, *arg):
        
        self.btn_rb_scr.append(canvas)
        self.btn_lis_scr.append(btn)

        for i in self.btn_lis_scr:
            i['background'] = default_boton_bg
            i['foreground'] = default_boton_fg

        for rb in self.btn_rb_scr:
            rb.canvas.itemconfig(1, fill=default_boton_bg, outline=default_outline)

    def ejecutar_script(self, btn, cliente, datos, frame, canvas):
        self.fr_cv_scripts = []
        self.fr_cv_scripts.append(canvas)
        btn.focus_set()

        ## Al hacer click se cambiar de color.
        if btn:
            #* aqui si quieres poner fondo al boton
            btn.configure(
                #bg=cl_btn_actbg,
                fg=default_boton_acfg
            )

            # #* aqui si quieres poner fondo al canvas
            for rb in self.fr_cv_scripts:
                rb.canvas.itemconfig(1, fill=default_boton_bg,
                                    outline=default_boton_acfg)

class Automatizar(ttk.Frame):
    def __init__(self, parent, app, application=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        global PST_AUT
        self.btn_lis_cli = []
        self.bfr_rb_list = []
        self.click = True
        self.cont = 0
        PST_AUT = self
        self.iconos()
        self.frames()
        self.app = app
        self.bind("<Motion>", lambda x: self.AUT_motion(x))
    
    def AUT_motion(self, event):
        global PST_AUT
        PST_AUT = event.widget
    
    def iconos(self):
        self.close_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"close1.png").resize((80, 60)))
        self.goclient_ico = ImageTk.PhotoImage(
            Image.open(path_icon+r"goclient.png").resize((20, 20)))

    def src_sudo(self):
        tittle = "{} SCRIPT de {}".format(("AFB"), ("SUDO"))
        password = "Qk6vzwZM8!wAohw"
        file = '/home/esy9d7l1/Compliance/./remoteexec.sh '+password
        subprocess.Popen(["gnome-terminal", "-e", file, "-t",
                        tittle, "--geometry", '200x30'])

    def frames(self):
# TODO ---------- FRAME ARRIBA --------------
        global PST_AUT
        self.frame_titulo = tk.Frame(
            self,
            height=100
        )
        self.frame_titulo.pack(
            fill='both',
            padx=5,
            pady=(10,5),
            expand=0
        )
        self.frame_titulo.config(
            background=colour_fr_tittle,
            borderwidth=2,
            highlightbackground=color_bd_fr,
            highlightthickness=hhtk
        )
        # fuente de los titulos de los LABEL FRAMES
#TODO -------------- FRAME MEDIO-----------------------------
        self.frame_medio = tk.Frame(
            self,
        )
        self.frame_medio.pack(
            fill='both',
            padx=5,
            expand=1
        )
        self.frame_medio.config(
            background=default_bottom_app,
            borderwidth=2,
            highlightbackground=color_bd_fr,
            highlightthickness=hhtk
        )
#---------------------------------------------------------------------------------------------
#? ------------- PARTE 1 DE FRAMES MEDIO ------------------------
        self.fr_md1 = ttk.Frame(
            self.frame_medio,
        )
        self.fr_md1.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
        )
        self.fr_md1.config(
            borderwidth=0,
            border=0
        )
# ------------------------------------------------------------------
# #? ----------- CREAR  CANVAS PARA AÑADIR BOTONES Y SER SCROLLABLE
        self.canvas = tk.Canvas(
            self.fr_md1,
            background=default_bottom_app,
            width=300,
            borderwidth=0,
            border=0,
            highlightthickness=0
        )
        
        h = tk.Scrollbar(
            self.fr_md1,
            orient='vertical',
            command=self.canvas.yview
        )
        
        self.lb_frame_menu =  ttk.LabelFrame(
            self.canvas,
            text='CLIENTS',
            relief='groove'
        )
        
        self.lb_frame_menu.bind("<Configure>", lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0,0), window=self.lb_frame_menu, anchor="nw", width=300)
        
        self.canvas.config(yscrollcommand=h.set)

        self.canvas.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
            pady=10,
            padx=(5,0)
        )
        
        h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(20,0)
        )

        self.canvas.bind("<Button-5>", self._On_canvas_down)
        self.canvas.bind("<Button-4>", self._On_canvas_up)
        self.lb_frame_menu.bind("<Button-5>", self._On_canvas_down)
        self.lb_frame_menu.bind("<Button-4>", self._On_canvas_up)

        #* Tmaño de los botones
        y_alto_btn = 80
        x_ancho_btn = 200
        hg_btn = int(y_alto_btn - 22)
        wd_btn = int(x_ancho_btn - 22)
# # * ----------- BOTOTNES DE CLIENTES ------------
        with open(path_config.format("clientes")) as op:
            data = json.load(op)
            for clt in data:
                self.buttons_clientes = RadioButton(
                    self.lb_frame_menu,
                    alto=y_alto_btn,
                    ancho=x_ancho_btn,
                    radio = 25,
                    bg_color=default_bottom_app,
                    width=3
                )
                self.buttons_clientes.pack(
                    expand=0,
                    padx=10,
                    pady=10,
                    fill='both',
                )
                self.btn_clientes = BtnScripts(
                    self.buttons_clientes,
                    text=" "+clt['name'],
                    compound='left',
                    image=self.goclient_ico,
                )

                self.btn_clientes["command"] = partial(self.abrir_frames_politicas_,self.btn_clientes, clt['name'], self.buttons_clientes)
                
                self.btn_clientes.place(
                    relx=0.5,
                    rely=0.5,
                    anchor=tk.CENTER,
                    height=hg_btn,
                    width=wd_btn
                )

                self.btn_clientes.bind("<Button-5>", self._On_canvas_down)
                self.btn_clientes.bind("<Button-4>", self._On_canvas_up)
                self.buttons_clientes.bind("<Button-5>", self._On_canvas_down)
                self.buttons_clientes.bind("<Button-4>", self._On_canvas_up)
                self.btn_clientes.bind("<Button-1>", partial(self.on_enter, self.btn_clientes, self.buttons_clientes))

 # ********************************************************
#TODO ----------- LABEL FRAME POLITICA -------------------
        self.lb_frame_sistemas = ttk.LabelFrame(
            self.frame_medio,
            text='POLICY',
            relief='groove'
        )
        self.lb_frame_sistemas.pack(
            side='left',
            fill=tk.BOTH,
            expand=0,
            padx=5,
            pady=10
        )
#TODO ----------------------------------------------------
#------------------------------------------------------
# TODO -------------- LABEL FRAME SCRIPTS -------------
        self.lb_frame_scripts = ttk.LabelFrame(
            self.frame_medio,
            text="SCRIPTS",
            relief='groove'
            )
        self.lb_frame_scripts.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=1,
            padx=(0,5),
            pady=10
        )
#TODO -------------------------------------------------
#-----------------------------------------------------
# TODO ------------- FRAME PIE ----------------------
        self.frame_pie = tk.Frame(
            self,
            height=70
        )
        self.frame_pie.pack(
            fill='both',
            padx=5,
            pady=5,
            expand=0
        )
        self.frame_pie.config(
            background=colour_fr_pie,
            borderwidth=2,
            highlightbackground=color_bd_fr,
            highlightthickness=hhtk
        )

# TODO ------------- BOTON CERRAR, FRAME PIE
        global btn_cerrar
        btn_cerrar = tk.Button(
            self.frame_pie,
            image=self.close_icon,
        )
        btn_cerrar.pack(
            side=tk.RIGHT,
            padx=20,
            pady=5
        )
        btn_cerrar.config(
            background=colour_fr_pie,
            activebackground=colour_fr_pie,
            borderwidth=0,
            highlightbackground=colour_fr_pie
        )

    def _On_canvas_down(self, event):
        #list_event = event.widget
        PST_AUT.canvas.yview_scroll(1, "units")

    def _On_canvas_up(self, event):
        #list_event = event.widget
        PST_AUT.canvas.yview_scroll(-1, "units")

    def abrir_frames_politicas_(self, btn, cliente, canvas):
        global PST_AUT
        global framescript
        self.btn_activo  = canvas
        self.fr_cv_clientes = []
        self.fr_cv_clientes.append(canvas)
        btn.focus_set()

        ## Al hacer click se cambiar de color.
        if btn:
            # #* aqui si quieres poner fondo al boton
            btn.configure(
                #bg=cl_btn_actbg,
                fg=default_boton_acfg
            )

            # #* aqui si quieres poner fondo al canvas
            for rb in self.fr_cv_clientes:
                rb.canvas.itemconfig(1, fill=default_boton_bg, outline=default_boton_acfg)

        self.lb_frame_sistemas.pack_forget()
        self.lb_frame_scripts.pack_forget()
        if type(self.fr_clt) == str:
            framescript = ""
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
        else:
            self.fr_clt.borrar()
            if type(framescript) is not str:
                self.fr_clt.framescript.borrar_script()
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
            framescript = ""
        
    def on_enter(self, btn, btn_rb, *arg):
        global PST_AUT
        PST_AUT.bfr_rb_list.append(btn_rb)
        PST_AUT.btn_lis_cli.append(btn)
        for i in PST_AUT.btn_lis_cli:
            i['background']=default_boton_bg
            i['foreground']=default_boton_fg

        for rb in PST_AUT.bfr_rb_list:
            rb.canvas.itemconfig(1, fill=default_boton_bg, outline=default_outline)
    
    



