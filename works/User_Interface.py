# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:03:54 2023

@author: LUCAS
"""

import tkinter as tk
#import Personnages
import Lejeu as L
#import Conflicts as cft
import time as t
import threading

Moved=False
i,j=-9,-9

class DragManager():
    def __init__(self,widget,root,size,Game_state,num,conflict,canvas): #game_state contient le plateau et les equipes
        self.widget = widget
        self.root=root
        self.size=size
        self.Game_state=Game_state
        self.num=num
        self.conflict=conflict
        self.canvas=canvas
        self.perso=None
        self.Lcoords=self.center_cases()
        self.Coords_ini=(0,0)
        self.Click_coords=(0,0)
        self.perso_attack=None
        self.tooltip=None
        
    def Create_tooltip(self,txt):
        tooltip = tk.Toplevel()
        tooltip.geometry(f"+{self.root.winfo_pointerx()+15}+{self.root.winfo_pointery()+15}")
        tooltip.overrideredirect(True)
        tk.Label(tooltip, bg='#ffffcc', text=txt).pack()
        self.canvas.tooltips.append(tooltip)
        return tooltip
        
    def center(self,i,j):
        x=j*self.size+self.size/2
        y=i*self.size+self.size/2
        tupl=([x,y],(i,j))
        return tupl

    def center_cases(self):
        L=[]
        for i in range(1,12):
            for j in range(7):
                tupl=self.center(i,j)
                L.append (tupl)
        return L  
    
    def distance_min(self,x,y): 
        Lrelative=[]         
        Lid=[]
        self.Lcoords=self.center_cases()
        for elt in self.Lcoords:
            Id=elt[1]
            coords=elt[0]
            coords[0]-=x
            coords[1]-=y
            Dist=(abs(coords[0])+abs(coords[1]),Id)

            Lrelative.append(Dist[0])
            Lid.append(Dist)
        Min=min(Lrelative)
        for elt in Lid:
            if Min==elt[0]:
                return elt
        
    def give_coords(self,x,y):    
        i,j=self.distance_min(x, y)[1]    #i,j sont les coordoonées de la case
        i-=1  
        if self.num==1:
            i=10-i
            j=6-j
        return i,j
    
    def Create_dot(self,x0,y0,x1,y1,color,event):
        x0+=18
        y0+=18
        x1-=18
        y1-=18
        if color=="#ddddc2":
            self.canvas.create_oval(x0,y0,x1,y1, fill="#c6c6ad", outline='',tag='dot')
        elif color=="#567646":
            self.canvas.create_oval(x0,y0,x1,y1, fill="#466636", outline='',tag='dot')
    
    def Create_cirle(self,x0,y0,x1,y1,color,event):
        x0+=30
        y0+=30
        x1-=30
        y1-=30
        if color=="#ddddc2":
            self.canvas.create_oval(x0,y0,x1,y1, fill="#c6c6ad", outline='',tag='dot')
        elif color=="#567646":
            self.canvas.create_oval(x0,y0,x1,y1, fill="#446434", outline='',tag='dot')
    
    def Mod_Range(self,stat,event):
        L=self.conflict.Range(stat)
        pla=self.Game_state[0]
        if stat=='Vit':
            radius=self.widget.perso.Vit 
        elif stat =='Por':
            radius=self.widget.perso.Por
        for elt in L:
            i=elt[1][0]
            j=elt[1][1]            
            if self.num==1:
                ibis=11-i
                jbis=6-j
                x,y=self.center(ibis,jbis)[0]
                if (ibis+jbis) % 2 == 0:
                    color = "#ddddc2"
                else:
                    color = "#567646"
            else:
                i+=1
                x,y=self.center(i,j)[0]
                if (i+j) % 2 == 0:
                    color = "#ddddc2"
                else:
                    color = "#567646"
            x0=x-10
            y0=y-10
            x1=x+10
            y1=y+10
            
  
            if elt[0]:
                self.Create_dot(x0, y0, x1, y1, color,event)
                
            if self.num==1:
                if self.widget.perso.Nom=="Assassin":
                    pi,pj=self.widget.perso.True_pos
                else:
                   pi,pj=self.widget.perso.Pos
                R=self.conflict.Check_r_obstacless((pi,pj),(i,j),radius)
                if (ibis-1) in range(len(pla)) and jbis in range(len(pla[0])) and (pla[i][j]!=0) and R and elt[0]==False:
                    self.Create_cirle(x0, y0, x1, y1, color, event)
            else:
                if self.widget.perso.Nom=="Assassin":
                    pi,pj=self.widget.perso.True_pos
                else:
                   pi,pj=self.widget.perso.Pos
                pi+=1
                R=self.conflict.Check_r_obstacless((pi-1,pj),(i-1,j),radius)
                if (i-1) in range(len(pla)) and j in range(len(pla[0])) and pla[i-1][j]!=0 and R and elt[0]==False:
                    self.Create_cirle(x0, y0, x1, y1, color, event)
 
    def Kill_dots(self):
        L=self.canvas.find_withtag('dot')
        for Id in L:
            self.canvas.delete(Id)
            
    def add_dragable(self):
        self.conflict.widget=self.widget
        if self.conflict.Good_team():
            self.widget.bind("<ButtonPress-1>", self.On_start)
            self.widget.bind("<B1-Motion>", self.On_drag)
            self.widget.bind("<ButtonRelease-1>", self.On_drop)
            self.widget.configure(cursor="hand2")

    def On_start(self, event):
        self.conflict.widget=self.widget
        self.Hide_data(event)
        
        xd = event.x_root -  self.root.winfo_rootx() - self.widget.winfo_width()//2
        yd = event.y_root - self.root.winfo_rooty() - self.widget.winfo_height()//2
        
        i,j=self.give_coords(xd,yd)
        self.Coords_ini=(i,j)
        self.perso=self.Game_state[0][i][j]
        self.widget.place(x=xd,y=yd)
        
        
        if self.conflict.etape=='Mid':
            self.Mod_Range('Vit',event)
        
    def On_drag(self, event):
        xd = event.x_root -  self.root.winfo_rootx() - self.widget.winfo_width()//2
        yd = event.y_root - self.root.winfo_rooty() - self.widget.winfo_height()//2
        self.widget.place(x=xd,y=yd)

    def On_drop(self, event):
        xd = event.x_root -  self.root.winfo_rootx() - self.widget.winfo_width()//2
        yd = event.y_root - self.root.winfo_rooty() - self.widget.winfo_height()//2
            
        i,j=self.give_coords(xd,yd)
        
        if self.conflict.Authorized_move(i, j):
            (i,j)=self.Coords_ini
            self.Game_state[0][i][j]=0
            i,j=self.give_coords(xd,yd)        
            self.Game_state[0][i][j]=self.perso
            self.widget.perso.Move((i,j))
            global Moved
            Moved=True
            if self.give_coords(xd,yd) != self.Coords_ini:
                self.canvas.conflict.moves_left-=1
            
        other_window=event.widget.master.window_comm
        window=event.widget.master.window
        window.Move()
        other_window.Move()
        self.Kill_dots()
        
    def add_passover(self):
        self.canvas.tag_bind(self.widget,"<Enter>",self.On_enter)
        self.canvas.tag_bind(self.widget,"<Leave>",self.On_leave)
        
    def On_enter(self,event):
        x=event.x
        y=event.y
        i,j=self.distance_min(x, y)[1]
        tags=self.canvas.gettags(self.widget)
        if "caseb" in tags:
            light_color="#eeeee2"
            if self.conflict.etape== "Ini"and i<=9:
                light_color="#ffddc2"
        else:
            light_color="#96B686"
            if self.conflict.etape== "Ini" and i<=9:
                light_color="#897646"

        self.canvas.itemconfig(self.widget, fill=light_color)
        
    def On_leave(self,event):
        x=event.x
        y=event.y
        i,j=self.distance_min(x, y)[1]
        tags=self.canvas.gettags(self.widget)
        if "caseb" in tags:
            color="#ddddc2"
            if self.conflict.etape== "Ini" and i<=9:
                color="#ffccb1"
        else:
            color="#567646"
            if self.conflict.etape== "Ini" and i<=9:
                color="#786535"
        self.canvas.itemconfig(self.widget, fill=color)        
    
    def add_enter(self):
        self.widget.bind("<Enter>",self.Give_data)
        self.widget.bind("<Leave>",self.Hide_data)
        
    def Give_data(self,event):
        txt=''
        xd = event.x_root -  self.root.winfo_rootx() - self.widget.winfo_width()//4
        yd = event.y_root - self.root.winfo_rooty() - self.widget.winfo_height()//4

        i,j=self.give_coords(xd,yd)
        txt=L.Get_info((i,j), self.Game_state)

        tooltip=self.Create_tooltip(txt)     
        event.widget.tooltip =tooltip      
        
    def Hide_data(self,event):
        event.widget.tooltip.destroy()
        
    def add_Rclickable(self):
        self.conflict.widget=self.widget
        if self.conflict.Good_team():
            self.widget.bind("<ButtonPress-3>", self.On_Rclick)
            
    def add_Lclickable(self):
        # self.widget.enable=False

        self.widget.unbind("<ButtonPress-1>")
        self.widget.unbind("<B1-Motion>")
        self.widget.unbind("<ButtonRelease-1>")
        self.widget.unbind("<ButtonPress-3>")
        self.widget.bind("<ButtonPress-1>", self.On_Lclick)

    def remove_Lclickable(self):    
        self.widget.unbind("<ButtonPress-1>")
        self.add_Rclickable()
        self.add_dragable()
        
    def On_Rclick(self,event):
        self.Hide_data(event)
        self.conflict.widget=self.widget
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Attaque", command=self.Attacking)
        menu.add_command(label="Capacitée", command=self.Capacité)
        menu.add_command(label="Objet", command=self.f3)
        menu.post(event.x_root, event.y_root)
        self.Click_coords=(event.x_root, event.y_root)
        
    def On_Lclick(self,event):
        
        self.Hide_data(event)
        self.conflict.widget=self.widget
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Attaque", command=self.Attacked)
        menu.add_command(label="Annuler", command=self.Abort)
        menu.post(event.x_root, event.y_root)
        self.Click_coords=(event.x_root, event.y_root)
        
    def Attacking(self):
        txt="Prêt à attaquer"
        x,y=self.Click_coords
        x-=self.root.winfo_rootx()
        y-=self.root.winfo_rooty()
        event=tk.Event()
        event.type = "4" # ButtonPress event code
        event.num = 1    # left mouse button
        event.x = x 
        event.y = y    
        # self.tooltip=self.Create_tooltip(txt)
        print(txt)
        print("")
        i,j=self.give_coords(x,y)
        self.perso=self.Game_state[0][i][j]
        self.Mod_Range("Por", event)
        self.conflict.widget=self.widget
        for widget in self.root.winfo_children():
            if widget.winfo_class() == "Label":  
                self.canvas.add_select(widget,self.perso)
        
    def Attacked(self):
        if self.perso_attack.Nom=="Assassin":
            i,j=self.perso_attack.True_pos
        else:
            i,j=self.perso_attack.Pos
        self.conflict.widget=self.widget
        if self.conflict.Authorized_attack(i,j,self.perso_attack):
            self.widget.perso.Def=self.widget.perso.Def - self.perso_attack.Att
            print(self.widget.perso.Nom + " Touché")
            print(" Défense - " + str(self.perso_attack.Att))
            self.canvas.conflict.moves_left-=1
            if not self.conflict.Is_alive(self.widget.perso):
                self.widget.destroy()
                i,j=self.widget.perso.Pos
                self.Game_state[0][i][j]=0
                print(self.widget.perso.Nom + " Eliminé")
                other_window=self.widget.master.window_comm
                window=self.widget.master.window
                window.Move()
                other_window.Move()
        else:
            print("Missed")
        print("")
        self.Kill_dots()
        for widget in self.root.winfo_children():
            if widget.winfo_class() == "Label":
                self.canvas.remove_select(widget)
    
    def Abort(self):
        print("Annulation")
        print("")   
        self.Kill_dots()
        for widget in self.root.winfo_children():
            if widget.winfo_class() == "Label":
                self.canvas.remove_select(widget)
                
    def On_select(self,event):
        xd = event.x_root -  self.root.winfo_rootx() 
        yd = event.y_root - self.root.winfo_rooty() 
        
        global Moved
        global i
        global j
        i,j=self.give_coords(xd,yd)
        
        Moved=True
        # print( self.Coords_ini,"SELECTIONNE")
         
    def selecting(self):
            self.widget.perso.Capacite=True
            x,y=self.Click_coords
            x-=self.root.winfo_rootx()
            y-=self.root.winfo_rooty()
            
            event=tk.Event()
            event.type = "4" # ButtonPress event code
            event.num = 1    # left mouse button
            event.x = x 
            event.y = y    
            
            global Moved
            Moved=False
            
            self.Mod_Range("Vit", event)
            for widget in self.root.winfo_children():
                if widget.winfo_class() == "Label":  
                    widget.unbind("<ButtonPress-1>")
                    widget.unbind("<B1-Motion>")
                    widget.unbind("<ButtonRelease-1>")
                    widget.unbind("<ButtonPress-3>")  

            for widget in self.canvas.find_all():
                tags=self.canvas.gettags(widget)
                if "casev" in tags or "caseb" in tags:
                    self.canvas.tag_bind(widget,"<ButtonPress-1>",self.On_select)
    #                 self.canvas.tag_bind(widget,"<ButtonPress-3>",self.Undo)
                    
    # def Undo(self,event):
    #     self.Abort()
    
    def deselecting(self):
        self.widget.perso.Capacite=False
        
        for widget in self.canvas.find_all():
            tags=self.canvas.gettags(widget)
            if "casev" in tags or "caseb" in tags:
                self.canvas.tag_unbind(widget, "<Button-1>")
                
        for widget in self.root.winfo_children():
            if widget.winfo_class() == "Label" : 
                self.canvas.remove_select(widget)   #remove select et les unbinds comme il faut

    
    def Capacité(self):
        L=["Sniper","Tank","Fast"]
        if self.widget.perso.Nom in L:
            print("Ce personnage n'a pas de capacité")
        elif self.widget.perso.Nom =="Assassin":
            self.Feinte(1)
        elif self.widget.perso.Nom =="Builder":
            self.Build(1)
        elif self.widget.perso.Nom =="Breaker":
            self.Break(1)
        elif self.widget.perso.Nom =="Teleport":
            self.Tp(1)
        elif self.widget.perso.Nom =="Healer":
            self.Heal(1)
    
    def Feinte(self,etape):
        if etape==1:
            print("Cliquez la ou vous voulez apparaitre")
            print("Votre vrai position reste la même et est inconnu de l'ennemi")
            
            self.selecting()
            
            self.thread = threading.Thread(target=self.Monitor)
            self.thread.start()
            
        elif etape==2:
            global i
            global j
            self.widget.perso.Move((i,j))

            self.deselecting()
                   
            i,j=self.widget.perso.Pos
            pi,pj=self.widget.perso.True_pos
            self.Game_state[0][i][j]=0
            self.Game_state[0][pi][pj]=self.widget.perso
            
            # self.canvas.Add_invis(i,j,self.widget.perso)
            
            self.Kill_dots()
            self.widget.master.window_comm.Move()

    def Build(self,etape):
        if etape==1:
            print("Cliquez la ou vous voulez construire un mur")
            print("")
            self.selecting()
            
            self.thread = threading.Thread(target=self.Monitor)
            self.thread.start()
            
        elif etape==2:
            self.deselecting()
            global i
            global j
            i,j
            self.canvas.Add_wall(i,j)
            self.canvas.othercanvas.Add_wall(i,j)
            self.Kill_dots()
    
    def Break(self,etape):
        if etape==1:
            print("Cliquez la ou vous voulez détruire un mur")
            print("")
            self.widget.perso.Capacite=True
            self.selecting()
            self.thread = threading.Thread(target=self.Monitor)
            self.thread.start()
        elif etape==2:
             self.deselecting()
             global i
             global j
             self.canvas.Remove_wall(i,j)
             self.canvas.othercanvas.Remove_wall(i,j)
             self.Kill_dots()
             self.widget.perso.Capacite=False
        
    def Tp(self,etape):
        if etape==1:
            print("Cliquez la ou vous voulez vous teleporter")
            
            self.selecting()
            
            self.thread = threading.Thread(target=self.Monitor)
            self.thread.start()
        
        elif etape==2:
            global i
            global j
            pi,pj=self.widget.perso.Pos
            self.Game_state[0][pi][pj]=0
            self.widget.perso.Move((i,j))
            self.deselecting()
            i,j=self.widget.perso.Pos
            self.Game_state[0][i][j]=self.widget.perso
            
            self.Kill_dots()
            self.widget.master.window_comm.Move()
            self.widget.master.window.Move()
        
    def Heal(self,etape):
        if etape==1:
            print("Cliquez la ou vous voulez soigner")
            
            self.selecting()
            
            self.thread = threading.Thread(target=self.Monitor)
            self.thread.start()
        elif etape==2:
            global i
            global j
            
            perso=self.Game_state[0][i][j]
            if perso==0:
                print("Echec")
            elif perso.Def==perso.Defmax:
                print("Echec, vie déjà au max")  
            elif perso.Def + 600 > perso.Defmax:
                perso.Def=perso.Defmax
                print("Soin effectué")
            else:
                perso.Def+=600
                print("Soin effectué")
                
            self.deselecting()
            self.Kill_dots()
                
    def f3(self,event):
        print("Objet indisponible pour l'instant")
        
        
    def Monitor(self):
        global Moved
        global i
        global j
        i,j=(-9,-9)
        self.conflict.widget=self.widget

        while Moved==False:
            if self.conflict.moves_left<=0:
                print("plus de coup disponible")
                self.Kill_dots()
                self.deselecting()
                Moved=True
            else:
                while not self.conflict.Authorized_move(i,j):
                    print(i,j,self.conflict.Authorized_move(i,j))
                    t.sleep(1)
                self.canvas.conflict.moves_left-=1
                if self.widget.perso.Nom=="Assassin":
                    self.Feinte(2)
                elif self.widget.perso.Nom=="Builder":
                    self.Build(2)
                elif self.widget.perso.Nom=="Breaker":
                    self.Break(2)
                elif self.widget.perso.Nom=="Teleport":
                    self.Tp(2)
                elif self.widget.perso.Nom=="Healer":
                    self.Heal(2)
            
        
        