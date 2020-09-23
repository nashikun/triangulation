import random,math,copy,triangulation,sys,tas,numpy
from itertools import combinations

class Graphe:
    def __init__(self,nom=''):
        self.sommets=[]
        self.aretes=[]
        self.n=0
        self.m=0
        self.name=nom        

    def __str__(self):
        text="V({})=".format(self.name)+"{\n"
        for x in self.sommets:
            text+= str(x)
        text+="}\n"+" E({})".format(self.name)+"{\n"
        for x in self.aretes:
            text+=str(x)
        text+="}"
        return text
       
    def ajouteSommet(self,x,y):
        som=Sommet(x,y)
        self.sommets.append(som)
        self.n+=1
        return som

    def connecte(self,x,y,Vitesse,Longueur):
        Ar=Arete(x,y,Vitesse,Longueur)
        self.aretes.append(Ar)
        x.aretes.append(Ar)
        y.aretes.append(Ar)
        self.m+=1
        return Ar
    
    def renomme(self,name):
        self.name=name

    def ajouteRoute(self, v1, v2, vmax):
        return self.connecte(v1,v2,vmax,v1.distance(v2))
       
    def ajouteNationale(self, v1,v2):
        res = self.ajouteRoute(v1,v2,90)
        res.color=(.3,0.,0.)
        return res

    def ajouteDepartementale(self, v1,v2):
        res = self.ajouteRoute(v1,v2,60)
        res.color=(.3,.3,0.)
        return res

    def trace(self,afficheur):
        afficheur.renomme(self.name)
        for x in self.sommets:
            afficheur.changeCouleur(x.couleur)
            afficheur.tracePoint(x.sommet)
            if x.label != None:
                afficheur.traceTexte(x.sommet,x.label)
        for x in self.aretes:
            afficheur.changeCouleur(x.couleur)
            afficheur.traceLigne(x.sommets[0].sommet,x.sommets[1].sommet)

    def djikstra(self,depart):
        for s in self.sommets:
            s.chemin=None
        cumul={s: sys.float_info.max for s in self.sommets}
        cumul[depart]=0
        L=[depart]
        while L:
            s=L.pop(L.index(min(L,key = lambda x:cumul[x])))
            for e in s.aretes:
                s2=e.voisin(s)
                if cumul[s]+e.cout<cumul[s2]:
                    if cumul[s2]==sys.float_info.max:
                        L.append(s2)
                    s2.chemin=e
                    cumul[s2]=cumul[s]+e.cout

    def traceArbreDesChemins(self):
        for s in self.sommets:
            if s.chemin is None:
                s.couleur=(0.,1.,0.)
            else:
                s.chemin.couleur=(0.,1.,0.)

    def fixeCarburantCommeCout(self):
        for s in self.aretes:
            s.cout=s.length
       
    def fixeTempsCommeCout(self):
        for s in self.aretes:
            s.cout=s.length/s.Vit

    def cheminOptimal(self,arrivee):
        d=arrivee
        L=[]
        while d.cout != None:
            L.append[d.chemin]
            d=d.chemin.voisin(d)
        return L[::-1]

    def colorieChemin(self,chemin,c):
        for e in chemin:
            e.couleur=c
        if len(chemin)>1:
            for i in chemin[0].sommets:
                if i not in chemin[1].sommets:
                    d=i
                    break
            for i in chemin[-1].sommets:
                if i not in chemin[-2].sommets:
                    f=i
                    break
            d.couleur=c
            f.couleur=c

            
    def djikstraAvecTas(self,depart):
        for s in self.sommets:
            s.chemin=None
        cumul={s: sys.float_info.max for s in self.sommets}
        cumul[depart]=0
        L=tas.Tas(lambda s : cumul[s])
        depart.cle=L.ajoute(depart)
        while not L.empty():
            s=L.pop()
            for e in s.aretes:
                s2=e.voisin(s)
                if cumul[s]+e.cout<cumul[s2]:
                    if cumul[s2]==sys.float_info.max:
                        s2.cle=L.ajoute(s2)
                    s2.chemin=e
                    cumul[s2]=cumul[s]+e.cout
                    L.actualise(s2.cle)
            
    def djikstraPartiel(self,depart,arrivee):
        for s in self.sommets:
            s.chemin=None
            cumul={s: sys.float_info.max for s in self.sommets}
            cumul[depart]=0
            L=tas.Tas(lambda s : cumul[s])
            depart.cle=L.ajoute(depart)
            count=1
            k=1
        while k:
            if L.empty():
                return -1
            s=L.pop()
            for e in s.aretes:
                s2=e.voisin(s)
                if cumul[s]+e.cout<cumul[s2]:
                    if cumul[s2]==sys.float_info.max:
                        s2.cle=L.ajoute(s2)
                        s2.chemin=e
                        cumul[s2]=cumul[s]+e.cout
                        L.actualise(s2.cle)
                        count+=1
                    if s2==arrivee:
                        k=0
                        break

    def astar(self,depart,arrivee,moncout=lambda x,y: x.distance(y) ):
        for s in self.sommets:
            s.chemin=None
            cumul={s: sys.float_info.max for s in self.sommets}
            cumul[depart]=0
            L=tas.Tas(lambda s : cumul[s]+moncout(s,arrivee))
            depart.cle=L.ajoute(depart)
            count=1
            k=1
        while k:
            if L.empty():
                return -1
            s=L.pop()
            for e in s.aretes:
                s2=e.voisin(s)
                if cumul[s]+e.cout<cumul[s2]:
                    if cumul[s2]==sys.float_info.max:
                        s2.cle=L.ajoute(s2)
                        s2.chemin=e
                        cumul[s2]=cumul[s]+e.cout
                        L.actualise(s2.cle)
                        count+=1
                    if s2==arrivee:
                        k=0
                        break

    def matriceCout(self, tournee):
        l=len(tournee)
        C=numpy.zeros((l,l))
        for i,s in enumerate(tournee):
            s.label=i
            self.djikstraAvecTas(s)
            for j,s2 in enumerate(tournee):
                cout=0
                d=s2
                while d.chemin != None:
                    cout+=d.chemin.cout
                    d=d.chemin.voisin(d)
                c[i,j]=cout
        return c

    def voyageurDeCommerceNaif(self,tournee):

        C=self.matriceCout(tournee)
        l=len(tournee)
        meilleurItineraire=[]
        minCout=sys.float_info.max
        visites=[False for i in range(l)]
        curPath=[]
        curCost=0

        def backtrack(curCost):
            nonlocal C,l,meilleurItineraire,minCout,visites,curPath
            if curCost>=minCost:
                return False
            if len(curPath)==l+1:
                minCost=curCost
                meilleuritineraire=curPath[:]
                return True
            if len(curPath)==l:
                curCost+=C[curPath[-1].label,0]
                curPath.append(0)
                return backtrack() 
            for i,t in tournee:
                if visites[i]==0:
                    cost=C[CurPath[-1].label,t.label]
                    curCost+=cost
                    curPath.append(t)
                    res=backtrack()
                    if res:
                        return res
                    else:
                        curCost-=Cost
                        curCost.pop()
            return False
        backtrack()
        return minCout,meilleurItineraire

    def Prim(self):
        ar=self.aretes[0]
        ar.selection=true
        def f(e):
            c=sys.float_info.max
            if e.sommets[0] in som ^ e.sommets[1] in som:
                c=e.cost
            return c
        
        tas=Tas(f)
        for e in self.aretes:
            e.clef=tas.ajoute(f(e))

        while not tas.empty:
            ar=tas.pop()
            ar.selection=True
            for i in [0,1]:
                k=ar.sommets[i]
                if k not in som:
                    k.selection=True
                    for e in k.aretes:
                        tas.actualise(e.cle)
                    
    def colorieSelection(self,couleur):
        for x in self.sommets:
            if x.selection: x.couleur=couleur
        for x in self.aretes:
            if x.selection: x.couleur=couleur

    def grapheDeCout(self,tournee):
        h=Graphe()
        C=self.matriceCout(tournee)
        l=len(C)
        for i in range(l):
            x,y=tournee[i]
            h.ajouteSommet(x,y)
            tournee[i].Image=h.sommets[i]
            h.sommets[i].Image=tournee[i]
            h.label=str(i+1)
        for i in range(0,l-1):
            for j in range(i+1,l):
                h.connecte(h.sommets[i],h.sommets[j],0,C[i,j])
        return h 
                
                
class Arete:
    def __init__(self,s1,s2,Vitesse,Longueur):
        self.sommets = [s1,s2]
        self.selection=False
        self.Vit=Vitesse
        self.length=Longueur
        self.couleur=(0.,0.,0.)
        self.cout=1
        self.cle=None
        
    def __str__(self):
        return  "  { {"+self.sommets[0].Name+" - "+self.sommets[1].Name+ "}" + " (long. = {} km vlim. = {} km/h) \n" .format(self.length,self.Vit)
        
    def voisin(self,x):
        if x==self.sommets[0]:
            return self.sommets[1]
        elif x==self.sommets[1]:
            return self.sommets[0]
        return -1

    
class Sommet:
    def __init__(self,x,y):
        self.sommet=(x,y)
        self.selection=False
        self.couleur=(0.,0.,0.)
        self.aretes=[]
        self.chemin=None
        self.cle=None
        self.label=None
        self.Image=None

    def __str__(self):
        return  "  {}  (x = {} km y = {} km ) \n".format(self.label,self.sommet[0],self.sommet[1])

    def distance(self,v):
        return math.sqrt((self.sommet[0]-v.sommet[0])**2+(self.sommet[1]-v.sommet[1])**2)

   
def pointsAleatoires(n,L):
    graphe=Graphe()
    for i in range(n):
        ar=(random.uniform(-L/2,L/2),random.uniform(-L/2,L/2))
        while Sommet(ar[0],ar[1]) in graphe.sommets:
            ar=(random.uniform(-L/2,L/2),random.uniform(-L/2,L/2))
        graphe.ajouteSommet(ar[0],ar[1])
    return graphe

def test_gabriel(g, v1, v2):
    d=v1.distance(v2)/2
    c=Sommet((v1.sommet[0]+v2.sommet[0])/2,(v1.sommet[1]+v2.sommet[1])/2)
    for v in g.sommets:
        if v != v1 and v != v2 and c.distance(v)<d:
            break
    else:
        return True
    return False
    
def test_gvr(g,v1,v2):
    d=v1.distance(v2)
    for v in g.sommets:
        if v!=v1 and v !=v2 and v1.distance(v)<d and  v2.distance(v)<d:
            break
    else:
        return True
    return False

def gabriel(g):
    h=copy.deepcopy(g)
    for v1,v2 in combinations(g.sommets,2):
        if test_gabriel(g,v1,v2):
            h.ajouteRoute(v1,v2,0)
    return h

def gvr(g):
    h=copy.deepcopy(g)
    for v1,v2 in combinations(h.sommets,2):
        if test_gabriel(h,v1,v2):
            h.ajouteRoute(v1,v2,0)
    return h

def reseau(g):
    for s1,s2 in combinations(g.sommets,2):
        if test_gabriel(g, s1, s2):
            if test_gvr(g,s1,s2):
                g.ajouteNationale(s1,s2)
            else:
                g.ajouteDepartementale(s1,s2)   
    return g

def timing(fonction):
    timing=[]
    for i in range(1,3):
        start=time.time()
        for j in range(10):
            fonction(pointsAleatoires(10**i,10*random.random()))
        timing.append((time.time()-start)/10)
    return timing

def delaunay(g):
    t=triangulation.Triangulation(g)
    def selectionneAretes(graphe,v1,v2,v3,v4):
        graphe.ajouteNationale(v1, v2)
    g = t.construitGrapheDeSortie(selectionneAretes)
    g.renomme("Delaunay(" + str(g.n()) + ")");
    return g

def reseaurapide(g):
    t=triangulation.Triangulation(g)
    def selectionneAretes(graphe,v1,v2,v3,v4):
        d=v1.distance(v2)
        c=Sommet((v1[0]+v2[0])/2,(v1[1]+v2[1])/2)
        for v in [v3,v4]:
            if c.distance(v)<d/2:
                break
            else:
                for v in [v3,v4]:
                    if v.distance(v1)<d and v.distance(v2)<d:
                        graphe.ajouteNationale(v1, v2)
                        break
                else:
                    graphe.ajouteDepartementale(v1,v2)
    g = t.construitGrapheDeSortie(selectionneAretes)
    g.renomme("Delaunay(" + str(g.n()) + ")");
    return g
