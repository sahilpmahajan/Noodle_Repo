import os
import argparse
from collections import defaultdict
d = defaultdict(list)
#read data, make a list of lists, sort list of lists, convert lists of lists to dictionary 
#read from file as list of strings, convert to dictionary with key as name of country and list as value of that key. List contains no of gold, silver, bronze respectively
#all sorting has been done with optimised bubble sort algorithm (once sorted, it breaks)

#parser = argparse.ArgumentParser()
#parser.add_argument('--path', type=str, required=True)
#parser.add_argument('--output', type=str, required=True)
#args = parser.parse_args()



content = []




with open('test.txt') as f:
	content+= f.read().splitlines() 

print(content)
def modData(S):
	#S = india-1-2-4
	m = []
	for e in range(len(S)):
		if(S[e] == '-'):
			m.append(e)
	#m = [5,7,9]
	l = []
	l.append(S[0:m[0]])#name
	l.append(S[m[0]+1:m[1]])
	l.append(S[m[1]+1:m[2]])#silver
	l.append(S[m[2]+1:])#bronze
	return l #l = ['india','1','2','4']

def sortData(l):#l is a list of lists
	#bubblesort according to l[i] then change l[i]->l[i[1]]
	for i in range(len(l)):
		ch = True
		j = 0
		while j>=0 and j<len(l)-i-1:
			if(l[j][1]<l[j+1][1]):
				m = l[j+1]
				l[j+1]=l[j]
				l[j] = m
				ch = False #no swapping = ch is true, time to break
			j = j + 1
		if(ch):
			break
	#lexicon sort
	while i >0 and i < (len(l)-1):
		if(l[i][1]==l[i+1][1]):
			temp = i
			while(l[temp][1]==l[temp+1][1] and temp+1<len(l)):
				temp = temp + 1 #temp will be last index with same as the one behind [0,12,12,12] will have i = 1, temp =3 
				if(temp + 1) == len(l):#segmentation error prevent
					break
			m=i
			while m<=temp:
				ch = True
				n = m
				while n>=m and n<=temp-1-(m-i):
					if(l[n][0]>l[n+1][0]):
						temp2 = l[n+1]
						l[n+1]=l[n]
						l[n] = temp2
						ch = False #no swapping = ch is true, time to break
					n = n + 1
				if(ch):
					break
				m = m + 1
			i = temp - 1
		i = i + 1			

	return l
	
		
	
def func():
	LL = []
	for e in range(len(content)):
		s = content[e]
		l = modData(s)
		for i in range(1,len(l)):
			l[i]=int(l[i])
		LL.append(l)
	LL = sortData(LL)
	for e in range(len(LL)):
		d[LL[e][0]]=LL[e][1:]
	#now we just need to sort dictionaries based on gold medals and then lexographically
	print(d)

func()
		
	
	 
