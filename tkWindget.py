#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 07:37:01 2023

@author: tze
"""

from tkinter import Frame, Button, Label, GROOVE, StringVar, Tk, SUNKEN
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import os
#we need load file element: that is a button with a label where the name of the file is displayed
#here we need to send the refrerence to error message, stringvar for display, we keep name and dir name of the loaded file, we need to send the command how to read the file, arrangement should always be vertical
#button, label label text, label with filename

#we need load files and clear files element: two buttons with labellist with sliders


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


class OnOffButton(Frame):
    def __init__(self,**kwargs):
        kwargs=self.process_kwargs(**kwargs)
        super().__init__(kwargs['parent'])
        kwargs['parent']=self
        self.command=kwargs['command']
        self.__state='off'
        self.__enable=False
        self.images={
        'on':ImageTk.PhotoImage(Image.open(os.path.join(kwargs['imagepath'],kwargs['images'][0]))),
        'off':ImageTk.PhotoImage(Image.open(os.path.join(kwargs['imagepath'],kwargs['images'][1])))
            }
        self.button=Button(kwargs['parent'], image=self.images[self.__state], command=self.execute_press)
        self.button.pack()
        
    def process_kwargs(self,**kwargs):
        if 'parent' not in kwargs:
            kwargs['parent']=None
        if 'images' not in kwargs:
            kwargs['images']=['on.png','off.png']#first on then off
        if 'imagepath' not in kwargs:
            kwargs['imagepath']=os.path.join(os.path.dirname(__file__), 'images')
        if 'command' not in kwargs:
            kwargs['command']=self.placeholder
        if 'width' not in kwargs:
            kwargs['width']=10
        return kwargs

    def process_press(self):
        if self.__state=='off':
            self.__state='on'
        elif self.__state=='on':
            self.__state='off'
    
    def get_state(self):
        return self.__state
    
    def change_state(self,*args):
        if args:
           if args[0]=='on' or args[0]=='off':
               self.__state=args[0]
               self.button.config(image=self.images[self.__state])
    def execute_press(self):
        if self.__enable:
            self.process_press()
            self.button.config(image=self.images[self.__state])
            self.command()
            
    def enable_press(self):
        self.__enable=True
    
    def disable_press(self):
        self.__enable=False
    
    def placeholder(self,*args):
        pass



class Rotate(Frame):
    def __init__(self,**kwargs):
        kwargs=self.process_kwargs(**kwargs)
        super().__init__(kwargs['parent'])
        kwargs['parent']=self
        self.choice=kwargs['typevar']
        self.choice_list=kwargs['choice_list']
        self.command=kwargs['command']
        if kwargs['direction'] == 'horizontal' or kwargs['direction'] != 'vertical':
            self.prepare_elements(0,180,**kwargs)
            self.direction_horizontal()
        else:
            self.prepare_elements(90,270,**kwargs)
            self.direction_vertical()
        self.choice.set(self.choice_list[0])
        
    def process_kwargs(self,**kwargs):
        if 'parent' not in kwargs:
            kwargs['parent']=None
        if 'typevar' not in kwargs:
            kwargs['typevar']=StringVar()
        if 'imagepath' not in kwargs:
            kwargs['imagepath']=os.path.join(os.path.dirname(__file__), 'images', "button.png")
        if 'choice_list' not in kwargs:
            kwargs['choice_list']=['a','b','c']
        if 'command' not in kwargs:
            kwargs['command']=self.placeholder
        if 'direction' not in kwargs:
            kwargs['direction']='horizontal'
        if 'width' not in kwargs:
            kwargs['width']=10
        return kwargs
        
    def prepare_elements(self,*args,**kwargs):
        image = Image.open(kwargs['imagepath'])
        self.imageminus=ImageTk.PhotoImage(image.rotate(args[0]))
        self.imageplus=ImageTk.PhotoImage(image.rotate(args[1]))
        self.minus=Button(kwargs['parent'], image=self.imageminus,command=lambda lidx=-1: self.choice_change(lidx),bg='lightblue')
        self.plus=Button(kwargs['parent'], image=self.imageplus,command=lambda lidx=+1: self.choice_change(lidx),bg='lightblue')
        self.label=Label(kwargs['parent'], textvariable=self.choice, borderwidth=2,relief=GROOVE, width=kwargs['width'])
        
                
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
        
class AppFrame(Frame):
    def __init__(self,**kwargs):
        kwargs=self.process_kwargs(**kwargs)
        super().__init__(kwargs['parent'])
        self.appgeometry=kwargs['appgeometry']
        self.root=self
        
    
    def __str__(self):
        return 'Regular App Frame'
    
    def process_kwargs(self,**kwargs):
        if 'parent' not in kwargs:
            kwargs['parent']=Tk()
            self.approot=kwargs['parent']
        if 'appgeometry' not in kwargs:
            kwargs['appgeometry']=(200,200,10,10)
        return kwargs

    def init_start(self):
        self.root.pack(pady = (25,25), padx = (25,25))
        self.approot.title(str(self))
        self.approot.geometry('%dx%d+%d+%d' % self.appgeometry)
        self.approot.mainloop()


class Test_GUI(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,appgeometry=(400, 400, 25, 25))
        self.approot.title("Windgets to see")
        self.rotate=Rotate(parent=self.root,direction='horizontal')
        self.rotate.grid(row=0,column=1)
        self.press=OnOffButton(parent=self.root)
        self.press.enable_press()
        self.press.grid(row=1,column=1)
        
        self.loadfile=LoadDataFile(parent=self.root, width=24)
        self.loadfile._write_function=self.write_file
        self.loadfile.grid(row=2,column=1)
        
        
    def write_file(self):
        variable="hey"
        print(variable)
        

if __name__=='__main__':
    Test_GUI().init_start()