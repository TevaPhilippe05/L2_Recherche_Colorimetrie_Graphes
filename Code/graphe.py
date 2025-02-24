import random
import pygame
import math

class Graphe:
    def __init__(self, n):
        self.taille = n
        self.l_adj = [[] for i in range(self.taille)]

    def graph_circulaire_aleatoire(self, p, CENTER, RADIUS):
        """Graphe aléatoire circulaire coordonnées"""
        for k in range(self.taille):
            angle = 2 * math.pi * k / self.taille
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            self.l_adj[k].append([x,y, (0,0,0), x, y])

        for i in range (self.taille):
            for j in range (i+1, self.taille):
                x = random.random()
                if x < p:
                    self.l_adj[i].append(j+1)
                    self.l_adj[j].append(i+1)

    def graph_non_circulaire_aleatoire(self, p, WIDTH, HEIGHT):
        """Graphe aléatoire non circulaire coordonnées"""
        self.points_aleatoires(WIDTH, HEIGHT)

        for i in range (self.taille):
            for j in range (i+1, self.taille):
                if random.random() < p:
                    self.l_adj[i].append(j+1)
                    self.l_adj[j].append(i+1)
    
    def graph_planaire_aleatoire(self, p, WIDTH, HEIGHT):
        """Génère un graphe planaire"""
        self.points_aleatoires(WIDTH, HEIGHT)

        for i in range(self.taille):
            for j in range(i + 1, self.taille):
                if random.random() < p and self.peut_ajouter_arete(i, j): # On va aussi vérifier qu'on peut placer l'arrête
                    self.l_adj[i].append(j + 1)
                    self.l_adj[j].append(i + 1)

    def points_aleatoires(self, WIDTH, HEIGHT):
        """Placement aléatoire des points"""
        for k in range(self.taille):
            x = random.randint(45, WIDTH - 45)
            y = random.randint(45, HEIGHT - 45)
            # Ici on essaye d'eloigner les points pour qu'ils ne soit pas superposés
            for j in range(10):
                for i in range(0, k):
                    while (self.l_adj[i][0][0] - x < 50 and self.l_adj[i][0][0] - x > -50) or (self.l_adj[i][0][1] - y < 50 and self.l_adj[i][0][1] - y > -50):
                        x = random.randint(45, WIDTH - 45)
                        y = random.randint(45, HEIGHT - 45)
            self.l_adj[k].append([x, y, (0,0,0), x, y]) # Fois 2 car on a les nouvelles coordonnées et les coordonnées initiales 

    def peut_ajouter_arete(self, i, j):
        """Vérifie si l'arête (i, j) ne coupe aucune autre"""
        A = (self.l_adj[i][0][0], self.l_adj[i][0][1]) # coord du premier point
        B = (self.l_adj[j][0][0], self.l_adj[j][0][1]) # coord du deuxieme point

        for u in range(self.taille):
            for v in self.l_adj[u][1:]:  # Vérifie toutes les arêtes déjà placées
                C = (self.l_adj[u][0][0], self.l_adj[u][0][1])
                D = (self.l_adj[v - 1][0][0], self.l_adj[v - 1][0][1])
                    
                if (A != C and A != D and B != C and B != D) and self.segments_se_croisent(A, B, C, D): # Si les sommet en ont un en commun ils se croisent pas
                    return False
        return True

    def segments_se_croisent(self, A, B, C, D):
        """Vérifie si les segments AB et CD se croisent
        J'utilise le produit vectoriel pour vérifier que A et B sont de part et d'autres de CD
        et que C et D sont de part et d'autre de AB.
        """
        val1 = (B[1] - A[1]) * (C[0] - B[0]) - (B[0] - A[0]) * (C[1] - B[1])
        val2 = (B[1] - A[1]) * (D[0] - B[0]) - (B[0] - A[0]) * (D[1] - B[1])
        val3 = (D[1] - C[1]) * (A[0] - D[0]) - (D[0] - C[0]) * (A[1] - D[1])
        val4 = (D[1] - C[1]) * (B[0] - D[0]) - (D[0] - C[0]) * (B[1] - D[1])
        
        return (val1 * val2 < 0 and val3 * val4 < 0)

    def force_graph_coord(self, graphe):
        """Graphe non aléatoire coordonnées"""
        self.l_adj = graphe

    def change_coordonne(self, WIDTH, HEIGHT, new_WIDTH, new_HEIGHT):
        """Changer les coordonnées en fonction de la taille de la page"""
        for k in range(self.taille):
            x = self.l_adj[k][0][3]/WIDTH * new_WIDTH
            y = self.l_adj[k][0][4]/HEIGHT * new_HEIGHT
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
            c1 = random.randint(0, 255)
            c2 = random.randint(0, 255)
            c3 = random.randint(0, 255)
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
        ind = point
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
    def glouton1(self, ordre_priorite):
        liste_couleur = []
        for i in range(len(self.l_adj)):
            t = i/(len(self.l_adj)-1)
            if t < 0.5:
                liste_couleur.append((((1 - 2*t)*255), 2*t*255, 0))
            else:
                liste_couleur.append((0, 2*(1-t)*255, (2*t-1)*255))

        """Attribue les couleurs du graphes avec un ordre de priorité"""
        self.l_adj[ordre_priorite[0]-1][0][2] = liste_couleur[0]
        for i in range (1, len(ordre_priorite)):
            couleur_valide = False
            ind_couleur = 0
            while not couleur_valide:
                couleur_valide = not self.verification_voisin_point_couleur(ordre_priorite[i]-1, liste_couleur[ind_couleur])
                if couleur_valide:
                    self.l_adj[ordre_priorite[i]-1][0][2] = liste_couleur[ind_couleur]
                ind_couleur += 1
    
    # Algorithme glouton 2
    def glouton2(self):
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
        self.glouton1(ordre_priorite)

    def compte_couleur_graphe(self):
        couleurs = []

        for noeud in self.l_adj:
            couleur = noeud[0][2]
            
            est_deja_presente = False
            for c in couleurs:
                if c == couleur:
                    est_deja_presente = True
                    break

            if not est_deja_presente:
                couleurs.append(couleur)

        return len(couleurs)

    def compare_graphe1_graphe2(self):
        ordre1 = list(range(1, self.taille + 1))
        ordre2 = list(range(1, self.taille + 1))
        random.shuffle(ordre2)
        self.glouton1(ordre1)
        print("Sur glouton 1 avec un ordre de 1 à N : " + str(self.compte_couleur_graphe()))
        self.glouton1(ordre2)
        print("Sur glouton 1 avec un ordre aléatoire : " + str(self.compte_couleur_graphe()))
        self.glouton2()
        print("Sur glouton 2 : " + str(self.compte_couleur_graphe()))

    def stat_compare_graphe1_graphe2_sur_graph_circulaire_aleatoire(self, m, p, WIDTH, HEIGHT):
        ordre1 = list(range(1, self.taille + 1))
        ordre2 = list(range(1, self.taille + 1))
        random.shuffle(ordre2)
        tab = [0, 0, 0]
        for i in range(m):
            self.graph_circulaire_aleatoire(p, WIDTH, HEIGHT)
            self.glouton1(ordre1)
            g1_ord1 = self.compte_couleur_graphe()
            self.glouton1(ordre2)
            g1_ord2 = self.compte_couleur_graphe()
            self.glouton2()
            g2 = self.compte_couleur_graphe()
            if g1_ord1 < g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            elif g1_ord1 == g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                    tab[1] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[1] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            else:
                if g1_ord1 <= g2:
                    tab[1] += 1
                else:
                    if g1_ord2 < g2:
                        tab[1] += 1
                    elif g1_ord2 == g2:
                        tab[1] += 1
                        tab[2] += 1
                    else:
                        tab[2] += 1
            self.l_adj = [[] for i in range(self.taille)]

        print("Sur un graphe circulaire aléatoire de " + str(self.taille) + " points :\n\nL'algo glouton 1 avec un ordre allant de 1 à " + str(self.taille) + " renvoie dans " + str(tab[0]) + " % " + 
        "des cas le moins de couleurs.\nL'algo glouton 1 avec un ordre aléatoire " + " renvoie dans " + str(tab[1]) + " % " + "des cas le moins de couleurs.\nL'algo glouton 2 renvoie dans " + 
        str(tab[2]) + " % " + "des cas le moins de couleurs.")
    
    def stat_compare_graphe1_graphe2_sur_graph_non_circulaire_aleatoire(self, m, p, CENTER, RADIUS):
        ordre1 = list(range(1, self.taille + 1))
        ordre2 = list(range(1, self.taille + 1))
        random.shuffle(ordre2)
        tab = [0, 0, 0]
        for i in range(m):
            self.graph_non_circulaire_aleatoire(p, CENTER, RADIUS)
            self.glouton1(ordre1)
            g1_ord1 = self.compte_couleur_graphe()
            self.glouton1(ordre2)
            g1_ord2 = self.compte_couleur_graphe()
            self.glouton2()
            g2 = self.compte_couleur_graphe()
            if g1_ord1 < g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            elif g1_ord1 == g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                    tab[1] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[1] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            else:
                if g1_ord1 <= g2:
                    tab[1] += 1
                else:
                    if g1_ord2 < g2:
                        tab[1] += 1
                    elif g1_ord2 == g2:
                        tab[1] += 1
                        tab[2] += 1
                    else:
                        tab[2] += 1
            self.l_adj = [[] for i in range(self.taille)]

        print("Sur un graphe non circulaire aléatoire de " + str(self.taille) + " points :\n\nL'algo glouton 1 avec un ordre allant de 1 à " + str(self.taille) + " renvoie dans " + str(tab[0]) + " % " + 
        "des cas le moins de couleurs.\nL'algo glouton 1 avec un ordre aléatoire " + " renvoie dans " + str(tab[1]) + " % " + "des cas le moins de couleurs.\nL'algo glouton 2 renvoie dans " + 
        str(tab[2]) + " % " + "des cas le moins de couleurs.")


    def stat_compare_graphe1_graphe2_sur_graph_circulaire_aleatoire(self, m, p, WIDTH, HEIGHT):
        ordre1 = list(range(1, self.taille + 1))
        ordre2 = list(range(1, self.taille + 1))
        random.shuffle(ordre2)
        tab = [0, 0, 0]
        for i in range(m):
            self.graph_circulaire_aleatoire(p, WIDTH, HEIGHT)
            self.glouton1(ordre1)
            g1_ord1 = self.compte_couleur_graphe()
            self.glouton1(ordre2)
            g1_ord2 = self.compte_couleur_graphe()
            self.glouton2()
            g2 = self.compte_couleur_graphe()
            if g1_ord1 < g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            elif g1_ord1 == g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                    tab[1] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[1] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            else:
                if g1_ord1 <= g2:
                    tab[1] += 1
                else:
                    if g1_ord2 < g2:
                        tab[1] += 1
                    elif g1_ord2 == g2:
                        tab[1] += 1
                        tab[2] += 1
                    else:
                        tab[2] += 1
            self.l_adj = [[] for i in range(self.taille)]

        print("Sur un graphe circulaire aléatoire de " + str(self.taille) + " points :\n\nL'algo glouton 1 avec un ordre allant de 1 à " + str(self.taille) + " renvoie dans " + str(tab[0]) + " % " + 
        "des cas le moins de couleurs.\nL'algo glouton 1 avec un ordre aléatoire " + " renvoie dans " + str(tab[1]) + " % " + "des cas le moins de couleurs.\nL'algo glouton 2 renvoie dans " + 
        str(tab[2]) + " % " + "des cas le moins de couleurs.")
    
    def stat_compare_graphe1_graphe2_sur_graph_planaire_aleatoire(self, m, p, WIDTH, HEIGHT):
        ordre1 = list(range(1, self.taille + 1))
        ordre2 = list(range(1, self.taille + 1))
        random.shuffle(ordre2)
        tab = [0, 0, 0]
        for i in range(m):
            self.graph_planaire_aleatoire(p, WIDTH, HEIGHT)
            self.glouton1(ordre1)
            g1_ord1 = self.compte_couleur_graphe()
            self.glouton1(ordre2)
            g1_ord2 = self.compte_couleur_graphe()
            self.glouton2()
            g2 = self.compte_couleur_graphe()
            if g1_ord1 < g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            elif g1_ord1 == g1_ord2:
                if g1_ord1 < g2:
                    tab[0] += 1
                    tab[1] += 1
                elif g1_ord1 == g2:
                    tab[0] += 1
                    tab[1] += 1
                    tab[2] += 1
                else:
                    tab[2] += 1
            else:
                if g1_ord1 <= g2:
                    tab[1] += 1
                else:
                    if g1_ord2 < g2:
                        tab[1] += 1
                    elif g1_ord2 == g2:
                        tab[1] += 1
                        tab[2] += 1
                    else:
                        tab[2] += 1
            self.l_adj = [[] for i in range(self.taille)]

        print("Sur un graphe non circulaire aléatoire de " + str(self.taille) + " points :\n\nL'algo glouton 1 avec un ordre allant de 1 à " + str(self.taille) + " renvoie dans " + str(tab[0]) + " % " + 
        "des cas le moins de couleurs.\nL'algo glouton 1 avec un ordre aléatoire " + " renvoie dans " + str(tab[1]) + " % " + "des cas le moins de couleurs.\nL'algo glouton 2 renvoie dans " + 
        str(tab[2]) + " % " + "des cas le moins de couleurs.")