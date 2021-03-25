import networkx as nx
import matplotlib.pyplot as plt

#Calcul d'une seconde represontation du bipari
def secondRep(G,n,m):
    res = [[] for i in range(m)]
    for i in range(n):
        for x in G[i]:
            res[x].append(i)
    return res

def exploreB(v,V,comp):
    flagsOnG[v] = 1
    for x in Gb[v-n]:
        if flagsOnG[x+n] == 0 and V[x+n] == 1:
            flagsOnG[x+n] = 1
            comp.add(x+n)
            exploreW(x,V,comp) 

def exploreW(v,V,comp):
    flagsOnG[v] = 1
    for x in Gw[v]:
        if flagsOnG[x] == 0 and V[x] == 1:
            flagsOnG[x] = 1
            comp.add(x)
            exploreB(x,V,comp)

#Composantes connexes de G et de G_barre restreints à V
def connectedComps(V):
    l = 0
    flagRoot = True
    for i in range(n+m):
        if flagRoot and V[i] == 1:
            root = i
            flagRoot = False
        l += V[i]
    comp = set()
    comp.add(root)
    if root < n:
        exploreW(root,V,comp)
    else:
        exploreB(root,V,comp)
    if sum(flagsOnG) < l:
        for x in comp:
            V[x] = 0
        return [comp] + connectedComps(V)
    else:
        return [comp]

n,m = 10,10
Gw = [[0],[1,2,3],[1,2],[3,4],[4,5],[3,5],[6,7,8,9],[7,8],[8,9],[9,6]]
Gb = secondRep(Gw,n,m)
subV = [0 for i in range(n+m)]
flagsOnG = [0 for i in range(n+m)]
flagsOnG_b = [0 for i in range(n+m)] #à remettre à zero après chaque décomposition

print(Gw)
print(Gb)
comps = connectedComps([1 for i in range(n+m)])
print(comps)
"""
G = nx.bipartite.gnmk_random_graph(4, 4, 10, seed=123)
top = nx.bipartite.sets(G)[0]
pos = nx.bipartite_layout(G, top)
nx.draw(G, pos=pos)
plt.show()
"""

G = nx.Graph()
f = lambda x : chr(x+ord('a'))
G.add_nodes_from([i for i in range(n)])
G.add_nodes_from([f(i) for i in range(m)])
for i in range(n):
    for x in Gw[i]:
        G.add_edge(i, f(x))
colors = ['#DDDDDD' for i in range(n)]+['#999999' for i in range(m)]
nx.draw(G, with_labels=True, font_weight='bold',node_color=colors)
plt.show()
