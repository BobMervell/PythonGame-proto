# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 11:00:00 2023

@author: LUCAS
"""

class Conflict():
    def __init__(self,Game_state,num):
        self.widget=None
        self.Game_state=Game_state
        self.num=num
        self.etape='Ini'
        self.moves_left=0
    
    def Good_team(self):
        if self.widget.perso in self.Game_state[1][self.num-1]:
            return True
        return False
    
    def Not_taken(self,i,j):
        if self.widget.perso.Pos!=(i,j):
            for i2,row in enumerate(self.Game_state[0]):
                for j2,perso in enumerate(row):
                    if perso!=0:
                        if perso.Nom=="Assassin" and (perso.Pos==(i,j) or perso.True_pos==(i,j)):
                            return False
                        elif perso.Pos==(i,j):
                            return False
        return True

    def Ini_ok(self,i,j):
        if self.num==1:
            if i>1:
                return False
        else:
            if i<9:
                return False
        return True
    
    def Check_reach(self,start,end,obstacles,nbr):
        Lmove = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if start == end:
            return True
        elif nbr == 0:
            return False
        else:
            for move in Lmove:
                next_pos = start[0] + move[0], start[1] + move[1]
                if next_pos in obstacles or next_pos[0] < 0 or next_pos[0] > 10 or next_pos[1] < 0 or next_pos[1] > 6:
                    None
                else:
                    if self.Check_reach(next_pos, end, obstacles, nbr - 1):
                        return True
        return False
    
    def Check_r_obstacless(self,start,end,nbr):
        Lmove = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if start == end:
            return True
        elif nbr == 0:
            return False
        else:
            for move in Lmove:
                next_pos = start[0] + move[0], start[1] + move[1]
                if next_pos[0] < 0 or next_pos[0] > 10 or next_pos[1] < 0 or next_pos[1] > 6:
                    None
                else:
                    if self.Check_r_obstacless(next_pos, end, nbr - 1):
                        return True
        return False
            
    def Find_obs(self):
        Lobs=[]
        for i,ligne in enumerate(self.Game_state[0]):
            for j,elt in enumerate(ligne):
                if elt!=0:
                    Lobs.append((i,j))
        return Lobs
    
    def Range(self,stat):
        if self.widget.perso.Nom=="Assassin":
            ligne,col=self.widget.perso.True_pos
        else:
            ligne,col=self.widget.perso.Pos
            
        L=[]
        Lobs=self.Find_obs()
        if stat=='Vit':
            if self.widget.perso.Nom=="Teleport" and self.widget.perso.Capacite==True:
                radius=self.widget.perso.Vit +1
                Lobs=[]
            else:
                radius=self.widget.perso.Vit
        if stat =='Por':
            radius=self.widget.perso.Por

        for i in range(len(self.Game_state[0])):
            for j in range (len(self.Game_state[0][i])):
                distance =int( ((i - ligne)**2 + (j - col)**2)**0.5)
                if distance <= radius:
                    L.append((self.Check_reach((ligne,col),(i,j),Lobs,radius),(i,j)))
        return L
    
    def Is_alive(self,perso):
        if perso.Def <= 0:
            return False
        return True
    
    def Is_won(self):
        if self.num==1:
            for elt in self.Game_state[1][0]:
                if elt.Nom=="Assassin" and elt.True_pos[0]==10:
                    return True
                elif elt.Nom !="Assassin" and elt.Pos[0]==10:
                    return True
            return False
        elif self.num==2:
            for elt in self.Game_state[1][1]:
                if elt.Nom=="Assassin" and elt.True_pos[0]==0:
                    return True
                elif elt.Pos[0]==0:
                    return True
            return False
                
    def Authorized_move(self,i,j):
        Ml=self.moves_left>0
        Nt=self.Not_taken(i,j)
        I=self.Ini_ok(i,j)
        
        Lobs=self.Find_obs()
        start=self.widget.perso.Pos    
        radius= self.widget.perso.Vit
        
        if self.widget.perso.Nom=="Assassin":
            start=self.widget.perso.True_pos
        elif self.widget.perso.Nom=="Breaker" and self.widget.perso.Capacite==True:
            Lobs=[]
            Nt=True
        elif self.widget.perso.Nom=="Teleport" and self.widget.perso.Capacite==True:
            Lobs=[]
            radius= self.widget.perso.Vit + 1
            
        elif self.widget.perso.Nom=="Healer" and self.widget.perso.Capacite==True:
             Lobs=[]
             Nt=True

        
        Cr=self.Check_reach(start,(i,j),Lobs ,radius)
        # print("0000000000000000",Cr,"Cr",Nt,"Nt",Ml,"Ml")
        # print(self.etape=='Mid' and Nt and Cr and Ml,"total")
        if self.etape=='Ini' and Nt and I:
            return True
        if self.etape=='Mid' and Nt and Cr and Ml:
            return True
        print("impossible")
        return False

    def Authorized_attack(self,i,j,perso):
        Ml=self.moves_left>0
        radius=perso.Por
        if self.widget.perso.Nom=="Assassin":
            if self.widget.perso.True_pos != self.widget.perso.Pos:
                self.widget.perso.Pos = self.widget.perso.True_pos
                window=self.widget.master.window
                window.Move()
                return False
            else:
                pi,pj=self.widget.perso.Pos
        else:
            pi,pj=self.widget.perso.Pos
        self.Game_state[0][pi][pj]=0
        Cr=self.Check_reach((i,j),(pi,pj), self.Find_obs(),radius)
        self.Game_state[0][pi][pj]=self.widget.perso
        if Cr and Ml:
            return True
        return False











        