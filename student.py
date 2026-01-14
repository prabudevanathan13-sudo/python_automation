class Student:
    def __init__(self):
        self.students = {}
    def add_student(self):
        username = input("enter user name")
        name = input("enter the name")
        mark= int(input("enter the mark"))
        self.students[username]= {"name":name,"mark":mark}
        print("student data stored sucessfully \n")
    

    def display_student(self):
        for username, details in self.students.items():
            print("username", username)
            print("name",details["name"])
            print("mark", details["mark"])


s1= Student()
s1.add_student()

print(s1.display_student())  
    

    
