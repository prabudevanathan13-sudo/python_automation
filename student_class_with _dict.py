class Student:
    def __init__(self):
        self.students = {}

    def add_student(self, r_no, name, m1, m2, m3):
        self.students[r_no] = {
            "name": name,
            "m1": m1,
            "m2": m2,
            "m3": m3
        }

    def total(self, r_no):
        s = self.students[r_no]
        return s["m1"] + s["m2"] + s["m3"]

    def avg(self, r_no):
        return self.total(r_no) / 3

    def display(self):
        for r_no, details in self.students.items():
            print("Roll No :", r_no)
            print("Name    :", details["name"])
            print("M1      :", details["m1"])
            print("M2      :", details["m2"])
            print("M3      :", details["m3"])
            print("Total   :", self.total(r_no))
            print("Average :", self.avg(r_no))
            print("----------------------")
if __name__ == "__main__":
    c1 = Student()

    no = int(input("Enter the roll number: "))
    name = input("Enter the name: ")
    m1 = int(input("Enter M1 mark: "))
    m2 = int(input("Enter M2 mark: "))
    m3 = int(input("Enter M3 mark: "))

    c1.add_student(no, name, m1, m2, m3)
    c1.display()
