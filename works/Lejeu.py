# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:25:53 2023

@author: LUCAS
"""
import copy as C
import Personnages

def Plateau():
    Plat=[[0 for i in range (7)] for i in range (11)]
    return Plat

def Compo_Team(nbr):
    Listeperso =[Personnages.Fast,Personnages.Tank,Personnages.Sniper]
    team1=[]
    team2=[]
    print("Choix des personnages pour l'équipe 1 : ")
    for i in range(nbr):
        for j, personnage in enumerate(Listeperso):
            print(j+1, personnage.__name__)
        choix =input("Choisissez le numéro du personnage "+str(i+1)+" : ")
        
        while not choix.isdigit() or int(choix)<1 or int(choix)>len(Listeperso):
            choix = input("Numéro invalide veuillez recommencez ")
        Perso=Listeperso[int(choix)-1]
        P=Perso()
        team1.append(P)
            
        
    print("Choix des personnages pour l'équipe 2 : ")
    for i in range(nbr):
        for j, personnage in enumerate(Listeperso):
            print(j+1, personnage.__name__)
        choix =input("Choisissez le numéro du personnage "+str(i+1)+" : ")
        
        while not choix.isdigit() or int(choix)<1 or int(choix)>len(Listeperso):
            choix = input("Numéro invalide veuillez recommencez ")
        Perso=Listeperso[int(choix)-1]
        P=Perso()
        team2.append(P)
    
    return team1,team2

"Surement à mettre dans l'autre fichier"
def Get_Position():  
    pos=input("Rentrez la position désirée (ex: C 5): ")
    if pos=="echap" or pos=="Echap" or pos=="ECHAP":
        Abort()
    Lpos=pos.split()
    while len(Lpos)==0 or not Lpos[-1].isdigit() or int(Lpos[-1])<1 or int(Lpos[-1])>16 or len(Lpos)!=2 or (Lpos[0]!='A' and Lpos[0]!='B'and Lpos[0]!='C' and Lpos[0]!='D' and Lpos[0]!='E' and Lpos[0]!='F'and Lpos[0]!='G'and Lpos[0]!='H'):
        pos = input("Position invalide, veuillez recommencer : ")
        if pos=="echap" or pos=="Echap" or pos=="ECHAP":
            Abort()
        Lpos=pos.split()
    ligne=int(Lpos[-1])
    L=['A','B','C','D','E','F','G','H']
    for i,elt in enumerate(L):
        if Lpos[0]==elt:
            col=i+1
    return ligne-1,col-1   

def Check_Reach(start, end, obstacles, nbr):
    Lmove = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    if start == end:
        return True
    elif nbr == 0:
        return False
    else:
        for move in Lmove:
            next_pos = start[0] + move[0], start[1] + move[1]
            if next_pos in obstacles or next_pos[0] < 0 or next_pos[0] > 15 or next_pos[1] < 0 or next_pos[1] > 7:
                continue
            else:
                if Check_Reach(next_pos, end, obstacles, nbr - 1):
                    return True
        return False

def Get_name(Perso):
    return Perso.Nom

def Get_info(pos,Game_state):
    txt=''
    teams=Game_state[1]
    for i,Team in enumerate(teams):
        for j,Perso in enumerate(Team):
            if Perso.Nom=="Assassin":
                if Perso.Pos==pos or Perso.True_pos==pos:
                    txt='Equipe '+ str(i+1)+ ' ' + str(Perso)
            if Perso.Pos==pos:
                txt='Equipe '+ str(i+1)+ ' ' + str(Perso)
    if Game_state[0][pos[0]][pos[1]] != 0:
        if Game_state[0][pos[0]][pos[1]].Nom=="Wall":
            txt=str(Game_state[0][pos[0]][pos[1]])
        
    return txt


def Find_obs(plateau):
    Lobs=[]
    for i,ligne in enumerate(plateau):
        for j,elt in enumerate(ligne):
            if elt==2:
                Lobs.append((i,j))
    return Lobs

def Range(Perso,plateau,stat):
    ligne,col=Perso.Pos
    L=[]
    if stat=='Vit':
        radius=Perso.Vit    
    if stat =='Por':
        radius=Perso.Por

    Lobs=Find_obs(plateau)
    for c in range(max(0, col - radius), min(len(plateau[0]), col + radius + 1)):
        for r in range(max(0, ligne - radius), min(len(plateau), ligne + radius + 1)):
            if (r,c) != Perso.Pos and (r - ligne) ** 2 + (c - col) ** 2 <= radius ** 2:
                L.append((Check_Reach(Perso.Pos,(r,c),Lobs,radius),(r,c)))
        return L
    
def Mod_Range(Perso,plateau,stat):
    L=Range(Perso,plateau,stat)
    for elt in L:
        ligne=elt[1][0]
        col=elt[1][1]
        if elt[0]:
            if plateau[ligne][col]==0:
                plateau[ligne][col]=1
            elif (ligne,col) not in Find_obs(plateau):
                plateau[ligne][col]=3
    return plateau

def Placement_Ini(Teams):
    plateau=Plateau()
    print("Placement initial de l'équipe 1: ")
    for Perso in Teams[0]:
        Affichage(plateau)
        print('Placement de : ' + Get_name(Perso))
        ligne,col=Get_Position()
        while plateau[ligne][col] != 0:
            print("Emplacement déjà pris veuillez recommencer: ")
            ligne,col=Get_Position()
        while ligne<0 or ligne>1:
            print("Position invalide veuillez recommencer: ")
            ligne,col=Get_Position()
        Perso.Move((ligne,col))
        plateau[ligne][col]=Perso
    Affichage (plateau)
    
    print("Placement initial de l'équipe 2: ")
    for Perso in Teams[1]:
        Affichage(plateau)
        print('Placement de : ' + Get_name(Perso))
        ligne,col=Get_Position()
        while plateau[ligne][col] != 0:
            print("Emplacement déjà pris veuillez recommencer: ")
            ligne,col=Get_Position()
        while ligne<9 or ligne>11:
            print("Position invalide veuillez recommencer: ")
            ligne,col=Get_Position()
        Perso.Move((ligne,col))
        plateau[ligne][col]=Perso
        print(plateau)
    Affichage(plateau)
    
    return plateau

def Affichage(plateau):
    print(' A B C D E F G H ')
    print(' _ _ _ _ _ _ _ _')
    for i,elt in enumerate(plateau):
        print('|',end='')
        for thing in elt:
            if thing==0:
                print('. ',end='')
            elif thing == 1:
                print('X ',end='')
            elif thing == 2:
                print('# ',end='')
            elif thing == 3:
                print('* ',end='')
            elif Get_name(thing)=='Sniper':
                print('S ',end='')
            elif Get_name(thing)== 'Tank':
                print('T ',end='')
            elif Get_name(thing)=='Fast':
                print('F ',end='')
            else:
                print('error ',end='')
        print('| '+ str(i+1))
    print(' _ _ _ _ _ _ _ _')

def Move(Perso,plateau):
    L=C.deepcopy(plateau)
    Lperso=['Sniper','Tank','Fast']
    Affichage(Mod_Range(Perso,L,'Vit'))
    ligne,col=Get_Position()
    obstacles=Find_obs(plateau)
    while not Check_Reach(Perso.Pos,(ligne,col),obstacles,Perso.Vit) or plateau[ligne][col] in Lperso:
        print("Position hors de portée veuillez recommencer: ")
        ligne,col=Get_Position()
    L0,C0=Perso.Pos
    plateau[L0][C0]=0
    plateau[ligne][col]=Perso
    Perso.Move((ligne,col))
    Affichage(plateau)
    return plateau

def Hit(Perso,plateau,Teams):
    L=C.deepcopy(plateau)
    Lperso=['Sniper','Tank','Fast']
    Affichage(Mod_Range(Perso,L,'Por'))
    print("Qui voulez vous attaquer: ")
    ligne,col=Get_Position()
    obstacles=Find_obs(plateau)
    while not (Check_Reach(Perso.Pos,(ligne,col),obstacles,Perso.Por)) or plateau[ligne][col] not in Lperso: #On redemande tant qu'il n'est pas dans la range max ou tant que la cible n'est pas un autre perso
        print("Position hors de portée ou aucune cible trouvée veuillez recommencer: ")
        ligne,col=Get_Position()
    for Team in Teams:
        for Cible in Team:
            if Cible.Pos==(ligne,col):
                Cible.Def=Cible.Def-Perso.Att
    return plateau 

def Check_life(teams,plateau):
    for Team in teams:
        L=[]
        for Num,Perso in enumerate(Team):
            if Perso.Def<= 0:
                L.append(Num)
        for Num in L:
            del Team[Perso]
            plateau[Perso.Pos[0]][Perso.Pos[1]]=0

def Check_win(teams, plateau):
    team1_win = False
    team2_win = False
    for Num, Perso in enumerate(teams[0]):
        if Perso.Pos[0] == 15:
            team1_win = True
    for Num, Perso in enumerate(teams[1]):
        if Perso.Pos[0] == 0:
            team2_win = True
    if team1_win and team2_win:
        print("Les deux équipes ont gagné!")
        return (True, 0)
    elif team1_win:
        print("L'équipe 1 a gagné!")
        return (True, 1)
    elif team2_win:
        print("L'équipe 2 a gagné!")
        return (True, 2)
    else:
        return (False, 3)

def Get_play(Perso,Plateau,Teams):
    print('1 Attaquer: ')
    print('2 Se déplacer:')
    move=input("Voulez vous attaquer ou vous déplacer: ")
    while not move.isdigit() or int(move)<1 or int(move)>2:
        move=input("Numéro invalide veuillez recommencer: ")
    if int(move)==2:
        return Move(Perso,Plateau)
    elif int(move)==1:
        return Hit(Perso,Plateau,Teams)
    
def Game(nbr_perso):
    print("Voici les règles :")
    print("démerde toi")
    Teams=Compo_Team(nbr_perso)
    Plateau=Placement_Ini(Teams)
    
    while not Check_win(Teams,Plateau)[0]:
        print("Au tour du joueur 1 :")
        for Num,Perso in enumerate(Teams[0]):
            Check_life(Teams,Plateau)
            Affichage(Plateau)
            print("Tour du personnage " + Get_name(Perso)+' '+ 'P'+ str(Num+1))   #Rajouter un get_name(perso)
            while True:
                try:
                    Plateau=Get_play(Perso,Plateau,Teams)
                    break
                except Exception as e:
                    print(e)
        print("Au tour du joueur 2 :")
        for Num,Perso in enumerate(Teams[1]):
            Affichage(Plateau)
            print("Tour du personnage " + Get_name(Perso)+' '+ 'P'+ str(Num+1))
            while True:
                try:
                    Plateau=Get_play(Perso,Plateau,Teams)
                    break
                except Exception as e:
                    print(e)
        
        Check_life(Teams,Plateau)
        
    Affichage(Plateau)
    return(Check_win(Teams, Plateau))

def Abort():
  raise Exception('Abandon')
        


#[[0, 0, 0, 0, 0, 0, 0, 0], ['Tank', 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 'Sniper'], [0, 0, 0, 0, 0, 0, 0, 0], [0, 'Fast', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 'Tank', 0, 0, 0, 0, 'Sniper'], [0, 0, 0, 0, 0, 'Fast', 0, 0]]

#Liste bugs, pour le joueur 2 pour le déplacement l'affichage de la portée ne se fait pas l'affichage à l'air d'aparaître a partir de la ligne 8 // Done
#Vu que le jeu fait joué 1 perso à la fois il n'est pas toujours possible d'avancer 2 perso lorsqu'ils se suivent
#Check_life n'est pas implémentée dans le Game //Done
#Rajoutr une fct abort // Done
#On sort de la boucle et je te tabasse pour bug 4 // Done?
#Mauvais affichage range d'attaque // D0ne
#Input vide fait crash // Done
#bug echap dans placement ini


#Tour du personnage P2
# 1 Attaquer: 
# 2 Se déplacer:

# Voulez vous attaquer ou vous déplacer: 1
#  A B C D E F G H 
#  _ _ _ _ _ _ _ _
# |. . . . . * T X | 1
# |. . . . . S X . | 2
# |. . . . . . . . | 3
# |. . . . . . . . | 4
# |. . . . . . . . | 5
# |. . . . . . . . | 6
# |. . . . . . . . | 7
# |. . . . . . . . | 8
# |. . . . . . . . | 9
# |. . . . . . . . | 10
# |. . . . . . . . | 11
# |. . . . . . . . | 12
# |. . . . . . . . | 13
# |. . . . . . . . | 14
# |S . . . . . F . | 15
# |. T . . . . . . | 16
#  _ _ _ _ _ _ _ _
# Qui voulez vous attaquer: 

# Rentrez la position désirée (ex: C 5): F 1
# {'P1': <Personnages.Fast object at 0x000001DC6F641B50>, 'P2': <Personnages.Tank object at 0x000001DC6F6418B0>, 'P3': <Personnages.Sniper object at 0x000001DC6F641C40>} 1
# [[0, 0, 0, 0, 0, 'Fast', 'Tank', 0], [0, 0, 0, 0, 0, 'Sniper', 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], ['Sniper', 0, 0, 0, 0, 0, 'Fast', 0], [0, 'Tank', 0, 0, 0, 0, 0, 0]] 2
# {'P2': <Personnages.Tank object at 0x000001DC6F6418B0>, 'P3': <Personnages.Sniper object at 0x000001DC6F641C40>} 3
# [[0, 0, 0, 0, 0, 'Fast', 'Tank', 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], ['Sniper', 0, 0, 0, 0, 0, 'Fast', 0], [0, 'Tank', 0, 0, 0, 0, 0, 0]] 4
#  A B C D E F G H 
#  _ _ _ _ _ _ _ _
# |. . . . . F T . | 1
# |. . . . . . . . | 2
# |. . . . . . . . | 3
# |. . . . . . . . | 4
# |. . . . . . . . | 5
# |. . . . . . . . | 6
# |. . . . . . . . | 7
# |. . . . . . . . | 8
# |. . . . . . . . | 9
# |. . . . . . . . | 10
# |. . . . . . . . | 11
# |. . . . . . . . | 12
# |. . . . . . . . | 13
# |. . . . . . . . | 14
# |S . . . . . F . | 15
# |. T . . . . . . | 16
#  _ _ _ _ _ _ _ _
# Tour du personnage P3
# 1 Attaquer: 
# 2 Se déplacer:

# Voulez vous attaquer ou vous déplacer: 1
#  A B C D E F G H 
#  _ _ _ _ _ _ _ _
# |. . . X X * * X | 1
# |. . X X X . X X | 2
# |. . . X X X X X | 3
# |. . . . X X X . | 4
# |. . . . . X . . | 5
# |. . . . . . . . | 6
# |. . . . . . . . | 7
# |. . . . . . . . | 8
# |. . . . . . . . | 9
# |. . . . . . . . | 10
# |. . . . . . . . | 11
# |. . . . . . . . | 12
# |. . . . . . . . | 13
# |. . . . . . . . | 14
# |S . . . . . F . | 15
# |. T . . . . . . | 16
#  _ _ _ _ _ _ _ _
# Qui voulez vous attaquer: 

# Rentrez la position désirée (ex: C 5): 