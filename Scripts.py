# -*- coding: utf-8 -*-
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from getpass import getuser
import subprocess
from jsonpath_ng.ext import parse
from functools import partial
from ScrollableNotebook  import *
from Compliance import fondo_app, _Font_Boton

#* variable para actualizar la ventana
PST_AUT = ""
FR_POL = ""
fr_clt = False
framescript = ""
#* PATH
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
path_config = mypath+"Compliance/.conf/{}.json"

# * COLORES INICIALES
# ? -------------------------------------------------------------
color_bd_fr = '#383838'
colour_fr_pie = '#C65D7B'
colour_fr_tittle = '#F68989'
cl_btn_actbg = '#8FBDD3'
cl_btn_actfg = '#A97155'
cl_btn_bg = '#F4FCD9'
cl_btn_fg = '#534340'
# ? -------------------------------------------------------------
class FramesPoliticas(ttk.Frame):
    def __init__(self, parent, cliente, frame, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        global PST_AUT
        global FR_POL
        self.btn_lis_pol = []
        self.frame = frame
        FR_POL = self.frame
        self.cliente = cliente
        self.bind_all("<Motion>", self.FR_POL_motion)
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
            background=fondo_app,
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
            text='POLICY : {}'.format(cliente)
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
        url = path_icon+"{}".format("icon_sys.png")
        self.gopolitica_ico = ImageTk.PhotoImage(
            Image.open(url).resize((20, 20)))
        with open('/home/esy9d7l1/Compliance/.conf/clientes.json') as op:
            data = json.load(op)
            for clt in data[cliente]:
                for pol in clt['politica']:
                    for sis_pol in pol:
                        self.botones_politica = BtnScripts(
                            self.lb_frame_politica,
                            text=sis_pol,
                            compound='left',
                            image=self.gopolitica_ico,
                        )
                        self.botones_politica.pack(
                            expand=0,
                            padx=15,
                            pady=10,
                            ipady=15,
                            fill='both',
                        )
                        self.botones_politica["command"] = partial(self.abrir_frames_scripts_,self.botones_politica, self.cliente, sis_pol, self.frame)
                        
                        self.botones_politica.bind("<Button-5>", self.OnVsb_down)
                        self.botones_politica.bind("<Button-4>", self.OnVsb_up)
                        self.botones_politica.bind("<Button-1>", partial(self.on_enter, self.botones_politica))

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
    
    def abrir_frames_scripts_(self, btn, cliente, politica, frame):
        global framescript
        btn.focus_set()
        self.frame = frame
        politica = politica
        if btn:
            btn.configure(
                bg=cl_btn_actbg,
                fg=cl_btn_actfg
            )
        if type(framescript) == str:
            self.framescript = FramesScripts(self, cliente, frame, politica)
            framescript =  self.framescript
            print("\n(1) FRAME __{}__\n".format(self.framescript))
        else:
            self.framescript.borrar_script()
            self.framescript = FramesScripts(self, cliente, self.frame, politica)
            print("(2) FRAME __{}__\n".format(self.framescript))

    def OnVsb_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def OnVsb_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def on_enter(self, btn, *arg):
        self.btn_lis_pol.append(btn)

        for i in self.btn_lis_pol:
            i['background']=cl_btn_bg
            i['foreground']=cl_btn_fg
        if btn.focus_set:
            btn['background']=cl_btn_actbg
            btn['foreground']=cl_btn_actfg
    
    def on_leave(self, e):
        widget = e.widget
        widget['background']=cl_btn_bg
        widget['foreground']=cl_btn_fg

class FramesScripts(ttk.Frame):
    def __init__(self, parent, cliente, frame, politica, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        global PST_AUT
        self.frame = frame
        self.cliente = cliente
        self.politica = politica
        global framescript
        print("\n** FRAME QUE LLEGA ** :: ", framescript)
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
            background=fondo_app,
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
            text='{} - SCRIPTS - {}'.format(cliente, politica),
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

        with open('/home/esy9d7l1/Compliance/.conf/clientes.json') as op:
            data = json.load(op)
            for elemt in data[self.cliente]:
                for pol in list(elemt['politica']):
                    for k, v in pol.items():
                        if self.politica == k:
                            for i in v:
                                self.btn_scr = BtnScripts(
                                    self.lb_frame_script,
                                    text=i,
                                    width=10,
                                    height=4,
                                )
        grid_by_column(self.lb_frame_script, 4)

        self.canvas3.bind("<Button-5>", self.OnVsb_down)
        self.canvas3.bind("<Button-4>", self.OnVsb_up)
        self.lb_frame_script.bind("<Button-5>", self.OnVsb_up)
        self.lb_frame_script.bind("<Button-4>", self.OnVsb_down)

    def añadir_btn_scrips(self):
        self.btn_scr = BtnScripts(
            self.lb_frame_script,
            text="sudo_preg4",
            width=10,
            height=4,
        #command=self.src_sudo
        )
        self.btn_scr.grid(row=0, column=0, padx=10, pady=10)

    def icons_and_scripts(self, politica, data):
        busca_scripts = parse(f"{politica}..scripts")
        scripts = [e.value for e in busca_scripts.find(data)]
        return scripts

    def borrar_script(self):
        print(" si BORRA FRAME SCRIPTS SELF ***--{}--***".format(framescript))
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

class BtnScripts(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)

        BtnScripts.configure(self,
            background=cl_btn_bg,
            foreground=cl_btn_fg,
            font=_Font_Boton,
            relief='ridge',
            activeforeground=cl_btn_actbg,
            activebackground=cl_btn_actfg,
            border=2,
            highlightthickness=2,
            highlightbackground=fondo_app
        )

class Automatizar(ttk.Frame):
    def __init__(self, parent, app, application=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        global PST_AUT
        self.btn_lis_cli = []
        self.click = True
        self.cont = 0
        PST_AUT = self
        self.iconos()
        self.frames()

        self.bind("<Motion>", lambda x: self.AUT_motion(x))
    
    def AUT_motion(self, event):
        global PST_AUT
        PST_AUT = event.widget
        #print(PST_AUT)
    
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
            highlightthickness=2
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
            background=fondo_app,
            borderwidth=2,
            highlightbackground=color_bd_fr,
            highlightthickness=2
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
            background=fondo_app,
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

# # * ----------- BOTOTNES DE CLIENTES ------------
        with open(path_config.format("clientes")) as op:
            data = json.load(op)
            for clt in data:
                self.buttons_clientes = BtnScripts(
                    self.lb_frame_menu,
                    text=clt,
                    compound='left',                    
                    image=self.goclient_ico,
                )
                
                self.buttons_clientes["command"] = partial(self.abrir_frames_politicas_,self.buttons_clientes, clt)

                self.buttons_clientes.pack(
                    expand=0,
                    padx=15,
                    pady=10,
                    ipady=15,
                    fill='both',
                )
                #self.buttons_clientes.bind("<Button-1>", self._OnVsb_down)
                self.buttons_clientes.bind("<Button-5>", self._On_canvas_down)
                self.buttons_clientes.bind("<Button-4>", self._On_canvas_up)
                self.buttons_clientes.bind("<Button-1>", partial(self.on_enter, self.buttons_clientes))
                #self.buttons_clientes.bind("<FocusOut>", self.buttons_clientes.on_leave)
# ********************************************************
#TODO ----------- LABEL FRAME POLITICA -------------------
        self.lb_frame_sistemas = ttk.LabelFrame(
            self.frame_medio,
            text='POLICY',
            width=400
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
            )
        self.lb_frame_scripts.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=1,
            padx=(0,5),
            pady=10
        )
        # self.lb_frame_scripts.config(
        #     borderwidth=3,
        # )
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
            highlightthickness=2
        )
# TODO ------------- BOTON CERRAR, FRAME PIE
        self.btn_cerrar = tk.Button(
            self.frame_pie,
            image=self.close_icon,
        )
        self.btn_cerrar.pack(
            side=tk.RIGHT,
            padx=20,
            pady=5
        )
        self.btn_cerrar.config(
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

    def abrir_frames_politicas_(self, btn, cliente):
        global PST_AUT
        global framescript
        btn.focus_set()

        if btn:
            btn.configure(
                bg=cl_btn_actbg,
                fg=cl_btn_actfg
            )
        self.lb_frame_sistemas.pack_forget()
        self.lb_frame_scripts.pack_forget()
        #framescript = ""
        if type(self.fr_clt) == str:
            print("1")
            framescript = ""
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
        else:
            print("2")
            self.fr_clt.borrar()
            if type(framescript) is not str:
                print("DISTINTO")
                self.fr_clt.framescript.borrar_script()
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
            framescript = ""

    def on_enter(self, btn, *arg):
        global PST_AUT
        self.btn_lis_cli.append(btn)
        for i in self.btn_lis_cli:

            i['background']=cl_btn_bg
            i['foreground']=cl_btn_fg

        if btn.focus_set:
            btn['background']=cl_btn_actbg
            btn['foreground']=cl_btn_actfg
