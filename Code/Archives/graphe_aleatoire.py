# Graphe aléatoire
def rand_graph(self, p):
    for i in range (self.taille):
        for j in range (i+1, self.taille):
            x = random.random()

            if x < p:
                self.l_adj[i].append(j+1)
                self.l_adj[j].append(i+1)