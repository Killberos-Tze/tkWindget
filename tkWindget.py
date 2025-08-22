#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 07:37:01 2023

@author: tze
"""

from tkinter import Frame, Button, Label, GROOVE, StringVar, Tk, SUNKEN, Entry, DoubleVar, IntVar, DISABLED, NORMAL
from tkinter.filedialog import askopenfilename
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import ImageTk, Image
from RW_data.RW_files import Write_to, Read_from
import os
#we need load file element: that is a button with a label where the name of the file is displayed
#here we need to send the refrerence to error message, stringvar for display, we keep name and dir name of the loaded file, we need to send the command how to read the file, arrangement should always be vertical
#button, label label text, label with filename

#we need load files and clear files element: two buttons with labellist with sliders

#this is only for loading data files
class LoadSingleFile(Frame):

    def __init__(self,*args,parent=None,ini,write_ini=Write_to.ini_inst_proj,read=Read_from.ihtm,path='load_file_path',filetypes=[("All files","*.*")],**kwargs):
        super().__init__(parent)
        self._parent=self
        self._init_references(ini,write_ini,read,filetypes,path)
        self._prepare_elements(**kwargs)
        if self._path=='ref_file_path' and 'ref_file_name' in self._ini:
            if self._ini['ref_file_name']!='':
                self._load_data(os.path.join(self._ini['ref_file_path'],self._ini['ref_file_name']))
    #it has to be added separately 
    def add_action(self,action):
        self._action=action

    def _init_references(self,ini,write_ini,read,filetypes,path):
        self._filetypes=filetypes
        self._write_ini=write_ini
        self._ini=ini
        self._read=read
        self._path=path

    def _action(self):
        pass

    def get_data(self):#it returns the pointer
        return self.data

    def reset(self):
        self.reset_label()
        self.reset_data()
    
    def reset_data(self):
        self.data=None
        
    def reset_label(self):
        self.labelbutton.reset()

    def _prepare_elements(self,*args,**kwargs):
        self.labelbutton=LabelButton(self._parent, font=('Courier',10),command=self._get_file,**kwargs)
        self.labelbutton.grid(row=1,column=1)

    def _load_data(self,filename):
        self.data=self._read(filename)
        if self.data['error']=='':
            self.labelbutton.set_var(os.path.basename(filename))
            self._ini[self._path]=os.path.dirname(filename)
            if self._path=='ref_file_path':
                self._ini['ref_file_name']=os.path.basename(filename)
            self._write_ini()
            self._action()
        else:
            self.labelbutton.set_var(self.data['error'])

    def _get_file(self,**kwargs):
        self.reset_label()
        filename=askopenfilename(title="Select file", initialdir=self._ini[self._path], filetypes=self._filetypes)
        if filename:#to check if anything has been read out
            #change the folder where to look for the files
            self._load_data(filename)
        else:
            self.reset_data()

    def config(self,*args,**kwargs):
        self.labelbutton.config(*args,**kwargs)

    def disable(self):
        self.labelbutton.config(state=DISABLED)

    def enable(self):
        self.labelbutton.config(state=NORMAL)

class LabelButton(Button):
    def __init__(self,*args,textvariable=StringVar,**kwargs):
        if textvariable==StringVar:
            self.var=textvariable()
        else:
            self.var=textvariable

        if 'text' in kwargs:
            self.default=kwargs['text']
            kwargs.pop('text')
        else:
            self.default=''
        self.reset()

        super().__init__(*args,textvariable=self.var,**kwargs)

    def set_var(self,text):
        self.var.set(text)

    def get_var(self):
        return self.var.get()

    def clear(self):
        self.var.set("");
    def reset(self):
        self.var.set(self.default);


class LabelFrame(Frame):
    def __init__(self,*args, parent=None, textvariable=StringVar, borderwidth=2,relief=SUNKEN,**kwargs):
        super().__init__(parent);
        parent=self;
        if textvariable==StringVar:
            self.var=textvariable()
        else:
            self.var=textvariable
        if 'text' in kwargs:
            self.default=kwargs['text']
            kwargs.pop('text')
        else:
            self.default=''
        tmp=Label(parent, textvariable=self.var, borderwidth=borderwidth, relief=relief,**kwargs)
        tmp.pack()
        self.reset()


    def set_var(self,string):
        self.var.set(string);
    def get_var(self):
        return self.var.get();
    def clear(self):
        self.var.set("");
    def reset(self):
        self.var.set(self.default);

#you need to add full list of kwargs in init 
class OnOffButton(Frame):
    def __init__(self,*args, parent=None, images=['on.png','off.png'],imageon=None, imageoff=None, imagepath=os.path.join(os.path.dirname(__file__), 'images'), command=None, commandon=None, commandoff=None, width=10):
        if command==None:
            command=self.placeholder
        if commandon==None:
            commandon=self.placeholder
        if commandoff==None:
            commandoff=self.placeholder
        super().__init__(parent)
        self.parent=self
        self.command=command
        self.commandon=commandon
        self.commandoff=commandoff
        self.__state='off'
        self.__enable=False
        self.images={
        'on':ImageTk.PhotoImage(Image.open(os.path.join(imagepath,images[0]))),
        'off':ImageTk.PhotoImage(Image.open(os.path.join(imagepath,images[1])))
            }
        if imageon!=None:
            self.images['on']=ImageTk.PhotoImage(Image.open(os.path.join(imagepath,imageon)))
        if imageoff!=None:
            self.images['off']=ImageTk.PhotoImage(Image.open(os.path.join(imagepath,imageoff)))
        
        self.button=Button(self.parent, image=self.images[self.__state], command=self.execute_press)
        self.button.grid(row=1,column=1)

    def get_state(self):
        return self.__state

    def change_state(self,*args):
        if args:
           if args[0]=='on' or args[0]=='off':
               self.__state=args[0]
               self.button.config(image=self.images[self.__state])
    def execute_press(self):
        if self.__enable:
            if self.__state=='off':
                self.__state='on'
                self.commandon()
            elif self.__state=='on':
                self.__state='off'
                self.commandoff()
            self.button.config(image=self.images[self.__state])
            self.command()

    def enable_press(self):
        self.__enable=True

    def disable_press(self):
        self.__enable=False

    def placeholder(self,*args):
        pass
    
class CheckBox(OnOffButton):
    def __init__(self,*args, text='', textvariable=StringVar, orientation='EW',**kwargs):
        super().__init__(*args,imageon='box_on.png', imageoff='box_off.png',**kwargs)
        self.label=LabelFrame(parent=self.parent,text=text,textvariable=textvariable)
        if orientation=='WE':
            self.label.grid(row=1,column=0)
        elif orientation=='NS':
            self.label.grid(row=2,column=1)
        elif orientation=='SN':
            self.label.grid(row=0,column=1)
        else:
            self.label.grid(row=1,column=2)
        self.enable_press()

#you need to add full list of kwargs in init
class Rotate(Frame):
    def __init__(self,*args, parent=None, typevar=StringVar, imagepath=os.path.join(os.path.dirname(__file__), 'images', "button.png"), choice_list=['a','b','c'], command=None, direction='horizontal', width=10):
        if command==None:
            command=self.placeholder
        super().__init__(parent)
        parent=self
        self.var=typevar()
        self.choice_list=choice_list
        self.command=command
        if direction == 'horizontal' or direction != 'vertical':
            self.prepare_elements(0,180,parent=parent,imagepath=imagepath,width=width)
            self.direction_horizontal()
        else:
            self.prepare_elements(90,270,parent=parent,imagepath=imagepath,width=width)
            self.direction_vertical()
        self.var.set(self.choice_list[0])

    def prepare_elements(self,*args, parent,imagepath,width):
        image = Image.open(imagepath)
        self.imageminus=ImageTk.PhotoImage(image.rotate(args[0]))
        self.imageplus=ImageTk.PhotoImage(image.rotate(args[1]))
        self.minus=Button(parent, image=self.imageminus,command=lambda lidx=-1: self.choice_change(lidx),bg='lightblue')
        self.plus=Button(parent, image=self.imageplus,command=lambda lidx=+1: self.choice_change(lidx),bg='lightblue')
        self.label=Label(parent, textvariable=self.var, borderwidth=2,relief=GROOVE, width=width)

    def placeholder(self,*args):
        pass

    def direction_horizontal(self):
        self.minus.grid(row=1,column=1)
        self.label.grid(row=1,column=2)
        self.plus.grid(row=1,column=3)

    def direction_vertical(self):
        self.minus.grid(row=3,column=1)
        self.label.grid(row=2,column=1)
        self.plus.grid(row=1,column=1)

    def choice_change(self,idx):
        idx=(self.choice_list.index(self.var.get())+idx) % len(self.choice_list)
        self.var.set(self.choice_list[idx])
        self.command(self.var.get())

    def set_var(self,value):
        self.var.set(value);
    def get_var(self):
        return self.var.get();



class FigureFrame(Frame):
    def __init__(self,*args, parent=None, figclass=Figure,figkwargs={},figsize=(8.5/2.54,6/2.54), axsize=(0.2,0.2,0.7,0.7)):
        super().__init__(parent)
        parent=self

        self.plot=figclass(**figkwargs)
        if figclass==Figure:    
            self.plot.set_size_inches(figsize)
            self.plot.myaxes=self.plot.add_axes(axsize)

        self.canvas=FigureCanvasTkAgg(self.plot,master=parent)
        self.canvas.get_tk_widget().grid(row=1,column=1)
        toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=2,column=1)
        if str(self.plot)=="v_draw":
            self.plot.add_canvas(self.canvas)
            self.plot.canvasdraw()
        else:
            self.canvas.draw()

    def __str__(self):
        return 'Regular App Frame'

class StringEntry(Frame):
    def __init__(self,*args, parent=None,textvariable=StringVar,validate="key",selectbackground='#f00',**kwargs):
        super().__init__(parent)
        parent=self
        if textvariable in [StringVar, DoubleVar, IntVar]:
            self.var=textvariable()
        else:
            self.var=textvariable
        if 'text' in kwargs:
            self.default=kwargs['text']
            kwargs.pop('text')
        else:
            self.default=''
        self.reset()

        self.Entry=Entry(parent,textvariable=self.var,validate=validate,selectbackground=selectbackground,**kwargs)
        self.Entry['validatecommand']=(self.Entry.register(self.Check_input), '%P','%d')
        self.Entry.grid(row=1,column=1)

    def set_var(self,string):
        self.var.set(string);
    def get_var(self):
        return self.var.get();
    def clear(self):
        self.var.set("");
    def reset(self):
        self.var.set(self.default);

    def config(self,*args,**kwargs):
        self.Entry.config(*args,**kwargs)

    def disable(self):
        self.Entry.config(state=DISABLED)

    def enable(self):
        self.Entry.config(state=NORMAL)

    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                float(inStr)
                return False
            except:
                return True #it returns only true of false allowing or not allwing the insert action
        return True


class FloatEntry(StringEntry):
    def __init__(self,*args, parent=None,textvariable=DoubleVar,**kwargs):
        super().__init__(*args, parent=parent,textvariable=textvariable,**kwargs)

    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                float(inStr)
                if float(inStr)==0.:#this prevents that input string starts with zero so user can't set layer thickness to zero
                    return False
            except:
                return False #it returns only true of false allowing or not allwing the insert action
        return True

class IntEntry(StringEntry):
    def __init__(self,*args, parent=None,textvariable=IntVar,**kwargs):
        super().__init__(*args, parent=parent,textvariable=textvariable,**kwargs)

    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                int(inStr)
            except:
                return False #it returns only true of false allowing or not allwing the insert action
        return True
#integer with limited number of digits        
class IntLimEntry(StringEntry):
    def __init__(self,*args, parent=None,textvariable=IntVar,inlen=3,**kwargs):
        super().__init__(*args, parent=parent,textvariable=textvariable,**kwargs)
        self.inlen=inlen
    def Check_input(self,inStr,acttyp):
        if acttyp == '1': #insert
            try:
                int(inStr)
                if len(inStr)>self.inlen:
                    return False
            except:
                return False #it returns only true of false allowing or not allwing the insert action
        return True


class IPEntry(Frame):
    def __init__(self,*args,parent=None,address="None:None",**kwargs):
        if parent!=None:
            super().__init__(parent)
        else:
            super().__init__(*args,**kwargs)
        parent=self
        self.entry_list=[]
        self.ipfields=[IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]

        Label(parent,text="IP Address").grid(row=0,column=0,columnspan=6,sticky="W")
        Label(parent,text="Port").grid(row=0,column=7,columnspan=2,sticky="W")

        for i in range (0,7):
            if i%2==0:
                self.entry_list.append(IntLimEntry(parent=parent,textvariable=self.ipfields[int(i/2)],width=3))
                self.entry_list[-1].grid(row=1,column=i)
            else:
                Label(parent,text=".").grid(row=1,column=i)

        Label(parent,text=":").grid(row=1,column=7)
        self.entry_list.append(IntLimEntry(parent=parent,textvariable=self.ipfields[4],inlen=4,width=4))
        self.entry_list[-1].grid(row=1,column=8)

        if address=="None:None":
            self.set_address("127.0.0.1")
            self.set_port("5025")
        else:
            self.set_address_port(address)

    def set_address_port(self,string):
        self.set_address(string.split(":")[0])
        self.set_port(string.split(":")[1])

    def set_address(self,string):
        ipfields=string.split(".")
        for i in range(0,len(self.ipfields)-1):
            self.ipfields[i].set(int(ipfields[i]))

    def set_port(self,string):
        self.ipfields[-1].set(int(string))

    def get_address(self):
        out=""
        for item in self.ipfields[0:3]:
            out=out+str(item.get())+"."
        out=out+str(self.ipfields[3].get())
        return out

    def get_port(self):
        return self.ipfields[-1].get()

    def get_address_port(self):
        return self.get_address()+":"+str(self.get_port())

    def disable(self):
        for item in self.entry_list:
            item.disable()

    def enable(self):
        for item in self.entry_list:
            item.enable()

class AppFrame(Frame):
    def __init__(self, file, parent=Tk, appgeometry= (200,200,10,10)):
        self.appgeometry=appgeometry
        if parent==Tk:
            self.approot=parent()
            super().__init__(self.approot)
            self.frameroot=self  
        else:
            super().__init__(parent)
            self.frameroot=self
            self.approot=None
        self.ini=Read_from.ini_inst(file)
        self.file=file
        if self.ini['error']:
            self.ini={}
            self.ini['error']=''
            self.ini['save_file_path']='Document'
            self.ini['ref_file_path']='Documents'
            self.ini['load_file_path']='Documents'
            self.write_ini()

    def __str__(self):
        return 'Regular App Frame'

    def init_start(self):
        if self.approot!=None:
            self.frameroot.pack(pady = (25,25), padx = (25,25))
            self.approot.title(str(self))
            self.approot.geometry('%dx%d+%d+%d' % self.appgeometry)
            self.approot.bind("<1>", lambda event: event.widget.focus_set())
            self.approot.mainloop()

    def write_ini(self):
        tmp=self.ini.pop('error')
        Write_to.ini_inst_proj(self.file,self.ini)
        self.ini['error']=tmp


