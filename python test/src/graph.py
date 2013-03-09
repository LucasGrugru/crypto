#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import *              
from PyQt4.QtCore import *          #permet d'utiliser les objets de base Qt 
from PyQt4.QtGui import *      
from random import *
import Image                        # Construire des Images (Ulam)
import ImageDraw                    
import os                           # Commandes Système
import sys 
import re                           # Expression réguliere


class El_gamal(QWidget):
    def __init__(self, parent=None):         # constructeur de l'objet
        QWidget.__init__(self, parent)



        self.label_text_origine = QLabel("Texte D'origine a crypter")
        self.text_origine = QTextEdit("Text a crypter...")
        self.label_text_ascii = QLabel("Texte ASCII")
        self.text_ascii = QTextEdit("Text en ASCII ... ")
        self.label_text_crypter = QLabel("Texte Crypter avec ElGamal")
        self.text_crypter = QTextEdit("Text crypter ... ")
        self.label_text_decrypter = QLabel("Texte Decrypter")
        self.text_decrypter = QTextEdit("Text decrypte ... ")


        self.label_taille_clef =QLabel("Taille de la cle en bits")
        self.taille_clef = QLineEdit("64")
        self.label_tour = QLabel("Nombre de tours ")
        self.tour = QLineEdit("20")

        self.label_nombre_premier = QLabel("Nombre premier")
        self.nombre_premier = QLineEdit("")
        self.nombre_premier.setReadOnly(True)
        
        self.label_cle_prive = QLabel("Cle Prive")
        self.cle_prive = QLineEdit("")
        self.cle_prive.setReadOnly(True)

        self.label_cle_public = QLabel("Cle Public")
        self.cle_public = QLineEdit("")
        self.cle_public.setReadOnly(True)
        
        self.label_k_alea = QLabel("Nombre k")
        self.k_alea = QLineEdit("")
        self.k_alea.setReadOnly(True)        
        
        self.label_g_alea = QLabel("Nombre g")
        self.g_alea = QLineEdit("")
        self.g_alea.setReadOnly(True)        
        
        self.label_a_decrypt = QLabel("Nombre a ")
        self.a_decrypt = QLineEdit("")
        self.a_decrypt.setReadOnly(True)

        self.generer = QPushButton("Generer les cles")
        self.crypter = QPushButton("Crypter")
        self.decrypter = QPushButton("Decrypter")
              
        layout_principal = QGridLayout()
        layout_bouton = QVBoxLayout()
        layout_cle = QGridLayout()                                              #Done
        layout_texte_claire = QVBoxLayout()
        layout_texte_ascii = QVBoxLayout()
        layout_texte_crypter = QVBoxLayout()
        layout_texte_decrypter = QVBoxLayout()

        layout_bouton.addWidget(self.generer)
        layout_bouton.addWidget(self.crypter)
        layout_bouton.addWidget(self.decrypter)

        layout_cle.addWidget(self.label_taille_clef, 0, 0)
        layout_cle.addWidget(self.taille_clef, 0 ,1 )
        layout_cle.addWidget(self.label_tour, 1, 0)
        layout_cle.addWidget(self.tour, 1, 1)
        layout_cle.addWidget(self.label_nombre_premier, 2, 0)
        layout_cle.addWidget(self.nombre_premier, 2, 1)
        layout_cle.addWidget(self.label_cle_prive, 3, 0)
        layout_cle.addWidget(self.cle_prive, 3, 1)
        layout_cle.addWidget(self.label_cle_public, 4, 0)
        layout_cle.addWidget(self.cle_public, 4 , 1 )
        layout_cle.addWidget(self.label_k_alea, 5, 0)
        layout_cle.addWidget(self.k_alea, 5, 1)
        layout_cle.addWidget(self.label_g_alea, 6, 0)
        layout_cle.addWidget(self.g_alea, 6, 1)
        layout_cle.addWidget(self.label_a_decrypt, 7, 0)
        layout_cle.addWidget(self.a_decrypt, 7, 1)


        
        layout_texte_claire.addWidget(self.label_text_origine)
        layout_texte_claire.addWidget(self.text_origine)

        layout_texte_ascii.addWidget(self.label_text_ascii)
        layout_texte_ascii.addWidget(self.text_ascii)

        layout_texte_crypter.addWidget(self.label_text_crypter)
        layout_texte_crypter.addWidget(self.text_crypter)

        layout_texte_decrypter.addWidget(self.label_text_decrypter)
        layout_texte_decrypter.addWidget(self.text_decrypter)

        layout_principal.addLayout(layout_bouton, 0, 1)
        layout_principal.addLayout(layout_cle, 0, 0)
        layout_principal.addLayout(layout_texte_claire, 1, 0)
        layout_principal.addLayout(layout_texte_ascii, 1, 1)
        layout_principal.addLayout(layout_texte_crypter, 2, 0)
        layout_principal.addLayout(layout_texte_decrypter, 2, 1)
        self.setLayout(layout_principal)


        #Debut des SIGNAL

        self.generer.connect(self.generer, SIGNAL("clicked(bool)"), self.generer_el)
        self.crypter.connect(self.crypter, SIGNAL("clicked(bool)"), self.crypt_el)
        self.decrypter.connect(self.decrypter, SIGNAL("clicked(bool)"), self.decrypt_el)



    #Va etre utile pour trouver le module d'un grande nombre dans les conditions de miller rabin.
    def exponentiationModulaire(self, base, exposant, module):
        resultat = 1
        while exposant > 0:
            if exposant & 1 > 0:
                resultat = (resultat * base) % module
            exposant >>= 1 #permet un decalage des bits (div par 2 )
            base = (base * base) % module
        return resultat

    ## Transforme un nombre décimal en un nombre binaire.
    def decimalToBinaire(self, nombre):
	    i=0
	    power = 0
	    while power < nombre:
		    power = int(self.expo(2,i))
		    i=i+1
	    binaire = ''

	    for j in range(i-2,-1,-1):
		    power = int(self.expo(2,j))
		    if nombre-power >= 0:
			    nombre = nombre - power
			    binaire = binaire + '1'
		    else:
			    binaire = binaire + '0'
	    return binaire

    #Il y a encore de grande possibilité d'amélioration
    def miller(self, n, k):
        d=(n-1)>>1                          #Décalage des bits
        s = 1
        while not d&1 :                     #Pose n comme 2^s * d (ou d impaire et s pair)
            s+=1
            d>>=1

        # n - 1 =  2^" + str(s) + " * " + str(d)
        # Nombre de tests demandé : " + str(k)
        compteur = 0
        for i in range(k):

            #Nombre a et r aleatoire (peuvent etre optimisé ! )
            a = self.genere(len(str(self.decimalToBinaire(n))) - 1)            
            r = randint(0, s-1)
            
            #print "condition"
            if(self.exponentiationModulaire(a, d, n) !=1):
                if(self.exponentiationModulaire(a, self.expo(2,r)*d, n)!=-1): #Possibilité d'opti ici aussi
                    compteur+= 1
                else :
                    return 0
            else:
                return 0

        if(compteur == k): #Verifie si tout les tour on trouvé qu'il etait premier ou non 
            return 1
        else:
            return 0


    ##
    def expo(self, x,n):
        resultat = 1
        while (n != 0):
            if ((n % 2) == 1):
                resultat = resultat * x
                n=n-1
            x = x*x
            n = n/2
        return resultat



    ## Genère un nombre aléatoire en fonction du nombre de bits demandé
    ## Pas de limites
    def genere(self, puissance): #Cle de 1024 bits
        i = 0 
        nombre = 0
        while(i < puissance):
            bit =  int(random()*2)
            if(bit == 1):
                nombre += self.expo(2, puissance)
            i += 1
            puissance -= 1 


        nombre += self.expo(2, puissance) 
        nombre += 1

        return nombre


    ## Calcule le PGCD de 2 nombres (a refaire, trop long)
    def PGCD(self, a, b):        
        trouver = False
        pgcd = 1
        inter_a = a 
        inter_b = b
        if(a == 0 or b==0):
            return 0
        else:
            while(trouver == False):
                if(a >= b):     
                    inter_a = a%b
                    if(inter_a==0):
                        pgcd = b
                        trouver = True
                    else:
                        a = inter_a
                elif(a < b):                                
                    inter_b=b%a
                    if(inter_b == 0):
                        pgcd = a
                        trouver = True
                    else :
                        b = inter_b
                    
            return pgcd                      



    def generer_el(self):

        tour = int(self.tour.text())
        p = self.genere(int(self.taille_clef.text()))

        var = self.miller(p, tour)
        while (var != 0):    
            p-= 2 
            var = self.miller(p, tour) 
        
        p += 1                
        g = randint(1, p-1)
        x = randint(1, p-1) #Clé privé
        cle_pub = self.exponentiationModulaire(g, x, p)


        

        # k doit etre premier avec nb -1 
        trouver = False
        while(trouver == False):
            k = self.genere(64)
            zed = self.PGCD(k, p-1)
            if(zed == 1):
                trouver = True

        a = self.exponentiationModulaire(g, k, p)
        self.nombre_premier.setText(str(p))
        self.cle_prive.setText(str(x))
        self.cle_public.setText(str(cle_pub))
        self.k_alea.setText(str(k))
        self.g_alea.setText(str(g))
        self.a_decrypt.setText(str(a))
    
    
        ## Transforme un message en un bloc ASCII en rajoutant des 0 pour les nombre inférieur a 3 chiffres
    def convert(self, chaine):
        result = ""
        inter = ""
        inter.encode('utf8') 
        for i in chaine :
            #i.encode('utf8')

            i = ord(i)
            inter = str(i)
            inter = inter.zfill(5)
            result += inter
        return result
        
    '''
    def debloque(self, message, bloc):
        for j in range(0, len(new_message), 3) :    
            two = new_message[j+1]
            three = new_message[j+2]
            letter = str(new_message[j]) + str(two) + str(three)
            message_decrypt += chr(int(letter))
        return message_decrypt
    '''
    
    
    def completion(self, message_ascii, longueur_p):
        longueur_restant = longueur_p - (len(str(message_ascii))%longueur_p)                
        message_ascii = message_ascii.zfill(len(str(message_ascii))+longueur_restant)
        return message_ascii
    
    
    def decompletion(self, message_ascii):
        mess = ""
        if(len(str(message_ascii))%5 != 0):
            for i in range(len(str(message_ascii))%5 , len(message_ascii), 1):
                mess += message_ascii[i] 
        else :
            return message_ascii 
        return mess
    
    def cryptogramme_maximum(self, p_bis, cle_pub, k, p):
        cryptogramme = ""
        for i in range(p_bis) :
            cryptogramme += '65355'
        return len(str(int(cryptogramme) * self.exponentiationModulaire(cle_pub, k, p)))
    
    
    
    
    
    
        
    
    def crypt_el(self):
        k = int(self.k_alea.text())
        cle_pub = int(self.cle_public.text())
        p = int(self.nombre_premier.text())
        test = QString(self.text_origine.toPlainText())

        print "Test : " , dir(test)
        #message = str(self.text_origine.toPlainText())
        message = test.toUtf8()
        print type(message)
        print message
        message_ascii = self.convert(message)
        print "Message ASCII avant completion : " , message_ascii
        print "Longueur du message ACSII : " , len(message_ascii)

        message_ascii = self.completion(message_ascii, len(str(p)))
        print "Message ASCII après completion : " , message_ascii
        print "Longueur de message ACSII : " , len(message_ascii)

        maxi = self.cryptogramme_maximum(len(str(p)), cle_pub, k, p)        
        print "Maximum d'un cryptogramme : " , maxi
        print "Longueur de p : " , len(str(p))
        print '\n'
        message_crypter = ""       
        cryptogramme = ""       
        for i in range(0, len(str(message_ascii)), len(str(p))):
            for j in range(i, i+len(str(p)), 1):
                cryptogramme += message_ascii[j]
            print "Partie du Message a coder : " , cryptogramme
            print "Longueur du message a coder : " , len(cryptogramme)    
            part_crypter = str(int(cryptogramme) * self.exponentiationModulaire(cle_pub, k, p))     
            print "Message coder avant completion : " , part_crypter
            print "Longueur du message coder : " , len(part_crypter)            
            if(len(part_crypter) < maxi):
                part_crypter = part_crypter.zfill(maxi)
            print "Message coder après completion : " , part_crypter   
            print "Longueur de mess coder après completion : " , len(part_crypter)
            message_crypter += part_crypter
            part_crypter = ""
            cryptogramme = ""                 
        
        
        
        self.text_ascii.setText(str(message_ascii))   
        self.text_crypter.setText(str(message_crypter))            
        '''
        ##CRYPTAGE
        ready = False          #Permet au demarrage de compter une fois la taille d'un paquet qui a été crypter
        #Il y a un problème car la longueur du paquet crypter est variable a quelque chiffre près (1 ou 2 )

        # Cette boucle crypte par paquet, et tout les paquets entiers
        # On a choisi plus haut de faire par paquet de 10 lettres, soit 30 chiffres par paquet. (codé en ASCII soit maxi 3 chiffres par lettre)
        for i in range(0, len(str(message_asci))-paquet, paquet):           # On parcours le message transformé en ASCII
            for j in range(i, i+paquet):                                    # On en fait un paquet, tant que le paquet est égal a 30 
                part += message_asci[j]

            cyp = str(int(part) * self.exponentiationModulaire(cle_pub, k, p))            
            
            if(ready == False):                                                                     # Mesure la taille d'un paquet crypté
                global taille  
                taille = len(cyp)
                ready = True
            
            if(len(cyp) != taille+2):
                ecart = (taille+2) - len(cyp)
                while(ecart != 0):
                    cyp = "0" + cyp
                    ecart -= 1 
            print "Message en ACSII   : " , part 
            print "Message en crypter : " , cyp   # On l'affiche
            message_crypter += cyp                                                                    # On crypte le paquet
            part = "" 

        #Compte combien de lettre on été oublié. (en effet on ne peut pas faire des paquet toujours plein : exemple il reste 3 lettres)
        lenght = len(message_asci)%paquet

        part = ""
        for i in range(len(message_asci) - lenght, len(message_asci), 1):   #On récupere tout ce qui n'a pas été mis en paquet
            part += message_asci[i]
        cyp = str(int(part) * self.exponentiationModulaire(cle_pub, k, p))              #Et on le crypte           

        if(len(cyp) != taille+2):
            ecart = (taille+2) - len(cyp)
            while(ecart != 0):
                cyp += "0"
                ecart -= 1 
        message_crypter += cyp   
        '''
        


    

    def decrypt_el(self):
        message_crypter = str(self.text_crypter.toPlainText())
        a = int(self.a_decrypt.text())
        x = int(self.cle_prive.text())
        p = int(self.nombre_premier.text())
        k = int(self.k_alea.text())
        cle_pub = int(self.cle_public.text())
        maxi = self.cryptogramme_maximum(len(str(p)), cle_pub, k, p)
        print "\nDecryptage " 
        print "Maximum " , maxi 
        message_decrypter = ""
        cryptogramme = "" 
        print '\n'
        middle = ""
        for i in range(0, len(message_crypter), maxi):
            for j in range(i, i+maxi): 
                cryptogramme += message_crypter[j]  
            print "Cryptogramme choisi :" , cryptogramme                               
            print "Longueur du Cryptogramme : ", len(cryptogramme)
            middle = str(int(cryptogramme)/self.exponentiationModulaire(a,x,p))
            print "Cryptogramme traduit : ", middle
            #if(len(middle) < (len(str(p))*5)):
            #    middle = middle.zfill(len(str(p))*5)
            if(len(middle) < len(str(p))):
                middle = middle.zfill(len(str(p)))
            print "Traduction competer par des 0 : " , middle 
            print "Longueur du message ASCII traduit : " , len(middle)
            message_decrypter += middle 
            middle = "" 
            cryptogramme = ""
        
        
        
        
        print '\n'
        print message_decrypter
        mess = self.decompletion(message_decrypter)
        print "Message decompleter : " , mess        
        message_decrypter = mess
        self.text_decrypter.setText(mess)        
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
        #self.text_decrypter.setText(final)                  
        print traduc
        '''    
        print message_decrypter    
        print "Longueur : " , len(message_decrypter)     
        if(len(message_decrypter) % 5 != 0):
            message_decrypter = message_decrypter.zfill((5-len(message_decrypter)%5)+len(message_decrypter))
    
        print '\n'
        print message_decrypter
        print "longueur : " , len(message_decrypter)
        '''
        
        
        '''
        global taille 
        message_decrypter = ""
        taille_convert = 0
        message_crypter = str(self.text_crypter.toPlainText())
        a = int(self.a_decrypt.text())
        x = int(self.cle_prive.text())
        p = int(self.nombre_premier.text())
        paquet = 3 *30 
        ## on reparcours les blocs de taille "taille" calculer précédement lors du cryptage (problème d'ailleur ... )
        part = ""
        print "La taille est de" , taille
        for i in range(0, len(message_crypter)-taille+2, taille+2) : #On reparcours 
            for j in range(i, i+taille+2):
                part += message_crypter[j]
            
            print "Partie décoder : " +str(part)
            
            mess = str(int(part)/self.exponentiationModulaire(a,x,p))
            if(len(mess) != paquet):
                manque = paquet - len(mess)
                for i in range(manque):
                    mess = "0" + mess 
            print mess        
            message_decrypter += mess
            part = "" 

        part = ""

        #Puis on la décrypte
        for i in range(len(message_crypter)-(len(message_crypter)%taille), len(message_crypter), 1):            
            part += str(message_crypter[i])        

        mess = str(int(part)/self.exponentiationModulaire(a,x,p))

        #On rajoute des '0' au besoin 
        if((len(mess)%taille)%3 == 2):
            mess = "0" + mess
        if((len(mess)%taille)%3 == 1):
            mess = "00" + mess

        #et on ajoute ce dernier bloc decrypter au message total 
        message_decrypter += mess     


        final = "" 
        #Puis on effectue un decryptage du code ASCI par pas de 3 
        for i in range(0, len(str(message_decrypter)), 3) :
            lettre = str(message_decrypter[i]) + str(message_decrypter[i+1])+ str(message_decrypter[i+2])
            if(int(lettre) != 0):
                final += str(chr(int(lettre)))
        '''
        print "final : " , final        
        print type(traduc)
        st = QString(traduc)
        #st.toAscii()
        #print st 
        #print dir(st)
        #traduc = traduc.decode('utf8')

        self.text_decrypter.setText(st)


        


        
if __name__ == "__main__":                            # Main
    app = QApplication(sys.argv)       
    Mafenetre = El_gamal()
    Mafenetre. setBaseSize(600, 400)                  #Taille de la fenetre
    Mafenetre.show()            
    Mafenetre.setWindowTitle("ElGamal")               #Titre a changer S.V.P
    app.exec_()





