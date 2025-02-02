import random
import math

class Graphe:

    def __init__(self, n):
        self.taille = n
        self.l_adj = [[]for i in range(self.taille)]

    # Graphe aléatoire coordonnées
    def rand_graph_coord(self, p, CENTER, RADIUS):      
        for k in range(self.taille):
            angle = 2 * math.pi * k / self.taille
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            self.l_adj[k].append([x,y])

        for i in range (self.taille):
            for j in range (i+1, self.taille):
                x = random.random()

                if x < p:
                    self.l_adj[i].append(j+1)
                    self.l_adj[j].append(i+1)

    
    def change_coordonne(self, CENTER, RADIUS):
        for k in range(self.taille):
            angle = 2 * math.pi * k / self.taille
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            self.l_adj[k][0][0] = x ; self.l_adj[k][0][1] = y