class Employee:
    def __init__(self):
        self.emp_id={}
    def add_employee(self):
        print("====Employee details===")
        eid = int(input("enter the employee roll no: "))
        name = input("enter the employee name: ")
        dept= input("enter the employee dept : ")
        salary = int(input("enter the employee salary: "))
        print("==adding employee details==")
        
        self.emp_id[eid]={
            "name":name,
            "dept":dept,
            "salary":salary
        }
        print("Employee details added sucessfully")
        
    def emp_update(self):
        eid = int(input("enter the employee roll no_for update: "))
        if eid in self.emp_id:
            new_dept= input("enter the employee dept : ")
            self.emp_id[eid]['dept'] = new_dept
            print("Employee dept updated  sucessfully")
        else:
            print("Employee deptnot updated ")
    def delete_employee(self,eid):
        eid = int(input("enter the employee roll no_for delete: "))
        if eid in self.emp_id:
            del self.emp_id[eid]
            print("employee details deleted ")
        else:
            print("employee details not deleted")
    
    def display_emp_details(self):
        if not self.emp_id:
            print("employee is not in the database")
            return
        for emp_id,data in self.emp_id.items():
            
            print(
                f"employee_id:{emp_id}, "
                f"emp_ name is :{data['name']}, "
                f"emp_dept is :{data['dept']}, "
                f"emp_salary is: {data['salary']} ")
if __name__ == "__main__":
    
    e1=Employee()
    while True:
        print("employee details")
        print("1) ADD employee details")
        print("2) UPDATE employee details")
        print("3) DELETE employee details")
        print("4) SHOW employee details")
        print("5) EXIT")
        choice = int(input("enter the choice from 1-5 : "))
        if choice == 1:
            e1.add_employee()
        elif choice == 2:
            e1.emp_update()
        elif choice == 3:
            e1.delete_employee()
        elif choice == 4:
            e1.display_emp_details()
        elif choice == 5:
            print("Exiting program")
            break
        else:
            print("Invalid choice")
