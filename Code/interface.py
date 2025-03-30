import pygame
import math

from graphe import *

### Imposer un graphe

# Graphe circulaire peu dense
# N = 8
graphe = [[[720.0, 400.0, -1, 720.0, 400.0], 3, 4, 5], [[626.3, 626.3, -1, 626.3, 626.3], 5], [[400.0, 720.0, -1, 400.0, 720.0], 1, 4, 5, 6, 7], 
          [[173.7, 626.3, -1, 173.7, 626.3], 1, 3, 7, 8], [[80.0, 400.0, -1, 80.0, 400.0], 1, 2, 3, 6], [[173.7, 173.7, -1, 173.7, 173.7], 3, 5, 7, 8], 
           [[400.0, 80.0, -1, 400.0, 80.0], 3, 4, 6], [[626.3, 173.7, -1, 626.3, 173.7], 4, 6]]

# Graphe circulaire dense
# N = 8
graphe2 = [[[720.0, 400.0, -1, 720.0, 400.0], 2, 3, 4, 5, 6, 8], [[626.3, 626.3, -1, 626.3, 626.3], 1, 3, 4, 5, 6, 7, 8], 
           [[400.0, 720.0, -1, 400.0, 720.0], 1, 2, 4, 5, 7, 8], [[173.7, 626.3, -1, 173.7, 626.3], 1, 2, 3, 5, 6, 7, 8], 
           [[80.0, 400.0, -1, 80.0, 400.0], 1, 2, 3, 4, 6, 7, 8], [[173.7, 173.7, -1, 173.7, 173.7], 1, 2, 4, 5],
           [[400.0, 80.0, -1, 400.0, 80.0], 2, 3, 4, 5, 8], [[626.3, 173.7, -1, 626.3, 173.7], 1, 2, 3, 4, 5, 7]]

# Graphe planaire avec 1 seul sommet de degré 5
# N = 8
graphe3 = [[[96, 737, -1, 96, 737], 6, 3, 2, 4, 8], [[365, 599, -1, 365, 599], 5, 1], [[468, 490, -1, 468, 490], 1], 
           [[229, 305, -1, 229, 305], 6, 7, 1, 8], [[585, 390, -1, 585, 390], 2, 6], [[703, 165, -1, 703, 165], 1, 4, 5, 7], 
           [[299, 95, -1, 299, 95], 6, 4, 8], [[46, 247, -1, 46, 247], 4, 7, 1]]

# Graphe avec chaque sommets (12) de degrés 5
N = 12
graphe4 = [[[385, 22, -1, 385.0, 22.0], 2, 3, 8, 9, 12], [[623, 130, -1, 623.0, 130.0], 1, 3, 4, 5, 9], [[150, 122, -1, 150.0, 122.0], 1, 2, 4, 7, 8], 
           [[384, 229, -1, 384.0, 229.0], 2, 3, 5, 6, 7], [[604, 375, -1, 604.0, 375.0], 2, 4, 6, 9, 10], [[387, 477, -1, 387.0, 477], 4, 5, 7, 10, 11], 
           [[175, 367, -1, 175.0, 367.0], 3, 4, 6, 8, 11], [[94, 590, -1, 94.0, 590.0], 1, 3, 7, 11, 12], [[712, 592, -1, 712.0, 592.0], 1, 2, 5, 10, 12], 
           [[518, 662, -1, 518.0, 662.0], 5, 6, 9, 11, 12], [[271, 664, -1, 271.0, 664.0], 6, 7, 8, 10, 12], [[356, 752, -1, 356.0, 752.0], 1, 8, 9, 10, 11]]

WIDTH, HEIGHT = 800, 800
p = 0.8 # Proba de création du graphe (plus elle est élevé, plus il y a d'arrêtes)
# N = 10
G = Graphe(N)
G.force_graph_coord(graphe4)

"""
G.supprime_p_newG(2, graphe)
G.fusionne_3p_newG(1, 3, 4, graphe)
G.trouve_non_adjacent([5,6,7,8,9], graphe)
print(G.compte_tab(graphe))
print(G.sommets_graphe(graphe))
print(graphe)
print(G.sommet_degres_min(graphe))
print(G.voisin_point(graphe, 6))
"""

### Graphe aléatoire circulaire
RADIUS_RATIO = 0.4  # Rayon fait 40 % de la largeur de l'écran
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = int(WIDTH * RADIUS_RATIO)
# G.graph_circulaire_aleatoire(p, CENTER, RADIUS)

### Graphe aléatoire non circulaire
# G.graph_non_circulaire_aleatoire(p, WIDTH, HEIGHT)

### Graphe planaire aléatoire
# G.graph_planaire_aleatoire(p, WIDTH, HEIGHT)

### Colorimétrie aléatoire
# G.couleur_aleatoire()

### Colorimétrie glouton 1
ordre1 = list(range(1, G.taille + 1))
ordre2 = list(range(1, G.taille + 1))
random.shuffle(ordre2)
# G.glouton1(ordre1)
# G.glouton1(ordre2)

### Colorimétrie glouton 2
# G.glouton2()

# Algorithme de colorimétrie numéro 3
G.algo3(graphe4)

"""
G.stat_compare_algo1_algo2_sur_graph(100, p, WIDTH, HEIGHT, "graphe_planaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(10000, p, WIDTH, HEIGHT, "graphe_planaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(100, p, WIDTH, HEIGHT, "graphe_non_circulaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(1000, p, WIDTH, HEIGHT, "graphe_non_circulaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(100, p, CENTER, RADIUS, "graphe_circulaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(1000, p, CENTER, RADIUS, "graphe_circulaire_aleatoire")
"""

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Graphes")
font = pygame.font.Font(None, 36)
selected_point = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE: # Si on redimensionne la fenêtre
            new_WIDTH, new_HEIGHT = event.w, event.h
            G.change_coordonne(WIDTH, HEIGHT, new_WIDTH, new_HEIGHT)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i in range(G.taille):
                x, y = G.l_adj[i][0][:2]
                
                if math.hypot(mouse_x - x, mouse_y - y) < 14:
                    selected_point = i

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_point = None

        elif event.type == pygame.MOUSEMOTION and selected_point is not None:  # Déplacement
            new_WIDTH, new_HEIGHT = screen.get_width(), screen.get_height()
            mouse_x, mouse_y = event.pos
            G.l_adj[selected_point][0][0] = mouse_x
            G.l_adj[selected_point][0][1] = mouse_y
            
            G.l_adj[selected_point][0][3] = mouse_x / new_WIDTH * WIDTH
            G.l_adj[selected_point][0][4] = mouse_y / new_HEIGHT * HEIGHT


    screen.fill((35, 35, 35))
    
    # Dessiner les liaisons entre les points
    deja_trace = []
    for l in range(G.taille):
        for m in range(1, len(G.l_adj[l])):
            ind_point_1 = l
            x_1 = G.l_adj[l][0][0]
            y_1 = G.l_adj[l][0][1]
            
            ind_point_2 = G.l_adj[l][m] - 1
            x_2 = G.l_adj[ind_point_2][0][0]
            y_2 = G.l_adj[ind_point_2][0][1]

            # Pour ne pas tracer deux fois une ligne
            deja_trace_b = False
            for n in range(len(deja_trace)):
                if deja_trace[n] == [ind_point_2, ind_point_1]:
                    deja_trace_b = True

            if not deja_trace_b:
                pygame.draw.line(screen, (50, 50,170), (x_1, y_1), (x_2, y_2), 5)
                deja_trace.append([ind_point_1, ind_point_2])

    # Dessiner les points
    G.draw_point(screen, font)

    pygame.display.flip()  # Mise à jour de l'affichage

pygame.quit()