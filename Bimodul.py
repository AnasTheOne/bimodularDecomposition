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

#complementaire pour vérifier
def complement(G):
    res = [[] for i in range(n[1])]
    for i in range(n[0]):
        for j in range(n[1]):
            if not j in G[i]:
                res[i].append(j)
    return res

#génération aléatoire
def randomGen(n,p):
    G = []
    for i in range(n[0]):
        L = []
        for j in range(n[1]):
            if random.random() < p:
                L.append(j)
        G+=[L]
    return G

#connected components
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

#à verifier: linéarité, pourquoi les flags deviennent obsolètes  
def connecetedComps_b(V):
    nonVisited = [ {i for i in range(n[0]) if V[0][i] == 1}, {i for i in range(n[1]) if V[1][i] == 1}]
    toVisit = [set(),set()]
    comps = []
    while lenL(nonVisited)>0:
        c = 0
        if len(nonVisited[0]) == 0:
            c = 1
        toVisit[c].add(nonVisited[c].pop())
        comp = set()
        while lenL(toVisit)>0:
            c = 0
            if len(toVisit[c]) == 0:
                c=1
            v = toVisit[c].pop()
            comp.add(v+n[0]*c)
            N_v = set()
            for x in G[c][v]:
                if x in nonVisited[1-c]:
                    N_v.add(x)
                    nonVisited[1-c].remove(x)
            toVisit[1-c].update(nonVisited[1-c])
            nonVisited[1-c] = N_v
        comps += [comp]
    return comps

#Pas encore au point
def KpS(V):
    d = [[],[]]
    resV = []
    for c in range(2):
        for i in range(n[c]):
            if V[c][i]==1:
                d[c] += [(i,len(G[c][i]))]
        d[c].sort(key=lambda tup: tup[1],reverse=True)
    r = 1
    s = n[1]
    while not sum([d[0][i-1][1] for i in range(1,r+1)]) == r*s + sum([d[1][i-1][1] for i in range(s+1,n[1]+1)]):
        if r == n[0]: break
        r += 1
        s = n[1] - min([j for j in range(n[1]) if d[1][j][1]<r],default = 0) 
    resV += [{d[0][i][0] for i in range(r)}]
    resV += [{d[1][i][0] for i in range(n[1]-s,n[1])}]
    return(resV)

def positionKpsPlot(comp):
    pos = {}
    k = 0
    for x in kpsComp[0]:
        pos[x] = (1, k)
        k+=1
    l = 0
    for x in kpsComp[1]:
        pos[f(x)] = (2, l)
        l+=1
    k = max(k,l)
    l = max(k,l)
    for x in range(n[0]):
        if not x in kpsComp[0]:
            pos[x] = (1, k+5)
            k+=1
    for x in range(n[1]):
        if not x in kpsComp[1]:
            pos[f(x)] = (2, l+5)
            l+=1
    return pos
n = [10,10]
N = n[0]+n[1]
#Gw = [[0],[1,2,3],[1,2],[3,4],[4,5],[3,5],[6,7,8,9],[7,8],[8,9],[9,6]]
#Gw = [[5], [0, 1, 8], [0, 8], [0, 3, 4, 8], [1, 3], [4, 7, 8, 9], [7], [7, 8, 9], [5, 6], [0, 3, 6, 8]]
#Gw = [[0, 1, 2, 3, 4, 5, 7, 8, 9], [0, 1, 2, 3, 5, 6, 8, 9], [2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 5, 7, 8], [0, 2, 3, 4, 6, 7, 8, 9], [0, 1, 3, 4, 5, 7, 8, 9], [0, 1, 3, 4, 5, 6, 7, 8, 9], [0, 2, 3, 4, 6, 7, 8, 9], [1, 4, 5, 6, 7, 8, 9], [0, 1, 2, 4, 5, 6, 7, 8, 9]]

#Gw = [[0, 1, 2, 3, 4, 5, 8], [0, 2, 3, 4, 6, 7, 8, 9], [0, 1, 2, 3, 6, 7, 8], [0, 1, 2, 3, 4, 6, 7, 9], [0, 1, 2, 3, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [0, 1, 2, 3, 4, 6, 8, 9], [0, 1, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9]]
Gw = randomGen(n,0.7)
G=[Gw,Gb(Gw,n)]
V = [[1 for i in range(n[0])],[1 for i in range(n[1])]]
print(Gw)
coms = connecetedComps(V)
print("BFS: ", coms)
coms_b = connecetedComps_b(V)
print("BFS_b: ", coms_b)
kpsComp = KpS(V)
print("K+S: ",kpsComp)

#affichage
G = nx.Graph()
G.add_nodes_from([i for i in range(n[0])], bipartite=0)
G.add_nodes_from([f(i) for i in range(n[1])], bipartite=1)
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


colors = ['#000000' for i in range(N)]
color = ['#FF0000' ,'#00FF00' ,'#0000FF' ,'#00FFFF' ,'#FFFF00' ,'#FF00FF' ,'#C0C0C0','#808080','#800000','#808000','#008000','#800080','#008080','#000080','#FFA07A','#556B2F',"#20B2AA"]
r = random.randint(0, 10)
for i in range(len(coms)):
    for y in coms[i]:
        colors[y] = color[(i*13+r)%len(color)]
plt.figure()
nx.draw(G, with_labels=True, font_weight='bold',node_color=colors)
plt.figure()
r = random.randint(0, 10)
for i in range(len(coms_b)):
    for y in coms_b[i]:
        colors[y] = color[(i*13+r)%len(color)]
nx.draw(G_barre, with_labels=True, font_weight='bold',node_color=colors)
#show K+s
plt.figure()
pos = positionKpsPlot(kpsComp)
nx.draw(G, pos=pos)
plt.show()
