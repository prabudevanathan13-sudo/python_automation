# Parent class
class Person:
    def __init__(self, name):
        self.name = name   # Encapsulation

    def show_name(self):
        print("Name:", self.name)


# Child class (Inheritance)
class Student(Person):
    def __init__(self, name, roll_no):
        super().__init__(name)   # calling parent constructor
        self.roll_no = roll_no

    # Polymorphism (method overriding)
    def show_name(self):
        print("Student Name:", self.name)
        print("Roll No:", self.roll_no)


# Another Child class
class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def show_name(self):
        print("Teacher Name:", self.name)
        print("Subject:", self.subject)


# Main program
if __name__ == "__main__":
    s1 = Student("Rahul", 101)
    t1 = Teacher("Anita", "Maths")

    s1.show_name()
    print("------")
    t1.show_name()
