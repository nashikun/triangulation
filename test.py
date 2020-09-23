# coding: utf-8

import graphe,graphique

def creerGrapheFigure1():
    '''Crée le Graphe de la figure 1'''
    g = graphe.Graphe("Graphe de la figure 1")
    s1 = g.ajouteSommet(1.0, 1.0,couleur=(1.,0.,0.))
    s2 = g.ajouteSommet(2.0, 3.5,couleur=(1.,0.,0.))
    s3 = g.ajouteSommet(2.5, 2.5,couleur=(1.,0.,0.))
    s4 = g.ajouteSommet(5.0, 2.0,couleur=(1.,0.,0.))
    g.connecte(s1, s2, 4.0, 90.,couleur=(0.,1.,0.))
    g.connecte(s1, s4, 5.2, 124.,couleur=(0.,1.,0.))
    g.connecte(s2, s3, 2.0, 54.,couleur=(0.,1.,0.))
    g.connecte(s2, s4, 5.0, 90.,couleur=(0.,1.,0.))
    return g

def testQuestion1_2():
    '''Teste que la création d'un graphe ne plante pas '''
    print("Question 1.2 :")
    creerGrapheFigure1()
    print("Ok. Pas de plantage")  

def testQuestion1_3(): 
    ''' Teste l'affichage d'un graphe dans la console '''
    print("Question 1.3 :")
    g = creerGrapheFigure1()
    print(g)
    
def testQuestion1_4(): 
    ''' Teste l'affichage graphique d'un graphe '''
    graphique.affiche(graphe.reseau(graphe.pointsAleatoires(100,3)), (-3.,3.), 30.)

def testQuestion3_1():
    g=graphe.reseau(graphe.pointsAleatoires(100,3))
    g.djikstra(g.sommets[0])
    g.traceArbreDesChemins()
    graphique.affiche(g,(-3.,3.), 100.)

def testQuestion3_2():
    g=graphe.reseau(graphe.pointsAleatoires(30,3))
    g.fixeCarburantCommeCout()
    g.astar(g.sommets[0],g.sommets[29])
    for s in g.sommets:
        if s.chemin != None:
            s.chemin.couleur=(0.,1.,0.)
    graphique.affiche(g,(-3.,3.), 100.)
    


if __name__ == "__main__":
#    testQuestion1_2()
#    testQuestion1_3()
    testQuestion3_1()
    
