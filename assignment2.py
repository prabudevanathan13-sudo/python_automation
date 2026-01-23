#1 Convert a tuple into a list, modify the list, and convert it back to a tuple.
num =(1,2,3,4,5)
print(num)#print the orginal output

t=list(num)
t.append(9)
print(t)# converting tuple to list

l=tuple(t)
print(l)#converting list to tuple

#2 Given a tuple (1,2,3,4,5), create a new tuple containing only even numbers.

num =(1,2,3,4,5)
even=()

for x in (num):
    if x % 2 ==0:
        even = even + (x,) #creates a tuple
print(even)

#3 Write a program to find the index of an element in a tuple without using index()
num =(1,2,3,4,5)

for i in range(len(num)):
    print(i, num[i])
#metjod 2 with enumerate
num =(1,2,3,4,5)
target = 3

for i, v in enumerate(num):
    if v == target:
        print("Index:", i)
        
#Check if two tuples have any common elements
num1 =(1,2,3,4,5)
num2=(3,4,6,8)

common = tuple(set(num1)& set(num2))
print(common)

#Create a tuple of 5 user inputs and calculate their sum.

#method 1
n1=int(input("enter the first number:"))
n2=int(input("enter the second number:"))
n3=int(input("enter the third number:"))
n4=int(input("enter the fourth number:"))
n5=int(input("enter the fiveth number:"))

num=(n1,n2,n3,n4,n5)
total=(n1+n2+n3+n4+n5)
print("given number", num)
print("total", total)

#method 2

import numpy as np 
num= tuple(map(int,input("enter the 5 inputs").split()))
total=np.sum(num)
print(total)
#Input a tuple of numbers and print only the even numbers.

n1=int(input("enter the first number:"))
n2=int(input("enter the second number:"))
n3=int(input("enter the third number:"))
n4=int(input("enter the fourth number:"))
n5=int(input("enter the fiveth number:"))

num=(n1,n2,n3,n4,n5)
even_no =()
for i in num:
    if i % 2 == 0:
        even_no=even_no+(i,)
print(even_no)

#print till greatest no is print 
num=[1,2,3,6,5]
n = 0
for x in num:
    if x > n:
        n = x
        print(n)


#remove duplicate in list
a= ["india","pakistan","japan","usa","japan"]
print(set(a))
# method 2
b =[]
for x in a:
    if x not in b:
        b.append(x)
print(b)

#third method

c=[]
[c.append(x)for x in a if x not in c]
print(c)


#regix for printing
import re 
text=("product date is 13-11-1985"
    "product mail id is prabu.devanathan@com")

patten=re.search(r'\d{2}-\d{2}-\d{4}',text)
print(patten.group())


#fibonic series
n= 10
a,b =0,1
count =0 
while count<n:
    print(a)
    a,b=b,a+b
    count+=1
    
print("prime next program")
for i in range(2,21):
    for x in range(2, int(i**0.5)+1):
        if i % x == 0:
            break
    else:
        print(i)
            

a=[1,2,4,4,5,6,7]
even =[]
for i in a:
    if i % 2 ==0:
        even =even+[i]
        print(even)


duplicate=set()
seen=set()
for i in a:
    if i in seen:
        duplicate.add(i)
    else:
        seen.add(i)
print(duplicate)
# find the dulicate in comprimenhision

dup=[x for x in set(a) if a.count(x)>1 ]
print(dup)

#find the first  duplicate
seen =set()
for i in a:
    if i in seen:
        print(i)
        break
    seen.add(i)

n =7
a,b=0,1
count =0 
while count<n:
    print(a)
    a,b= b,a+b 
    count+=1 

for i in range(2,21):
    for j in range(2, int(i**0.5)+1):
        if i%j==0:
            
            break 
    else:
        print(i)

q=[1,2,3,4,5,5,7]
duplicate=set()
seen=set()
for i in q:
    if i in seen:
        duplicate.add(i)
    else:
        seen.add(i)
print(duplicate)

duplicate=[x for x in set(q) if q.count (x)>1 ]
print(duplicate)
    