import random
import pygame
import math

class Graphe:
    def __init__(self, n):
        self.taille = n
        self.l_adj = [ [] for i in range(self.taille)]

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


    def draw_point(self, screen, font):
        """Dessiner les points du graphes en prenant en compte leur couleur"""
        for k in range(self.taille):
            x = self.l_adj[k][0][0]
            y = self.l_adj[k][0][1]
            color = self.l_adj[k][0][2]
            pygame.draw.circle(screen, color, (int(x), int(y)), 14)
            
            # Ajout du numéro du noeud à sa droite
            num = font.render(str(k + 1), True, (255, 255, 255))
            num_x = int(x) + 25
            num_y = int(y) - num.get_height() // 2
            screen.blit(num, (num_x, num_y))

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

    def voisin_point(self, point:int):
        """Permet de connaitre les voisins d'un point"""
        ind = point - 1
        for e in range(1,len(self.l_adj[ind])):
            print(self.l_adj[ind][e])
    
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

    def verification_voisin_point_couleur(self, point:int, couleur):
        """Vérifie que tout les voisins d'un points ont une couleur différente de la couleur donnée en paramètre"""
        ind = point - 1
        couleur_presente = False
        for q in range(1,len(self.l_adj[ind])):
            color_v = self.l_adj[self.l_adj[ind][q]-1][0][2] # Sélectionne la couleur du voisin q du point du graphe
            if color_v == couleur:
                couleur_presente = True
        return couleur_presente
    
    def verification_colorimetrie_graphe(self):
        """Vérifie que tout les points du graphes on des voisins avec des couleurs différentes"""
        couleur_differente = True
        for r in range(self.taille):
            if not self.verification_voisin_point(r):
                couleur_differente = False
        return couleur_differente


    # Algorithme glouton 1
    def glouton1(self,liste_couleur, ordre_priorite):
        """Attribue les couleurs du graphes avec un ordre de priorité"""
        for elem in ordre_priorite:
            couleur_valide = False
            ind_couleur = 0
            while not couleur_valide and ind_couleur < len(ordre_priorite):
                couleur_valide = not self.verification_voisin_point_couleur(elem, liste_couleur[ind_couleur])
                if couleur_valide:
                    self.l_adj[elem - 1][0][2] = liste_couleur[ind_couleur]
                ind_couleur += 1
    
    # Algorithme glouton 2
    def glouton2(self, liste_couleur):
        """Fait appel au premier algorithme glouton en lui soumettant un
        ordre de priorité qui correspond à l'ordre inverse des plus petits
        degrés calculés en enlevant les points déjà calculés"""

        # Construction d'un tableau temporaire des lien
        tab_lien = [[] for u in range(self.taille)]
        for v in range(self.taille):
            for w in range(1,len(self.l_adj[v])):
                tab_lien[v].append(self.l_adj[v][w])

        liste_termine = False
        liste_point = []
        while not liste_termine:
            
            # Obtention de la première valeur en vue d'une comparaison
            cherche_donnee = True
            i = 0
            while cherche_donnee and i <= len(tab_lien):
                if len(tab_lien[i]) != 0:
                    minim = [tab_lien[i], len(tab_lien[i]), i + 1]
                    cherche_donnee = False
                i += 1

            # Iteration jusqu'a obtenir le minimum de la liste
            for y in range(0, self.taille):
                if len(tab_lien[y]) < minim[1] and len(tab_lien[y]) != 0:
                    minim = [tab_lien[y], len(tab_lien[y]), y + 1]
            
            # On enleve le points pour la suite du programme
            liste_point.append(minim[2])
            for z in range(minim[1]):
                ind = minim[0][0] # Et pas minim[0][z] car la liste se réduit au fur et a mesure (puisque l'on supprime les éléments)
                minim[0].remove(ind)
                tab_lien[ind-1].remove(minim[2])
                stock = ind

            # Si le tableau des lien est vide on s'arrête
            liste_termine = True
            for x in range(self.taille):
                if len(tab_lien[x]) > 0:
                    liste_termine = False
            if liste_termine:
                liste_point.append(stock)

        ordre_priorite = liste_point[::-1]
        self.glouton1(liste_couleur, ordre_priorite)