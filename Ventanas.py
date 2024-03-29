# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
from PIL import Image, ImageTk
from Compliance import   hlh_def, default_Framework, default_select_fg, default_select_bg, home, parse, pathIcon, pathConfig, pers_scrText_fg, modo_dark, hhtk, default_scrText_bg, default_bottom_app, default_scrText_fg, default_scrText_bg, bg_submenu, default_scrText_fg, fuente_texto, fg_submenu, default_scrText_fg, default_color_titulos, _Font_Texto, default_scrText_fg, default_scrText_bg, default_scrText_fg, default_hglcolor, _Font_Menu, oddrow, evenrow
from DataExtraction import MyEntry
from pathlib import Path
from tkinter import messagebox as mb


fileApariencaIni = str(pathConfig).format("apariencia.ini")

def beep_error(f):
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    return applicator

class Ventana(ttk.Frame):
    def __init__(self, parent, app, name_vtn, customer, path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.customer = customer
        self.app = app
        self.path_ventanas = Path(home,path)
        self.tt_vtn = name_vtn
        self.click = True        

        self.vtn_ventanas = tk.Toplevel(self)
        self.vtn_ventanas.config(
            background=default_bottom_app
        )
        screen_width = self.app.root.winfo_x()
        screen_height= self.app.root.winfo_y()
        position_top = int(screen_height)
        position_right = int(screen_width+150)
        parse.read(fileApariencaIni, encoding="utf-8")
        window_width = parse.get('medidas_ventana', 'width')
        window_height = parse.get('medidas_ventana', 'height')
        self.vtn_ventanas.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_ventanas.resizable(0,0)

        self.vtn_ventanas.title('{} for client {}'.format(self.tt_vtn, self.customer))
        self.vtn_ventanas.tk.call('wm', 'iconphoto', self.vtn_ventanas._w, tk.PhotoImage(file=pathIcon.format(r'ventanas.png')))       
        self.vtn_ventanas.columnconfigure(0, weight=1)
        self.vtn_ventanas.rowconfigure(1, weight=1)
        self.vtn_ventanas.rowconfigure(2, weight=1)

        self.iconos()
        self.WIDGETS_VENTANA()
        self.menu_clickDerecho()
        self.menuList_clickDerecho()
        self.cargar_ventanas(self.customer)
        self.tree.bind("<ButtonRelease-1>", self.selecionar_elemntFile)
        self.tree.bind("<Key>", lambda e: self.app.widgets_SoloLectura(e))
        self.srcRisk.bind("<Key>", lambda e: self.app.widgets_SoloLectura(e))
        self.srcImpact.bind("<Key>", lambda e: self.app.widgets_SoloLectura(e))
        self.srcVariable.bind("<Key>", lambda e: self.app.widgets_SoloLectura(e))
        self.cbxUser.bind("<Key>", lambda e: self.app.widgets_SoloLectura(e))
        self.VTN_entry.bind("<Any-KeyRelease>", self.on_entr_str_busca_key_release)
        self.srcImpact.bind("<Button-3>", self.display_menu_clickDerecho)
        self.srcRisk.bind("<Button-3>", self.display_menu_clickDerecho)
        self.srcVariable.bind("<Button-3>", self.display_menu_clickDerecho)
        self.VTN_entry.bind("<Button-3>", self.display_menu_clickDerecho)
        self.listServer.bind("<Button-3>", self.display_menuLis_clickDerecho)
        self.VTN_entry.bind("<Motion>", lambda x :self.act_elemt_text(x))
        self.srcImpact.bind("<Motion>", lambda x :self.act_elemt_src(x))
        self.srcRisk.bind("<Motion>", lambda x :self.act_elemt_src(x))
        self.srcVariable.bind("<Motion>", lambda x :self.act_elemt_src(x))
        self.listServer.bind("<Motion>", lambda x :self.act_elemt_list(x))
        self.VTN_entry.bind("<FocusIn>", lambda e: self.clear_bsq(e))
        self.VTN_entry.bind("<FocusOut>", lambda e: self.clear_bsq(e))    
        self.VTN_entry.bind("<KeyPress>", lambda e: self.clear_bsq_buttom(e))    
        self.VTN_entry.bind("<Control-v>",lambda e:self.sel_text(e))
        self.VTN_entry.bind("<Control-V>",lambda e:self.sel_text(e))
        ## --- Selecionar elemento hacia abajo
        self.tree.bind("<Down>", lambda e:self.TreeDown(e))
        self.tree.bind("<Up>", lambda e:self.TreeUp(e))
        self.VTN_entry.bind("<Control-x>",self.limpiar_bsq2)
        self.VTN_entry.bind("<Control-X>",self.limpiar_bsq2)
        self.VTN_entry.bind("<Control-f>",self._buscar_focus)        
        self.VTN_entry.bind("<Control-F>",self._buscar_focus)              
        self.srcRisk.bind("<Control-a>",lambda e:self._seleccionar_todo(e))
        self.srcImpact.bind("<Control-a>",lambda e:self._seleccionar_todo(e))
        self.srcVariable.bind("<Control-a>",lambda e:self._seleccionar_todo(e))
        self.listServer.bind("<Control-a>",lambda e:self._selALL_optionLis(e))
        self.srcRisk.bind("<Control-A>",lambda e:self._seleccionar_todo(e))
        self.srcImpact.bind("<Control-A>",lambda e:self._seleccionar_todo(e))
        self.srcVariable.bind("<Control-A>",lambda e:self._seleccionar_todo(e))
        self.listServer.bind("<Control-A>",lambda e:self._selALL_optionLis(e))
        self.srcRisk.bind("<Control-f>",self.act_buscar)
        self.srcImpact.bind("<Control-f>",self.act_buscar)
        self.srcVariable.bind("<Control-f>",self.act_buscar)
        self.listServer.bind("<Control-f>",self.act_buscar)
        self.tree.bind("<Control-f>",self.act_buscar)
        self.srcRisk.bind("<Control-F>",self.act_buscar)
        self.srcImpact.bind("<Control-F>",self.act_buscar)
        self.srcVariable.bind("<Control-F>",self.act_buscar)
        self.listServer.bind("<Control-F>",self.act_buscar)
        self.tree.bind("<Control-F>",self.act_buscar)
        self.srcRisk.bind("<Control-C>",self.copiar_env)
        self.srcImpact.bind("<Control-C>",self.copiar_env)
        self.srcVariable.bind("<Control-C>",self.copiar_env)
        self.listServer.bind("<Control-C>",self.copiar_env)
        self.cbxUser.bind("<Control-C>",self.copiar_env)
        
    def iconos(self):
        self.buscar_icon = ImageTk.PhotoImage(
                    Image.open(pathIcon.format(r"buscar.png")).resize((25, 25)))
        self.cerrar_icon = ImageTk.PhotoImage(
                    Image.open(pathIcon.format(r"reduce.png")).resize((25, 25)))
        self.copiar_icon = ImageTk.PhotoImage(
                    Image.open(pathIcon.format(r"copiarALL.png")).resize((20, 20)))
        self.limpiar_icon = ImageTk.PhotoImage(
                    Image.open(pathIcon.format(r"limpiar.png")).resize((25, 25)))
    
    def cerrar_vtn(self):
        self.vtn_ventanas.destroy()
    
    def clear_bsq_buttom(self, event):
        text_widget = event.widget
        entry = self.var_ent_buscar.get()
        long_entry = len(entry)
        if long_entry <=1:
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=tk.W)
            self.cargar_ventanas(self.customer)
            self.limpiar_widgets()
    
    def clear_bsq(self, event):
        text_widget = event.widget
        entry = self.var_ent_buscar.get()
        if entry == "Buscar Directories / File ...":
            parse.read(fileApariencaIni, encoding="utf-8")
            modo_dark = parse.get('dark', 'modo_dark')
            if modo_dark == 'True':
                text_widget.config(
                    foreground=pers_scrText_fg,
                    font=_Font_Texto
                )
            else:
                text_widget.config(
                    foreground=default_scrText_fg,
                    font=_Font_Texto
                )
            self.var_ent_buscar.set("")
            text_widget.icursor(0)
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=tk.W)
        elif entry == "":
            text_widget.config(
                foreground="gray75", 
                font=_Font_Texto
            )
            self.var_ent_buscar.set("Buscar Directories / File ...")
            text_widget.icursor(0)
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=tk.W)
        
    def limpiar_bsq(self):
        #customer = PST_DESV.varClient.get()
        self.var_ent_buscar.set("Buscar Directories / File ...")
        #self.var_ent_buscar.set("")
        self.VTN_entry.focus()
        self.VTN_entry.icursor(0)
        self.btnLimpiar.grid_forget()
        self.btnBuscar.grid(row=0, column=1, sticky=tk.W)
        self.menu_Contextual.entryconfig("  Limpiar", state="disabled")
        self.cargar_ventanas(self.customer)
        self.limpiar_widgets()
    
    def limpiar_bsq2(self, event=None):
        self.var_ent_buscar.set("")
        self.VTN_entry.focus()
        self.VTN_entry.icursor(0)
        self.btnLimpiar.grid_forget()
        self.btnBuscar.grid(row=0, column=1, sticky=tk.W)
        self.menu_Contextual.entryconfig("  Limpiar", state="disabled")
        self.cargar_ventanas()
        self.limpiar_widgets()
    
    def on_entr_str_busca_key_release(self, event):
        VTN_entry_Event = event.widget
        #customer = PST_DESV.varClient.get()
        self._buscar(VTN_entry_Event)
        if len(VTN_entry_Event.get()) == 0:
            self.cargar_ventanas(self.customer)
        return 'break'

    def _buscar(self, event=None):
        VTN_entry_Event = event
        VTN_entry_Event.focus()
        # self._buscar_todo(VTN_entry_Event.get())
        try:
            words = VTN_entry_Event.get().split(' ')
            if (len(words) > 2):
                file = [ n for n in words if "/" in n]
                file = str(file).replace(",","").replace("[","").replace("]","").replace("'","").replace(";","")
                self._buscar_todo(file)
            else:
                self._buscar_todo(VTN_entry_Event.get())
        except:
            pass
        
    def _buscar_todo(self, txt_buscar=None):
        valor_aBuscar = txt_buscar
        if valor_aBuscar == "Buscar Directories / File ...":
            self.cargar_ventanas(self.customer)
            self.limpiar_widgets()
        else:
            valor_Buscado = [n for n in self.ventanas if valor_aBuscar in n]
            if valor_aBuscar:
                self.limpiar_tree()
                with open(self.path_ventanas, encoding='utf-8') as g:
                    data = json.load(g)
                    count = 0
                    for md in sorted(data[self.customer], key=lambda md:md['object']):
                        for vb in valor_Buscado:
                            if vb == md['object']:
                                if count % 2 == 0:
                                    self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                                else:
                                    self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                                count += 1
                self.limpiar_widgets()
                self.btnBuscar.forget()
                self.btnLimpiar.grid(row=0, column=1, sticky=tk.W)
                self.menu_Contextual.entryconfig("  Limpiar", state="normal")
            else:
                pass

    def cargar_ventanas(self, customer):
        #crear una lista vacia
        self.ventanas = []
        #limpiando el arbol de vistas
        self.limpiar_tree()
        #Cargar datos desde el archivo JSON
        with open(self.path_ventanas, encoding='utf-8') as g:
            data = json.load(g)
            count = 0
            try:
                for md in sorted(data[customer], key=lambda md:md['object']):
                    #guardar solo el valor de 'object a una lista'
                    self.ventanas.append(md['object'])
                    if count % 2 == 0:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                    else:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                    count += 1
            except KeyError:
                mb.showerror("No such file or directory", "No existen datos para {}, del cliente {}".format(self.path_ventanas, customer))

    def limpiar_tree(self):
        records = self.tree.get_children()
        for elemnt in records:
            self.tree.delete(elemnt)
    
    def selecionar_elemntFile(self, event):
        tree_event = event.widget
        try:
            item_id = tree_event.selection()[0]
            #item_id = tree_event.focus()
            index = tree_event.index(item_id)
            if tree_event.exists(index):
                dir_selecionado = tree_event.item(index, 'values')
                dir = dir_selecionado[0]
                self.cargar_elemt_seleccionado(dir)
        except:
            pass
    
    def cargar_elemt_seleccionado(self, dir):
        with open(self.path_ventanas, encoding='utf-8') as g:
                data = json.load(g)
                for md in data[self.customer]:
                    if dir == md['object']:
                        #limpiar------------------------------------                      
                        self.limpiar_widgets()
                        #-------------------------------------------
                        self.listServer.insert(tk.END,*md['servers'])
                        self.srcRisk.insert(tk.END,md['risk'])
                        self.srcImpact.insert(tk.END,md['impact'])
                        self.cbxUser['values'] = md["user"]
                        variables = str(md['variable'])
                        variables = variables.replace("[","").replace("]","").replace("'","").replace("\"","'").replace(",",";").replace("+",",").replace("`","\"")
                        if md['code'] == "2-DOC":
                            self.lbl4['text'] = "COMENTARIO"
                            self.lbl2['text'] = "RISK"
                            self.lbl3['text'] = "IMPACT"
                        else:
                            self.lbl2['text'] = "INFORMACION"
                            self.lbl3['text'] = "INFORMACION"
                            self.lbl4['text'] = "VARIABLES"
                        self.srcVariable.insert(tk.END,variables)
                        self.lbl_SO['text'] = "S.O : "+md['SO']
                        user = str(md["user"]).replace("[","").replace("]","").replace("'","")
                        self.cbxUser.set(user)
    
    def limpiar_widgets(self):
        self.lbl_SO['text'] = "SISTEMA OPERATIVO"
        self.listServer.delete(0,tk.END)
        self.srcRisk.delete('1.0',tk.END)
        self.srcImpact.delete('1.0',tk.END)
        self.cbxUser.option_clear()
        self.srcVariable.delete('1.0',tk.END)
    
    ## --- MENU CONTEXTUAL
    def act_elemt_text(self, event):
        event.widget.focus()
        if event.widget:
            self.menu_Contextual.entryconfig("  Buscar", state="disabled")
            self.menu_Contextual.entryconfig("  Pegar", state="normal")
            self.menu_Contextual.entryconfig("  Copiar", state="disabled")
            self.menu_Contextual.entryconfig("  Seleccionar todo", state="disabled")

    def act_elemt_list(self, event):
        event.widget.focus()
    
    def act_elemt_src(self, event):
        event.widget.focus()
        if event.widget:
            self.menu_Contextual.entryconfig("  Buscar", state="normal")
            self.menu_Contextual.entryconfig("  Pegar", state="disabled")
            self.menu_Contextual.entryconfig("  Copiar", state="normal")
            self.menu_Contextual.entryconfig("  Seleccionar todo", state="normal")
            self.menu_Contextual.entryconfig("  Limpiar", state="disabled")
    
    def act_buscar(self, event=None):
        self.VTN_entry.select_range(0,tk.END)
        self.VTN_entry.focus_set()
        return 'break'

    def _buscar_focus(self, event):
        entry_event = event.widget
        entry_event.select_range(0,tk.END)
        entry_event.focus_set()
        return 'break'

    def seleccionar_todo(self):
        self.srcEvent.tag_add("sel","1.0","end")
        return 'break'
    
    def _seleccionar_todo(self, event):
        srcEvent = event.widget
        srcEvent.tag_add("sel","1.0","end")
        return 'break'
    
    def copiar(self):
        seleccion = self.srcEvent.tag_ranges(tk.SEL)
        if seleccion:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(self.srcEvent.get(*seleccion).strip())
            self.srcEvent.tag_remove("sel","1.0","end")
            return 'break'
    
    @beep_error
    def copiar_env(self, event):
        wd_evn = event.widget
        seleccion = wd_evn.tag_ranges(tk.SEL)
        if seleccion:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(wd_evn.get(*seleccion).strip())
            wd_evn.tag_remove("sel","1.0","end")
            return 'break'
    
    def sel_text(self, event):
        if event.widget.select_present():
            self.var_ent_buscar.set("")
    
    def pegar(self):
        if self.srcEvent.select_present():
            self.var_ent_buscar.set("")
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=tk.W)
        self.srcEvent.event_generate("<<Paste>>")
        return 'break'
    
    def menu_clickDerecho(self):
        self.menu_Contextual = tk.Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.act_buscar,
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.copiar,
            state='normal',
        )
        self.menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.pegar,
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.seleccionar_todo,
            state='normal',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.limpiar_bsq2,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background=bg_submenu)
        self.menu_Contextual.add_command(label="  Cerrar pestaña", 
                                #image=self.cerrar_icon,
                                compound=tk.LEFT,
                                background=bg_submenu, foreground=fg_submenu,
                                activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
                                font=_Font_Menu,
                                command=self.cerrar_vtn
                                )
    
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.srcEvent = event.widget
        self.srcEvent.focus()
        if str(self.srcEvent) == str(self.VTN_entry):
            if len(self.VTN_entry.get()) > 0:
                self.menu_Contextual.entryconfig('  Limpiar', state='normal')
            else:
                self.menu_Contextual.entryconfig('  Limpiar', state='disabled')
        else:
            txt_select = event.widget.tag_ranges(tk.SEL)
            if txt_select:
                self.menu_Contextual.entryconfig("  Copiar", state="normal")
            else:
                self.menu_Contextual.entryconfig("  Copiar", state="disabled")
    
    def copiar_optionLis(self, event):
        listbox = event
        index = listbox.curselection()
        listCopiada = []
        for i in index:
            value = listbox.get(i)
            listCopiada.append(value)
        if listCopiada:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(listCopiada)
    
    def selALL_optionLis(self, event):
        listbox = event
        listbox.selection_set(0, tk.END)
    
    def _selALL_optionLis(self, event):
        listbox = event.widget
        listbox.selection_set(0, tk.END)
    
    def menuList_clickDerecho(self):
        self.menuLis_Contextual = tk.Menu(self, tearoff=0)
        ## buscar
        self.menuLis_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.act_buscar,
        )
        self.menuLis_Contextual.add_separator(background=bg_submenu)
        ## Copiar
        self.menuLis_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=lambda e=self.listServer:self.copiar_optionLis(e),
            state='disabled',
        )
        ## Pegar
        self.menuLis_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menuLis_Contextual.add_separator(background=bg_submenu)
        ## Selecionar todo
        self.menuLis_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=lambda e=self.listServer:self.selALL_optionLis(e),
            state='normal',
        )
        ## Limpiar
        self.menuLis_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            state='disabled',
        )
        self.menuLis_Contextual.add_separator(background=bg_submenu)
        ## Cerrar pestñaa
        self.menuLis_Contextual.add_command(
            label="  Cerrar pestaña", 
            #image=self.cerrar_icon,
            compound=tk.LEFT,
            background=bg_submenu, foreground=fg_submenu,
            activebackground=default_scrText_bg,activeforeground=default_scrText_fg,
            font=_Font_Menu,
            command=self.cerrar_vtn
        )
    
    def display_menuLis_clickDerecho(self, event):
        self.menuLis_Contextual.tk_popup(event.x_root, event.y_root)
        self.srcEvent = event.widget
        self.srcEvent.focus()
        index = self.srcEvent.curselection()
        try:
            self.srcEvent.selection_includes(index)
            self.menuLis_Contextual.entryconfig("  Copiar", state="normal")
        except:
            self.menuLis_Contextual.entryconfig("  Copiar", state="disabled")
    
    def TreeDown(self, event):
        tree_event = event.widget
        item_id = tree_event.selection()[0]
        #item_id = tree_event.focus()
        index = tree_event.index(item_id)+1
        if tree_event.exists(index):
            dir_selecionado = tree_event.item(index, 'values')
            dir = dir_selecionado[0]
            self.cargar_elemt_seleccionado(dir)
    
    def TreeUp(self, event):
        tree_event = event.widget
        item_id = tree_event.selection()[0]
        index = tree_event.index(item_id)-1
        if tree_event.exists(index):
            dir_selecionado = tree_event.item(index, 'values')
            dir = dir_selecionado[0]
            self.cargar_elemt_seleccionado(dir)

    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel","1.0","end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                self.app.root.clipboard_clear()
                self.app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel","1.0","end")
    
    def resizable(self, e):
        self.click = False
        if self.click == False:
            self.vtn_ventanas.resizable(1,1)
        
    def _release_callback(self, e):
        global window_width
        global window_height
        self.click = True
        self.vtn_ventanas.resizable(0, 0)
        alto = self.vtn_ventanas.winfo_height()
        ancho = self.vtn_ventanas.winfo_width()
        window_width = ancho
        window_height = alto
        window_width = str(window_width)
        window_height = str(window_height)
        
        parse.set('medidas_ventana', 'width', window_width)
        parse.set('medidas_ventana', 'height', window_height)
        with open(fileApariencaIni, 'w', encoding='utf-8') as configfile:
            parse.write(configfile)

    def WIDGETS_VENTANA(self):
        self.buscador = ttk.Frame(
            self.vtn_ventanas,
        )
        self.buscador.grid(column=0, row=0, sticky='nsew', padx=10, pady=5)

        self.datos = ttk.Frame(
            self.vtn_ventanas,
        )
        self.datos.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

        self.otros_datos = ttk.Frame(
            self.vtn_ventanas,
        )
        self.otros_datos.grid(column=0, row=2, sticky='nsew', padx=10, pady=5)
        
        self.sizegrid = ttk.Sizegrip(
            self.vtn_ventanas,
        )
        self.sizegrid.grid(row=3, column=0, sticky='nsew')
        self.sizegrid.bind(
            '<Button-1>', self.resizable
        )

        self.sizegrid.bind("<ButtonRelease-1>", self._release_callback)

        self.buscador.columnconfigure(0, weight=1)
        self.datos.columnconfigure(0, weight=1)
        self.otros_datos.columnconfigure(0, weight=1)
        self.buscador.rowconfigure(0, weight=1)
        self.datos.rowconfigure(0, weight=1)
        self.otros_datos.rowconfigure(0, weight=1)

        self.var_ent_buscar = tk.StringVar(self)
        self.VTN_entry = MyEntry(
            self.buscador,
            textvariable=self.var_ent_buscar,
        )
        self.var_ent_buscar.set("Buscar Directories / File ...")
        self.VTN_entry.grid(row=0, column=0, ipady=8, padx=10, pady=10, sticky='nsew')

        self.VTN_entry.config(
            foreground="gray75",
            font=(fuente_texto, 14)
        )

        self.btnBuscar = ttk.Button(
            self.buscador,
            text='Buscar',
            image=self.buscar_icon,
            command=lambda:self._buscar(self.VTN_entry)
        )
        self.btnBuscar.grid(row=0, column=1, pady=10, sticky=tk.W)

        self.btnLimpiar = ttk.Button(
            self.buscador,
            text='Limpiar',
            image=self.limpiar_icon,
            command= self.limpiar_bsq,            
        )
        self.btnLimpiar.grid(row=0, column=1, pady=10, sticky=tk.W)

        self.btnCerrar = tk.Button(
            self.buscador,
            text='Cerrar',
            image=self.app.iconoClose,
            command=self.cerrar_vtn
        )
        self.btnCerrar.config(
                background=default_bottom_app,
                highlightcolor=default_hglcolor,
                activebackground=default_bottom_app,
                border=0,
                highlightbackground=default_bottom_app,
            )
        self.btnCerrar.grid(row=0, column=2, padx=10, pady=10, sticky=tk.E)
        
        # ## ====================================================================================
        # ## --- CREAMOS EL PRIMER LABEL FRAME
        self.labelframe1=ttk.LabelFrame(
            self.datos, 
            text="DATOS",
            relief='groove'
        )
        self.labelframe1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        
        #Expandir lo que esta dentro del frame
        self.labelframe1.columnconfigure(0, weight=1)
        self.labelframe1.rowconfigure(0, weight=1)
        
        # ## --- creamos el scrollbar
        self.tree_scrollbar=tk.Scrollbar(self.labelframe1, orient=tk.VERTICAL)
        
        # ## ---creamos el treeview
        self.tree = ttk.Treeview(
            self.labelframe1, 
            yscrollcommand=self.tree_scrollbar.set,
        )
        # ## ---configuramos el scroll al trieview
        self.tree_scrollbar.config(command=self.tree.yview)
        # ## ---creamos las columnas
        self.tree['columns'] = ("NAME","OWNER","TIPO","OWNERGROUP","CODE")
        # ## --- formato a las columnas
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("NAME", anchor=tk.W, width=350)
        self.tree.column("OWNER", anchor=tk.CENTER, width=150)
        self.tree.column("TIPO", anchor=tk.CENTER, width=100)
        self.tree.column("OWNERGROUP", anchor=tk.CENTER, width=150)
        self.tree.column("CODE", anchor=tk.CENTER, width=100)
        # ## --- indicar cabecera
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("#1", text="NAME", anchor=tk.W)
        self.tree.heading("#2", text="OWNER", anchor=tk.CENTER)
        self.tree.heading("#3", text="TIPO", anchor=tk.CENTER)
        self.tree.heading("#4", text="OWNER GROUP", anchor=tk.CENTER)
        self.tree.heading("#5", text="CODE", anchor=tk.CENTER)

        modo_dark = parse.get('dark', 'modo_dark')
        if modo_dark == 'False':
            self.tree.tag_configure('oddrow', background=oddrow, foreground=default_scrText_fg)
            self.tree.tag_configure('evenrow', background=evenrow, foreground=default_scrText_fg)
        # Mostramo por pantalla.
        self.tree.grid(column=0, row=0, pady=10, padx=(5,0), sticky='nsew')
        self.tree_scrollbar.grid(column=1, row=0, sticky=tk.N+tk.S,padx=(0,5), pady=10)

        # ## ====================================================================================
        # ## --- CREAMOS EL SEGUNDO LABEL FRAME
        self.labelframe2=ttk.LabelFrame(
            self.otros_datos, 
            text="OTROS DATOS",
            relief='groove'
        )
        self.labelframe2.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        
        self.labelframe2.rowconfigure(1, weight=1)
        self.labelframe2.rowconfigure(3, weight=1)
        self.labelframe2.columnconfigure(2, weight=1)
        self.labelframe2.columnconfigure(4, weight=1)

        # ## --- SERVERs
        self.lbl1 = ttk.Label(
            self.labelframe2,
            text='SERVER',
        )
        self.lbl1.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
        
        self.listServer = tk.Listbox(
            self.labelframe2, 
            height=3
        )
        self.fr2_scroll1 = tk.Scrollbar(self.labelframe2, orient=tk.VERTICAL)
        self.listServer.config(
            selectmode=tk.EXTENDED,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
            highlightbackground=default_Framework,
            selectbackground=default_select_bg,
            selectforeground=default_select_fg,
            font=_Font_Texto,
            highlightcolor = default_hglcolor,
            borderwidth=0, 
            highlightthickness=hhtk,
            width=20,
            yscrollcommand=self.fr2_scroll1.set
        )
        self.fr2_scroll1.config(command=self.listServer.yview)
        self.listServer.grid(column=0, row=1, padx=(5,0), pady=10, sticky="nsew", rowspan=3)
        self.fr2_scroll1.grid(column=1, row=1, sticky='ns', pady=10, rowspan=3)
        
        ## --- RISK
        self.lbl2 = ttk.Label(
            self.labelframe2, 
            text='RISK',
        )
        self.lbl2.grid(row=0, column=2, pady=10, padx=10, sticky='W')
        
        self.srcRisk = st.ScrolledText(
            self.labelframe2,
        )
        self.srcRisk.config(
            font=_Font_Texto, 
            height=6,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0, 
            highlightthickness=hhtk,
            highlightbackground=default_Framework,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectforeground=default_select_fg,
            selectbackground=default_select_bg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
        )

        self.btnCpRisk = ttk.Button(
            self.labelframe2, 
            text='Copiar',
            image=self.copiar_icon,
            command=lambda e=self.srcRisk:self.copiarALL(e),
        )
        self.btnCpRisk.grid(row=0, column=3, padx=20, pady=10, sticky=tk.E)
        
        self.srcRisk.grid(row=1, column=2, pady=(5,10), padx=10, sticky='nsew', columnspan=2)
        
        ## --- IMPACT
        self.lbl3 = ttk.Label(
            self.labelframe2,
            text='IMPACT',
        )
        self.lbl3.grid(row=0, column=4, pady=10, padx=10, sticky='W')
        
        self.srcImpact = st.ScrolledText(
            self.labelframe2,
        )
        self.srcImpact.config(
            font=_Font_Texto, 
            height=6,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0, 
            highlightthickness=hhtk,
            highlightbackground=default_Framework,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectforeground=default_select_fg,
            selectbackground=default_select_bg,
            background=default_scrText_bg,
            foreground=default_scrText_fg,
        )

        self.btnCpImp = ttk.Button(
            self.labelframe2,
            text='Copiar',
            image=self.copiar_icon,
            command=lambda e=self.srcImpact:self.copiarALL(e),
        )
        self.btnCpImp.grid(row=0, column=5, padx=20, pady=10, sticky=tk.E)   
        
        self.srcImpact.grid(row=1, column=4, pady=(5,10), padx=10, sticky='nsew', columnspan=2)
        
        ## --- SO
        self.lbl_SO = ttk.Label(
            self.labelframe2,
            text='SISTEMAS OPERATIVO',
            foreground=default_color_titulos,
            justify='center',
        )
        self.lbl_SO.grid(row=2, column=2, pady=10, padx=10, sticky='w')
        
        ## --- USER
        self.cbxUser = ttk.Combobox(
            self.labelframe2,
        )
        self.cbxUser.config(
            font = _Font_Texto,
            justify='center',
        )
        self.cbxUser.set('CONTACTOS')
        self.cbxUser.grid(row=3, column=2, padx=10, pady=10, ipady=8, sticky='new')

        ## --- VARIABLE
        self.lbl4 = ttk.Label(
            self.labelframe2,
            text='VARIABLES',
        )
        self.lbl4.grid(row=2, column=3, pady=10, padx=10, sticky='W')

        self.srcVariable = st.ScrolledText(
            self.labelframe2,
        )
        self.srcVariable.config(
            font=_Font_Texto, 
            height=5,
            wrap=tk.WORD,
            highlightcolor=default_hglcolor,
            borderwidth=0, 
            highlightbackground=default_Framework,
            highlightthickness=hhtk,
            insertbackground=default_hglcolor,
            insertwidth=hlh_def,
            selectforeground=default_select_fg,
            selectbackground=default_select_bg,
        )

        self.btnCpVariable = ttk.Button(
            self.labelframe2, 
            text='Copiar',
            image=self.copiar_icon,
            command=lambda e=self.srcVariable:self.copiarALL(e),
        )
        self.btnCpVariable.grid(row=2, column=5, padx=20, pady=10, sticky=tk.E)

        self.srcVariable.grid(row=3, column=3, pady=(5,10), padx=10, sticky='nsew', columnspan=3)
