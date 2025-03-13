# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:41:08 2023

@author: LUCAS
"""

import Lejeu as L
import tkinter as tk
import PIL 
import User_Interface as UI
from PIL import ImageTk
import Communication as C
import Personnages
import os


class Affichage(tk.Canvas):
    def __init__(self, root,size,Game_state,num,other_root,conflict):
        tk.Canvas.__init__(self, root, width=size*8-2, height=size*13-2, bg="white")
        self.root=root
        self.size = size
        self.Game_state=Game_state
        self.num=num
        self.other_root=other_root
        self.conflict=conflict
        self.end=False
        self.texte=None
        self.root.window_comm=C.comm(self.other_root,self.size,self.Game_state,3-self.num)
        self.root.window=C.comm(self.root,self.size,self.Game_state,self.num)
        self.images=self.Get_img()
        self.Add_persos(self.Game_state[1])
        self.Create_board()
        self.tooltips=[]
        self.othercanvas=None
        
    def Get_img(self):
        dic={}
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construire le chemin complet vers les fichiers images
        fast=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'fast.png'))
        sniper=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'sniper.png'))
        tank=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'tank.png'))
        wall=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'wall.png'))
        assa=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'Assassin.png'))
        builder=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'Builder.png'))
        breaker=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'Breaker.png'))
        tp=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'Teleport.png'))
        healer=PIL.ImageTk.PhotoImage(file=os.path.join(current_directory, 'images', 'Healer.png'))

        
        dic['Fast']=fast
        dic['Sniper']=sniper
        dic['Tank']=tank
        dic['Wall']=wall
        dic['Assassin']=assa
        dic["Builder"]=builder
        dic["Breaker"]=breaker
        dic["Teleport"]=tp
        dic["Healer"]=healer
        return dic
            
    def Create_symbol(self,name):    
        for key,elt in self.images.items():
            if key==name:

                label=tk.Label(self.root, image=elt)
                label.photo = elt
                self.create_window(0, 0, window=label, anchor='nw')
                return label
    
    # def Set_invis(self,lab,i,j):
    #     img = lab.cget("image")
    #     # invis_V=ImageFilter.Colorize(color="#ddddc2", black=0.0)
    #     # invis_B=ImageFilter.Colorize(color="#567646", black=0.0)
    #     img_inverted = ImageOps.invert(img)
    #     # img_V=img.filter(invis_V)
    #     # img_B=img.filter(invis_B)
    #     # if (i+j) % 2 == 0:
    #     #     lab.config(image=img_V)
    #     # else:
    #     #     lab.config(image=img_B)
    #     lab.config(image=img_inverted)
    #     return lab
            
    def Board_normal(self):
       Lcasev=self.find_withtag("casev")
       Lcaseb=self.find_withtag("caseb")
       T=(Lcasev,Lcaseb)
       for i in range(len(T)):
           for case in T[i]:
               x1, y1, x2, y2 =self.coords(case)
               j=9
               if y1/self.size <= j:
                   if i ==1:
                       self.itemconfig(case, fill="#ddddc2")
                   else:
                       self.itemconfig(case, fill="#567646")
        
    def Board_ini(self):
        Lcasev=self.find_withtag("casev")
        Lcaseb=self.find_withtag("caseb")
        T=(Lcasev,Lcaseb)
        for i in range(len(T)):
            for case in T[i]:
                x1, y1, x2, y2 =self.coords(case)
                j=9
                if y1/self.size <= j:
                    if i ==1:
                        self.itemconfig(case, fill="#ffccb1")
                    else:
                        self.itemconfig(case, fill="#786535")
        y=12*self.size
        self.texte=self.create_text(0, y, text="Placement initial", font=("Arial", 14),anchor='nw')
        
    def Create_board(self):
        button = tk.Button(self.root, text="Prêt", command=self.Ready)
        xb=7*self.size+self.size//4
        yb=self.size//4
        button.place(x=xb,y=yb)
        for i in range(1,12):
            for j in range(7):
                x0 = j * self.size
                y0 = i * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                
                if (i+j) % 2 == 0:
                    color = "#ddddc2"   
                    Rec_id=self.create_rectangle (x0,y0,x1,y1,fill=color,tags='caseb')
                    UI.DragManager(Rec_id,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_passover()
                    
                else:
                    color = "#567646"
                    Rec_id=self.create_rectangle(x0,y0,x1,y1,fill=color,tags='casev')
                    UI.DragManager(Rec_id,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_passover()
        
        if self.num==1:
            for k in range(11):
                x = 7 * self.size
                y = k * self.size + 1.5*self.size
                self.create_text(x + self.size / 2, y, text=chr(107 - k), font=("Arial", 14))

                        
            for k in range(7):
                x = (k-1) * self.size + self.size
                y = self.size / 2
                self.create_text(x + self.size / 2, y, text=str(-k+7), font=("Arial", 14))
        else:                
            for k in range(11):
                x = 7 * self.size
                y = k * self.size + 1.5*self.size
                self.create_text(x + self.size / 2, y, text=chr(97 + k), font=("Arial", 14))
    
                        
            for k in range(7):
                x = (k-1) * self.size + self.size
                y = self.size / 2
                self.create_text(x + self.size / 2, y, text=str(k+1), font=("Arial", 14))

        self.Create_persos()
                
    def Create_persos(self):
        for i,row in enumerate(self.Game_state[0]):
            for j,perso in enumerate(row):
                if perso!=0:
                    name=L.Get_name(perso)
                    lab=self.Create_symbol(str(name))
                    lab.perso=perso
                    UI.DragManager(lab,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_dragable()
                    UI.DragManager(lab,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_enter()
                    UI.DragManager(lab,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_Rclickable()
                    if self.num==1:
                        i=10-i
                        j=6-j
                    x,y=j*self.size+self.size//4,(i+1)*self.size+self.size//4
                    lab.place(x=x+1,y=y+1)
            
    def Add_persos(self,teams):
        for i,team in enumerate(teams):
            for j,perso in enumerate(team):
                if i==0:
                    if j>6:
                        j-=7
                        i+=1
                    perso.Move((i,j))
                    self.Game_state[0][i][j]=perso
                else:
                    if j>6:
                        j-=7
                        i+=1
                    perso.Move((11-i,j))
                    self.Game_state[0][11-i][j]=perso
        self.root.window_comm.Move()
    
    def Add_wall(self,i,j):
        lab=self.Create_symbol("Wall")
        lab.perso=Personnages.Wall()
        lab.perso.Move((i,j))
        self.Game_state[0][i][j]=lab.perso
        
        UI.DragManager(lab,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_enter()
        UI.DragManager(lab,self.root,self.size,self.Game_state,self.num,self.conflict,self).add_Rclickable()

        if self.num==1:
            i=10-i
            j=6-j
            
            
        x,y=j*self.size+self.size//4,(i+1)*self.size+self.size//4
        lab.place(x=x+1,y=y+1)
        print("Mur construit")
    
    def Remove_wall(self,i,j):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                if widget.perso.Pos==(i,j) and widget.perso.Nom=="Wall":
                    widget.destroy()
                    self.Game_state[0][i][j]=0
                    print("Mur détruit")
                    return None
        print("Echec")
    # def Add_invis(self,i,j,perso):
    #     lab=self.Create_symbol("Assassin")
    #     lab.perso=perso
    #     self.Set_invis(lab, i, j)
        
    #     x,y=j*self.size+self.size//4,(i+1)*self.size+self.size//4
    #     lab.place(x=x+1,y=y+1)
        
    def Ready(self):
        self.end=True

    def add_select(self,widget,perso):
        dnd=UI.DragManager(widget,self.root,self.size,self.Game_state,self.num,self.conflict,self)
        dnd.add_Lclickable()     
        dnd.perso_attack=perso
        
    def remove_select(self,widget):
        dnd=UI.DragManager(widget,self.root,self.size,self.Game_state,self.num,self.conflict,self)
        dnd.remove_Lclickable()     
    




'''
Notes:
29/03/23 -- pour le drag n drop d'une image, ce n'est pas le centre 
de l'image qui est pris en compte mais le coin superieur gauche 
d'ou le //4 et non par deux dans le drag n drop et non size//2 pose
aussi problème un peu sur la limite entre deux cases
(((corrigé)))

TclError: image "pyimage5" doesn't exist
surement car root2 essaie d'appeler les objet images que root 1 a déja créer'
(((corrigé)))

03/04/23

faire la communication entre les deux root voir chat gpt
(((fait)))


04/04/23

Dans UI, dans le drop, pour la gestiion de conflit si la la place
 est deja prise, on regarde les coordoonnées du prochain point ()
 on detecte bien mais on replace mal
 
 (((corrigé)))
 
 mais la quand on pose sur un emplacemet deja pris ca refuse pas de 
 soucis mais au tour d'apres, le widget sembe avoir perdu son attribut "perso"
 
 (((corrigé)))
 
 
 L'affichage le la range avec les dots ne marche pas d'une part on arrive pas 
 a voir quels sont les cases autorisés et d'autre part on a une erreur quand 
 on essaie de créer l'objet  oval
 
 Les dots ne s'affichent toujours pas et en plus les cases des rectanlges
 n'ont plus passover je n'arrive pas a appeler UI.draganddrop avec un objet 
 de type self.createrectangle, ca me dit que c'est un entier
 
 
(((passover corrigé)))


les dots s'affichent sur le joueur 1 mais safficher auu coordonnées inversé 
(((corrigé)))

J'ai voulu disable le dragndrop lorsque l'attaque est lancée avec une variable
 self.diasble mais elle reste inchangé genre quad je lance l'attque elle passe 
 en False mais quand je verifie son etat depuis le dnd elle reste en True

(((Changement d'idée')))
Doit cliquer deux fois pour attaquer, si clique une fois et commence le drop
bah on annule et on revient a l'etart de base

OK alors j'ai bien avancé je pense mais la j'ai une erreur avec les tooltip va
 falloir que je regle ca
 
 
La fonction add_wall dans l'afficghage est en cours'


le teleport en cours


         self.invis_V=ImageFilter.Colorize(color="#ddddc2", black=0.0)
         filter_2 = ImageFilter.Colorize(color="#567646", black=0.0)
 '''
 