import random

def rand_graph(n,p):
    l_adj = [[]for i in range(n)]
    for i in range (n):
        for j in range (i+1, n):
            x = random.random()

            if x < p:
                l_adj[i].append(j+1)
                l_adj[j].append(i+1)
    return l_adj

print(rand_graph(8,0.8))