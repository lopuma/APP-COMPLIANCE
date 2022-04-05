# -*- coding: utf-8 -*-
from heapq import heapify
import os
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from getpass import getuser
import subprocess

PST_AUT = ""
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
path_config = mypath+"Compliance/.conf/{}.json"

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
    def __init__(self, parent, cliente, frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))
        global PST_AUT
        self.frame = frame
        cliente = cliente
        self.fr_md2 = Frame(
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

        self.canvas=Canvas(
            self.fr_md2,
            background='#F6E7D8',
            width=400,
            borderwidth=0,
            border=0,
            highlightthickness=0
        )
        
        self.h=Scrollbar(
            self.fr_md2,
            orient='vertical',
            command=self.canvas.yview
        )

        self.lb_frame_politica = LabelFrame(
            self.canvas,
            text='Sistemas {}'.format(cliente),
            font=self.font_LabelFrame
        )

        self.lb_frame_politica.bind("<Configure>", lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #self._frame_id = self.canvas.create_window((0,0), window=self.lb_frame_politica, anchor="nw")
        self.canvas.create_window((0,0), window=self.lb_frame_politica, anchor="nw", width=400, height=675)

        self.canvas.config(yscrollcommand=self.h.set)
#
        self.canvas.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=0,
            padx=5,
        )

        #self.canvas.bind("<Configure>", self.resize_frame)

        self.h.pack(
            side=tk.RIGHT, 
            fill=tk.Y,
            pady=(15,0)
        )

        # self.lb_frame_politica.pack(
        #     fill=tk.BOTH,
        #     side='left',
        #     expand=0,
        #     pady=5
        # )

        self.lb_frame_politica.config(
            background='#F6E7D8',
            borderwidth=1,
            foreground="#874356",
            highlightthickness=0,
            #width=400,
            #height=500
        )

        self.canvas.bind("<Button-5>", self.OnVsb_down)
        self.canvas.bind("<Button-4>", self.OnVsb_up)
        self.lb_frame_politica.bind("<Button-5>", self.OnVsb_down)
        self.lb_frame_politica.bind("<Button-4>", self.OnVsb_up)

        # * ----------- BOTOTNES DE POLITICAS ------------
        with open(path_config.format("clientes")) as op:
            data = json.load(op)
            i = 0
            for clt in data[cliente]:
                print("cliente {}, politicas {}".format(cliente,clt['politica']))
                for pol in clt['politica']:
                    print("politica, en linea : ", pol['icon'])
                    # for sis_pol in pol:
                    #     print("Sis : ", sis_pol)
                    #     for politica in pol[sis_pol]:
                    #         lista = list(politica.keys())
                    #         print("---POLITICA--- ", lista[0])
                    #         for pp in lista:
                    #             print("---", pp)
                        
                        
                        
                    #     self.botones_politica = BtnCliente(
                    #         self.lb_frame_politica,
                    #         text=sis_pol,
                    #         command=lambda e=sis_pol: self.abrir_frames_politicas_(e)
                    #     )
                    #     self.botones_politica.pack(ipady=20)
                    #     #self.botones_politica.configure(font=('Open Sans', 15))
                    #     self.botones_politica.bind("<Button-5>", self.OnVsb_down)
                    #     self.botones_politica.bind("<Button-4>", self.OnVsb_up)
        # ************************************************
    def resize_frame(self, e):
        self.canvas.itemconfigure(self._frame_id, height=e.height, width=e.width)

    def borrar(self):
        self.canvas.destroy()
        self.canvas.pack_forget()
        self.h.destroy()
        self.h.pack_forget()
        self.lb_frame_politica.pack_forget()
        self.lb_frame_politica.destroy()
        self.fr_md2.pack_forget()
        self.fr_md2.destroy()
        print("frame borrado")
    
    def abrir_frames_politicas_(self, event):
        print(event)
    
    def OnVsb_down(self, event):
        #list_event = event.widget
        print("mas 1")
        self.canvas.yview_scroll(1, "units")

## --- FUNCIONES PARA SCROLLBAR
    def OnVsb_up(self, event):
        #list_event = event.widget
        print("menos 1")
        self.canvas.yview_scroll(-1, "units")

#TODO --- Clase BUTTON ---------------------------------
class BtnCliente(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))

        BtnCliente.pack_configure(self,
        expand=0,
        padx=15,
        pady=10,
        # ipadx=26,
        ipady=15,
        fill='both',
        )

        BtnCliente.config(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Open Sans', 13, font.BOLD),
            relief='raised',
            activebackground="#C5D8A4",
            activeforeground="#534340",
            borderwidth=2,
        )

class BtnScriptsClientes(tk.Button):
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

        BtnCliente.config(self,
            background="#F4FCD9",
            foreground="#534340",
            font=('Open sanz', 13, font.BOLD),
            relief='raised',
            activebackground="#C5D8A4",
            activeforeground="#534340",
            borderwidth=2,
        )

#TODO --- Clase SCRIPTS ---------------------------------
class Automatizar(ttk.Frame):
    def __init__(self, parent, app, application=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.font_LabelFrame = font.Font(font=("Open Sanz", 15, "bold"))

        global PST_AUT
        self.click = True
        self.cont = 0
        PST_AUT = self
        self.iconos()
        self.frames()

        self.bind("<Motion>", lambda x: self.AUT_motion(x))
    
    def AUT_motion(self, event):
        global PST_AUT
        PST_AUT = event.widget
    
    def iconos(self):
        self.close_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"close1.png").resize((80, 60)))
        self.ctti_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"ctti.png").resize((30, 30)))
        self.goclient_ico = ImageTk.PhotoImage(
            Image.open(path_icon+r"goclient.png").resize((20, 20)))
        

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
        global PST_AUT

        self.frame_titulo = Frame(
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
            highlightthickness=0,
            border=0
        )
# ------------------------------------------------------------------
# #? ----------- CREAR  CANVAS PARA AÑADIR BOTONES Y SER SCROLLABLE
        self.canvvas=Canvas(
            self.fr_md1,
            background='#F6E7D8',
            width=300,
            borderwidth=0,
            border=0,
            highlightthickness=0
        )

        h=Scrollbar(
            self.fr_md1,
            orient='vertical',
            command=self.canvvas.yview
        )

        self.lb_frame_menu =  LabelFrame(
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
            for clt in data:
                self.buttons_clientes = BtnCliente(
                    self.lb_frame_menu,
                    text=clt,
                    compound='left',                    image=self.goclient_ico,
                    command=lambda e=clt:self.abrir_frames_politicas_(e)
                )
                self.buttons_clientes.pack()
                self.buttons_clientes.bind("<Button-5>", self._OnVsb_down)
                self.buttons_clientes.bind("<Button-4>", self._OnVsb_up)
            

# ********************************************************
#TODO ----------- LABEL FRAME POLITICA -------------------
        self.lb_frame_sistemas=LabelFrame(
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
        self.lb_frame_scripts=LabelFrame(
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
# * ----------- BOTOTNES DE SCRIPS ------------
        self.btn_sudoPREG4=BtnScriptsClientes(self.lb_frame_scripts,
        text="sudo_preg4",
        width=10,
        height=4,
        command=self.src_sudo
        )
        self.btn_sudoPREG4.grid(row=0, column=0, padx=10, pady=10)

        self.btn_sudoPREG5=BtnScriptsClientes(self.lb_frame_scripts,
        text="sudo_preg4",
        width=10,
        height=4,
        command=self.src_sudo
        )
        self.btn_sudoPREG5.grid(row=0, column=1, padx=10, pady=10)

        self.btn_sudoPREG6=BtnScriptsClientes(self.lb_frame_scripts,
        text="sudo_preg4",
        width=10,
        height=4,
        command=self.src_sudo
        )
        self.btn_sudoPREG6.grid(row=0, column=2, padx=10, pady=10)
# ************************************************
#TODO -------------------------------------------------
#-----------------------------------------------------
# TODO ------------- FRAME PIE ----------------------
        self.frame_pie=Frame(
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
    def _OnVsb_down(self, event):
        #list_event = event.widget
        PST_AUT.canvvas.yview_scroll(1, "units")

## --- FUNCIONES PARA SCROLLBAR
    def _OnVsb_up(self, event):
        #list_event = event.widget
        PST_AUT.canvvas.yview_scroll(-1, "units")

    def abrir_frames_politicas_(self, cliente):
        print("{}----{}".format(cliente,self.fr_clt))
        self.lb_frame_sistemas.pack_forget()
        
        if type(self.fr_clt) == str:
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
        else:
            self.fr_clt.borrar()
            self.fr_clt = FramesPoliticas(self, cliente, self.frame_medio)
                
