#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import *              
      
from random import *
import Image                        # Construire des Images (Ulam)
import ImageDraw                    
import os                           # Commandes Système
import sys 
import re                           # Expression réguliere
from fct import * 


class Elgamal():
    def __init__(self, parent=None):         # constructeur de l'objet	

        self.text_origine = None
        self.tour = 20
        self.text_ascii = ""
        self.text_crypter = ""
        self.text_decrypter = ""
        self.taille_clef = None
        self.p = 0 
        self.cle_prive = 0
        self.cle_public = 0
        self.k = 0
        self.g = 0
        self.a = 0

    def getK(self):
        return self.k

    def setK(self, k):
        self.k = k

    def setG(self, g):
        self.g = g

    def getG(self):
        return self.g

    def getA(self):
        return self.a

    def setA(self, a):
        self.a = a

    def setPremier(self, p):
        self.p = p

    def getPremier(self):
        return self.p

    def getClePrive(self):
        return self.cle_prive 

    def getClePublic(self):
        return self.cle_public

    def setClePrive(self, cle_prive):
        self.cle_prive = cle_prive

    def setClePublic(self, cle_public):
        self.cle_public = cle_public

    def setTailleCle(self, taille_cle):
        self.taille_cle = int(taille_cle)
        print "taille clé change ! "
        print self.taille_cle

    def getTailleCle(self):
        return self.taille_cle

    def setTextDecrypter(self, text_decrypter):
        self.text_decrypter = text_decrypter

    def setTextAcsii(self, text_ascii):
        self.text_ascii = text_ascii

    def getTextAscii(self):
        return self.text_ascii 

    def getTextCrypter(self):
        return self.text_crypter

    def setTextCrypter(self, text_crypter):
        self.text_crypter = text_crypter

    def setTextOrigine(self, text_origine):
        self.text_origine =  text_origine

    def getTextOrigine(self):
        return self.text_origine 

    def getTour(self):
        return self.tour 

    def setTour(self, tour):
        self.tour = tour 
    

    def generer(self):
        self.taille_clef = self.getTailleCle()
        self.tour = self.getTour()        
        self.p = genere(self.taille_clef)
        var = miller(self.p, self.tour) #On genere la cle public :
        while (var != 1):    
            self.p-= 2 
            var = miller(self.p, self.tour) 
        
        #self.p += 1                
        self.g = randint(1, self.p-1)
        self.cle_prive = randint(1, self.p-1) #Clé privé
        self.cle_public = exponentiationModulaire(self.g, self.cle_prive, self.p)

        # k doit etre premier avec nb -1 
        trouver = False
        while(trouver == False):
            self.k = genere(64)
            zed = PGCD(self.k, self.p-1)
            if(zed == 1):
                trouver = True

        self.a = exponentiationModulaire(self.g, self.k, self.p)
        print "Finish"            
    
        
    
    def crypter(self):
        print dir(self.text_origine)
        
        message = self.text_origine.encode("utf-8")
        print message
        message_ascii = convert(message)
        print "Message ASCII avant completion : " , message_ascii
        print "Longueur du message ACSII : " , len(message_ascii)

        message_ascii = completion(message_ascii, len(str(self.p)))
        print "Message ASCII après completion : " , message_ascii
        print "Longueur de message ACSII : " , len(message_ascii)

        maxi = cryptogramme_maximum(len(str(self.p)), self.cle_public, self.k, self.p)        
        print "Maximum d'un cryptogramme : " , maxi
        print "Longueur de p : " , len(str(self.p))
        print '\n'
        message_crypter = ""       
        cryptogramme = ""       
        for i in range(0, len(str(message_ascii)), len(str(self.p))):
            for j in range(i, i+len(str(self.p)), 1):
                cryptogramme += message_ascii[j]
            print "Partie du Message a coder : " , cryptogramme
            print "Longueur du message a coder : " , len(cryptogramme)    
            part_crypter = str(int(cryptogramme) * exponentiationModulaire(self.cle_public, self.k, self.p))     
            print "Message coder avant completion : " , part_crypter
            print "Longueur du message coder : " , len(part_crypter)            
            if(len(part_crypter) < maxi):
                part_crypter = part_crypter.zfill(maxi)
            print "Message coder après completion : " , part_crypter   
            print "Longueur de mess coder après completion : " , len(part_crypter)
            message_crypter += part_crypter
            part_crypter = ""
            cryptogramme = ""                 
                
        self.text_ascii = message_ascii
        self.text_crypter = message_crypter            
        


    

    def decrypter(self):
        maxi = cryptogramme_maximum(len(str(self.p)), self.cle_public, self.k, self.p)
        print "\nDecryptage " 
        print "Maximum " , maxi 
        message_decrypter = ""
        cryptogramme = "" 
        print '\n'
        middle = ""
        for i in range(0, len(self.text_crypter), maxi):
            for j in range(i, i+maxi): 
                cryptogramme += self.text_crypter[j]  
            print "Cryptogramme choisi :" , cryptogramme                               
            print "Longueur du Cryptogramme : ", len(cryptogramme)
            middle = str(int(cryptogramme)/exponentiationModulaire(self.a,self.cle_prive,self.p))
            print "Cryptogramme traduit : ", middle
            
            if(len(middle) < len(str(self.p))):
                middle = middle.zfill(len(str(self.p)))
            print "Traduction completer par des 0 : " , middle 
            print "Longueur du message ASCII traduit : " , len(middle)
            message_decrypter += middle 
            middle = "" 
            cryptogramme = ""
        
        print '\n'
        print message_decrypter
        mess = decompletion(message_decrypter)
        print "Message decompleter : " , mess        
        message_decrypter = mess        
        final = ""
        lettre = ""
        traduc = ""
        for i in range(0, len(message_decrypter), 5):
            for j in range(i, i+5):
                lettre += message_decrypter[j]
            print "lettre : " , lettre
            if(int(lettre) != 0):
                traduc += unichr(int(lettre))
                final += lettre
            lettre = ""                  
        print traduc
        print "final : " , final        
        print type(traduc)
        #st = QString(traduc)
        self.text_decrypter = traduc
        #st.toAscii()
        #print st 
        #print dir(st)
        #traduc = traduc.decode('utf8')
        #self.text_decrypter.setText(st)







