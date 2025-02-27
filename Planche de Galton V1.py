""" 
Date : 27/02/25
Author : PAUL-CAMUS Akira ; LHERMITTE Léo 
"""

import random
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import Tk, Button, Label, Frame, ttk, Entry, StringVar, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Arbre:
    '''Constructeur de la classe Arbre, défini par le niveau de l'arbre (sa hauteur),
    et dans un second temps on crée l'arbre en emboitant des listes.'''
    def __init__(self,niveau):
        self.niveau=niveau
        self.arbre=self.creer_arbre(niveau)

    def creer_arbre(self,niveau):
        '''Construit un arbre binaire de profondeur donnée avec des feuilles
        initialisées à 0.'''
        if niveau==0:
            return [0,[],[]]
        return [None,Arbre(niveau-1),Arbre(niveau-1)]

    def est_vide(self):
        '''Vérifie si un arbres est vide.'''
        return self.niveau==0

    def est_feuille(self,arbre):
        '''Vérifie si un nœud est une feuille.'''
        return arbre==[]

    def inserer_bille(self,niveaux,position,distribution={}):
        '''Fait tomber une bille dans l'arbre jusqu'à une feuille en respectant
         la loi binomiale. Cette fonction est dépendante de la fonction
         laisser_tomber_n_bille(self,nb_billes)'''
        if self.niveau==0:
            distribution[position]+=1
            return
        if random.random() < 0.5:
            self.arbre[1].inserer_bille( niveaux-1, position, distribution)
        else:
            self.arbre[2].inserer_bille( niveaux-1, position+1, distribution)

    def laisser_tomber_n_billes(self,nb_billes):
        '''Simule la chute d'un nombre de billes dans l'arbre en les
        répartissant correctement. Cette fonction est dépendante de la fonction
        inserer_bille(self,niveaux,position,distribution={})'''

        distribution={}
        for i in range(0,self.niveau+1):
            distribution[i]=0
        for _ in range(nb_billes):
            self.inserer_bille(self.niveau,0,distribution)

        return distribution


class MyWindow(Tk):
    '''Initialisation de la classe MyWindow a partir de tkinter.'''
    def __init__(self):
        '''Constructeur de la classe MyWindow de tkinter.'
           Toutes les entrées'''
        super().__init__()

        #On défini le nombre de billes et colonnés qui sera modifié plus tard et une figure et un canvas pour tkinter
        self.nb_billes = StringVar()
        self.nb_colonnes = StringVar()
        self.figure = None
        self.canvas = None

        # Crée un panneau a gauche on l'on mettra les labels pour les paramètres
        left_frame = Frame(self, bg='#FFFFFF', width = 200)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)

        # Crée un label pour le titre en haut de la fenetre
        label = Label(self, text='\n Simulation de la planche de Galton \n',fg='black', bg='#1e7ac7',justify='center', font=('Arial', 14, 'bold'))
        label.pack(side='top', fill='x')

        #Crée un label affichant le titre de la zone des paramètres
        menu = Label(left_frame, text='Paramètres', font=('Arial',11))
        menu.pack(side = 'top',fill='x')

        #Crée un séparateur entre les paramètre et la courbe
        separator = ttk.Separator(left_frame, orient='horizontal')
        separator.pack(fill='x')

        #Label des billes et zone pour écrire le nombre de billes pour la simulation
        billes = Label(left_frame,text='Entrez le nombre de billes :')
        billes.pack(side = 'top', fill = 'x')
        self.nb_billes_entry = Entry(left_frame, textvariable = self.nb_billes)
        self.nb_billes_entry.pack(side='top')

        #De même que pour les billes mais pour les colonnes
        colonnes = Label(left_frame,text='Entrez le nombre de colonnes :')
        colonnes.pack(fill='x')
        self.nb_colonnes_entry = Entry(left_frame, textvariable = self.nb_colonnes)
        self.nb_colonnes_entry.pack(side='top')

        #Bouton permettant de lancer la simulation avec les paramètre écrits plus tôts
        button = Button(left_frame, text='Valider',bg = '#1e7ac7', command=self.run_simulation)
        button.pack(fill='x',padx=40, pady=10)

        #Petit séparateur entre les paramètres actuels et ceux a rentrée
        separator_2 = ttk.Separator(left_frame, orient='horizontal')
        separator_2.pack(fill='x')

        #Zone ou seront écrit les paramètres actuels
        settings = Label(left_frame, text='Paramètres actuels',font=('Arial',11))
        settings.pack(fill='x')

        #Labels affichant les paramètres qui ont été utilisé pour les paramètres de la simulation visible
        self.billes_label = Label(left_frame, text='Nombre de billes : 0', fg='black',bg='#FFFFFF')
        self.billes_label.pack(fill='x')
        self.colonnes_label = Label(left_frame,text='Nombre de colonnes: 0',fg='black',bg='#FFFFFF')
        self.colonnes_label.pack(fill='x')

        #Panneau pour mettre la courbes
        self.graph_frame = Frame(self, bg='#f0f0f0')
        self.graph_frame.pack(side='right', expand=True, fill='both')

        #Taille et titre de la fenetre
        self.geometry('900x600')
        self.title('Simulation planche de Galton')

    def afficher_graphe(self,distribution,n,nb_bille):
        '''Méthode permettant l'affichage de la répartition des
         billes et de la courbe de Gauss'''
        #Supprime le graphe précédent pour en afficher un autre
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        #Abscisse
        x=list(distribution.keys())
        y=list(distribution.values())

        #Crée la courbe de Gauss
        n = max(x)
        nb_billes = sum(y)
        mu = n/2
        sigma = np.sqrt(n)/2
        x_gauss = np.linspace(min(x),max(x),100)
        y_gauss = (nb_billes/(sigma*np.sqrt(2*np.pi)))*np.exp(-((x_gauss - mu) ** 2) / (2 * sigma ** 2))

        #Crée un graphe Mathplotlib
        self.figure, ax = plt.subplots(figsize=(6, 4))

        #On ajoute au graphe la courbe de gauss, l'histogramme des bille et la légende qui va avec
        ax.bar(x, y, color='#4682b4', alpha=0.6, label='Répartition des billes')
        ax.plot(x_gauss, y_gauss, color='red', linewidth=2, label='Courbe de Gauss')
        ax.set_xlabel('colonnes')
        ax.set_ylabel('Nombres de billes')
        ax.legend()

        #On place le canvas de Mathplotlib au sein de la fenetre Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def run_simulation(self):
        '''Méthode permettant de lancer la simulation de la planche de Galton'''
        try :
            #On récupere les valeurs entrées par l'utilisateur dans la zone des Paramètres
            nb_billes = int(self.nb_billes.get().strip())
            nb_colonnes = int(self.nb_colonnes.get().strip())

            #Vérifie si chaque champs des paramètres sont correctement remplis
            if nb_billes <= 0 :
                messagebox.showerror('Erreur', 'Le nombre de billes doit être un entier positif.')
                return
            if nb_colonnes <= 0:
                messagebox.showerror('Erreur', 'Le nombre de colonnes doit être un entier positif.')
                return
            if nb_billes>=1000000:
                messagebox.showerror('Attention','Le nombre important de billes risque de fortement ralentir la machine, veuillez baisser ce nombre')
            if nb_colonnes>=15:
                messagebox.showerror('Attention','Le nombre important de colonne risque de fortement ralentir la machine, veuillez baisser ce nombre')

            #On met a jour la zone des paramètres actuels avec... les paramètres actuels
            self.billes_label.config(text=f'Nombre de billes : {nb_billes}')
            self.colonnes_label.config(text=f'Nombre de colonnes : {nb_colonnes}')

            #On lance la simulation dans un arbre et on affiche le tout
            arbre = Arbre(nb_colonnes - 1)
            distribution = arbre.laisser_tomber_n_billes(nb_billes)
            self.afficher_graphe(distribution, nb_colonnes, nb_billes)

        except ValueError:
                    # Gestion des erreurs avec une boîte de message
                    messagebox.showerror('Erreur', 'Veuillez entrer un nombre entier valide dans chaque champ avant de valider.')

# On crée notre fenêtre et on l'affiche
if __name__ == '__main__' :
    window = MyWindow()
    window.mainloop()
