# coding: utf-8
# La ligne précédente est indispensable pour accpeter les accents dans le fichier 

# Importe les modules qui seront nécessaires
import math     # Fonctions mathématiques : math.cos, math.sin, math.pi, etc
import random   # Générateurs de nombres aléatoires
import numpy    # Calcul numérique sur des vecteurs, matrices, etc

# Importe le fichier graphique.py qui 
import graphique

class Sommet:
    '''Classe représentant un sommet d'un polygone'''
    
    def __init__(self, theta, r):
        '''Constructeur de la classe Sommet : (theta,r) sont les coordonnées polaires du sommet self'''
        self.deplace(theta, r)

    def deplace(self, theta, r):
        '''Déplace le sommet  self: (theta,r) sont les nouvelles coordonnées polaires'''
        
        # Sauvegarde les coordonnées polaires dans des attributs de l'objet self
        self.theta = theta
        self.r = r
        
        # Calcule les coordonnées cartésiennes (pour l'affichage)
        # On utilise la bibliothèque de calcul numérique numpy.
        self.pos = numpy.array([math.cos(theta), math.sin(theta)]) * r
        
    def __str__(self):
        '''Fonction spéciale de conversion en chaîne de caractères'''
    
        chaine = '({:0.2f},{:0.2f})'.format(self.pos[0], self.pos[1])
        return chaine
    
class Polygone:
    ''' Classe représentant un polygone du plan'''
    
    def __init__(self, n, R):
        '''Constructeur d'un objet Polygone : crée un polygone régulier
            à n sommets placés sur le cercle de rayon R centré sur l'origine'''
        
        # Vérifie que les arguments ont le type attendu
        assert isinstance(n, int)
        assert isinstance(R, float)
         
        # Crée comme attribut de self une liste pour accueillir les sommets
        self.sommets = []
        
        # Crée un attribut pour stocker le nom du polygone
        self.nom = str(n) + "-polygone régulier"

        # Remplie la liste des n sommets
        alpha = 2. * math.pi / n
        angle = math.pi / 2.
        for _ in range(n):
            self.sommets.append(Sommet(angle, R))
            angle += alpha

    def __str__(self):
        '''Fonction spéciale de conversion en chaîne de caractères'''
        chaine = self.nom + ' = ('
        if(len(self.sommets) > 0):
            chaine += str(self.sommets[0])
            for s in self.sommets[1:]:
                chaine += ', ' + str(s)
        chaine += ')'
        return chaine

    def secoue(self, amplitudeAngulaire, amplitudeRadiale):
        '''Fonction qui déplace aléatoirement chaque sommet selon une amplitude angulaire et radiale réglable'''
        
        # Modifie les coordonnées de chaque sommet à l'aide de la méthode deplace
        for s in self.sommets:
            s.deplace(
                s.theta + (random.random() * 2. - 1.) * amplitudeAngulaire, 
                s.r * (1. + (random.random() * 2. - 1.) * amplitudeRadiale)
            )
            
        # Change le nom du polygone
        self.nom = str(len(self.sommets)) + "-polygone secoué"
            
        
    def trace(self, afficheur):
        '''Fonction de dessin'''
        
        assert isinstance(afficheur, graphique.Afficheur)
        
        afficheur.renomme(self.nom)
        precedent = self.sommets[-1]
        afficheur.changeCouleur((0.,0.,0.))
        
        for suivant in self.sommets:
            afficheur.traceLigne(precedent.pos, suivant.pos)
            precedent = suivant
            
        afficheur.changeCouleur((1.,0.,0.))
        for sommet in self.sommets:
            afficheur.tracePoint(sommet.pos)


if __name__ == "__main__":
    triangle = Polygone(3, 10.)
    print(triangle)
    graphique.affiche(triangle, (0., 0.), 10., blocage = False)

    heptagone = Polygone(7, 10.)
    heptagone.secoue(math.pi / 5, 0.1)
    graphique.affiche(heptagone, (0., 0.), 10.)
