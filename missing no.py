number1 = [1,3,4,7]
m= max(number1)
for x in range(1, m+1):
    if x not in number1:
        print(x)
print("missing nos starting  non 1")

number2 =[10,12,14,17]
for y in range(number2[0], number2[-1]+1):
    if y not in number2:
        print(y)

a = ["apple", "orange"]
x,y = a
print(y)

#using for loop find the max of 3 nos
number = [5,6,4,3,8,9]

large_number = []
for i in range(len(number)):
    max_number = max(number)
    
    large_number.append(max_number)
    number.remove(max_number)
 
    print(large_number) 
print("using forloop to find max nos in list")   
#using normal method to  find the max of 3 nos
number1 = [5,6,4,3,8,9]
large_number=sorted(number1, reverse= True)
print("using sorted method")
print(large_number[:3])
    # remove dulicate in list using set()
text1=["prabu","raja","indu","perumal","indu"]
print(set(text1))

#memory usage for list tuple and dict

import sys
l=[1,2,3,4,6]
t=("raja",3,6,"raja")
d={"a":34,"b":56,"c":78}
print(f"list memory useage: {sys.getsizeof(l)}")
print(f"tuple memory useage: {sys.getsizeof(t)}")
print(f"dict memory useage: {sys.getsizeof(d)}")



#commmon items in both the set:
a = {"apple","mango","pineapple"}
b = {"mango","papaya","grapes"}
print(a & b)


text5= "malayalam"
lower_text=text5.lower()
print(lower_text)
reverse_text = (text5[::-1])
print(reverse_text)
if lower_text == reverse_text:
    print("paladrome")
else:
    print("not a paladrome")


#even or odd in single statement
num = int(input("enter the number:"))
print("even" if num%2==0 else "odd")
          
