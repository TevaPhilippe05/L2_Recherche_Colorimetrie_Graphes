import pygame
import math

from graphe import *

WIDTH, HEIGHT = 600, 600
RADIUS_RATIO = 0.4  # Rayon fait 40 % de la largeur de l'écran
p = 0.4 # Proba de création du graphe (plus elle est élevé, plus il y a d'arrêtes)
N = 10
G = Graphe(N)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Graphes circulaire")

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = int(WIDTH * RADIUS_RATIO)

# G.rand_graph_coord(0.2, CENTER, RADIUS)
graphe = [[[540.0, 300.0], 6, 8], [[469.7056274847714, 469.7056274847714], 8], [[300.0, 540.0], 5], [[130.29437251522862, 469.7056274847714], 8], [[60.0, 300.00000000000006], 3, 7, 8], [[130.29437251522856, 130.29437251522862], 1, 7, 8], [[299.99999999999994, 60.0], 5, 6], [[469.70562748477136, 130.29437251522856], 1, 2, 4, 5, 6]]
G.force_graph_coord(graphe)

print(G.l_adj)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE: # Si on redimensionne la fenêtre
            WIDTH, HEIGHT = event.w, event.h

            CENTER = (WIDTH // 2, HEIGHT // 2)
            RADIUS = int(WIDTH * RADIUS_RATIO)
            G.change_coordonne(CENTER, RADIUS)

    screen.fill((35, 35, 35))
    
    # Dessiner les points
    for k in range(G.taille):
        x = G.l_adj[k][0][0]
        y = G.l_adj[k][0][1]
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 8)

    # Dessiner les liaisons entre les points
    for l in range(len(G.l_adj)):
        for m in range(1, len(G.l_adj[l])):
            x_1 = G.l_adj[l][0][0]
            y_1 = G.l_adj[l][0][1]
            
            ind_point_2 = G.l_adj[l][m] - 1
            x_2 = G.l_adj[ind_point_2][0][0]
            y_2 = G.l_adj[ind_point_2][0][1]

            pygame.draw.line(screen, (255,255,255), (x_1, y_1), (x_2, y_2), 5)

    pygame.display.flip()  # Mise à jour de l'affichage

pygame.quit()