f = lambda x:x+x

print (f(10))

g = lambda x:x*x if (x>10) else x+x

print (g(20))

#nested if else

h= lambda x: x*x if (x>10) else (10 if x==9 else 0)

print (h(9))
