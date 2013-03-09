#! /usr/bin/python
#-*-coding: utf-8 -*-

import random
import sys
import math

def Bezout(c,phiN):
    r1=c
    r2=phiN
    u1=1
    v1=0
    u2=0
    v2=1
    while r2<>0 :
        q=r1/r2
        rs=r1
        us=u1
        vs=v1
        r1=r2
        u1=u2
        v1=v2
        r2=rs-q*r2
        u2=us-q*u2
        v2=vs-q*v2
    return r1,u1,v1 

# expension modulaire
def puissance(a,e,n):
    p=1
    while(e>0):
        if e%2!=0:
            print type(p),type(a),type(n)
            p=(p*a)%n
        a=(a*a)%n
        e=e/2
    return p

def temoin(a,n):
    m = n-1
    y = 1
    while m<>0 :
        if m%2 == 1 :
            y = (a*y) % n
            m = m-1
        else :
            b = a
            a = (a*a) % n
            if a==1 and b<>1 and b<>(n-1) :
                return True
            m=m/2
    if y <> 1 :
        return True
    else :
        return False

def millerRabin(n,t=40):
    for i in range(t):
        a = random.randint(2, n-1)
        if temoin(a,n) :
            return False
    return True

def randomNombrePremier(d=1000,f=10000):
    nbrePremier = random.randint(d,f)
    while not millerRabin(nbrePremier):
        nbrePremier = random.randint(d,f)
    return nbrePremier

def sizeInt(i):
    return len(map(int,str(i)))

def lstToStr(lst):
    msg=""
    for elt in lst:
        if(sizeInt(elt)==3):
            msg+=str(elt)
        elif(sizeInt(elt)==2):
            msg+="0"
            msg+=str(elt)
        elif(sizeInt(elt)==1):
            msg+="00"
            msg+=str(elt)
        else: # cas impossible
            msg+="000"
    return msg

def strToLst(msg):
    lst=[]
    for i in range(len(msg)):
        if(i%3==0):
            tmp=str(msg[i])
        elif(i%3==1):
            tmp+=str(msg[i])
        else:
            tmp+=str(msg[i])
            lst.append(int(tmp))
    return lst

def strInAscii(msg):
    lst=[]
    for i in range(len(msg)):
        lst.append(ord(msg[i]))
    return lst

def asciiInStr(msg):
    lst=""
    for i in range(len(msg)):
        lst+=chr(msg[i])
    return lst

def crypter(msg,clefs):
    msg = strInAscii(msg)
    msg = lstToStr(msg)
    msg = puissance(int(msg),clefs[0],clefs[1])
    return msg
    
def decrypter(msg,clefs):
    msg = puissance(msg,clefs[0],clefs[1])
    if(sizeInt(msg)%3==2):
        msg = "0"+str(msg)
    elif(sizeInt(msg)%3==1):
        msg = "00"+str(msg)
    else:
        msg = str(msg)
    msg = strToLst(str(msg))
    msg = asciiInStr(msg)
    
    return msg

def genererClefs(a,b):
    p=randomNombrePremier(a,b)
    q=randomNombrePremier(a,b)
    n=p*q
    phiN=(p-1)*(q-1)
    c = random.randint(99999,999999)
    r=0
    u=v=-1
    while not (r==1 and u>=0):
        c+=1
        (r,u,v) = Bezout(c,phiN)
    d=abs(u)
    return (c,n),(d,n)

if __name__=="__main__":
    a=9999999999999999999999999999999999999999999999999999999999999999999999999999999
    b=9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
    
    clefPublic,clefPrivee = genererClefs(a,b)
    
    msgACrypter = """mon message cryptée !!!"""
    print msgACrypter
    msgCrypter = crypter(msgACrypter, clefPublic)
    print msgCrypter
    msgDecrypter = decrypter(msgCrypter, clefPrivee)
    print msgDecrypter
