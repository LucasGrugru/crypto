import timeit

#Mettre au carré et multiplier
#version recursive
def samrec(x,n):
	tmp = 0
	if n==1:
		puissance = x
	else:
		tmp=samrec(x,n/2);
		if (n%2)==0:
			puissance = tmp*tmp
		else:
			puissance = tmp*tmp*x;
	return puissance
	
#Mettre au carré et multiplier
#version iterative
def sam(x,n):
    tmp = 1
    while n != 0:
        if (n % 2) == 1:
            tmp = tmp * x
            n=n-1
        x = x*x
        n = n/2
        #print n
    return tmp

print "Ce programme calcul x à la puissance n avec une technique d'exponentation rapide. Il effectue deux fois le calcul, une fois en utilisant un algorithme récursif, et une fois en utilisant un algorithme itératif"
x = input("entrez x : ")
n = input("entrez n : ")

print samrec(x,n)
print sam(x, n)
