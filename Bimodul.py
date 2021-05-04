import networkx as nx
import matplotlib.pyplot as plt
import random
from graphviz import Graph

graphviz = 2
posPlot = 0

f = lambda x : chr(x+ord('a'))
lenL = lambda L : len(L[0])+len(L[1])

#Calcul d'une seconde represontation du bipari
def Gb(Gw,n):
    res = [set() for i in range(n[1])]
    for i in range(n[0]):
        for x in Gw[i]:
            res[x].add(i)
    return res

#complementaire pour vérifier
def complement(G):
    res = [set() for i in range(n[0])]
    for i in range(n[0]):
        for j in range(n[1]):
            if not j in G[i]:
                res[i].add(j)
    return res

#génération aléatoire
def randomGen(n,p):
    G = []
    for i in range(n[0]):
        L = set()
        for j in range(n[1]):
            if random.random() < p:
                L.add(j)
        G+=[L]
    return G

#retourne True si M est un bimodule
def isBimodule(M):
    res = True
    for c in range(2):
        for i in range(n[c]):
            if not i in M[c]:
                isTrue = True
                isFalse = True
                for x in M[1-c]:
                    isFalse &= not x in G[c][i]
                    isTrue &= x in G[c][i]
                res &= isTrue or isFalse
    return res
  
#tri linéaire d'un tableau d'entiers
def triDegree(d):
    lenD= [len(d[0]),len(d[1])]
    sortedD = [[[] for i in range(lenD[1]+1)],[[] for i in range(lenD[0]+1)]]
    res = [[],[]]
    for c in range(2):
        for i in range(lenD[c]):
            sortedD[c][lenD[1-c] - d[c][i][1]] += [d[c][i]]
    for c in range(2):
        i = 0
        while i < lenD[1-c]+1:
            if len(sortedD[c][i])>0:
                res[c].append(sortedD[c][i].pop())
            else:
                i += 1

    return res

#connected components
def connectedComps(M):
    toVisit = [[],[]]# élements à visiter
    flagsVisited = [[0 for i in range(n[0])],[0 for i in range(n[1])]]# flags pour marquer 
    n_V = [len(M[0]),len(M[1])] #nombre d'élements dans V
    counter = [0,0] #compteur pour compter le nombre d'élements visités
    comps = [] # liste des composantes connexes 

    while counter[0]+counter[1] < sum(n_V):
        c = 0
        if counter[0] == n_V[0]:
            c = 1
        
        for i in range(n[c]):
            if flagsVisited[c][i]==0 and i in M[c]:
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
                    if flagsVisited[1-c][x] == 0 and x in M[1-c]:
                        toVisit[1-c].append(x)
                
        comps += [comp]
    return comps

#à verifier: linéarité, pourquoi les flags deviennent obsolètes  
def co_connectedComps(M):
    #elements non visités
    nonVisited = [set(),set()]
    for c in range(2):
        nonVisited[c].update(M[c])
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

#Decomposition K+S
def KpS(M):
    deg = [[],[]]#deg[0] est la liste des sommets blancs dont les élements sont des tuples (vetrex,deg(vertex))
    comp = []#liste des composantes
    if lenL(M)==2:
        if len(M[0])==1:
            x = next(iter(M[0]))
            y = next(iter(M[1]))
            if y in G[0][x]:
                return[[{x},set()],[set(),{y}]]
        return([M])
    for c in range(2):
        for i in range(n[c]):
            if i in M[c]:
                s = 0
                for x in G[c][i]:
                    if x in M[1-c]:
                        s+=1
                deg[c] += [(i,s)]
    deg = triDegree(deg)
    n_w, n_b= len(deg[0]),len(deg[1])  
    r,s = 1,n_b 
    S_0,S_1 = 0,0
    old_r,old_s = 0,s
    while r < n_w+1 or s > 0:
        if deg[1][s-1][1] == r-1 and s>0: # s isolé?
            comp += [[set(),{deg[1][s-1][0]}]]
            S_1 += deg[1][s-1][1]
            s-=1
            old_s = s
        else:
            while True:
                S_0 += deg[0][r-1][1]
                while s > 0 and deg[1][s-1][1]<r:
                    S_1 += deg[1][s-1][1]
                    s-=1
                if S_0 == r*s + S_1:
                    comp += [[{deg[0][i][0] for i in range(old_r,r)},{deg[1][i][0] for i in range(s,old_s)}]]
                    old_r,old_s = r,s
                    r+=1
                    break
                r += 1
    return(comp)

#retourne une composante avec les sommets triés 
def sortedDegreesComp(M):
    deg = [[],[]]#deg[0] est la liste des sommets blancs dont les élements sont des tuples (vetrex,deg(vertex))
    
    for c in range(2):
        for i in range(n[c]):
            if i in M[c]:
                s = 0
                for x in G[c][i]:
                    if x in M[1-c]:
                        s+=1
                deg[c] += [(i,s)]
    deg = triDegree(deg)
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

#separateurs contenant x,y de couleur col
def separators(x,y,col):
    neighborhood = [list(G[col][x]),list(G[col][y])]
    sortedGamma = [[-1 for i in range(n[1-col])],[-1 for i in range(n[1-col])]]

    for r in range(2):
        for x in neighborhood[r]:
            sortedGamma[r][x]=x
        i = 0
        while i < len(sortedGamma[r]):
            if sortedGamma[r][i]==-1:
                sortedGamma[r].pop(i)
            else:
                i+=1
    res = []
    i = 0
    j = 0
    while i < len(sortedGamma[0]) and j < len(sortedGamma[1]):
        if sortedGamma[0][i]==sortedGamma[1][j]:                
            i+=1
            j+=1
        elif sortedGamma[0][i]>sortedGamma[1][j]:
            res += [sortedGamma[1][j]]
            j+=1
        else:
            res += [sortedGamma[0][i]]
            i+=1
    
    while i < len(sortedGamma[0]):
        res += [sortedGamma[0][i]]
        i+=1
    while j < len(sortedGamma[1]):
        res += [sortedGamma[1][j]]
        j+=1

    return res

#Plus petit bimodule contenant x,y de couleur col
def PPBuv(x,y,col):
    M = [set(),set()]
    F = [[],[]]
    
    M[col].update({x})
    F[col].append(y)
    last = [-1,-1]
    last[col]=x
    while lenL(F) != 0:
        c = 0
        if len(F[c])==0:
            c = 1
        u = F[c].pop()
        v = last[c]
        if v!=-1:
            S = separators(u,v,c)
            F[1-c]+=[x for x in S if not x in M[1-c]]#à vérifier 04/05 (éviter les boucles infinies)
        M[c].add(u)
        last[c] = u

    return M 

#Donne pour chaque u l'ensemble PPBu trié
def PPB():
    L = [{},{}]
    for c in range(2):
        for u in range(n[c]):
            listePPBTriee = [[] for i in range(N+1)]
            for v in range(n[c]):
                I = [set(),set()]
                I[c].update({u,v})
                M = PPBuv(u,v,c)
                listePPBTriee[lenL(M)] += [M]
            finalPPBList = []
            for l in listePPBTriee:
                for m in l:
                    if lenL(m)!= N:
                        finalPPBList += [m]
            L[c][u] = finalPPBList
    return L

#L'union de A et B est un bimodule
def unionIsBimodule(A,B):
    if (len(A[0])==0 and len(B[1])==0) or (len(A[1])==0 and len(B[0])==0):#à verifier 04/05
        return True
    isBim = True
    for c in range(2):
        if len(A[c])>0 and len(B[c])>0:
            a = next(iter(A[c]))
            b = next(iter(B[c]))
            sep = set(separators(a,b,c))
            isBim &= sep.issubset(A[1-c].union(B[1-c]))
    return isBim

#Afficher la décomposition
def displayTree(T,t):
    if t == 0:
        print("Decomposition:")
    if T[0]=="leaf" or T[0]=="c-indecomposable":
        for i in range(t):
            print("--",end="")
        print(T)
    else:
        for i in range(t):
            print("--",end="")
        print(T[0])
        for i in range(1,len(T)):
            displayTree(T[i],4+t)
 
#décomposition récursive de M
def recursiveDecompose(M,listPPB):
    if lenL(M)==1:
        return(("leaf",M))#M est un sommet

    comps = KpS(M)
    if len(comps)>1:#M est un K+S
        return([("K+S",M)]+[recursiveDecompose(comp,listPPB) for comp in comps])
    else:
        comps = co_connectedComps(M)
        if len(comps)>1:#M est un série
            return([("serie",M)]+[recursiveDecompose(comp,listPPB) for comp in comps])
        else:
            comps = connectedComps(M)
            if len(comps)>1:#M est parallele
                return([("parallele",M)]+[recursiveDecompose(comp,listPPB) for comp in comps])
            else:#M est premier
                F = []
                for c in range(2):
                    for x in M[c]:
                        #pour chaque x,c on cherche i tq listPPB[c][x][i] est de taille inférieur à M
                        i = len(listPPB[c][x])-1
                        while i>0:
                            if i<lenL(M):
                                if listPPB[c][x][i][0]<M[0] and listPPB[c][x][i][1]<M[1]:
                                    break
                            i-=1
                        F+= [listPPB[c][x][i]]
                
                #calcul des classes d'équivalences pour la relation R(M,N) si M union N est un bimodule
                comps = [F.pop()]
                for m in F:
                    isAlreadyComponent = False
                    for i in range(len(comps)):
                        union = [m[0].union(comps[i][0]),m[1].union(comps[i][1])]
                        if len(union[0])!=1 or len(union[1])!=1:#à verifier 04/05
                            isBim = unionIsBimodule(m,comps[i])
                            if isBim:
                                isAlreadyComponent = True
                                comps[i] = union
                    if not isAlreadyComponent:
                        comps += [m]
                
                #séparation des sommets conflictuel
                finalComps = []
                for i in range(len(comps)):
                    for j in range(i+1,len(comps)):
                        inter = [comps[i][c].intersection(comps[j][c]) for c in range(2)]
                        if lenL(inter)!=0:
                            if len(inter[0])!=0:
                                finalComps+=[[inter[0],set()]]
                            if len(inter[1])!=0:
                                finalComps+=[[set(),inter[1]]]
                            comps[i]=[comps[i][0]-inter[0],comps[i][1]-inter[1]]
                            comps[j]=[comps[j][0]-inter[0],comps[j][1]-inter[1]]
                    finalComps += [comps[i]]
                
                return([("premier",M)]+[recursiveDecompose(comp,listPPB) for comp in finalComps])

#décomposition bimodulaire de G
def decompositionTree():
    M = [{i for i in range(n[0])},{i for i in range(n[1])}]
    listPPB = PPB()
    tree = recursiveDecompose(M,listPPB)
    displayTree(tree,0)
    return True

"""
n = [4,4]
Gw = [{0,1},{1,2},{2},{0,1,2}] # liste d'adjacence les noeuds blancs G_white

n = [11,10]
Gw = [{0,1},{1,2},{2},{0,1,2},{0,3,1,2,4,7,8,9},{0,1,2,3,5,7,8,9},{0,1,2,3,5,6},{0,1,2,3,7,8},{0,1,2,3,8},{0,1,2,3,8,9},{0,1,2,3,9}]
"""
n = [2,2]
Gw = [{0},{1}]#2K2
"""
n = [3,4]
Gw = [{0,1},{1,2},{2,3}]#P7

n = [4,3]
Gw = [{0,1},{1},{1,2},{2}]#Star123
"""
#Gw = randomGen(n,0.7)
N = n[0]+n[1]
G=[Gw,Gb(Gw,n)] #création du graphe avec la liste d'adjacence blanche et noir

M = [{i for i in range(n[0])},{i for i in range(n[1])}]
print(Gw)
coms = connectedComps(M)
print("BFS: ", coms)
coms_b = co_connectedComps(M)
print("BFS_b: ", coms_b)
kpsComp = KpS(M)
sortedPos = positionKpsPlot(sortedDegreesComp(M))
print("K+S: ",kpsComp)

decompositionTree()

#affichage
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
    if posPlot == 0:
        nx.draw(G, with_labels=True, font_weight='bold',node_color=colors)
    else:
        nx.draw(G, with_labels=True, font_weight='bold',node_color=colors,pos=sortedPos)
    
    #show G_barre
    plt.figure()
    r = random.randint(0, 10)
    for i in range(len(coms_b)):
        for c in range(2):
            for y in coms_b[i][c]:
                colors[y+c*n[0]] = color[(i*13+r)%len(color)]
    if posPlot == 0:
        nx.draw(G_barre, with_labels=True, font_weight='bold',node_color=colors)
    else:
        nx.draw(G_barre, with_labels=True, font_weight='bold',node_color=colors,pos=sortedPos)
    
    #show K+s
    try:
        plt.figure()
        l = 0
        plotReadyKPSComp = [[comp[0],{f(x) for x in comp[1]}]for comp in kpsComp]
        for i in range(len(kpsComp)-1):
            l += max(len(kpsComp[i][0]),len(kpsComp[i][1]))+2
            plt.axline((l-1, 1), (l-1, 2),color="red")
        pos = positionKpsPlot(plotReadyKPSComp)
        nx.draw(G, with_labels=True, pos=pos)

    except:
        plt.figure()
        print("problem with K+S")
        nx.draw(G, with_labels=True, pos=sortedPos)

    plt.show()
