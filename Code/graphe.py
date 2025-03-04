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
            self.l_adj[k].append([x,y, -1, x, y])

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
        l_arrete = []
        for i in range (self.taille - 1):
            for j in range(i + 1, self.taille):
                l_arrete.append((i,j))
        random.shuffle(l_arrete)

        for (i,j) in l_arrete:
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
            self.l_adj[k].append([x, y, -1, x, y]) # Fois 2 car on a les nouvelles coordonnées et les coordonnées initiales 

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
        nb_couleur = []
        liste_couleur = []
        for i in range(len(self.l_adj)):
            if not self.l_adj[i][0][2] in nb_couleur:
                nb_couleur.append(self.l_adj[i][0][2])

        for i in range(len(nb_couleur)):
            t = i/(len(nb_couleur))
            if t < 0.5:
                liste_couleur.append(((1 - 2*t) * 255, 2 * t * 255, 0))
            else:
                liste_couleur.append((0, 2*(1-t) * 255, (2 * t - 1) * 255))

        for k in range(self.taille):
            x = self.l_adj[k][0][0]
            y = self.l_adj[k][0][1]
            
            color = liste_couleur[self.l_adj[k][0][2]]
            pygame.draw.circle(screen, color, (int(x), int(y)), 14)
            
            # Ajout du numéro du noeud à sa droite
            num = font.render(str(k + 1), True, (255, 255, 255))
            num_x = int(x) + 25
            num_y = int(y) - num.get_height() // 2
            screen.blit(num, (num_x, num_y))

    def couleur_aleatoire(self):
        """Permet d'attribuer des couleurs aléatoires aux points du graphe"""
        max = 0
        un_sur_deux = True # Pour maximiser le nombre de couleurs
        for o in range(self.taille):
            if un_sur_deux:
                c = max
                un_sur_deux = False
            else:
                c = random.randint(0, max)
                un_sur_deux = True

            if c == max :
                max += 1
            self.l_adj[o][0][2] = c

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
        """Attribue les couleurs du graphes avec un ordre de priorité"""
        self.l_adj[ordre_priorite[0]-1][0][2] = 0
        for i in range (1, len(ordre_priorite)):
            couleur_valide = False
            ind_couleur = 0
            while not couleur_valide:
                couleur_valide = not self.verification_voisin_point_couleur(ordre_priorite[i]-1, ind_couleur)
                if couleur_valide:
                    self.l_adj[ordre_priorite[i]-1][0][2] = ind_couleur
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
        for i in range(len(self.l_adj)):
            if len(self.l_adj[i]) == 1:
                liste_point.append(i + 1)
        
        while not liste_termine:
            # Obtention de la première valeur en vue d'une comparaison
            cherche_donnee = True
            i = 0
            while cherche_donnee and i < len(tab_lien):
                if len(tab_lien[i]) != 0:
                    minim = [tab_lien[i], len(tab_lien[i]), i + 1]
                    cherche_donnee = False
                i += 1          
            if i == len(tab_lien):
                break

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
                if len(tab_lien[ind-1]) == 0:
                    liste_point.append(ind)

            # Si le tableau des lien est vide on s'arrête
            liste_termine = True
            for i in range(self.taille):
                if len(tab_lien[i]) > 0:
                    liste_termine = False

        ordre_priorite = liste_point[::-1]
        self.glouton1(ordre_priorite)

    def compte_couleur_graphe(self):
        """Compte les couleurs d'un graphe"""
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

    def reset_graphe(self):
        """Remet à 0 le graphe"""
        self.l_adj = [[] for i in range(self.taille)]

    def reset_couleur_graphe(self):
        """Remet à 0 les couleurs du graphe"""
        for i in range(len(self.l_adj)):
            self.l_adj[i][0][2] = -1

    def stat_compare_algo1_algo2_sur_graph(self, m, p, attribut1, attribut2, nom_graphe):
        """Comparare les deux algorithmes gloutons sur le graphe fourni"""
        ordre1 = list(range(1, self.taille + 1))
        ordre2 = list(range(1, self.taille + 1))
        random.shuffle(ordre2)
        tab = [0, 0, 0]

        min_g1_ord1 = -1
        min_g1_ord2 = -1
        min_g2 = -1

        moy_g1_ord1 = 0
        moy_g1_ord2 = 0
        moy_g2 = 0

        max_g1_ord1 = -1
        max_g1_ord2 = -1
        max_g2 = -1

        for i in range(m):
            if nom_graphe == "graphe_planaire_aleatoire":
                self.graph_planaire_aleatoire(p, attribut1, attribut2)
            elif nom_graphe == "graphe_non_circulaire_aleatoire":
                self.graph_non_circulaire_aleatoire(p, attribut1, attribut2)
            elif nom_graphe == "graphe_circulaire_aleatoire":
                self.graph_circulaire_aleatoire(p, attribut1, attribut2)

            self.glouton1(ordre1)
            g1_ord1 = self.compte_couleur_graphe()
            self.reset_couleur_graphe()
            self.glouton1(ordre2)
            g1_ord2 = self.compte_couleur_graphe()
            self.reset_couleur_graphe()
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

            moy_g1_ord1 += g1_ord1/m
            moy_g1_ord2 += g1_ord2/m
            moy_g2 += g2/m
            
            if min_g1_ord1 == -1:
                min_g1_ord1 = g1_ord1
                min_g1_ord2 = g1_ord2
                min_g2 = g2

                max_g1_ord1 = g1_ord1
                max_g1_ord2 = g1_ord2
                max_g2 = g2

            else:
                if g1_ord1 < min_g1_ord1:
                    min_g1_ord1 = g1_ord1
                if g1_ord2 < min_g1_ord2:
                    min_g1_ord2 = g1_ord2
                if g2 < min_g2:
                    min_g2 = g2

                if g1_ord1 > max_g1_ord1:
                    max_g1_ord1 = g1_ord1
                if g1_ord2 > max_g1_ord2:
                    max_g1_ord2 = g1_ord2
                if g2 > max_g2:
                    max_g2 = g2
            
            self.reset_graphe()

        tab[0] = round(tab[0] * (100 / m), 2)
        tab[1] = round(tab[1] * (100 / m), 2)
        tab[2] = round(tab[2] * (100 / m), 2)
        
        print("\nSur un " + nom_graphe + " de " + str(self.taille) + " points et avec " + str(m) + " tirages :\n\nL'algo glouton 1 avec un ordre allant de 1 à " + str(self.taille) + " renvoie dans " + str(tab[0]) + " % " + 
        "des cas le moins de couleurs.\nL'algo glouton 1 avec un ordre aléatoire " + " renvoie dans " + str(tab[1]) + " % " + "des cas le moins de couleurs.\nL'algo glouton 2 renvoie dans " + 
        str(tab[2]) + " % " + "des cas le moins de couleurs.\n")

        print(
            "Sur " + str(m) + " tirages, on obtient donc :\n\n" + 
            "Un nombre minimale de couleur de \n" +
            "Algo glouton 1 ordre 1 : " + str(min_g1_ord1) + "\nAlgo glouton 1 ordre 2 : " + str(min_g1_ord2) + "\nAlgo glouton 2 : " + str(min_g2) + "\n\n" + 
            "Un nombre moyen de couleur de :\n" +
            "Algo glouton 1 ordre 1 : " + str(round(moy_g1_ord1,2)) + "\nAlgo glouton 1 ordre 2 : " + str(round(moy_g1_ord2,2)) + "\nAlgo glouton 2 : " + str(round(moy_g2,2)) + "\n\n" + 
            "Un nombre maximal de couleur de :\n" +
            "Algo glouton 1 ordre 1 : " + str(max_g1_ord1) + "\nAlgo glouton 1 ordre 2 : " + str(max_g1_ord2) + "\nAlgo glouton 2 : " + str(max_g2)
            )