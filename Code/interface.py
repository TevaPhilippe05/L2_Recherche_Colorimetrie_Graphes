import pygame
import math

from graphe import *

WIDTH, HEIGHT = 600, 600
RADIUS_RATIO = 0.4  # Rayon fait 40 % de la largeur de l'écran
p = 0.2 # Proba de création du graphe (plus elle est élevé, plus il y a d'arrêtes)
N = 10
G = Graphe(N)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Graphes circulaire")

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = int(WIDTH * RADIUS_RATIO)

G.rand_graph_coord(0.2, CENTER, RADIUS)

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

    pygame.display.flip()  # Mise à jour de l'affichage

pygame.quit()