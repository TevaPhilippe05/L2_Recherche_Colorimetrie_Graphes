import pygame
import math

from graphe import *

WIDTH, HEIGHT = 800, 800
p = 0.8 # Proba de création du graphe (plus elle est élevé, plus il y a d'arrêtes)
N = 20
G = Graphe(N)

### Imposer un graphe
"""graphe = [[[720.0, 400.0, -1, 720.0, 400.0], 3, 4, 5], [[626.3, 626.3, -1, 626.3, 626.3], 5], [[400.0, 720.0, -1, 400.0, 720.0], 1, 4, 5, 6, 7], 
          [[173.7, 626.3, -1, 173.7, 626.3], 1, 3, 7, 8], [[80.0, 400.0, -1, 80.0, 400.0], 1, 2, 3, 6], [[173.7, 173.7, -1, 173.7, 173.7], 3, 5, 7, 8], 
          [[400.0, 80.0, -1, 400.0, 80.0], 3, 4, 6], [[626.3, 173.7, -1, 626.3, 173.7], 4, 6]]"""

graphe = [[[720.0, 400.0, -1, 720.0, 400.0], 2, 3, 4, 5, 6, 8], [[626.3, 626.3, -1, 626.3, 626.3], 1, 3, 4, 5, 6, 7, 8], 
             [[400.0, 720.0, -1, 400.0, 720.0], 1, 2, 4, 5, 7, 8], [[173.7, 626.3, -1, 173.7, 626.3], 1, 2, 3, 5, 6, 7, 8], 
             [[80.0, 400.0, -1, 80.0, 400.0], 1, 2, 3, 4, 6, 7, 8], [[173.7, 173.7, -1, 173.7, 173.7], 1, 2, 4, 5],
             [[400.0, 80.0, -1, 400.0, 80.0], 2, 3, 4, 5, 8], [[626.3, 173.7, -1, 626.3, 173.7], 1, 2, 3, 4, 5, 7]]

G.force_graph_coord(graphe)
G.supprime_p_newG(2, graphe)
G.fusionne_3p_newG(1, 3, 4, graphe)
G.trouve_non_adjacent([5,6,7,8,9], graphe)
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

# print(G.compte_couleur_graphe())
# G.compare_graphe1_graphe2()
# print(G.l_adj)
"""
G.stat_compare_algo1_algo2_sur_graph(100, p, WIDTH, HEIGHT, "graphe_planaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(10000, p, WIDTH, HEIGHT, "graphe_planaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(100, p, WIDTH, HEIGHT, "graphe_non_circulaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(1000, p, WIDTH, HEIGHT, "graphe_non_circulaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(100, p, CENTER, RADIUS, "graphe_circulaire_aleatoire")
G.stat_compare_algo1_algo2_sur_graph(1000, p, CENTER, RADIUS, "graphe_circulaire_aleatoire")


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Graphes")
font = pygame.font.Font(None, 36)
selected_point = None
"""
running = False
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