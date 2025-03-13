# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 15:50:26 2023

@author: LUCAS
"""
import tkinter as tk
import Affichage as A
import Personnages
import CharacterSelectForm as C
import Conflicts as cft
import threading
import time as t

def Get_name(Perso):
    return Perso.Nom

"get name et get perso info dans Lejeu ne devrait"
" pas avoir besoin d'etre la mais plutot dans personnages"

class MyThread(threading.Thread):
    def __init__(self,A1,A2,C1,C2):
        super().__init__()
        self.keep_going=True
        self.A1=A1
        self.A2=A2
        self.C1=C1
        self.C2=C2
    def run(self):
        x=self.A1.winfo_exists()
        y=self.A2.winfo_exists()
        while self.keep_going:
            while (not self.A1.end or not self.A2.end):
                if self.C1.Is_won():
                    print("L'équipe 1 à gagné fin de jeu ")
                    t.sleep(3)
                    self.A1.master.master.destroy()
                    exit()
                elif self.C2.Is_won():
                    print("L'équipe 2 à gagné fin de jeu ")
                    t.sleep(3)
                    self.A2.master.master.destroy()
                    exit()
                elif x and y and k>0:
                    t.sleep(1)
                    texte1="Tour N°: "+str(k) +" Coups restants " + str(self.C1.moves_left) 
                    texte2="Tour N°: "+str(k) +" Coups restants " + str(self.C2.moves_left)
                    self.A1.itemconfig(self.A1.texte,text=texte1)
                    self.A2.itemconfig(self.A2.texte,text=texte2)
                    x=self.A1.winfo_exists()
                    y=self.A2.winfo_exists()
            if x and y:
                next_turn(self,self.A1,self.A2,self.C1,self.C2)
    def stop(self):
        self.keep_going=False

k=0
def next_turn(t_prec,A1,A2,C1,C2):
    global k
    if k==0:
        A1.Board_normal()
        A2.Board_normal()  
        C1.etape="Mid"
        C2.etape="Mid"
    t_prec.stop()
    A1.end=False
    A2.end=False
    k+=1
    C1.moves_left+=1
    C2.moves_left+=1    
    t = MyThread(A1,A2,C1,C2)
    t.start()
def Get_team_compositions(team_size):
    Lgetperso=[Personnages.Fast,Personnages.Sniper,Personnages.Tank,Personnages.Assassin,Personnages.Builder,Personnages.Breaker,Personnages.Teleport,Personnages.Healer]
    Listeperso =['Fast','Tank','Sniper','Assassin',"Builder","Breaker","Teleport","Healer"]
    
    T1=[]
    T2=[]
    
    root = tk.Tk()

    form = C.CharacterSelectForm(root, Listeperso, team_size)
    result = form.run()

    if result is None:
        return None
    
    else:
        for elt in form.team_1:
            for Perso in Lgetperso:
                if elt==Get_name(Perso()):
                    T1.append(Perso())
        for elt in form.team_2:
            for Perso in Lgetperso:
                if elt==Get_name(Perso()):
                    T2.append(Perso())
    root.destroy()
    return T1,T2

def Run():
    teams=Get_team_compositions(4)
    root = tk.Tk()
    game1 = tk.Toplevel(root)
    game2 = tk.Toplevel(root) 
    
    pla=[[0 for k in range (7)] for k in range (11)]
    Game_state=(pla,teams)
    
    size=50
    
    game1.title("Joueur1")
    C1=cft.Conflict(Game_state, 1)
    A1=A.Affichage(game1,size,Game_state,1,game2,C1)
    
    A1.pack()
    
    game2.title("Joueur2")
    C2=cft.Conflict(Game_state, 2)
    A2=A.Affichage(game2,50,Game_state,2,game1,C2)
    A2.pack()
    
    A1.Board_ini()
    A2.Board_ini()
    
    A1.othercanvas=A2
    A2.othercanvas=A1

    t = MyThread(A1,A2,C1,C2)

    t.start()
    root.mainloop()
    t.stop()
    t.join()
Run()