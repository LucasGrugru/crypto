#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Cesar():
    def __init__(self, parent=None):
        self.text = ""
        self.cle = 0
        self.decalage = 0 
        self.text_code = ""
        
        
    def CrypterDecalage(self):
        self.text_code = ""                                      
        for i in range(len(self.text)):
            if(ord(self.text[i]) != 32):
                char = ord(self.text[i]) + self.decalage
                if(char > 122):
                    base = 97
                    retenu = 122-ord(self.text[i])
                    dec = self.decalage - retenu 
                    self.text_code += str(chr(base+dec))
                else:
                    self.text_code += str(chr(char))
            else:
                self.text_code+= str(self.text[i])    
          
    def DecrypterDecalage(self):
        self.text = ""
        for i in range(len(self.text_code)):
            if(self.text_code[i] != ' '):                                
                ascii = ord(self.text_code[i]) - self.decalage
                if(ascii < 97):
                    reste = 97-ascii
                    base = 122 - reste 
                    self.text += chr(base)                    
                else :
                    self.text += chr(ascii)
            else :
                self.text += chr(ascii)

    
    def CrypterCle(self):
        self.text_code = "" 
        self.text = self.text.lower()        
        self.cle = str(self.cle)
        k = 0
        ln = len(self.cle)
        for i in range(len(self.text)):
            if(self.text[i] != ' '):
                ascii = ord(self.text[i]) + int(self.cle[k])
                k+=1
                if(k == ln):
                    k = 0
                if(ascii > 122):
                    base = 97 
                    retenu = ascii - 122 
                    ascii = chr(retenu+base)
                    self.text_code += str(ascii)
                else :
                    self.text_code += str(chr(ascii))
            else :            
                self.text_code += str(self.text[i])
     
    
    def DecrypterCle(self):
        self.text = ""
        self.text_code = self.text_code.lower()
        self.cle =  str(self.cle)
        k = 0 
        ln = len(str(self.cle))
        for i in range(len(self.text_code)):
            if(self.text_code[i] != ' ' ):
                ascii = ord(self.text_code[i]) - int(self.cle[k])
                k+= 1
                if(k == ln):
                    k = 0 
                if(ascii < 97):
                    base = 122
                    retenu =  97 - ascii
                    ascii = chr(base - retenu)
                    self.text += str(ascii)
                else :
                    self.text += str(chr(ascii))
            else :
                self.text += str(self.text_code[i])     
                
    def getText(self):
        return self.text
        
    def setText(self, text):
        self.text = text 
        
    def getCle(self):
        return cle                
        
    def setCle(self, cle):
        self.cle = cle 
    
    def getTextCrypter(self):
        return self.text_code 
        
    def setTextCrypter(self, text_code):
        self.text_code = text_code
    
    def setDecalage(self, decalage):
        self.decalage = decalage
        
    def getDecalage(self):
        return self.decalage

        
    def setTextDecrypter(self, text_decrypter):
        self.text_decrypter = text_decrypter
        
        
