import networkx as nx
import matplotlib.pyplot as plt
import random
from graphviz import Graph

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
    res = [[] for i in range(n[0])]
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

#tri linéaire d'un tableau d'entiers
def triDegree(d):
    sortedD = [[[] for i in range(n[1]+1)],[[] for i in range(n[0]+1)]]
    res = [[],[]]
    for c in range(2):
        for i in range(n[c]):
            sortedD[c][n[1-c] - d[c][i][1]] += [d[c][i]]
    for c in range(2):
        i = 0
        while i < n[1-c]+1:
            if len(sortedD[c][i])>0:
                res[c].append(sortedD[c][i].pop())
            else:
                i += 1

    return res

#connected components
def connectedComps(V):
    toVisit = [[],[]]# élements à visiter
    flagsVisited = [[0 for i in range(n[0])],[0 for i in range(n[1])]]# flags pour marquer 
    n_V = [sum(V[0]),sum(V[1])] #nombre d'élements dans V
    counter = [0,0] #compteur pour compter le nombre d'élements visités
    comps = [] # liste des composantes connexes 

    while counter[0]+counter[1] < sum(n_V):
        c = 0
        if counter[0] == n_V[0]:
            c = 1
        
        for i in range(n[c]):
            if flagsVisited[c][i]==0 and V[c][i]==1:
                toVisit[c].append(i)
                break

        comp = [set(),set()]
        while lenL(toVisit)>0:
            c = 0
            if len(toVisit[c]) == 0:
                c=1
            v = toVisit[c].pop(0)
            if flagsVisited[c][v] == 0:
                flagsVisited[c][v] = 1
                counter[c] += 1
                comp[c].add(v)
                for x in G[c][v]:
                    if flagsVisited[1-c][x] == 0 and V[1-c][x]==1:
                        toVisit[1-c].append(x)
                
        comps += [comp]
    return comps

#à verifier: linéarité, pourquoi les flags deviennent obsolètes  
def connectedComps_b(V):
    #elements non visités
    nonVisited = [ {i for i in range(n[0]) if V[0][i] == 1}, {i for i in range(n[1]) if V[1][i] == 1}]
    toVisit = [set(),set()] # à visiter
    comps = [] #liste des composantes co-connexes
    while lenL(nonVisited)>0:
        c = 0
        if len(nonVisited[0]) == 0:
            c = 1
        toVisit[c].add(nonVisited[c].pop())
        comp = [set(),set()]
        while lenL(toVisit)>0:
            c = 0
            if len(toVisit[c]) == 0:
                c=1
            v = toVisit[c].pop()
            comp[c].add(v)
            N_v = set()
            for x in G[c][v]:
                if x in nonVisited[1-c]:
                    N_v.add(x)
                    nonVisited[1-c].remove(x)
            toVisit[1-c].update(nonVisited[1-c])
            nonVisited[1-c] = N_v
        comps += [comp]
    return comps

#Version linéaire de
def KpS(V):
    deg = [[],[]]#deg[0] est la liste des sommets blancs dont les élements sont des tuples (vetrex,deg(vertex))
    comp = []#liste des composantes

    
    #tri à linéariser
    for c in range(2):
        for i in range(n[c]):
            if V[c][i]==1:
                deg[c] += [(i,len(G[c][i]))]
    deg = triDegree(deg)
    n_w, n_b= len(deg[0]),len(deg[1])  
    r,s = 1,n_b 
    S_0,S_1 = 0,0
    old_r,old_s = 0,s
    deg[0]+=[(-1,-1)]
    while r < n_w+1 or s > 0:
        if deg[0][r-1][1] == s or deg[1][s-1][1] == old_r:
            if deg[0][r-1][1] == s:
                comp += [[{deg[0][r-1][0]},set()]]
                old_r += 1
                S_0 += deg[0][r-1][1]
                r+=1
            elif deg[1][s-1][1] == old_r:
                comp += [[set(),{f(deg[1][s-1][0])}]]
                old_s -= 1
                S_1 += deg[1][s-1][1]
                s-=1
        else:
            compFound = False
            while not compFound:
                S_0 += deg[0][r-1][1]
                while s > 0 and deg[1][s-1][1]<r:
                    S_1 += deg[1][s-1][1]
                    s-=1
                if S_0 == r*s + S_1:
                    comp += [[{deg[0][i][0] for i in range(old_r,r)},{f(deg[1][i][0]) for i in range(s,old_s)}]]
                    old_r,old_s = r,s
                    compFound = True
                r += 1
    return(comp)

def sortedDegreesComp(V):
    deg = [[],[]]#deg[0] est la liste des sommets blancs dont les élements sont des tuples (vetrex,deg(vertex))
    
    #tri à linéariser
    for c in range(2):
        for i in range(n[c]):
            if V[c][i]==1:
                deg[c] += [(i,len(G[c][i]))]
    deg = triDegree(deg)
    print(deg)
    return [[[x[0] for x in deg[0]],[f(x[0]) for x in deg[1]]]]

#Positions des points pour l'affichage du K+S
def positionKpsPlot(Comps):
    pos = {}
    k,l = 0,0
    for comp in Comps:
        for x in comp[0]:
            pos[x] = (k, 2)
            k+=1
        for x in comp[1]:
            pos[x] = (l, 1)
            l+=1
        m = max(k,l) + 2
        k = m
        l = m
    return pos


n = [4,4]
#Gw = [[0,1],[1,2],[2],[0,1,2]] # liste d'adjacence les noeuds blancs G_white
"""
n = [11,10]
Gw = [[0,1],[1,2],[2],[0,1,2],[0,1,2,3,4,7,8,9],[0,1,2,3,5,7,8,9],[0,1,2,3,5,6],[0,1,2,3,7,8],[0,1,2,3,8],[0,1,2,3,8,9],[0,1,2,3,9]]
"""
#Gw = [[0],[1,2,3],[1,2],[3,4],[4,5],[3,5],[6,7,8,9],[7,8],[8,9],[9,6]]
#Gw = [[5], [0, 1, 8], [0, 8], [0, 3, 4, 8], [1, 3], [4, 7, 8, 9], [7], [7, 8, 9], [5, 6], [0, 3, 6, 8]]
#Gw = [[0, 1, 2, 3, 4, 5, 7, 8, 9], [0, 1, 2, 3, 5, 6, 8, 9], [2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 5, 7, 8], [0, 2, 3, 4, 6, 7, 8, 9], [0, 1, 3, 4, 5, 7, 8, 9], [0, 1, 3, 4, 5, 6, 7, 8, 9], [0, 2, 3, 4, 6, 7, 8, 9], [1, 4, 5, 6, 7, 8, 9], [0, 1, 2, 4, 5, 6, 7, 8, 9]]
#Gw = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 4, 6, 8, 9], [0, 2, 3, 4, 5, 7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 3, 4, 6, 7, 8, 9], [0, 2, 3, 6, 7, 8, 9], [0, 4, 7, 8, 9], [0, 1, 2, 5, 6, 9], [0, 1, 3, 6, 7, 8, 9], [0, 2, 3, 4, 6, 7, 8]]
#Gw = [[0, 1, 2, 3, 4, 5, 8], [0, 2, 3, 4, 6, 7, 8, 9], [0, 1, 2, 3, 6, 7, 8], [0, 1, 2, 3, 4, 6, 7, 9], [0, 1, 2, 3, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [0, 1, 2, 3, 4, 6, 8, 9], [0, 1, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9]]
#Gw = [[0,1,5,6,7,8,9],[1,2,5,6,8,9],[2,3,5,6,7,8,9],[3,4,5,6,7,8,9],[4,5,6,7,8,9],[5,6],[6],[8],[8,9],[9]]
#Gw = [[0,1,5,6,7,8,9],[1,2,5,6,7,8,9],[2,3,5,6,7,8,9],[3,4,5,6,7,8,9],[4,5,6,7,8,9],[5,6],[6,7],[7,8],[8,9],[9]]

#Gw = [[0, 1, 2, 3], [1, 2, 3], [2, 3], [0, 1, 2, 3]]
#Gw = [[0, 2, 3], [0, 1, 3], [0, 2, 3], [0, 3]]

Gw = randomGen(n,0.7)
N = n[0]+n[1]
G=[Gw,Gb(Gw,n)] #création du graphe avec la liste d'adjacence blanche et noir
V = [[1 for i in range(n[0])],[1 for i in range(n[1])]]
#V = [[1,1,1,1,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]]
print(Gw)
coms = connectedComps(V)
print("BFS: ", coms)
coms_b = connectedComps_b(V)
print("BFS_b: ", coms_b)
#V = [[1,1,1,1,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]]
kpsComp = KpS(V)
sortedPos = positionKpsPlot(sortedDegreesComp(V))
#kpsComp = [{0,1,2},{0,1,2}]
print("K+S: ",kpsComp)
#affichage
graphviz = 1
if graphviz == 0:
    graph = Graph()
    nodes_left = {}
    nodes_right = {}
    for i in range(n[0]):
        nodes_left[i] = str(i)
    for i in range(n[1]):
        nodes_right[i] = f(i)
    for i in range(n[0]):
        for x in Gw[i]:
            graph.edge(nodes_left[i], nodes_right[x])

    graph.view()
elif graphviz == 1:
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
        for c in range(2):
            for y in coms[i][c]:
                colors[y+c*n[0]] = color[(i*13+r)%len(color)]
    
    plt.figure()
    nx.draw(G, with_labels=True, font_weight='bold',node_color=colors)
    
    #show G_barre
    plt.figure()
    r = random.randint(0, 10)
    for i in range(len(coms_b)):
        for c in range(2):
            for y in coms_b[i][c]:
                colors[y+c*n[0]] = color[(i*13+r)%len(color)]
    nx.draw(G_barre, with_labels=True, font_weight='bold',node_color=colors)
    
    #show K+s
    try:
        plt.figure()
        l = 0
        for i in range(len(kpsComp)-1):
            l += max(len(kpsComp[i][0]),len(kpsComp[i][1]))+2
            plt.axline((l-1, 1), (l-1, 2),color="red")
        pos = positionKpsPlot(kpsComp)
        nx.draw(G, with_labels=True, pos=pos)
    except:
        plt.figure()
        print("problem with K+S")
        nx.draw(G, with_labels=True, pos=sortedPos)

    plt.show()
