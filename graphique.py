# coding: utf-8

import sys
import numpy as np
import math
import copy
import PySide.QtCore as qtcore
import PySide.QtGui as qtgui
import traceback

class Afficheur(qtgui.QWidget):
    afficheurs = []
    size = (800, 600)
    coord = np.array((50, 50))
    decalage = np.array((40,40))
    
    def __init__(self, sujet, centre, ech):
        super(Afficheur, self).__init__()
        if(not "trace" in dir(sujet)):
            raise Exception('Méthode "trace" non définie dans la classe ' + str(sujet.__class__))

        app = qtgui.QApplication.instance()
        if not app:
            app = qtgui.QApplication(sys.argv)
        desktop = app.desktop()
        screen = desktop.screenGeometry(desktop.screenNumber(self))

        self.rayon = 4
        self.ech = ech
        self.centre = np.array(centre)
        self.crayon = None
        self.sujet = sujet
        self.setStyleSheet("background-color: gray")
        self.center = np.array(Afficheur.size) / 2.
        self.setGeometry(Afficheur.coord[0] + screen.x(), Afficheur.coord[1] + screen.y(), Afficheur.size[0], Afficheur.size[1])
        Afficheur.coord += Afficheur.decalage
        self.setWindowTitle("Afficheur")
        self.show()        
        
    def __pointVersPixel(self, p): 
        p = np.array(p)
        pixel = (p - self.centre) * self.ech
        pixel[1] = -pixel[1]
        pixel += self.center
        return qtcore.QPoint(pixel[0],pixel[1])
    
    def __pixelVersPoint(self, pixel):
        p = np.array((pixel.x(), pixel.y())) - self.center
        p[1] = -p[1]
        p = p / self.ech + self.centre
        return p
    
    def __pixelVersVecteur(self, pixel1, pixel2):
        assert isinstance(pixel1, qtcore.QPoint)
        assert isinstance(pixel2, qtcore.QPoint)
        v = np.array((pixel2.x(), pixel2.y())) - np.array((pixel1.x(), pixel1.y()))
        v[1] = -v[1]
        v = v / self.ech
        return v
        
    def tracePoint(self, p):
        assert self.crayon != None
        assert isinstance(p, tuple) or isinstance(p, np.ndarray)
        assert isinstance(p[0], float)
        assert isinstance(p[1], float)
        pixel = self.__pointVersPixel(p)
        self.crayon.drawEllipse(pixel, self.rayon, self.rayon)

    def traceLigne(self, p1, p2):
        assert self.crayon != None
        assert isinstance(p1, tuple) or isinstance(p1, np.ndarray)
        assert isinstance(p1[0], float)
        assert isinstance(p1[1], float)
        assert isinstance(p2, tuple) or isinstance(p2, np.ndarray)
        assert isinstance(p2[0], float)
        assert isinstance(p2[1], float)
        pixel1 = self.__pointVersPixel(p1)
        pixel2 = self.__pointVersPixel(p2)
        self.crayon.drawLine(pixel1, pixel2)
    
    def changeCouleur(self, couleur):
        assert self.crayon != None
        assert isinstance(couleur, tuple)
        assert isinstance(couleur[0], float)
        assert isinstance(couleur[1], float)
        assert isinstance(couleur[2], float)
        c = qtgui.QColor(couleur[0]*255, couleur[1]*255, couleur[2]*255)
        self.crayon.setPen(c)
        self.crayon.setBrush(c)

    def traceTexte(self, p, texte):
        assert isinstance(p, tuple) or isinstance(p, np.ndarray)
        assert isinstance(p[0], float)
        assert isinstance(p[1], float)
        assert isinstance(texte, str)
        pixel = self.__pointVersPixel(p)
        pixel += qtcore.QPoint(10,-10)
        self.crayon.drawText(pixel, texte)     
        
    def renomme(self, titre):
#        assert isinstance(titre, str)
#        titre = unicode(titre, 'utf-8')
        self.setWindowTitle(titre)
        
    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.clic = pos
        pos = self.__pixelVersPoint(pos)
        self.centre = self.centre

    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.centre -= self.__pixelVersVecteur(self.clic, pos)
        self.clic = pos
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.centre -= self.__pixelVersVecteur(self.clic, pos)
        self.clic = pos
        self.update()

    def wheelEvent(self, event):
        pos = event.pos()
        C = self.__pixelVersPoint(pos)
        k1 = self.ech
        k2 = k1 * math.exp(0.001 * event.delta())
        self.centre = (self.centre * k1 + C * (k2 -k1)) / k2
        self.ech = k2
        self.update()

    def paintEvent(self, event):
        if(self.crayon != None):
            return
        self.crayon = qtgui.QPainter(self)
        self.trace()
        self.crayon = None
        
    def trace(self):
        self.crayon.setFont(qtgui.QFont('Decorative', 10))
        if(self.sujet != None):
            try:
                self.sujet.trace(self)
            except AttributeError:
                self.close()
                qtgui.QApplication.quit()
                raise Exception('Méthode "trace" non définie dans la classe ' + str(self.sujet.__class__))
            except BaseException:
                traceback.print_exc()                
                self.close()
                qtgui.QApplication.quit()
        L = 100.;
        x = 20; y = 20;
        self.crayon.setPen('white')
        msg = '{0:.2f} km'.format(L / self.ech)
        l = self.crayon.fontMetrics().boundingRect(msg).width()
        self.crayon.drawText(x + (L-l)/2, y-2, msg);
        self.crayon.drawLine(x, y, x + L, y);
        self.crayon.drawLine(x, y - L/20, x, y + L/10);
        self.crayon.drawLine(x + L, y - L/20, x + L, y + L/10);


    def sauvegarde(self):
        filename = qtgui.QFileDialog.getSaveFileName(self, 'Fichier PDF')
        if filename:
            printer = qtgui.QPrinter(qtgui.QPrinter.HighResolution)
            printer.setPageSize(qtgui.QPrinter.A4)
            printer.setColorMode(qtgui.QPrinter.Color)
            printer.setOutputFormat(qtgui.QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            
            self.crayon = qtgui.QPainter(printer)
            self.trace()
            self.crayon = None

def affiche(sujet, centre, ech, blocage = True):
    '''Affiche dans une fenêtre l'objet sujet qui doit avoir une méthode trace''' 
    assert isinstance(centre, tuple)
    assert isinstance(ech, float)
    sujet = copy.deepcopy(sujet)
    app = qtgui.QApplication.instance()
    if not app:
        app = qtgui.QApplication(sys.argv)
    a = Afficheur(sujet, centre, ech)
    Afficheur.afficheurs.append(a)
    if(blocage):
        bloque()
    return a

def bloque():
    app = qtgui.QApplication.instance()
    if not app:
        app = qtgui.QApplication(sys.argv)
    app.exec_()

