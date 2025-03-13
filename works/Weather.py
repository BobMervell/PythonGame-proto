# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:26:40 2023

@author: LUCAS
"""
import Personnages

class Weather:
    def __init__(self,Game_state):
        self.Game_state=Game_state
        self.Nb_Rain=6
        self.Nb_Sun=6
        self.Nb_Snow=4
        self.Nb_Wind=5
        self.Nb_Sand=3
        self.Rain=(False,0)
        self.Sun=(False,0)
        self.Snow=(False,0)
        self.Wind=(False,0)
        self.Sand=(False,0)
    
    def Set_rain(self):
        self.Rain=(True,self.Nb_Rain)
        self.Sand=(False,0)
        self.Snow=(False,0)

    def Set_sun(self):
        self.Sun=(True,self.Nb_Sun)
        self.Snow=(False,0)

    def Set_Snow(self):
        self.Snow=(True,self.Nb_Snow)
        self.Sand=(False,0)
        self.Rain=(False,0)
   
    def Set_wind(self):
        self.Wind=(True,self.Nb_Wind)
    
    def Set_sand(self):
        self.Sand=(True,self.Nb_Sand)
        self.Sun=(False,0)
        self.Rain=(False,0)
        self.Snow=(False,0)
        
            
    def Weather_turn(self):
        if self.Rain[0] and self.Sun[0]:
            self.Rainbow()
            self.Rain[1]-=1
            self.Sun[1]-=1
        elif self.Wind[0] and self.Snow[0]:
            self.Snow_storm()
            self.Wind[1]-=1
            self.Snow[1]-=1
        elif self.Wind[0] and self.Sand[0]:
            self.Sand_storm()
            self.Wind[1]-=1
            self.Sand[1]-=1
        else:
            if self.Rain[0]:
                self.Rain[1]-=1
                self.Rainy()
            if self.Sun[0]:
                self.Sun[1]-=1
                self.Sunny
            if self.Wind[0]:
                self.Wind[1]-=1
                self.Windy()
            if self.Snow[0]:
                self.Snow[1]-=1
                self.Snowy()
            if self.Sand[0]:
                self.Sand[1]-=1
                self.Sandy()
                
    def Rainy(self):
        if self.Rain[1]==self.Nb_Rain:
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por-1
        elif self.Rain[1]==0:
            self.Rain=(False,1)
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por
    
    def Sunny(self):
        if self.Sun[1]==self.Nb_Sun:
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por+1
                    perso.Def-=perso.Def/10
                    
        elif self.Sun[1]==0:
            self.Sun=(False,1)
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por
        else:
            perso.Def-=perso.Def/10
        self.Sun[1]-=1
        
    def Sandy(self):
        if self.Sand[1]==self.Nb_Sand:
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por-2
                    perso.Def-=perso.Def/16
                    
        elif self.Sand[1]==0:
            self.Sand=(False,1)
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por
        else:
            perso.Def-=perso.Def/16
        
    def Snowy(self):
        if self.Snow[1]==self.Nb_Snow:
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Por=Personnages.Nom.Por-1
                    perso.Vit=Personnages.Nom.Vit-1
                    #Sauf pour les volants,leur vitesse reste inchangé
                    #mais ils marche desormais
                    perso.Def-=perso.Def/16
                    
        elif self.Snow[1]==0:
            self.Snow=(False,1)
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    perso.Por+=1
                    perso.Vit+=1
        else:
            perso.Def-=perso.Def/16
        
    def Windy(self):
        if self.Wind[1]==self.Nb_Wind:
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Vit=Personnages.Nom.Vit-1
                    #Sauf pour les volants,leur vitesse perd 2
                    if perso.Name=="Sniper":
                        perso.Por=Personnages.Nom.Por-1
                    
        elif self.Wind[1]==0:
            self.Wind=(False,1)
            teams=self.Game_state[1]
            for team in teams:
                for perso in team:
                    Nom=perso.Name
                    perso.Vit=Personnages.Nom.Vit
                    if perso.Name=="Sniper":
                        perso.Por=Personnages.Nom.por
                        
                        
'''Faire en sorte que pour tout les temps
 et quelque sois le tour, ca réinitialise 
 le stats porté vitesse ... comme il faut
        