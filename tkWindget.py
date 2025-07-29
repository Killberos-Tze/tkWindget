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
import os
#we need load file element: that is a button with a label where the name of the file is displayed
#here we need to send the refrerence to error message, stringvar for display, we keep name and dir name of the loaded file, we need to send the command how to read the file, arrangement should always be vertical
#button, label label text, label with filename

#we need load files and clear files element: two buttons with labellist with sliders

#this can be removed soon
class LoadDataFile(Frame):
    class container():
        pass

    def __init__(self,**kwargs):
        self.filename=StringVar()
        kwargs=self.process_kwargs(**kwargs)
        super().__init__(kwargs['parent'])
        kwargs['parent']=self
        self.prepare_elements(**kwargs)
        self.errormsg=kwargs['ErrorVar']
        #self.init_dir=kwargs['initialdir']
        self._write_function=kwargs['write_file']
        self._read_function=kwargs['read_file']
        self._action_function=kwargs['action']

    def prepare_elements(self,*args,**kwargs):
        rowcount=1
        self.browse=Button(kwargs['parent'], text="Load file", command=lambda kwargs=kwargs : self.get_file(**kwargs))
        self.browse.grid(row=rowcount,column=1,sticky='W')
        rowcount+=1
        self.titlelabel=Label(kwargs['parent'], font='Courier',width=24,text=kwargs['text'],anchor='w')
        self.titlelabel.grid(row=rowcount,column=1,columnspan=2,sticky='W')
        rowcount+=1
        self.filelabel=Label(kwargs['parent'], textvariable=self.filename, font='Courier',width=kwargs['width'], wraplength=240,justify='left',relief=SUNKEN,anchor='w')
        self.filelabel.grid(row=rowcount,column=1,columnspan=2,sticky='W')

    def get_file(self,**kwargs):
        self.errormsg.set('')
        filename=askopenfilename(title="Select file", initialdir=kwargs['initialdir'], filetypes=kwargs['filetypes'])
        if filename:#to check if anything has been read out
            #change the folder where to look for the files
            tmp=self._read_function(filename)
            if tmp.error=='':
                self.filename.set(os.path.basename(filename))
                self.filedir=os.path.dirname(filename)
                self._write_function()
                if tmp.data:
                    self.data=tmp.data
                if tmp.setup:
                    self.setup=tmp.setup
                self._action_function()
            else:
                self.filename.set('')
                self.errormsg.set(tmp.error)

    def default_read(self,filename):
        tmp=LoadDataFile.container()
        tmp.error='test'
        tmp.data=''
        tmp.setup=''
        return tmp

    def default_write(self):
        pass

    def default_action(self):
        pass

    def process_kwargs(self,**kwargs):
        if 'parent' not in kwargs:
            kwargs['parent']=None
        if 'text' not in kwargs:
            kwargs['text']='Loaded whatever:'
        if 'read_func' not in kwargs:
            kwargs['read_file']=self.default_read
        if 'write_file' not in kwargs:
            kwargs['write_file']=self.default_write
        if 'action' not in kwargs:
            kwargs['action']=self.default_action
        if 'width' not in kwargs:
            kwargs['width']=12
        if 'title' not in kwargs:
            kwargs['title']='Select file'
        if 'initialdir' not in kwargs:
            #initialdir should be a reference to a stringvar from main program
            kwargs['initialdir']=StringVar()
            kwargs['initialdir'].set('Documents')
        if 'ErrorVar' not in kwargs:
            kwargs['ErrorVar']=self.filename
        if 'filetypes' not in kwargs:
            kwargs['filetypes']=[("All files","*.*")]
        return kwargs

class LabelButton(Button):
    def __init__(self,*args,textvariable=StringVar,**kwargs):
        if textvariable==StringVar:
            self.var=textvariable()
        else:
            self.var=textvariable
        
        if 'text' in kwargs:
            self.default=kwargs['text']
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
        else:
            self.default=''
        self.reset()
            
        tmp=Label(parent, textvariable=self.var, borderwidth=borderwidth, relief=relief,**kwargs)
        tmp.pack()
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
        parent=self
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
        
        self.button=Button(parent, image=self.images[self.__state], command=self.execute_press)
        self.button.pack()

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

#you need to add full list of kwargs in init
class Rotate(Frame):
    def __init__(self,*args, parent=None, typevar=StringVar, imagepath=os.path.join(os.path.dirname(__file__), 'images', "button.png"), choice_list=['a','b','c'], command=None, direction='horizontal', width=10):
        if command==None:
            command=self.placeholder
        super().__init__(parent)
        parent=self
        self.choice=typevar()
        self.choice_list=choice_list
        self.command=command
        if direction == 'horizontal' or direction != 'vertical':
            self.prepare_elements(0,180,parent=parent,imagepath=imagepath,width=width)
            self.direction_horizontal()
        else:
            self.prepare_elements(90,270,parent=parent,imagepath=imagepath,width=width)
            self.direction_vertical()
        self.choice.set(self.choice_list[0])

    def prepare_elements(self,*args, parent,imagepath,width):
        image = Image.open(imagepath)
        self.imageminus=ImageTk.PhotoImage(image.rotate(args[0]))
        self.imageplus=ImageTk.PhotoImage(image.rotate(args[1]))
        self.minus=Button(parent, image=self.imageminus,command=lambda lidx=-1: self.choice_change(lidx),bg='lightblue')
        self.plus=Button(parent, image=self.imageplus,command=lambda lidx=+1: self.choice_change(lidx),bg='lightblue')
        self.label=Label(parent, textvariable=self.choice, borderwidth=2,relief=GROOVE, width=width)

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
        idx=(self.choice_list.index(self.choice.get())+idx) % len(self.choice_list)
        self.choice.set(self.choice_list[idx])
        self.command(self.choice.get())

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
            self.plot.add_draw(self.canvas.draw)
            self.plot.draw()
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
    def __init__(self,parent=Tk, appgeometry= (200,200,10,10)):
        self.appgeometry=appgeometry
        if parent==Tk:
            self.approot=parent()
            super().__init__(self.approot)
            self.frameroot=self  
        else:
            super().__init__(parent)
            self.frameroot=self
            self.approot=None

    def __str__(self):
        return 'Regular App Frame'

    def init_start(self):
        if self.approot!=None:
            self.frameroot.pack(pady = (25,25), padx = (25,25))
            self.approot.title(str(self))
            self.approot.geometry('%dx%d+%d+%d' % self.appgeometry)
            self.approot.bind("<1>", lambda event: event.widget.focus_set())
            self.approot.mainloop()


class Test_App(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(appgeometry=(600, 500, 25, 25))
        self.approot.title("Windgets to see")
        self.rotate=Rotate(parent=self.frameroot,direction='horizontal')
        self.rotate.grid(row=0,column=1)
        self.press=OnOffButton(parent=self.frameroot)
        self.press.enable_press()
        self.press.grid(row=1,column=1)

        self.loadfile=LoadDataFile(parent=self.frameroot, width=24)
        self.loadfile._write_function=self.write_file
        self.loadfile.grid(row=2,column=1)

        self.figure=FigureFrame(parent=self.frameroot)
        self.figure.grid(row=3,column=1)

        self.floatentry=FloatEntry(parent=self.frameroot)
        self.floatentry.grid(row=0,column=2)

        self.stringentry=StringEntry(parent=self.frameroot)
        self.stringentry.grid(row=1,column=2)

        self.intentry=IPEntry(parent=self.frameroot,inlen=4)
        self.intentry.grid(row=2,column=2)

        self.name=NameLabel(parent=self.frameroot,width=14)
        self.name.set_name("What I want")
        self.name.grid(row=3,column=2)

    def write_file(self):
        variable="hey"
        print(variable)

if __name__=='__main__':
    Test_App().init_start()

