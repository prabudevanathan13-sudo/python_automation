class student:
    def __init__(self,r_no,name,m1,m2,m3):
        self.r_no=r_no
        self.name=name
        self.m1=m1
        self.m2=m2
        self.m3=m3
    def total(self):
        return self.m1+self.m2+self.m3
    def avg(self):
        return self.total() / 3
        
    def display(self):
        print("no",self.r_no)
        print("name",self.name)
        print("m1",self.m1)
        print("m2",self.m2)
        print("m3",self.m3)
        print("total",self.total())
        print("avg",self.avg())
if __name__ == "__main__":
    
    no=int(input("enter the number:"))
    name=input("enter the name")
    m1=int(input("enter the m1 mark"))
    m2=int(input("enter the m2 mark"))
    m3=int(input("enter the m3 mark"))
    c1=student
    c1 = student(no,name,m1,m2,m3)
c1.display()
