import re
text1="welcome to python code"
text2="my phone no is 9972059900 and area code is 0413"
text3="9972059900"
text4="deenabtech@gmail.com"
text5= "13-11-1985"
simple_search=re.search("code",text1)
print(simple_search)
if simple_search:
    print("found",simple_search.group())
print(re.search(r"python",text1))
print(re.findall(r"\d+", text2))
print(re.fullmatch(r"\d{10}",text3))
print(re.fullmatch(r"\w+@\w+\.\w+",text4))
print(re.sub(r"\d+","XXXXX",text3))
print(re.fullmatch(r"\d{2}-\d{2}-\d{4}",text5))

print(re.fullmatch(r"^\d{10}^", "9876543210"))
print(re.split(r",\s*", "a,b,c"))

#match
print(re.match(r"python","python developer"))
#full match
print(re.fullmatch(r"\d+","area pincode is 0413"))

print(re.fullmatch(r"\d{10}","9972059900"))
print(re.fullmatch(r"\w+@\w\.\w","abc@gmail.com"))
print(re.fullmatch(r"\d{2}-\d{2}-\d{4}","13-11-1985"))
#findall
print(re.findall(r"india","all are my brothers and sisters in india"))
#replace

print(re.sub(r"\d+","xxx","997309876"))
#split
print(re.split(r"\s*","p,r,a,b,u"))
      
      
