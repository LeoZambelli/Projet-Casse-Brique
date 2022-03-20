#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Léo
#
# Created:     16/12/2020
# Copyright:   (c) Léo 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from upemtk import *
from time import time, sleep
from random import randint
from tkinter import*
from winsound import*
from os import*
from math import*



# Inititalisation des variables
ml=True
dx,dy=10,10
cx,cy= 500,450
dirx=1
diry=-1
r=10
tx,ty= 100,80
dep = 10
compteur=0
trait=[[0]*10 for l in range(5)]
x,y=400,350
flag=0
largeur = 800
hauteur = 600



#Création de la fenêtre de jeu
m=cree_fenetre(largeur, hauteur)

# liste de couleurs pour les briques
palette = ["lightsalmon", "coral", "tomato", "orangered","darkorange","orange"]


#On génère l'aire de jeu avecc une image au centre
rectangle(0, 0, largeur, hauteur,
              couleur='white', remplissage='blue', epaisseur=5, tag='')
image(400, 300, "vortex.png", ancrage=CENTER, tag='')

#Création du mur de briques, avec les couleurs de la liste choisies au hasard
for k in range(10):
    for l in range(5):
        a = randint(0,5)
        coul= palette[a]

        rectangle(80*k,30*l , 80*(k+1), 30*(l+1),couleur='blue', remplissage=coul, epaisseur=3, tag='')





#Création d'une fonction score contenant une indication textuelle "Score :" ainsi qu'un compteur qui affiche le score obtenu.
def score():
    global tx,ty,dirx,diry,r,cx,cy,compteur
    texte(760, 560, "Score : ",couleur='black', ancrage=SE, police="OCR A Extended", taille=24, tag='')
    mise_a_jour()
    compt=str(compteur)
    texte(780, 560, compt,couleur='black', ancrage=SE, police="OCR A Extended", taille=24, tag='sc')
    mise_a_jour()

#Création d'une fonction pour générer la barre de jeu
def barre():
    global cx, cy
    rectangle(cx, cy, cx+50, cy+5,couleur='cyan', remplissage='cyan', epaisseur=3, tag='barre')







#Vréation d'une fonction pour générer la balle. La direction de celle-ci (verticale ou horizontale) est inversée lorsqu'elle commence à atteindre les limites de la fenêtre. Lorsqu'elle détruit une brique, un son est émis et le compteur s'incrémente de 1.
def balle():
    global x,y,dirx,diry,r,compteur
    if y<10 or y>590:
        diry=-diry
    if  x<10 or x>790:
        dirx=-dirx
    for k in range(10):
        for l in range(5):
            if 80*k < x<80*k+80 and 30*l<y<30*l+30 and trait[l][k]==0:
                    import winsound
                    winsound.PlaySound('Metal Hit FX 02-wav.wav',winsound.SND_FILENAME|winsound.SND_ASYNC)
                    diry=-diry
                    rectangle(80*k,30*l , 80*(k+1), 30*(l+1),couleur='blue', remplissage="blue", epaisseur=3, tag='')
                    compteur+=1
                    efface('sc')
                    trait[l][k]=1

                    score()







#Lorsque la balle touche la barre, un autre son est émis.
    if cx <=x <= cx+100 and y==cy:
            import winsound
            winsound.PlaySound('Dodgeball-sound-effect.wav',winsound.SND_FILENAME|winsound.SND_ASYNC)
            diry=-diry




    x+=5*dirx
    y+=4*diry

    cercle(x, y, r, couleur='black', remplissage='grey', epaisseur=1, tag='cc')

    mise_a_jour()
score()
ml=True
while ml:
    efface("cc")
    balle()
    barre()
    sleep(0.0001)
    ev = donne_evenement()
    tev = type_evenement(ev)

#Mise en place des différentes commandes du jeu
    if tev == 'Quitte':
        ml=False
    if tev == 'Touche':
        nom_touche = touche(ev)
        if nom_touche == 'Space':
            ml=False
        # Lorsque la flèche de gauche est pressée, la barre se déplace vers la gauche.
        if nom_touche == 'Left':
            cx+= -50
        # Lorsque l'on presse la touche de gauche et que la balle atteint le centre de l'image, la trajectoire de la balle est déviée selon le cercle trigonométrique.
        if x ==400 and y ==300 and nom_touche=='Left':
            diry=diry*(5*pi/6)

        # Lorsque la flèche de droite est pressée, la barre se déplace vers la droite.
        elif nom_touche == 'Right':
            cx+=50
        # Lorsque l'on presse la touche de droite et que la balle atteint le centre de l'image, la trajectoire de la balle est déviée selon le cercle trigonométrique.
        if x ==400 and y ==300 and nom_touche=='Right':
            diry=diry*(pi/6)

        # Lorsque l'on appuie sur le p miniscule, le jeu se met en pause pendant 5 secondes et un son est émis.
        if  nom_touche=='p':
            import winsound
            winsound.PlaySound('OCLOCK-TIME-SOUND-EFFECT-YOUTUBER-freedownload.wav',winsound.SND_FILENAME|winsound.SND_ASYNC)
            sleep(5)

        #Lorsque l'on appuie sur le touche Echap ou Escape, la fenêtre de jeu se ferm, cela permet de quitter la partie.
        if nom_touche=='Escape':
            ferme_fenetre()
    if cx != 0 :
        efface('barre')
        rectangle(cx, cy, cx+100, cy+5,couleur='black', remplissage='black', epaisseur=3., tag='barre')

    # Une fois que lintégralité des briques est détruite, un image s'affiche nous indiquant que l'on a gagné et une petite musique est jouée.
    if compteur==50:
        image(400, 300, "you win.png", ancrage=CENTER, tag='win')
        mise_a_jour()
        import winsound
        winsound.PlaySound('Heart-Container-Get-The-Legend-of-Zelda-Twilight-Princess-hd.wav',winsound.SND_FILENAME|winsound.SND_ASYNC)
        ml=0

    # S'il on atteint le bas de la zone de jeu, on a perdu la partie, une image s'affiche, et la fenêtre se ferme au bout de 3 secondes.
    if y>590:
        image(400, 300, "game over.png", ancrage=CENTER, tag='g_over')
        mise_a_jour()
        import winsound
        winsound.PlaySound('game_over.wav',winsound.SND_FILENAME|winsound.SND_ASYNC)
        sleep(3)
        ferme_fenetre()



