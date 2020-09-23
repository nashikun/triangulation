# coding: utf-8

class Tas:
	class Element:
		def __init__(self, valeur, priorite, index):
			self.valeur = valeur
			self.priorite = priorite
			self.index = index

		def __str__(self):
			return str(self.valeur)
			
	def __init__(self, fonctionPriorite):
		self.L = []
		self.fonctionPriorite = fonctionPriorite
	
	def __str__(self):
		s = "["
		for elt in self.L:
			s += " " + str(elt)
		s += "]"
		return s
	
	def __parent(self, elt):
		if(elt.index == 0):
			return None
		else:
			return self.L[(elt.index-1) // 2]
	
	def __fils_gauche(self, elt):
		i = 2 * elt.index + 1
		if(i < len(self.L)):
			return self.L[i]
		else:
			return None

	def __fils_droit(self, elt):
		i = 2 * elt.index + 2
		if(i < len(self.L)):
			return self.L[i]
		else:
			return None	
	
	def __deplace(self, elt, index):
		assert isinstance(elt, Tas.Element)
		ancien = elt.index
		self.L[index] = elt
		elt.index = index
		return ancien
		
	def __promeut(self, elt):
		while(True):
			parent = self.__parent(elt)
			if(parent == None):
				break
			if(parent.priorite >= elt.priorite):
				break
			elt.index = self.__deplace(parent, elt.index)
		self.__deplace(elt, elt.index)
	
	def actualise(self, elt):
		assert isinstance(elt, Tas.Element)
		elt.priorite = self.fonctionPriorite(elt.valeur)
		self.__promeut(elt)
		
	def ajoute(self, valeur):
		elt = Tas.Element(valeur, self.fonctionPriorite(valeur), len(self.L))
		self.L.append(elt)
		self.__promeut(elt)
		return elt
	
	def empty(self):
		return len(self.L) == 0
	
	def pop(self):
		n = len(self.L)
		if(n == 0):
			return None
		
		tete = self.L[0]
		elt = self.L[n - 1]
		elt.index = 0
		
		while True:
			filsGauche = self.__fils_gauche(elt)
			filsDroit = self.__fils_droit(elt)
			plusPrioritaire = elt
			if(filsGauche != None and filsGauche.priorite > plusPrioritaire.priorite):
				plusPrioritaire = filsGauche
			if(filsDroit != None and filsDroit.priorite > plusPrioritaire.priorite):
				plusPrioritaire = filsDroit
			elt.index = self.__deplace(plusPrioritaire, elt.index)
			if(plusPrioritaire is elt):
				break
		self.L.pop()
		return tete.valeur

#########################################
# Exemple d'utilisatio de la classe Tas #
# Tri de tâches par ordre chronologique #
#########################################

class Tache:
	'''Tache devant être effectuée avant une date limite'''
	def __init__(self, jour, nom):
		self.jour = jour
		self.nom = nom
		# Cet attribut servira à accueillir la clé du tas
		self.cle = None
		
	def __str__(self):
		return self.nom + " ({})".format(self.jour)
	
if __name__ == "__main__":
	
	# Le niveau de priorité d'un événement x est -x.jour : on trie donc les événements par ordre chronologique
	def calculePriorite(tache):
		return -tache.jour
	
	# On crée un tas dont les éléments sont des événements triés par ordre chronologique
	T = Tas(calculePriorite)
	
	# Ajoute des événements au tas
	evts = [ Tache(5, "T1"), Tache(10, "T2"), Tache(5, "T3"), Tache(3, "T4")]
	for evt in evts:
		evt.cle = T.ajoute(evt)
		
	# Supposons que la tache 2 devienne soudain assez urgente 
	evts[1].jour = 4
	T.actualise(evts[1].cle)
	
	# Retirons dans l'ordre chronologie les éléments du tas
	while(not T.empty()):
		print(T.pop())
	
	
