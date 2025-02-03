import pygame
import math

from graphe import *

WIDTH, HEIGHT = 600, 600
RADIUS_RATIO = 0.4  # Rayon fait 40 % de la largeur de l'écran
p = 0.4 # Proba de création du graphe (plus elle est élevé, plus il y a d'arrêtes)
N = 8
G = Graphe(N)

graphe = [[[540.0, 300.0, (255, 0, 0)], 2, 6, 8], [[469.7056274847714, 469.7056274847714, (255, 0, 0)], 1, 3, 8], [[300.0, 540.0, (255, 0, 0)], 2, 4, 5], 
          [[130.29437251522862, 469.7056274847714, (255, 0, 0)], 3, 8], [[60.0, 300.00000000000006, (255, 0, 0)], 3, 7], 
          [[130.29437251522856, 130.29437251522862, (255, 0, 0)], 1, 7, 8], [[299.99999999999994, 60.0, (255, 0, 0)], 5, 6], 
          [[469.70562748477136, 130.29437251522856, (255, 0, 0)], 1, 2, 4, 6]]

"""graphe = [[[540.0, 300.0, (255, 0, 0)], 2, 6, 8], [[469.7056274847714, 469.7056274847714, (255, 0, 0)], 1, 3], [[300.0, 540.0, (255, 0, 0)], 2, 4, 5], 
          [[130.29437251522862, 469.7056274847714, (255, 0, 0)], 3, 8], [[60.0, 300.00000000000006, (255, 0, 0)], 3, 7], 
          [[130.29437251522856, 130.29437251522862, (255, 0, 0)], 1, 7], [[299.99999999999994, 60.0, (255, 0, 0)], 5, 6], 
          [[469.70562748477136, 130.29437251522856, (255, 0, 0)], 1, 4]]"""

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Graphes circulaire")

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = int(WIDTH * RADIUS_RATIO)

G.force_graph_coord(graphe)
# G.couleur_aleatoire()
G.glouton1(screen, [(255,255,255),(0,200,0), (0,0,200), (200,0,200), (128,0,128), (128,128,128)],[1,2,4,3,5,6,7,8])

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
    G.draw_point(screen)

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
                pygame.draw.line(screen, (255,255,255), (x_1, y_1), (x_2, y_2), 5)
                deja_trace.append([ind_point_1, ind_point_2])

    pygame.display.flip()  # Mise à jour de l'affichage

pygame.quit()