# coding: utf-8

import sys
import math

def distanceAuCarre(v1, v2):
    dx = (v1.x() - v2.x())
    dy = (v1.y() - v2.y())
    return dx**2+dy**2

def conditionDeDelaunay(A, B, C, D):
    dab2 = distanceAuCarre(A,B)
    dad2 = distanceAuCarre(A,D)
    dbc2 = distanceAuCarre(B,C)
    dbd2 = distanceAuCarre(B,D)
    dcd2 = distanceAuCarre(C,D)
    cosa = (dab2 + dad2 - dbd2) / (2 * math.sqrt(dab2) * math.sqrt(dad2))
    cosc = (dbc2 + dcd2 - dbd2) / (2 * math.sqrt(dbc2) * math.sqrt(dcd2))
    sina2 = 1. - cosa * cosa
    if(sina2 > 0.):
        sina = math.sqrt(sina2)
    else:
        sina = 0. 
    sinc2 = 1. - cosc * cosc
    if(sinc2 > 0.):
        sinc = math.sqrt(sinc2)
    else:
        sinc = 0.
    return sina * cosc + cosa * sinc >= 0

class Triangulation:
    
    class QuadEdge:
        '''Classe définissant un quad-edge : une arête connectée à deux faces et deux sommets'''
        def __init__(self, f1, f2, v1, v2):
            self.f1 = f1;
            self.f2 = f2;
            self.v1 = v1;
            self.v2 = v2;
        
        def __eq__(self, e):
            '''Méthode qui teste si deux quad-edges ont même extrémités'''
            if((self.v1 == e.v1) and (self.v2 == e.v2)):
                return True
            elif((self.v1 == e.v2) and (self.v2 == e.v1)):
                return True
            else:
                return False
        
        def __str__(self):
            return str(self.v1) + " - " + str(self.v2);
               
        def remplaceFace(self, ancienneFace, nouvelleFace):
            '''Méthode qui remplace une face adjacente au quad-edge par une autre'''
            if(self.f1 == ancienneFace):
                self.f1 = nouvelleFace
            else:
                self.f2 = nouvelleFace
    
    def lanceAlgorithme(self):
        # Construit la triangulation initiale. Complexité en O(n log(n))
        self.construitTriangulationInitiale()
        
        # Bascule les arêtes de la triangulation jusqu'à obtenir la triangulation de Delaunay
        self.basculeAretes()

        # Efface les sommets à l'infini
        for _ in range(3):
            self.graphe.sommets.pop()
        
    def __init__(self, g):
        '''Constructeur de la classe triangulation qui prend en entrée un nuage de points 
        et crée une triangulation de Delaunay'''
        self.racine = None
        self.quadEdges = []
        self.graphe = g;
        self.lanceAlgorithme()

    class Triangle:
        def __init__(self, v1, v2, v3):
            self.v1 = v1
            self.v2 = v2
            self.v3 = v3
            self.t12 = None
            self.t13 = None
            self.t23 = None
            self.e12 = None
            self.e13 = None
            self.e23 = None
            
        def contient(self, v):            
            ''' Méthode qui teste si un sommet est à l'intérieur d'un triangle'''
            v1 = self.v1; v2 = self.v2; v3 = self.v3
            det = (v1.x() - v3.x()) * (v2.y() - v3.y()) - (v1.y() - v3.y()) * (v2.x() - v3.x())
            c1 = ((v2.y() - v3.y()) * (v.x() - v3.x())+ (v3.x() - v2.x()) * (v.y() - v3.y())) * det  
            c2 = ((v3.y() - v1.y()) * (v.x() - v3.x())+ (v1.x() - v3.x()) * (v.y() - v3.y())) * det
            return (c1 > 0) and (c2 > 0) and (c1 + c2 < det * det)

        def trouve(self, v):
            '''Méthode récursive qui renvoie le triangle d'une triangulation qui contient un sommet.
            Renvoie le triangle contenant v, None si v n'est pas dans la triangulation'''
            
            t12 = self.t12; t13 = self.t13; t23 = self.t23
            if(t12 == None):
                return self
            else:
                if(t12.contient(v)):
                    return t12.trouve(v);
                elif(t13.contient(v)):
                    return t13.trouve(v);
                elif(t23.contient(v)):
                    return t23.trouve(v);
                else: 
                    return None;

        def aPourSommet(self, v):
            '''Méthode qui teste si un sommet est un sommet d'un triangle
            Renvoie vrai si v est un sommet du triangle'''
            return self.v1 == v or self.v2 == v or self.v3 == v

        def troisiemeSommet(self, a, b):
            ''' Renvoie le troisième sommet d'un triangle à partir des deux autres'''
            
            if(self.v1 != a and self.v1 != b):
                return self.v1
            elif(self.v2 != a and self.v2 != b):
                return self.v2
            else: 
                return self.v3

        def remplaceSommet(self, ancienSommet, nouveauSommet):
            ''' Méthode qui substitue un sommet par un autre dans un triangle '''
            if(self.v1 == ancienSommet):
                self.v1 = nouveauSommet
            elif(self.v2 == ancienSommet):
                self.v2 = nouveauSommet
            elif(self.v3 == ancienSommet):
                self.v3 = nouveauSommet
            else:
                raise Exception("Bad vertex" + ancienSommet)

        def retrouveArete(self, v1, v2):
            '''Méthode qui renvoie le quad-edge d'un triangle ayant deux sommets pour extrêmités'''
            e = Triangulation.QuadEdge(None, None, v1, v2);
            if(self.e12 == e):
                return self.e12;
            elif(self.e13 == e):
                return self.e13;
            elif(self.e23 == e):
                return self.e23;
            else:
                raise Exception("getEdge");           

        def remplaceArete(self, ancienneArete, nouvelleArete):
            '''Méthode qui substitue le quad-edge d'un triangle par un autre'''     
            if(self.e12 == ancienneArete):
                self.e12 = nouvelleArete
            elif(self.e13 == ancienneArete):
                self.e13 = nouvelleArete
            elif(self.e23 == ancienneArete):
                self.e23 = nouvelleArete
            else:
                raise Exception("changeEdge")
    
    def construitTriangleInitial(self):
        '''Méthode qui construit une triangulation initiale faite de trois sommets à l'infini'''
        xmin = sys.float_info.max
        xmax = sys.float_info.min
        ymin = sys.float_info.max
        ymax = sys.float_info.min
        
        for v in self.graphe.sommets:
            if(v.x() > xmax):
                xmax = v.x()
            if(v.x() < xmin):
                xmin = v.x()
            if(v.y() > ymax):
                ymax = v.y()
            if(v.y() < ymin):
                ymin = v.y()

        k = 1.1E2
        width = k*(xmax - xmin)
        height = k*(ymax - ymin)

        v1 = self.graphe.ajouteSommet(xmin - width, ymin - height)
        v2 = self.graphe.ajouteSommet(xmax + width, ymin - height)
        v3 = self.graphe.ajouteSommet((xmin+xmax)/2, ymax + height)
        
        self.racine = Triangulation.Triangle(v1, v2, v3)
        
        e12 = Triangulation.QuadEdge(None, self.racine, v1, v2)
        e13 = Triangulation.QuadEdge(None, self.racine, v1, v3)
        e23 = Triangulation.QuadEdge(None, self.racine, v2, v3)
        self.racine.e12 = e12
        self.racine.e13 = e13
        self.racine.e23 = e23

    def supprimeAretes(self):
        for s in self.graphe.sommets:
            s.aretes.clear()
    
    def construitTriangulationInitiale(self):
        self.quadEdges = [];
        self.construitTriangleInitial()
        
        for v in self.graphe.sommets:
            t = self.racine.trouve(v)
            if(t != None):
                t.t12 = Triangulation.Triangle(t.v1, t.v2, v)
                t.t13 = Triangulation.Triangle(t.v1, t.v3, v)
                t.t23 = Triangulation.Triangle(t.v2, t.v3, v)

                e1v = Triangulation.QuadEdge(t.t12, t.t13, t.v1, v)
                e2v = Triangulation.QuadEdge(t.t12, t.t23, t.v2, v)
                e3v = Triangulation.QuadEdge(t.t13, t.t23, t.v3, v)
                self.quadEdges.append(e1v)
                self.quadEdges.append(e2v)
                self.quadEdges.append(e3v)

                t.t12.e12 = t.e12
                t.e12.remplaceFace(t, t.t12)
                t.t12.e13 = e1v
                t.t12.e23 = e2v

                t.t13.e12 = t.e13
                t.e13.remplaceFace(t, t.t13)
                t.t13.e13 = e1v
                t.t13.e23 = e3v

                t.t23.e12 = t.e23
                t.e23.remplaceFace(t, t.t23)
                t.t23.e13 = e2v
                t.t23.e23 = e3v;   

    def basculeAretes(self):
        pile = []
        for qe in self.quadEdges:
            pile.append(qe)

        while(len(pile) > 0):
            e = pile.pop()
    
            f1 = e.f1
            f2 = e.f2
            if(f1 != None and f2 != None):
                v1 = e.v1
                v2 = e.v2
    
                v3 = f1.troisiemeSommet(v1, v2)
                v4 = f2.troisiemeSommet(v1, v2)
    
                if(not conditionDeDelaunay(v3, v1, v4, v2)):
                    v1v3 = f1.retrouveArete(v1, v3)
                    v2v3 = f1.retrouveArete(v2, v3)
                    v1v4 = f2.retrouveArete(v1, v4)
                    v2v4 = f2.retrouveArete(v2, v4)
                    f1.remplaceArete(v2v3, v1v4)
                    f2.remplaceArete(v1v4, v2v3)
                    v2v3.remplaceFace(f1, f2)
                    v1v4.remplaceFace(f2, f1)
                    f1.remplaceSommet(v2, v4)
                    f2.remplaceSommet(v1, v3)
                    e.v1 = v3
                    e.v2 = v4
                    pile.append(v1v3)
                    pile.append(v2v3)
                    pile.append(v1v4)
                    pile.append(v2v4)

    def construitGrapheDeSortie(self, selectionneArete):
        '''Méthode qui construit la triangulation de Delaunay à partir du nuage de points passé au constructeur'''

        # Sélectionne les arêtes
        graphe = self.graphe 
        racine = self.racine       
        for qe in self.quadEdges:
            v1 = qe.v1
            v2 = qe.v2
            if(not (racine.aPourSommet(v1) or racine.aPourSommet(v2))):
                v3 = qe.f1.troisiemeSommet(v1, v2)
                v4 = qe.f2.troisiemeSommet(v1, v2)                
                selectionneArete(graphe, v1, v2, v3, v4)
        return self.graphe;