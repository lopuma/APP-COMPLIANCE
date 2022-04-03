# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from getpass import getuser
import subprocess

user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
frame_inicial = ""
fr_clt = ""
list_client = [
    "AFB",
    "ASISA",
    "CESCE",
    "CTTI",
    "ENEL",
    "EUROFRED",
    "FT",
    "INFRA",
    "LBK",
    "PLANETA",
    "SERVIHABITAT"
    ]
#TODO --- Clase FRAMES ---------------------------------
class FramesPoliticas(tk.Frame):
    def __init__(self, parent, cliente, frame):
        super().__init__(parent)
        self.fontFrame = font.Font(font=("Comfortaa", 15, "bold"))
        self.cliente = parent

        self.canvvas=Canvas(
            frame,
            background='#F6E7D8',
        )
        
        self.h=Scrollbar(
            frame,
            orient='vertical',
            command=self.canvvas.yview
        )

        self._pr_ = LabelFrame(
            self.canvvas,
            text='Sistemas {}'.format(cliente),
            width=250,
            font=self.fontFrame
        )

        self._pr_.bind("<Configure>", lambda e:self.canvvas.configure(scrollregion=self.canvvas.bbox("all")))

        self.canvvas.create_window((0,0), window=self._pr_, anchor="nw")

        self.canvvas.config(yscrollcommand=self.h.set)

        self.canvvas.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
            padx=5,
        )
        
        self.h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(15,0)
        )

        self._pr_.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
            pady=5
        )

        self._pr_.config(
            background='#F6E7D8',
            borderwidth=3,
            foreground="#874356",
            width=250
        ) 

        # * ----------- BOTOTNES DE POLITICAS ------------
        self.btn_os=BtnCliente(self._pr_,
        text="SISTEMAS",
        command=lambda e="SISTEMAS": self.abrir_frames_politicas_(e)
        ).pack()

        self.btn_ssh=BtnCliente(self._pr_,
        text="SSH",
        command=lambda e="SSH": self.abrir_frames_politicas_(e)
        ).pack()

        self.btn_sudo=BtnCliente(self._pr_,
        text="SUDO",
        command=lambda e="SUDO": self.abrir_frames_politicas_(e)
        ).pack()
# ************************************************
    
    def borrar(self):
        self.canvvas.destroy()
        self.canvvas.pack_forget()
        self.h.destroy()
        self.h.pack_forget()
        self._pr_.pack_forget()
        self._pr_.destroy()
        print("frame borrado")
    
    def abrir_frames_politicas_(self, event):
        print(event)
#TODO --- Clase BUTTON ---------------------------------
class BtnCliente(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)

        BtnCliente.pack_configure(self,
        expand=1,
        padx=15,
        pady=10,
        ipadx=26,
        ipady=10,
        fill='both',
        )

        BtnCliente.config(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Comfortaa', 13, font.BOLD),
            relief='raised',
            activebackground="#C5D8A4",
            activeforeground="#534340",
            borderwidth=2,
        )

class BtnScriptsClientes(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)

        # BtnCliente.pack_configure(self,
        # expand=1,
        # padx=15,
        # pady=10,
        # ipadx=26,
        # ipady=10,
        # fill='both',
        # )

        BtnCliente.config(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Comfortaa', 13, font.BOLD),
            relief='raised',
            activebackground="#C5D8A4",
            activeforeground="#534340",
            borderwidth=2,
        )
#TODO --- Clase SCRIPTS ---------------------------------
class Scripts(ttk.Frame):
    def __init__(self, parent, app, application=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.click = True
        self.cont = 0
        self.iconos()
        self.frames()

    def iconos(self):
        self.close_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"close1.png").resize((60, 50)))
        self.ctti_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"ctti.png").resize((30, 30)))

        # self.g1_icon = Image.open(file=path_icon+r"g1.gif")
        # self.g1_icon = self.g1_icon.rezise((30,30))
        self.g1_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"g1.gif").resize((30, 30)))

    def src_sudo(self):
        tittle = "{} SCRIPT de {}".format(("AFB"), ("SUDO"))
        password = "Qk6vzwZM8!wAohw"
        file = '/home/esy9d7l1/Compliance/./remoteexec.sh '+password
        subprocess.Popen(["gnome-terminal", "-e", file, "-t",
                         tittle, "--geometry", '200x30'])

    def frames(self):
# TODO ---------- FRAME ARRIBA --------------
        self.frame_titulo = Frame(
            self,
            height=90
        )
        self.frame_titulo.pack(
            fill='both',
            padx=5,
            pady=5,
            expand=0
        )
        self.frame_titulo.config(
            background='#F68989',
            borderwidth=5,
            highlightbackground='black',
            highlightthickness=2
        )
        # fuente de los titulos de los LABEL FRAMES
        self.fontFrame = font.Font(font=("Comfortaa", 15, "bold"))

#TODO -------------- FRAME MEDIO-----------------------------
        self.frame_medio = Frame(
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
        self.fr_md1 = Frame(
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
        )          
# ------------------------------------------------------------------
#? ----------- CREAR  CANVAS PARA AÑADIR BOTONES Y SER SCROLLABLE
        self.canvvas=Canvas(
            self.fr_md1,
            background='#F6E7D8',
            width=255,
            #height=400
        )
        
        h=Scrollbar(
            self.fr_md1,
            orient='vertical',
            command=self.canvvas.yview
        )

        self.lb_frame_menu =  LabelFrame(
            self.canvvas,
            text='Clientes',
            font=self.fontFrame,
            width=20
        )
        
        self.lb_frame_menu.bind("<Configure>", lambda e:self.canvvas.configure(scrollregion=self.canvvas.bbox("all")))

        self.canvvas.create_window((0,0), window=self.lb_frame_menu, anchor="nw")
        
        self.canvvas.config(yscrollcommand=h.set)

        self.canvvas.pack(
            fill=tk.BOTH,
            side='left',
            expand=0,
            padx=5,
        )
        
        h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(15,0)
        )

        self.lb_frame_menu.config(
            background='#F6E7D8',
            borderwidth=3,
            foreground="#874356"
        )

        self.canvvas.bind_all("<Button-5>", self._OnVsb_down)
        self.canvvas.bind_all("<Button-4>", self._OnVsb_up)

# * ----------- BOTOTNES DE CLIENTES ------------

        self.btn_afb = BtnCliente(self.lb_frame_menu,
        text="AFB",
        command=lambda e="AFB":self.abrir_frames_politicas_(e)
        )
        self.btn_afb.pack()

        self.btn_asisa = BtnCliente(self.lb_frame_menu,
        text="ASISA",
        command=lambda e="ASISA":self.abrir_frames_politicas_(e)
        )
        self.btn_asisa.pack()

        self.btn_cesce = BtnCliente(self.lb_frame_menu,
        text="CESCE",
        command=lambda e="CESCE":self.abrir_frames_politicas_(e)
        )
        self.btn_cesce.pack()

        self.btn_ctti = BtnCliente(self.lb_frame_menu,
        text="CTTI",
        #image=self.ctti_icon,
        #compound='top',
        command=lambda e="CTTI":self.abrir_frames_politicas_(e)
        )
        self.btn_ctti.pack()

        self.btn_enel = BtnCliente(self.lb_frame_menu,
        text="ENEL",
        command=lambda e="ENEL":self.abrir_frames_politicas_(e)
        )
        self.btn_enel.pack()

        self.btn_eurofred = BtnCliente(self.lb_frame_menu,
        text="EUROFRED",
        command=lambda e="EUROFRED":self.abrir_frames_politicas_(e)
        )
        self.btn_eurofred.pack()

        self.btn_ft = BtnCliente(self.lb_frame_menu,
        text="FT",
        command=lambda e="FT":self.abrir_frames_politicas_(e)
        )
        self.btn_ft.pack()

        self.btn_infra = BtnCliente(self.lb_frame_menu,
        text="INFRA",
        command=lambda e="INFRA":self.abrir_frames_politicas_(e)
        )
        self.btn_infra.pack()

        self.btn_lbk = BtnCliente(self.lb_frame_menu,
        text="LBK",
        command=lambda e="LBK":self.abrir_frames_politicas_(e)
        )
        self.btn_lbk.pack()

        self.btn_planeta = BtnCliente(self.lb_frame_menu,
        text="PLANETA",
        command=lambda e="PLANETA":self.abrir_frames_politicas_(e)
        )
        self.btn_planeta.pack()

        self.btn_servihabitat = BtnCliente(self.lb_frame_menu,
        text="SERVIHABITAT",
        command=lambda e="SERVIHABITAT":self.abrir_frames_politicas_(e)
        )
        self.btn_servihabitat.pack()
# ********************************************************
#TODO ----------- LABEL FRAME POLITICA -------------------
        self.lb_frame_sistemas=LabelFrame(
            self.frame_medio,
            text='Sistemas',
            width=250,
            font=self.fontFrame
            )
        self.lb_frame_sistemas.pack(
            side='left',
            fill=tk.BOTH,
            expand=0,
            pady=5,
        )
        self.lb_frame_sistemas.config(
            background='#F6E7D8',
            borderwidth=3,
            foreground="#874356"
        )
#TODO ----------------------------------------------------
#------------------------------------------------------
# TODO -------------- LABEL FRAME SCRIPTS -------------
        self.lb_frame_scripts=LabelFrame(
            self.frame_medio,
            text="Scripts",
            font=self.fontFrame,
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
# * ----------- BOTOTNES DE SCRIPS ------------
        self.btn_sudoPREG4=BtnScriptsClientes(self.lb_frame_scripts,
        text="sudo_preg4",
        width=10,
        height=4,
        command=self.src_sudo
        )
        self.btn_sudoPREG4.grid(row=0, column=0)

        self.btn_sudoPREG5=BtnScriptsClientes(self.lb_frame_scripts,
        text="sudo_preg4",
        width=10,
        height=4,
        command=self.src_sudo
        )
        self.btn_sudoPREG5.grid(row=0, column=1)

        self.btn_sudoPREG6=BtnScriptsClientes(self.lb_frame_scripts,
        text="sudo_preg4",
        width=10,
        height=4,
        command=self.src_sudo
        )
        self.btn_sudoPREG6.grid(row=0, column=2)
        

# ************************************************
#TODO -------------------------------------------------
#-----------------------------------------------------
# TODO ------------- FRAME PIE ----------------------
        self.frame_pie=Frame(
            self,
            height=60
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
        self.btn_cerrar=Button(
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
# TODO ------------------------------------------------------------
#-----------------------------------------------------
## --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_down(self, event):
        #list_event = event.widget
        self.canvvas.yview_scroll(1, "units")
        print("que hace 1")

## --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_up(self, event):
        #list_event = event.widget
        self.canvvas.yview_scroll(-1, "units")
        print("que hace 2")

    def abrir_frames_politicas_(self, cliente):
        global fr_clt
        global frame_inicial
        self.lb_frame_sistemas.pack_forget()
        if type(frame_inicial) == str:
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
            frame_inicial = self.fr_clt
        else:
            self.fr_clt.borrar()
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
            frame_inicial = self.fr_clt
                
