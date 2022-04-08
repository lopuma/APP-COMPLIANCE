# -*- coding: utf-8 -*-
import os
import json
from pickle import FRAME
import tkinter as tk
from tkinter import ttk
from tkinter import font
from traceback import print_tb
from PIL import Image, ImageTk
from getpass import getuser
import subprocess
from jsonpath_ng.ext import parse
from functools import partial
#* variable para actualizar la ventana
PST_AUT = ""
FR_POL = ""
FR_SCR = ""
fr_pol = False
fr_clt = False
fr_scr = ""
frame_script_Clt = ""
#* Lista de botones
#btn_lis_pol = []
btn_lis_cli = []
btn_lis_scr = []

#* PATH
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
path_config = mypath+"Compliance/.conf/{}.json"

class FramesPoliticas(tk.Frame):
    def __init__(self, parent, cliente, frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))
        global PST_AUT
        global FR_POL
        self.frame = frame
        FR_POL = self.frame
        self.cliente = cliente
        self.btn_lis_pol = []
        print("FRAME SCRIPT SELF : ", self.frame)
        print("FRAME SCRIPT : ", FR_POL)
        self.bind_all("<Motion>", self.FR_POL_motion)
        self.fr_md2 = tk.Frame(
            self.frame,
        )

        self.fr_md2.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
        )

        self.fr_md2.config(
            background='#F6E7D8',
            borderwidth=0,
            highlightthickness=0,
            border=0
        )

        self.canvas = tk.Canvas(
            self.fr_md2,
            background='#F6E7D8',
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

        self.lb_frame_politica = tk.LabelFrame(
            self.canvas,
            text='Sistemas {}'.format(cliente),
            font=self.font_LabelFrame
        )

        self.lb_frame_politica.bind("<Configure>", lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0,0), window=self.lb_frame_politica, anchor="nw", width=400, height=675)

        self.canvas.config(yscrollcommand=self.h.set)
#
        self.canvas.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=0,
            padx=5,
        )

        self.h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(15,0)
        )

        self.lb_frame_politica.config(
            background='#F6E7D8',
            borderwidth=1,
            foreground="#874356",
            highlightthickness=0,
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
                        self.botones_politica = BtnPolitica(
                            self.lb_frame_politica,
                            text=sis_pol,
                            compound='left',
                            image=self.gopolitica_ico,
                        )
                        self.botones_politica.pack(ipady=20)
                        self.botones_politica["command"] = partial(self.abrir_frames_scripts_,self.botones_politica, self.cliente, sis_pol, self.frame)
                        
                        self.botones_politica.bind("<Button-5>", self.OnVsb_down)
                        self.botones_politica.bind("<Button-4>", self.OnVsb_up)
                        self.botones_politica.bind("<FocusIn>", partial(self.botones_politica.on_enter, self.botones_politica))
        # ************************************************
    def FR_POL_motion(self, event):
        global FR_POL
        FR_POL = event.widget
        #print("FRAME :: --->> ", FR_POL)
  
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
        global btn_lis_scr
        global fr_scr
        global frame_script_Clt
        global FR_SCR
        btn.focus_set()
        self.frame = frame
        politica = politica
        btn_lis_scr = []
        if btn:
            btn.configure(
                bg="#8FBDD3",
                fg="#A97155"
            )
        if type(fr_scr) == str:
            print("3 - politica")
            fr_scr = FramesScripts(self, cliente, frame, politica)
            frame_script_Clt = fr_scr
            FR_SCR = frame_script_Clt
            print("fr_scr - 3 :",fr_scr)
            print("frame_script_Clt - 3 :",frame_script_Clt)
        else:
            print("4 - politica")
            self.borrar_frame_script(fr_scr)
            fr_scr = FramesScripts(self, cliente, self.frame, politica)
            frame_script_Clt = fr_scr
            print("fr_scr - 4 :",fr_scr)
            print("frame_script_Clt - 4 :",frame_script_Clt)

    def borrar_frame_script(self, frame_scr):
        print("frame sale error : ", frame_scr)
        frame_scr.borrar_script()
    

## --- FUNCIONES PARA SCROLLBAR
    def OnVsb_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def OnVsb_up(self, event):
        self.canvas.yview_scroll(-1, "units")

class FramesScripts(tk.Frame):
    def __init__(self, parent, cliente, frame, politica, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))
        global PST_AUT
        self.frame = frame
        self.cliente = cliente
        self.politica = politica

        self.fr_md3 = tk.Frame(
            self.frame,
        )

        self.fr_md3.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=1,
        )

        self.fr_md3.config(
            background='#F6E7D8',
            borderwidth=0,
            highlightthickness=0,
            border=0
        )

        self.canvas3 = tk.Canvas(
            self.fr_md3,
            background='#F6E7D8',
            borderwidth=0,
            border=0,
            highlightthickness=0
        )
        
        self.scr3 = tk.Scrollbar(
            self.fr_md3,
            orient='vertical',
            command=self.canvas3.yview
        )

        self.lb_frame_script = tk.LabelFrame(
            self.canvas3,
            text='{} Scripts {}'.format(cliente, politica),
            font=self.font_LabelFrame
        )

        self.lb_frame_script.bind("<Configure>", lambda e:self.canvas3.configure(scrollregion=self.canvas3.bbox("all")))

        self.canvas3.create_window((0,0), window=self.lb_frame_script, anchor="nw")

        self.canvas3.config(yscrollcommand=self.scr3.set)
#
        self.canvas3.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=1,
            padx=5,
        )

        self.scr3.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(15,0)
        )

        self.lb_frame_script.config(
            background='#F6E7D8',
            borderwidth=3,
            foreground="#874356",
            highlightthickness=0,
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
                widget.grid(row=row, column=column, sticky="nw")

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

class BtnCliente(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))
        
        BtnCliente.pack_configure(self,
        expand=0,
        padx=15,
        pady=10,
        ipady=15,
        fill='both',
        )

        BtnCliente.configure(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Open Sans', 13, font.BOLD),
            relief='ridge',
            activeforeground="#8FBDD3",
            activebackground="#A97155",
            border=2,
            highlightthickness=2,
            highlightbackground="#F6E7D8"
        )

    def on_enter(self, btn, *arg):
        global btn_lis_cli
        global PST_AUT
        btn_lis_cli.append(btn)
        print("\nBTN ---", btn, "---\n")
        print("\nLISTA DE BOTONES :", btn_lis_cli, "\n")

        # widget = e.widget
        for i in btn_lis_cli:
            print("QUE AHCE", self)
            print(PST_AUT)

            i['background']="#F4FCD9"
            i['foreground']="#534340"

        if btn.focus_set:
            print("y tuuuuuuuuuuu")
            btn['background']="#8FBDD3"
            btn['foreground']="#A97155"
        else:
            btn_lis_cli = []
            print("tu si o que")
    
    def on_leave(self, e):
        global btn_lis_cli
        btn_lis_cli = []


class BtnPolitica(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))
        self.btn_lis_pol = []
        BtnPolitica.pack_configure(self,
        expand=0,
        padx=15,
        pady=10,
        ipady=15,
        fill='both',
        )

        BtnPolitica.configure(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Open Sans', 13, font.BOLD),
            relief='ridge',
            activeforeground="#8FBDD3",
            activebackground="#A97155",
            border=2,
            highlightthickness=2,
            highlightbackground="#F6E7D8"
        )

    def on_enter(self, btn, *arg):
        #global btn_lis_pol
        self.btn_lis_pol.append(btn)

        for i in self.btn_lis_pol:
            i['background']="#F4FCD9"
            i['foreground']="#534340"
        if btn.focus_set:
            btn['background']="#8FBDD3"
            btn['foreground']="#A97155"
    
    def on_leave(self, e):
        widget = e.widget
        widget['background']="#F4FCD9"
        widget['foreground']="#534340"

class BtnScripts(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))

        # BtnCliente.pack_configure(self,
        # expand=1,
        # padx=15,
        # pady=10,
        # ipadx=26,
        # ipady=10,
        # fill='both',
        # )

        BtnScripts.configure(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Open Sans', 13, font.BOLD),
            relief='ridge',
            activeforeground="#8FBDD3",
            activebackground="#A97155",
            border=2,
            highlightthickness=2,
            highlightbackground="#F6E7D8"
        )

class Automatizar(ttk.Frame):
    def __init__(self, parent, app, application=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))
        #global btn_lis_pol
        global PST_AUT
        self.click = True
        self.cont = 0
        PST_AUT = self
        #btn_lis_cli = []
        self.iconos()
        self.frames()

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
        #global btn_lis_cli
        #btn_lis_cli = []
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
            background='#F68989',
            borderwidth=5,
            highlightbackground='black',
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
            background='#F6E7D8',
            borderwidth=5,
            highlightbackground='black',
            highlightthickness=2
        )
#---------------------------------------------------------------------------------------------
#? ------------- PARTE 1 DE FRAMES MEDIO ------------------------
        self.fr_md1 = tk.Frame(
            self.frame_medio,
        )
        self.fr_md1.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
        )
        self.fr_md1.config(
            background='#F6E7D8',
            borderwidth=0,
            highlightthickness=0,
            border=0
        )
# ------------------------------------------------------------------
# #? ----------- CREAR  CANVAS PARA AÑADIR BOTONES Y SER SCROLLABLE
        self.canvvas = tk.Canvas(
            self.fr_md1,
            background='#F6E7D8',
            width=300,
            borderwidth=0,
            border=0,
            highlightthickness=0
        )
        
        h = tk.Scrollbar(
            self.fr_md1,
            orient='vertical',
            command=self.canvvas.yview
        )
        
        self.lb_frame_menu =  tk.LabelFrame(
            self.canvvas,
            text='Clientes',
            font=self.font_LabelFrame,
        )
        
        self.lb_frame_menu.bind("<Configure>", lambda e:self.canvvas.configure(scrollregion=self.canvvas.bbox("all")))

        self.canvvas.create_window((0,0), window=self.lb_frame_menu, anchor="nw", width=300)
        
        self.canvvas.config(yscrollcommand=h.set)

        self.canvvas.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
        )
        
        h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(15,0)
        )
        
        self.lb_frame_menu.config(
            background='#F6E7D8',
            borderwidth=1,
            highlightthickness=0,
            foreground="#874356",
        )

        self.canvvas.bind("<Button-5>", self._OnVsb_down)
        self.canvvas.bind("<Button-4>", self._OnVsb_up)
        self.lb_frame_menu.bind("<Button-5>", self._OnVsb_down)
        self.lb_frame_menu.bind("<Button-4>", self._OnVsb_up)

# # * ----------- BOTOTNES DE CLIENTES ------------
        with open(path_config.format("clientes")) as op:
            data = json.load(op)
            # global btn_lis_cli
            # btn_lis_cli = []
            # print("AL ABRIR BTN :: ", btn_lis_cli)
            for clt in data:
                self.buttons_clientes = BtnCliente(
                    self.lb_frame_menu,
                    text=clt,
                    compound='left',                    
                    image=self.goclient_ico,
                )
                
                self.buttons_clientes["command"] = partial(self.abrir_frames_politicas_,self.buttons_clientes, clt)

                self.buttons_clientes.pack()
                #self.buttons_clientes.bind("<Button-1>", self._OnVsb_down)
                self.buttons_clientes.bind("<Button-5>", self._OnVsb_down)
                self.buttons_clientes.bind("<Button-4>", self._OnVsb_up)
                self.buttons_clientes.bind("<FocusIn>", partial(self.buttons_clientes.on_enter, self.buttons_clientes))
                #self.buttons_clientes.bind("<FocusOut>", self.buttons_clientes.on_leave)
# ********************************************************
#TODO ----------- LABEL FRAME POLITICA -------------------
        self.lb_frame_sistemas = tk.LabelFrame(
            self.frame_medio,
            text='Sistemas',
            width=400,
            font=self.font_LabelFrame
            )
        self.lb_frame_sistemas.pack(
            side='left',
            fill=tk.BOTH,
            expand=0,
            pady=5,
            padx=5
        )
        self.lb_frame_sistemas.config(
            background='#F6E7D8',
            borderwidth=3,
            foreground="#874356"
        )
#TODO ----------------------------------------------------
#------------------------------------------------------
# TODO -------------- LABEL FRAME SCRIPTS -------------
        self.lb_frame_scripts = tk.LabelFrame(
            self.frame_medio,
            text="Scripts",
            font=self.font_LabelFrame,
            )
        self.lb_frame_scripts.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=1,
            padx=5,
            pady=5,
        )
        self.lb_frame_scripts.config(
            background='#F6E7D8',
            borderwidth=3,
            foreground="#874356"
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
            background='#C65D7B',
            borderwidth=5,
            highlightbackground='black',
            highlightthickness=2
        )
# TODO ------------- BOTON CERRAR, FRAME PIE
        self.btn_cerrar = tk.Button(
            self.frame_pie,
            # text="Cerrar",
            # anchor='center',
            image=self.close_icon,
        )
        self.btn_cerrar.pack(
            side=tk.RIGHT,
            padx=20,
            pady=5
        )
        self.btn_cerrar.config(
            background="#C65D7B",
            # foreground="white",
            activebackground="#C65D7B",
            # font=('Source Sans Pro',12, font.BOLD),
            borderwidth=0,
            highlightbackground="#C65D7B"
        )
#TODO------------------------------------------------------------
#----------------------------------------------------------------
    def _OnVsb_down(self, event):
        #list_event = event.widget
        PST_AUT.canvvas.yview_scroll(1, "units")

## --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_up(self, event):
        #list_event = event.widget
        PST_AUT.canvvas.yview_scroll(-1, "units")

    def abrir_frames_politicas_(self, btn, cliente):
        global PST_AUT
        global fr_pol
        global fr_scr
        #global btn_lis_cli
        btn.focus_set()
        #btn_lis_cli = []
        # print("self : ", self)
        # print("global : ", PST_AUT)

        if btn:
            btn.configure(
                bg="#8FBDD3",
                fg="#A97155"
            )
        self.lb_frame_sistemas.pack_forget()
        self.lb_frame_scripts.pack_forget()
        fr_scr = ""
        if type(self.fr_clt) == str:
            print("1 - cliente")
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
            print("nuevo frame - 1 ", self.fr_clt, "\n")
        else:
            print("2 - cliente")
            self.fr_clt.borrar()
            if type(frame_script_Clt) != str:
                self.fr_clt.borrar_frame_script(frame_script_Clt)
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
            print("nuevo frame - 2 ", self.fr_clt, "\n")
