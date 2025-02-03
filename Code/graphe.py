import random
import pygame
import math

class Graphe:

    def __init__(self, n):
        self.taille = n
        self.l_adj = [[]for i in range(self.taille)]

    def rand_graph_coord(self, p, CENTER, RADIUS):
        """Graphe aléatoire coordonnées"""
        for k in range(self.taille):
            angle = 2 * math.pi * k / self.taille
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            self.l_adj[k].append([x,y, (255, 0, 0)])

        for i in range (self.taille):
            for j in range (i+1, self.taille):
                x = random.random()

                if x < p:
                    self.l_adj[i].append(j+1)
                    self.l_adj[j].append(i+1)

    def force_graph_coord(self, graphe):
        """Graphe non aléatoire coordonnées"""
        self.l_adj = graphe

    def change_coordonne(self, CENTER, RADIUS):
        """Changer les coordonnées en fonction de la taille de la page"""
        for k in range(self.taille):
            angle = 2 * math.pi * k / self.taille
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            self.l_adj[k][0][0] = x ; self.l_adj[k][0][1] = y


    def draw_point(self, screen):
        """Dessiner les points du graphes en prenant en compte leur couleur"""
        for k in range(self.taille):
            x = self.l_adj[k][0][0]
            y = self.l_adj[k][0][1]
            color = self.l_adj[k][0][2]
            pygame.draw.circle(screen, color, (int(x), int(y)), 8)

    def couleur_aleatoire(self):
        """Permet d'attribuer des couleurs aléatoires aux points du graphe"""
        for o in range(self.taille):
            c1 = random.randint(0, 256)
            c2 = random.randint(0, 256)
            c3 = random.randint(0, 256)
            self.l_adj[o][0][2] = (c1, c2, c3)

    def donne_couleur(self, point:int, color):
        """Permet d'attribuer une couleur à un point du graphe"""
        ind = point - 1
        self.l_adj[ind][0][2] = color
    
    def verification_voisin_point(self, point:int):
        """Vérifie que tout les voisins d'un points ont une couleur différente"""
        ind = point - 1
        color = self.l_adj[ind][0][2]
        couleur_differente = True
        for q in range(1,len(self.l_adj[ind])):
            color_v = self.l_adj[self.l_adj[ind][q]-1][0][2] # Sélectionne la couleur du voisin q du point du graphe
            if color == color_v:
                couleur_differente = False
        return couleur_differente
    
    def verification_colorimetrie_graphe(self):
        """Vérifie que tout les points du graphes on des voisins avec des couleurs différentes"""
        couleur_differente = True
        for r in range(self.taille):
            if not self.verification_voisin_point(r):
                couleur_differente = False
        return couleur_differente