#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from math import *              
from PyQt4.QtCore import *          #permet d'utiliser les objets de base Qt 
from PyQt4.QtGui import *                      
import os                           # Commandes Système
import sys 
import re                           # Expression réguliere
from graph import *
from Elgamal import *
from fct import *
from Largonjem import *
from Cesar import *
from Eratosthene import *
from sha1 import *
from RSA import *

class Rassemblement(QWidget):
    def __init__(self, parent=None):         # constructeur de l'objet
        QWidget.__init__(self, parent)
        self.onglet = QTabWidget()                                              #Consctructeur des onglets

        self.largonjem = QWidget()                                              #QWidget largonjem          //OPE
        self.cesar = QWidget()                                                  #QWidget Cesar              //OPE
        self.elgamal = QWidget()                                                #QWidget elgamal            //OPE
        self.eratos = QWidget()                                                 #QWidget eratos             //OPE
        self.divers = QWidget()                                                 #QWidget Chinois && Wilson  //OPE
        self.sha = QWidget()                                                    #QWidget sha                //OPE
        self.rsa = QWidget()                                                    #QWidget rsa                //OPE

        #rsa

        self.label_rsa_cle_public = QLabel(self.trUtf8("Clé public"))
        self.label_rsa_cle_prive = QLabel(self.trUtf8("Clé privée"))
        self.label_rsa_module = QLabel(self.trUtf8("Module"))

        self.edit_rsa_public = QLineEdit()
        self.edit_rsa_privee = QLineEdit()
        self.edit_rsa_module = QLineEdit()

        self.label_text_edit_rsa_decrypt = QLabel(self.trUtf8("Texte à crypter : "))
        self.label_text_edit_rsa_crypt = QLabel(self.trUtf8("Texte à décrypter : "))

        self.text_edit_rsa_decrypt = QTextEdit("abc")
        self.text_edit_rsa_crypt = QTextEdit()

        self.button_rsa_crypter = QPushButton("Crypter")
        self.button_rsa_decrypter = QPushButton("Decrypter")
        self.button_rsa_generer = QPushButton(self.trUtf8("Génerer"))

        layout_rsa_main = QGridLayout()

        layout_rsa_main.addWidget(self.label_rsa_cle_public, 0,0)
        layout_rsa_main.addWidget(self.label_rsa_cle_prive, 1,0)
        layout_rsa_main.addWidget(self.label_rsa_module, 2,0)

        layout_rsa_main.addWidget(self.edit_rsa_public, 0,1)
        layout_rsa_main.addWidget(self.edit_rsa_privee, 1, 1)
        layout_rsa_main.addWidget(self.edit_rsa_module, 2,1)
    
        layout_rsa_main.addWidget(self.label_text_edit_rsa_decrypt, 4,0)
        layout_rsa_main.addWidget(self.label_text_edit_rsa_crypt, 4,1)

        layout_rsa_main.addWidget(self.text_edit_rsa_decrypt, 5,0)
        layout_rsa_main.addWidget(self.text_edit_rsa_crypt, 5,1)

        layout_rsa_main.addWidget(self.button_rsa_crypter, 6,0)
        layout_rsa_main.addWidget(self.button_rsa_decrypter, 6,1)
        layout_rsa_main.addWidget(self.button_rsa_generer, 3,1)

        self.rsa.setLayout(layout_rsa_main)

        self.button_rsa_generer.connect(self.button_rsa_generer, SIGNAL("clicked(bool)"), self.rsa_generer)
        self.button_rsa_generer.connect(self.button_rsa_crypter, SIGNAL("clicked(bool)"), self.rsa_crypt)
        self.button_rsa_generer.connect(self.button_rsa_decrypter, SIGNAL("clicked(bool)"), self.rsa_decrypt)


        #Largonjem
        
        self.label_largonjem_normal = QLabel("Texte à crypter".decode("utf-8"))
        self.label_largonjem_crypter = QLabel("Texte crypté".decode("utf-8"))
        self.text_edit_largonjem_normal = QTextEdit("abc")
        self.text_edit_largonjem_crypter = QTextEdit()
        self.button_largonjem_crypt = QPushButton("Crypter")
        layout_largonjem_principal = QGridLayout()

        layout_largonjem_principal.addWidget(self.label_largonjem_normal, 0, 0)
        layout_largonjem_principal.addWidget(self.text_edit_largonjem_normal, 1, 0)
        
        layout_largonjem_principal.addWidget(self.label_largonjem_crypter, 0, 1)
        layout_largonjem_principal.addWidget(self.text_edit_largonjem_crypter, 1 , 1)
        layout_largonjem_principal.addWidget(self.button_largonjem_crypt)

        self.largonjem.setLayout(layout_largonjem_principal)
        self.button_largonjem_crypt.connect(self.button_largonjem_crypt, SIGNAL("clicked(bool)"), self.LargonjemCrypt)
        
        self.largonjem_instance = Largonjem()

        #Cesar
        self.cesar_instance = Cesar()
        
        self.label_cesar_decalage = QLabel("Decalage")
        self.label_cesar_cle = QLabel("Clé".decode("utf-8"))
        self.label_cesar_crypt = QLabel("Texte a crypter")
        self.label_cesar_decrypt = QLabel("Texte crypté".decode("utf-8"))

        self.text_edit_cesar_crypt = QTextEdit("abc")
        self.text_edit_cesar_decrypt = QTextEdit()
        
        self.line_edit_cesar_decalage = QLineEdit("9")
        self.line_edit_cesar_cle = QLineEdit("0")
        self.button_cesar_crypt = QPushButton("Crypter par décalage".decode("utf-8"))
        self.button_cesar_crypt_bis = QPushButton("Crypter par clé".decode("utf-8"))
        self.button_cesar_decrypt = QPushButton("Décrypter par décalage".decode("utf-8"))
        self.button_cesar_decrypt_bis = QPushButton("Décrypter par clé".decode("utf-8"))       
        
        layout_cesar_principal = QGridLayout()
        layout_cesar_principal.addWidget(self.label_cesar_decalage, 0, 0)
        layout_cesar_principal.addWidget(self.line_edit_cesar_decalage, 0, 1)
        layout_cesar_principal.addWidget(self.label_cesar_cle,1 , 0)
        layout_cesar_principal.addWidget(self.line_edit_cesar_cle, 1, 1)
        layout_cesar_principal.addWidget(self.label_cesar_crypt, 2, 0)
        layout_cesar_principal.addWidget(self.text_edit_cesar_crypt, 3, 0)
        layout_cesar_principal.addWidget(self.label_cesar_decrypt, 2, 1)
        layout_cesar_principal.addWidget(self.text_edit_cesar_decrypt, 3, 1)
        layout_cesar_principal.addWidget(self.button_cesar_crypt, 4, 0)
        layout_cesar_principal.addWidget(self.button_cesar_crypt_bis , 4 , 1)
        layout_cesar_principal.addWidget(self.button_cesar_decrypt, 5, 0)
        layout_cesar_principal.addWidget(self.button_cesar_decrypt_bis , 5 ,1)        
                
        self.cesar.setLayout(layout_cesar_principal)

        
        self.button_cesar_crypt.connect(self.button_cesar_crypt, SIGNAL("clicked(bool)"), self.CesarCryptDecalage)
        self.button_cesar_crypt_bis.connect(self.button_cesar_crypt_bis, SIGNAL("clicked(bool)"), self.CesarCryptCle)
        self.button_cesar_decrypt.connect(self.button_cesar_decrypt, SIGNAL("clicked(bool)"), self.CesarDecryptDecalage)
        self.button_cesar_decrypt_bis.connect(self.button_cesar_decrypt_bis, SIGNAL("clicked(bool)"), self.CesarDecryptCle)


        #ElGamal
        self.el = Elgamal()

        self.label_bits = QLabel("Taille de la cle : ")
        self.label_premier = QLabel("Nombre premier : ")
        self.label_tour = QLabel("Nombre de tours : ")
        self.label_clePrive = QLabel("Clée Privé : ".decode("utf-8"))
        self.label_clePublic = QLabel("Clée Public : ".decode("utf-8"))
        self.label_a = QLabel("Nombre Aleatoire a : ")
        self.label_g = QLabel("Nombre Aleatoire g : ")
        self.label_origine = QLabel("Texte à crypter".decode("utf-8"))
        self.label_ascii = QLabel("Texte en ASCII")
        self.label_crypter = QLabel("Texte crypter ")
        self.label_decrypter = QLabel("Texte décrypter".decode("utf-8"))
        self.label_error_elgamal = QLabel("")

        self.line_edit_bits = QLineEdit("32")
        self.line_edit_premier = QLineEdit()
        self.line_edit_tour = QLineEdit("20")
        self.line_edit_clePrive = QLineEdit()
        self.line_edit_clePublic = QLineEdit()        
        self.line_edit_a = QLineEdit()
        self.line_edit_g = QLineEdit()

        self.text_edit_origine = QTextEdit()
        self.text_edit_ascii = QTextEdit()
        self.text_edit_crypter = QTextEdit()    
        self.text_edit_decrypter = QTextEdit()

        self.bouton_crypter = QPushButton("Crypter")
        self.bouton_decrypter = QPushButton("Décrypter".decode("utf-8"))
        self.bouton_generer = QPushButton("Générer".decode("utf-8"))

        layout_elgamal_principal = QGridLayout()
        layout_elgamal_principal.addWidget(self.label_bits, 0, 0)
        layout_elgamal_principal.addWidget(self.line_edit_bits, 0, 1)
        layout_elgamal_principal.addWidget(self.label_tour, 1, 0)
        layout_elgamal_principal.addWidget(self.line_edit_tour, 1, 1)
        layout_elgamal_principal.addWidget(self.label_premier , 2, 0)
        layout_elgamal_principal.addWidget(self.line_edit_premier ,2, 1)
        layout_elgamal_principal.addWidget(self.label_clePublic, 3,0)
        layout_elgamal_principal.addWidget(self.line_edit_clePublic, 3, 1)
        layout_elgamal_principal.addWidget(self.label_clePrive, 4, 0)
        layout_elgamal_principal.addWidget(self.line_edit_clePrive, 4, 1)
        layout_elgamal_principal.addWidget(self.label_a, 0, 2)
        layout_elgamal_principal.addWidget(self.line_edit_a, 0, 3)
        layout_elgamal_principal.addWidget(self.label_g, 1, 2)
        layout_elgamal_principal.addWidget(self.line_edit_g, 1, 3)

        layout_elgamal_principal.addWidget(self.label_origine, 5, 0, 1, 2) 
        layout_elgamal_principal.addWidget(self.text_edit_origine, 6, 0, 1 , 2)
        layout_elgamal_principal.addWidget(self.label_ascii, 5, 2, 1, 2)
        layout_elgamal_principal.addWidget(self.text_edit_ascii , 6 ,2, 1, 2)
        layout_elgamal_principal.addWidget(self.label_crypter , 7, 0, 1, 2)
        layout_elgamal_principal.addWidget(self.text_edit_crypter, 8, 0, 1, 2)
        layout_elgamal_principal.addWidget(self.label_decrypter, 7, 2, 1, 2)
        layout_elgamal_principal.addWidget(self.text_edit_decrypter, 8, 2, 1, 2)
        layout_elgamal_principal.addWidget(self.bouton_generer, 2 , 2, 1 , 2)
        layout_elgamal_principal.addWidget(self.bouton_crypter, 3, 2 ,1 ,2)
        layout_elgamal_principal.addWidget(self.bouton_decrypter , 4, 2, 1, 2)
        layout_elgamal_principal.addWidget(self.label_error_elgamal, 9, 0, 1, 4)

        self.bouton_generer.connect(self.bouton_generer, SIGNAL("clicked(bool)"), self.GenererElgamal)
        self.bouton_crypter.connect(self.bouton_crypter, SIGNAL("clicked(bool)"), self.CrypterElgamal)
        self.bouton_decrypter.connect(self.bouton_decrypter, SIGNAL("clicked(bool)"), self.DecrypterElgamal)

        self.elgamal.setLayout(layout_elgamal_principal)


        #Eratosthene
        self.eratos_instance = Eratosthene()
        
        self.label_eratos_nombre = QLabel("Maximum")
        self.line_edit_eratos = QLineEdit("10")
        self.text_edit_eratos = QTextEdit()
        self.button_eratos_genere = QPushButton("Générer".decode("utf-8"))
        layout_erastos_principal = QGridLayout()
        layout_erastos_principal.addWidget(self.label_eratos_nombre, 0, 0)
        layout_erastos_principal.addWidget(self.line_edit_eratos, 0, 1)
        layout_erastos_principal.addWidget(self.button_eratos_genere, 0, 2)
        layout_erastos_principal.addWidget(self.text_edit_eratos, 1, 0, 1, 2)              
        
        self.eratos.setLayout(layout_erastos_principal)
        
        self.button_eratos_genere.connect(self.button_eratos_genere, SIGNAL("clicked(bool)"), self.GenererEratos)


        #SHA1
        self.label_sha_message = QLabel("Message")
        self.label_sha_crypter = QLabel("Message Crypter")
        self.text_edit_sha_message = QTextEdit()
        self.text_edit_sha_decrypter = QTextEdit()
        self.button_sha_hascher = QPushButton("Hascher")
        

        layout_sha_principal = QGridLayout()
        layout_sha_principal.addWidget(self.label_sha_message, 0, 0)
        layout_sha_principal.addWidget(self.text_edit_sha_message, 1, 0)
        layout_sha_principal.addWidget(self.label_sha_crypter , 0, 1)
        layout_sha_principal.addWidget(self.text_edit_sha_decrypter, 1, 1)
        layout_sha_principal.addWidget(self.button_sha_hascher, 2, 0, 1, 2)

        self.button_sha_hascher.connect(self.button_sha_hascher, SIGNAL("clicked(bool)"), self.HascherSHA)

        self.sha.setLayout(layout_sha_principal)


        #Mise en place des QWidgets dans les onglets
        self.onglet.addTab(self.largonjem, "Largonjem")
        self.onglet.addTab(self.cesar, "Cesar")
        self.onglet.addTab(self.elgamal, "ElGamal")
        self.onglet.addTab(self.eratos, "Eratosthene")
        self.onglet.addTab(self.sha, "SHA1")
        self.onglet.addTab(self.rsa, "RSA")


        principale = QVBoxLayout()
        principale.addWidget(self.onglet)
        self.setLayout(principale)

    ### FONCTION RSA
    def rsa_generer(self):
        a = 9999999999999999999999999999999999999999999999999999999999999999999999999999999
        b = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        clefPublic,clefPrivee = genererClefs(a,b)
        self.edit_rsa_public.setText(str(clefPublic[0]))
        self.edit_rsa_privee.setText(str(clefPrivee[0]))
        self.edit_rsa_module.setText(str(clefPublic[1]))

    def rsa_crypt(self):
        if((len(self.edit_rsa_public.text()) <= 0) and (len(self.edit_rsa_privee.text()) <= 0) and (len(self.edit_rsa_module.text()) <= 0)):
            self.rsa_generer()
        self.text_edit_rsa_crypt.setText(str(crypter(str(self.text_edit_rsa_decrypt.toPlainText()),\
                                                (int(self.edit_rsa_public.text()),int(self.edit_rsa_module.text())))))
            
    def rsa_decrypt(self):
        print (int(self.edit_rsa_privee.text()),int(self.edit_rsa_module.text()))
        if not((len(self.edit_rsa_public.text()) <= 0) and (len(self.edit_rsa_privee.text()) <= 0) and (len(self.edit_rsa_module.text()) <= 0)):
            self.text_edit_rsa_decrypt.setText(str(decrypter(int(self.text_edit_rsa_crypt.toPlainText()),\
                                                        (int(self.edit_rsa_privee.text()),\
                                                        int(self.edit_rsa_module.text()))\
                                                        )))



    #### FONCTION ELGAMAL
    def GenererElgamal(self):
        if((len(self.line_edit_tour.text()) > 0) and (int(self.line_edit_bits.text()) > 0)):
            print self.line_edit_bits.text().toInt()[0]
            
            self.el.setTailleCle(int(self.line_edit_bits.text().toInt()[0]))
            self.el.setTour(int(self.line_edit_tour.text()))            
            print "taille " , self.el.getTailleCle()
            self.el.generer()
            self.line_edit_premier.setText(str(self.el.p))
            self.line_edit_clePrive.setText(str(self.el.cle_prive))
            self.line_edit_clePublic.setText(str(self.el.cle_public))        
            self.line_edit_a.setText(str(self.el.a))
            self.line_edit_g.setText(str(self.el.g))

        else :
            self.label_error_elgamal.setText("Erreur : ajouter un nombre de bits et indiquer le nombre de tours ! ".decode("utf-8"))


    def CrypterElgamal(self):        
        if(len(self.text_edit_origine.toPlainText()) > 0 ):
            self.txt = QString(self.text_edit_origine.toPlainText())

            self.el.setTextOrigine(unicode(self.text_edit_origine.toPlainText()))
            self.el.crypter()
            self.text_edit_ascii.setText(self.el.text_ascii)
            self.text_edit_crypter.setText(self.el.text_crypter)
        else :
            self.label_error_elgamal.setText("Erreur : veuillez mettre un texte à crypter ".decode("utf-8"))

    def DecrypterElgamal(self):
        
        if(len(str(self.text_edit_crypter.toPlainText()))>0):
            self.el.text_origine = str(self.text_edit_crypter.toPlainText())
            self.el.decrypter()
            strId = QString(self.el.text_decrypter)
            self.text_edit_decrypter.setText(strId)

        else :
            self.label_error_elgamal.setText("Rien à decrypter".decode("utf-8"))

                

    #### FONCTION LARGONJEM
    def LargonjemCrypt(self):
        self.largonjem_instance.setText(str(self.text_edit_largonjem_normal.toPlainText()))
        self.largonjem_instance.crypter()
        self.text_edit_largonjem_crypter.setText(str(self.largonjem_instance.getTextCrypter()))
    

    #Algorithme de cryptage de cesar avec simple decalage ou clé
    def CesarCryptDecalage(self):
        self.cesar_instance.setText(str(self.text_edit_cesar_crypt.toPlainText()))
        self.cesar_instance.setDecalage(int(self.line_edit_cesar_decalage.text())) 
        self.cesar_instance.CrypterDecalage()
        self.text_edit_cesar_decrypt.setText(str(self.cesar_instance.getTextCrypter()))       
    
    def CesarCryptCle(self):
        self.cesar_instance.setText(str(self.text_edit_cesar_crypt.toPlainText()))
        self.cesar_instance.setCle(int(self.line_edit_cesar_cle.text()))
        self.cesar_instance.CrypterCle()
        self.text_edit_cesar_decrypt.setText(str(self.cesar_instance.getTextCrypter()))
        
    def CesarDecryptCle(self):
        self.cesar_instance.setTextDecrypter(str(self.text_edit_cesar_decrypt.toPlainText()))
        self.cesar_instance.setCle(int(self.line_edit_cesar_cle.text()))
        self.cesar_instance.DecrypterCle()
        self.text_edit_cesar_crypt.setText(str(self.cesar_instance.getText()))
        
    def CesarDecryptDecalage(self):
        self.cesar_instance.setTextDecrypter(str(self.text_edit_cesar_decrypt.toPlainText()))
        self.cesar_instance.setDecalage(int(self.line_edit_cesar_decalage.text()))
        self.cesar_instance.DecrypterDecalage()
        self.text_edit_cesar_crypt.setText(str(self.cesar_instance.getText()))
    
    
    ##### FONCTION ERATOSTHENE
    def GenererEratos(self):
        self.eratos_instance.setNombre(int(self.line_edit_eratos.text()))
        self.eratos_instance.Generer()                               
        self.text_edit_eratos.setText(str(self.eratos_instance.getListe()))       

    ###### FONCTION SHA
    def HascherSHA(self):
        text = self.text_edit_sha_message.toPlainText()       
        self.sha_instance = sha1()
        self.text_edit_sha_decrypter.setText(self.sha_instance.sha1(text))


        
if __name__ == "__main__":
    app = QApplication(sys.argv)       
    Mafenetre = Rassemblement()        
    Mafenetre. setBaseSize(600, 400)
    Mafenetre.show()            
    Mafenetre.setWindowTitle("The Final (CountDown ?)")
    app.exec_()





