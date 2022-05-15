#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Jose Alvaro Cedeño 2022
# For license see LICENSE
import csv
import os
from tkinter import *
from tkinter import filedialog
from pathlib import Path
import tkinter as tk

filename_r = ""
hostname = ""
path = os.path.expanduser("~/Descargas/")

def menu():
    print("\n1. ABRIR FICHERO SFIT CSV\n")
    print("2. GENERAR FICHERO DECORADO SFIT\n")
    print("\t3. SALIR\n")

def open_file():
    global filename_r
    global hostname
    root = Tk()
    root.withdraw()
    filename_r = filedialog.askopenfilename(
        initialdir="~/Descargas/",
        title='Seleccionar archivo CSV',
        filetypes=(("CSV File", "*.CSV"),)
    )
    if len(filename_r) > 0:
        hostname = Path(filename_r).stem
        print("\033[0;32m"+"\nFICHERO ABIERTO : ", filename_r + "\033[0m")

def decorar_csv():
    if len(filename_r) > 0:
        file_result = path+'{}.txt'.format(hostname)
        guardado = open(file_result, 'w')
        with open(filename_r) as file:
            data = csv.reader(file, delimiter=',')
            for linea in data:
                if linea[2] == 'WARNING' or linea[2] == 'ERROR': 
                    server = linea[0]
                    MESSAGE_SEVERITY = "MESSAGE SEVERITY : "+linea[2]
                    ENTRY = "ENTRY : "+linea[3]
                    LINE_NUMBER = "LINE NUMBER : "+linea[4]
                    VALUE = "VALUE : "+linea[5]
                    DESCRIPTION = "DESCRIPTION : "+linea[6]
                    FILE = "FILE : "+linea[8]                    
                    guardado.write("+-----------------------------------------------------------+\n")
                    guardado.write(MESSAGE_SEVERITY+"\n")
                    guardado.write(ENTRY+"\n")
                    guardado.write(LINE_NUMBER+"\n")
                    guardado.write(VALUE+"\n")
                    guardado.write(DESCRIPTION+"\n")
                    guardado.write(FILE+"\n")
                    guardado.write("+-----------------------------------------------------------+\n\n")
        print("")
        print("\033[0;32m"+"FICHERO GUARDADO CORRECTAMENTE {}.txt, para el SERVER [{}]".format(hostname, server)+"\033[0m")
        guardado.close()
    else:
        print("")
        print("\033[0;31m"+"\nError no as selecionado ningun archivo CSV\n"+"\033[0m")
os.system('clear')
while True:
    menu()
    elecion = input('Elegir una opcion >> : ')
    if elecion == "1":
        os.system('clear')
        open_file()
    elif elecion == "2":
        os.system('clear')
        decorar_csv()
    elif elecion == "3":
        print("")
        print("\033[1;31m"+"ADIOS"+"\033[0m")
        print("")
        break
    else:
        print("")
        input("\033[0;33m"+"No as indicado ninguna opcion correcta...\n\npulsa una tecla para continuar...  "+"\033[0m")
        os.system('clear')