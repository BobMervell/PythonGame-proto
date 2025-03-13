# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:18:47 2023

@author: LUCAS
"""

class Personnages:
    def __init__(self,Att,Def,Vit,Por,Vis,Pos,Capa):
        self.Nom=self.__class__.__name__
        self.Att=Att
        self.Def=Def
        self.Defmax=Def
        self.Por=Por
        self.Vit=Vit
        self.Vis=Vis
        self.Capa=Capa
        self.Pos=Pos
                
    def __str__(self):
        # if self.Nom=="Assassin":
        #     print(self.True_pos)
        return self.Nom + ":\n Attaque: " + str(self.Att)  + "\n Défense: " + str(self.Def)+"\n Vitesse: "+str(self.Vit) +"\n Portée: " + str(self.Por) +   "\n Capacitée: " + self.Capa +"\n Position: " + str(self.Pos)

class Fast(Personnages):
    def __init__(self):
        super().__init__(Att=800,Def=1000,Vit=3,Por=2,Vis=5,Pos=(0,0),Capa="Aucune")
        
    def Move(self,New_Pos):
        self.Pos=New_Pos
        
class Tank(Personnages):
    def __init__(self):
        super().__init__(Att=1000,Def=2000,Vit=1,Por=1,Vis=5,Pos=(0,0),Capa="Aucune")
        
    def Move(self,New_Pos):
        self.Pos=New_Pos
        
class Healer(Personnages):
    
    def __init__(self):
        super().__init__(Att=600,Def=1500,Vit=2,Por=2,Vis=5,Pos=(0,0),Capa="Heal")
        self.Capacite=False
        
    def Move(self,New_Pos):
        self.Pos=New_Pos

        
class Teleport(Personnages):
    def __init__(self):
        super().__init__(Att=900,Def=1100,Vit=2,Por=2,Vis=5,Pos=(0,0),Capa="Teleport")
        self.Capacite=False
        
    def Move(self,New_Pos):
        self.Pos=New_Pos
        
class Builder(Personnages):
    def __init__(self):
        super().__init__(Att=600,Def=1700,Vit=1,Por=1,Vis=5,Pos=(0,0),Capa="Construire")
        self.Capacite=False
        
    def Move(self,New_Pos):
        self.Pos=New_Pos 
        
class Breaker(Personnages):
    def __init__(self):
        super().__init__(Att=1100,Def=1200,Vit=1,Por=1,Vis=5,Pos=(0,0),Capa="Détruire")
        self.Capacite=False
        
    def Move(self,New_Pos):
        self.Pos=New_Pos    
        
class Sniper(Personnages):
    def __init__(self):
        super().__init__(Att=900,Def=1100,Vit=1,Por=3,Vis=7,Pos=(0,0),Capa="Aucune")
        
    def Move(self,New_Pos):
        self.Pos=New_Pos
                
class Assassin(Personnages):
     def __init__(self):
         super().__init__(Att=1500,Def=900,Vit=1,Por=2,Vis=5,Pos=(0,0),Capa="Feinte")
         self.True_pos=self.Pos
         self.Capacite=False
         self.used=False

     def Move(self,New_Pos):
        if self.Capacite==True:
            self.Pos=New_Pos
            self.used=True
            
        elif self.used==True:
            diffi=self.True_pos[0]-self.Pos[0]
            diffj=self.True_pos[1]-self.Pos[1]
            self.True_pos=New_Pos
            self.Pos=(New_Pos[0]-diffi,New_Pos[1]-diffj)
            if self.Pos[0] < 0 or  self.Pos[0] > 10 or  self.Pos[1] < 0 or  self.Pos[1] > 6:
                self.used=False
                self.Pos=self.True_pos
        else:
            self.Pos=New_Pos
            self.True_pos=New_Pos

class Wall(Personnages):
    def __init__(self):
        super().__init__(Att=0,Def=99999999,Vit=0,Por=0,Vis=0,Pos=(0,0),Capa="Aucune")
    
    def Move(self,New_Pos):
        self.Pos=New_Pos