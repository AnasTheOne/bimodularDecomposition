import networkx as nx
import matplotlib.pyplot as plt
import random

f = lambda x : chr(x+ord('a'))
lenL = lambda L : len(L[0])+len(L[1])

#Calcul d'une seconde represontation du bipari
def Gb(Gw,n):
    res = [[] for i in range(n[1])]
    for i in range(n[0]):
        for x in Gw[i]:
            res[x].append(i)
    return res

def complement(G):
    res = [[] for i in range(n[1])]
    for i in range(n[0]):
        for j in range(n[1]):
            if not j in G[i]:
                res[i].append(j)
    return res

def randomGen(n,p):
    G = []
    for i in range(n[0]):
        L = []
        for j in range(n[1]):
            if random.random() < p:
                L.append(j)
        G+=[L]
    return G



def connecetedComps(V):
    toVisit = [[],[]]
    flagsVisited = [[0 for i in range(n[0])],[0 for i in range(n[1])]]
    counter = [0,0]
    comps = []

    while counter[0]+counter[1] < N:
        c = 0
        if counter[0] == n[0]:
            c = 1
        
        for i in range(n[c]):
            if flagsVisited[c][i]==0 and V[c][i]==1:
                toVisit[c].append(i)
                break

        comp = set()
        while lenL(toVisit)>0:
            c = 0
            if len(toVisit[c]) == 0:
                c=1
            v = toVisit[c].pop(0)
            if flagsVisited[c][v] == 0:
                flagsVisited[c][v] = 1
                counter[c] += 1
                comp.add(v+n[0]*c)
                for x in G[c][v]:
                    if flagsVisited[1-c][x] == 0 and V[1-c][x]==1:
                        toVisit[1-c].append(x)
                
        comps += [comp]
    return comps
    
def connecetedComps_b(V):
    toVisit = [[],[]]
    flagsVisited = [[0 for i in range(n[0])],[0 for i in range(n[1])]]
    counter = [0,0]
    comps = []

    while counter[0]+counter[1] < N:
        c = 0
        if counter[0] == n[0]:
            c = 1
        
        for i in range(n[c]):
            if flagsVisited[c][i]==0 and V[c][i]==1:
                toVisit[c].append(i)
                break

        comp = set()
        while lenL(toVisit)>0:
            c = 0
            if len(toVisit[c]) == 0:
                c=1
            v = toVisit[c].pop(0)
            if flagsVisited[c][v] == 0:
                flagsVisited[c][v] = 1
                counter[c] += 1
                comp.add(v+n[0]*c)
                for x in range(n[1-c]):
                    if not x in G[c][v]:
                        if flagsVisited[1-c][x] == 0 and V[1-c][x]==1:
                            toVisit[1-c].append(x)
                
        comps += [comp]
    return comps
    

n = [10,10]
N = n[0]+n[1]
#Gw = [[0],[1,2,3],[1,2],[3,4],[4,5],[3,5],[6,7,8,9],[7,8],[8,9],[9,6]]
#Gw = [[5], [0, 1, 8], [0, 8], [0, 3, 4, 8], [1, 3], [4, 7, 8, 9], [7], [7, 8, 9], [5, 6], [0, 3, 6, 8]]
#Gw = [[0, 1, 2, 3, 4, 5, 7, 8, 9], [0, 1, 2, 3, 5, 6, 8, 9], [2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 5, 7, 8], [0, 2, 3, 4, 6, 7, 8, 9], [0, 1, 3, 4, 5, 7, 8, 9], [0, 1, 3, 4, 5, 6, 7, 8, 9], [0, 2, 3, 4, 6, 7, 8, 9], [1, 4, 5, 6, 7, 8, 9], [0, 1, 2, 4, 5, 6, 7, 8, 9]]
Gw = randomGen(n,0.8)
G=[Gw,Gb(Gw,n)]

print(Gw)
coms = connecetedComps([[1 for i in range(n[0])],[1 for i in range(n[1])]])
print("BFS: ", coms)
coms_b = connecetedComps_b([[1 for i in range(n[0])],[1 for i in range(n[1])]])
print("BFS_b: ", coms_b)

#affichage
G = nx.Graph()
G.add_nodes_from([i for i in range(n[0])])
G.add_nodes_from([f(i) for i in range(n[1])])
for i in range(n[0]):
    for x in Gw[i]:
        G.add_edge(i, f(x))

Gw = complement(Gw)
G_b=[Gw,Gb(Gw,n)]
G_barre = nx.Graph()
G_barre.add_nodes_from([i for i in range(n[0])])
G_barre.add_nodes_from([f(i) for i in range(n[1])])
for i in range(n[0]):
    for x in Gw[i]:
        G_barre.add_edge(i, f(x))

colors = ['#DDDDDD' for i in range(n[0])]+['#999999' for i in range(n[1])]
color = ['#FF0000','#FFFF00','#0000FF','#00FFFF','#FF00FF','#00FF00','#EEEEEE','#555511','#115555','#551155','#111155','#115511','#551111',]
r = random.randint(0, 10)
for i in range(len(coms)):
    for y in coms[i]:
        colors[y] = color[(i+r)%len(color)]
plt.figure()
nx.draw(G, with_labels=True, font_weight='bold',node_color=colors)
plt.figure()
r = random.randint(0, 10)
for i in range(len(coms_b)):
    for y in coms_b[i]:
        colors[y] = color[(i+r)%len(color)]
nx.draw(G_barre, with_labels=True, font_weight='bold',node_color=colors)
plt.show()
