class Employee:
    def __init__(self):
        self.emp_id = {}

    def add_emp(self, eid, name, dept, sal):
        self.emp_id[eid] = {
            "name": name,
            "dept": dept,
            "sal": sal
        }
        print("Employee details added successfully")

    def update_emp(self, eid, new_dept):
        if eid in self.emp_id:
            self.emp_id[eid]["dept"] = new_dept
            print("Department updated successfully")
        else:
            print("Employee ID not found")

    def delete_emp(self, eid):
        if eid in self.emp_id:
            del self.emp_id[eid]
            print("Employee record deleted successfully")
        else:
            print("Employee ID not found")

    def emp_display(self):
        if not self.emp_id:
            print("No employee records found")
        for emp_id, data in self.emp_id.items():
            print(
                f"Employee ID: {emp_id}, "
                f"Name: {data['name']}, "
                f"Dept: {data['dept']}, "
                f"Salary: {data['sal']}"
            )


if __name__ == "__main__":
    e1 = Employee()

    # ADD employee
    eid = int(input("Enter employee ID: "))
    name = input("Enter employee name: ")
    dept = input("Enter employee dept: ")
    sal = int(input("Enter salary: "))
    e1.add_emp(eid, name, dept, sal)

    print("\n--- Employee List ---")
    e1.emp_display()

    # UPDATE employee
    update_id = int(input("\nEnter employee ID to update dept: "))
    new_dept = input("Enter new department: ")
    e1.update_emp(update_id, new_dept)

    print("\n--- After Update ---")
    e1.emp_display()

    # DELETE employee
    delete_id = int(input("\nEnter employee ID to delete: "))
    e1.delete_emp(delete_id)

    print("\n--- After Delete ---")
    e1.emp_display()
