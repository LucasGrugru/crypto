#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import *              
from random import *


#Va etre utile pour trouver le module d'un grande nombre dans les conditions de miller rabin.
def exponentiationModulaire(base, exposant, module):
    resultat = 1
    while exposant > 0:
        if exposant & 1 > 0:
            resultat = (resultat * base) % module
        exposant >>= 1 #permet un decalage des bits (div par 2 )
        base = (base * base) % module
    return resultat


## Transforme un nombre décimal en un nombre binaire.
def decimalToBinaire(nombre):
    i=0
    power = 0
    while power < nombre:
	    power = int(expo(2,i))
	    i=i+1
    binaire = ''
    for j in range(i-2,-1,-1):
	    power = int(expo(2,j))
	    if nombre-power >= 0:
		    nombre = nombre - power
		    binaire = binaire + '1'
	    else:
		    binaire = binaire + '0'
    return binaire

#Exponentiation rapide normale
def expo(x,n):
    resultat = 1
    while (n != 0):
        if ((n % 2) == 1):
            resultat = resultat * x
            n=n-1
        x = x*x
        n = n/2
    return resultat



#
# Fonction PGCD surement a refaire (utilisé l'algo d'euclide)
#
def PGCD(a, b):        
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

## Genère un nombre aléatoire en fonction du nombre de bits demandé
## Pas de limites
def genere(puissance): #Cle de 1024 bits
    i = 0 
    nombre = 0
    while(i < puissance):
        bit =  int(random()*2)
        if(bit == 1):
            nombre += expo(2, puissance)
        i += 1
        puissance -= 1 


    nombre += expo(2, puissance) 
    nombre += 1

    return nombre


## Transforme un message en un bloc ASCII en rajoutant des 0 pour les nombre inférieur a 3 chiffres
def convert(chaine):
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



#Il y a encore de grande possibilité d'amélioration
def miller(n, k):
    if(n == 1):
        return 0

    d=(n-1)>>1                          #Décalage des bits
    s = 1
    while not d&1 :                     #Pose n comme 2^s * d (ou d impaire et s pair)
        s+=1
        d>>=1

    #print " n - 1 =  2^" + str(s) + " * " + str(d)

    
    for i in range(k):  
        a = randint(1, n-1) 
        y = exponentiationModulaire(a, d, n)
        
        if((y !=1) and(y != n-1)): #Possibilité d'opti ici aussi
            j = 0 
            while(j< s and y != n-1):
                y = exponentiationModulaire(y, 2, n)                 
                if(y == 1):
                    return 0 # non premier
                j+= 1
                if(y != n-1):
                    return 0 # non premier
    return 1 #surement premier  

#ajoute des 0 à la fin du message ascii qui n'est pas completé
def completion(message_ascii, longueur_p):
    longueur_restant = longueur_p - (len(str(message_ascii))%longueur_p)                
    message_ascii = message_ascii.zfill(len(str(message_ascii))+longueur_restant)
    return message_ascii


#Enleve les 0 ajouter a la fin d'un message acsii qui a du être completé
def decompletion(message_ascii):
    mess = ""
    if(len(str(message_ascii))%5 != 0):
        for i in range(len(str(message_ascii))%5 , len(message_ascii), 1):
            mess += message_ascii[i] 
    else :
        return message_ascii 
    return mess


#calcule la taille maximum d'un cryptogramme en fonction du nombre premier p
#Les messages etant codé en UTF-8 (soit 16 bits = 65535 au maximum) on calcule le crypgramme max pour faire la différences avec les autres et rajouter au besoin des "0"
def cryptogramme_maximum(p_bis, cle_pub, k, p):
    cryptogramme = ""
    for i in range(p_bis) :
        cryptogramme += '65355'
    return len(str(int(cryptogramme) *exponentiationModulaire(cle_pub, k, p)))



def facto_iteratif(n):
    if(n == 0):
        return 1
    else :
        i = 1
        total = 1
        while(i < n +1):
            total = total * (i + 1)
            i+=1
        return total

