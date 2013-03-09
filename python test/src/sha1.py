# -*- coding: utf-8 -*-
from collections import deque
import string
from fct import *

class sha1():
	def __init__(self, parent=None):
		self.h0=0x67452301
		self.h1=0xEFCDAB89
		self.h2=0x98BADCFE
		self.h3=0x10325476
		self.h4=0xC3D2E1F0

		self.k1 = 0x5A827999 #pour 0≤t≤19
		self.k2 = 0x6ED9EBA1 #pour 20≤t≤39
		self.k3 = 0x8F1BBCDC #pour 40≤t≤59
		self.k4 = 0xCA62C1D6 #pour 60≤t≤79 


	#fonction qui convertis vers le binaire
	def bin2(self, n): 
	    res = []
	    while n > 0:
		res.insert(0, str(int(n % 2)))
		n = n // 2
	    return "".join(res)


	def leftrotate(self, nb, string):
		print "orig" + string + ", value" + str(nb)
		tmp = string[:nb]
		string = string[nb:]
		string = string + tmp
		print string
		return string

	def sha1(self, value):
                toInt = ""
                value = str(value)#.toStdString()
                for x in range(len(value)):
                    print "in"
                    toInt += str(ord(value[x]))
                value = decimalToBinaire(int(toInt))
		#value valeur en binaire
		print value
		longueurorig = len(value)
		print "La longueur est : " + str(longueurorig)
		value = value + "1"
		print value
		longueur = len(value)
		print "La longueur est : " + str(longueur)
		print "Nombre de 0 a ajouter : " + str(512-64-longueur%512)
		for k in range(512-64-longueur%512) :
			value = value + "0"
		print value

		#conversion de la valeur original en nombre de 64 bits
		longueurorigbin = self.bin2(longueurorig)
		print longueurorigbin
		longueurorigbin = str(longueurorigbin)
		print longueurorigbin
		for k in range(64-len(longueurorigbin)):
			value = "0" + value
		print longueurorigbin

		#concatenation des deux valeurs
		value = value + longueurorigbin
		print value
		# a ce stade, value contient la valeur a acher !
		print "Le reste de la divison du nombre de caracteres par 512 est (doit etre egal a 0) : " + str(len(value)%512)
		for k in range(len(value)/512):
			#recuperation de block de 512 octets
			block = value[k*512:(k+1)*512]
	
			#decoupage en 16 mots de 32 bits, on les place dans un tableau table
			table = []
			for k in range(16):
				table.append(block[k*32:(k+1)*32])
			tableint = []
			for k in range(16):
                                print table[k]
                                print type(table[k])
				tableint.append(int(table[k],2))
			print table
			print tableint
	
			#génération de 80 mots de 32 bits à patir de nos 16 mots de 32 bits	
			for k in range(16, 80):
				temp = self.bin2(tableint[k-3] ^ tableint[k-8] ^ tableint[k-14] ^ tableint[k-16])
				temp = self.leftrotate(1, temp)
				temp2 = int(temp, 2)
				tableint.append(temp2)
			print block
			print tableint
	
			#initialisation des valeurs
			a = self.h0
			b = self.h1
			c = self.h2
			d = self.h3
			e = self.h4
		    
			for i in range(80):
			    if 0 <= i <= 19:
				    f = (b & c) | ((not b) & d)
				    k = self.k1
			    if 20 <= i <= 39:
				    f = b ^ c ^ d
				    k = self.k2
			    if 40 <= i <= 59:
				    f = (b & c) | (b & d) | (c & d)
				    k = self.k3
                if 60 <= i <= 79:
                    f = b ^ c ^ d
                    k = self.k4
                    atmp = self.bin2(a)
                    atmp = self.leftrotate(5, atmp)
                    a = int(atmp, 2)

                temp = a + f + e + k + tableint[i]
                e = d
                d = c
                ctmp = self.leftrotate(30, self.bin2(b))
                c = int(ctmp, 2)
                b = a
                a = temp

                self.h0 = self.h0 + a
                self.h1 = self.h1 + b 
                self.h2 = self.h2 + c
                self.h3 = self.h3 + d
                self.h4 = self.h4 + e


		digest = self.bin2(self.h0) + self.bin2(self.h1) + self.bin2(self.h2) + self.bin2(self.h3) + self.bin2(self.h4)
		return hex(int(digest,2))

