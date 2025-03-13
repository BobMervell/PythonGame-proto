# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:43:00 2023

@author: LUCAS
"""
import tkinter as tk

 
class comm:
    def __init__(self,root,size,Game_state,num):
        self.root=root
        self.size=size
        self.Game_state=Game_state
        self.num=num
        
    def Move(self):
       for child in self.root.winfo_children():
           if isinstance(child, tk.Label):
               if child.perso.Nom=="Assassin":
                   if child.perso in self.Game_state[1][self.num-1]:
                       i,j=child.perso.True_pos
                   else:        
                       i,j=child.perso.Pos
               else:
                   i,j=child.perso.Pos
                   
               if self.num==1:
                   i=10-i
                   j=6-j
               x=j*self.size+self.size//4
               y=(i+1)*self.size+self.size//4  
               child.place(x=x+1,y=y+1)
               
               if child.perso.Def<=0:
                   child.destroy()
                   
                    
        