# -*- coding: utf-8 -*-
# Copyright (c) Jose Alvaro Cedeño 2022
# For license see LICENSE
# Version  3.0
import csv
import os
import sys
from tkinter import filedialog
from pathlib import Path
import tkinter as tk
filename_r = ""
hostname = ""
clear = ""
my_os = sys.platform
home = Path.home()
path = Path(home, "Downloads")
print(my_os)
if(my_os == 'linux'):
    clear = "clear"
else:
    clear = "cls"

def menu():
    print("\n1. ABRIR FICHERO SFIT CSV\n")
    print("2. GENERAR FICHERO DECORADO SFIT\n")
    print("\t3. SALIR\n")

def open_file():
    global filename_r
    global hostname
    root = tk.Tk()
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
        file_result = Path(path, '{}.txt'.format(hostname))
        with open(filename_r, encoding='utf-8') as file:
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
                    with open(file_result, 'a', encoding='utf-8') as gd:
                        
                        gd.write("+-----------------------------------------------------------+\n")
                        gd.write(MESSAGE_SEVERITY+"\n")
                        gd.write(ENTRY+"\n")
                        gd.write(LINE_NUMBER+"\n")
                        gd.write(VALUE+"\n")
                        gd.write(DESCRIPTION+"\n")
                        gd.write(FILE+"\n")
                        gd.write("+-----------------------------------------------------------+\n\n")
        try:
            print("\033[0;32m"+"FICHERO GUARDADO CORRECTAMENTE {}.txt, para el SERVER [{}]".format(hostname, server)+"\033[0m")
        except UnboundLocalError:
            print("")
            print("\033[0;31;43m"+"No existen WARNING or ERROR, en el CSV : [ {} ]".format(hostname)+"\033[0m")
            #os.remove(file_result)
    else:
        print("")
        print("\033[1;31m"+"\nError, no as selecionado ningun archivo CSV\n"+"\033[0m")
os.system(clear)
while True:
    menu()
    elecion = input('Elegir una opcion >> : ')
    if elecion == "1":
        os.system(clear)
        open_file()
    elif elecion == "2":
        os.system(clear)
        decorar_csv()
    elif elecion == "3":
        print("")
        print("\033[1;31m"+"ADIOS"+"\033[0m")
        print("")
        break
    else:
        print("")
        input("\033[0;31m"+"No as indicado ninguna opcion correcta...\n\npulsa una tecla para continuar...  "+"\033[0m")
        os.system(clear)
