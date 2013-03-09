from math import *

class Eratosthene():
    def __init__(self, parent=None):
        self.n = 0
        self.liste = []
    
    def Generer(self):
        self.liste = [i for i in range(2,self.n)] 
        for k in range(2, int(sqrt(self.n))):
            self.liste = [x for x in self.liste if x%k!=0 or x == k]	
	
    def setListe(self, liste):
        self.liste = liste 

    def getListe(self):
        return str(self.liste) 

    def setNombre(self, n):
        self.n = n 

    def getNombre(self):
        return self.n

