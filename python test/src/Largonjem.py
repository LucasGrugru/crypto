#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Largonjem():
    def __init__(self, parent=None):
        self.voyelle = ['a', 'e', 'i', 'o', 'u', 'y']
        self.text = "" 
        self.text_crypter = ""    
    
    
    def crypter(self):
        self.text_crypter = ""
        self.text += ' '
        
        mot = []
        phrase = []

        longueur = len(self.text)
        j = 0
        fin_mot = False
        consonne = 1
        
        while(j < longueur):                            #On parcours toute la phrase
            if(self.text[j] == ' '):                    #On coupe la phrase en mot des que l'on rencontre un espace
                fin_mot = True
                print "Mot " , mot
            elif (self.text[j] == ' ' and len(mot) == 0) :
                fin_mot = False
                
            else :
                print self.text[j]
                mot.append(self.text[j])                #Ajout des lettres    
            if(fin_mot == True ):                       #Une fois un mot trouvé
                i = 0
                while(i < len(self.voyelle)) :          #On regarde si la premiere lettre est une consonne   
                    if(mot[0] == self.voyelle[i]):
                        consonne = 0 
                    i += 1
                i = 0 
                
                if(consonne == 0):                      #si consonne alors on ne modifie pas le mot
                    phrase+=mot                         #On l'ajoute
                else :
                    char = mot[0] 
                    mot.append(char)
                    mot.append('e')
                    mot.append('m')                                                            
                    del mot[0]
                    mot.insert(0, 'l')
                    mot.append(' ')                                        
                    phrase += mot
                fin_mot = False
                consonne = 1
                mot = []
            j+= 1
          
        #On remet l'integrale de la phrase crypté    
        i = 0    
        while(i < len(phrase)):
            self.text_crypter += phrase[i]
            i += 1                
                                    

    
            
    def getText(self):
        return self.text
        
    def getTextCrypter(self):
        return self.text_crypter
        
    def setText(self, text):
        self.text = text
        
    def setTextCrypter(self, text_crypter):
        self.text_crypter = text_crypter

        

        



