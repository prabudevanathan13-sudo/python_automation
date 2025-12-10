       
import unittest
import tests
from html_reporter import HTMLTestRunner
import sys
import os
from Test.Test_school_management import school_student_mgnt
from Test.Test_school_management import Student
from Test.Test_school_management import Teacher
from Test.Test_calculator import Item
from Test.Test_calulator1 import calci
from Test.Test_bank_account import Test_bank_Prabu_accounts
# Creating Objects
obj = school_student_mgnt("Ram", 30)
stu = Student("Jasvikaa", 12, 101, 92)
teacher = Teacher("Dinesh", 35, "Maths")


# Create items

item1 = Item("Milk", 60, 2)
item2 = Item("Bread", 40, 1)
item3 = Item("Eggs", 7, 10)
grand_total = item1.total_price() + item2.total_price() + item3.total_price()

#calculater
calc = calci()

#banking
acc1 = Test_bank_Prabu_accounts("Prabu", 1000)




class Test_school_student_mgnt(unittest.TestCase):
	
	def test_management(self):
		stu.show()
		teacher.show()
		print("Grade:", stu.calculate_grade())
        
class Test_Item(unittest.TestCase):
    def test_total_price(self):
        #grand_total = item1.total_price() + item2.total_price() + item3.total_price()
        print("Total Amount =", grand_total)

class Test_calci(unittest.TestCase):
    def test_cal(self):
        print("Addition:", calc.add(10, 5))
        print("Subtraction:", calc.subtract(10, 5))
        print("Multiplication:", calc.multiply(10, 5))
        print("Division:", calc.divide(10, 5))
      
class Test_bank_Prabu_accounts(unittest.TestCase):
    
    def test_bank(self):
        acc1.check_balance()
        acc1.deposit(500)
        acc1.withdraw(300)
        acc1.check_balance()
        #print(f"Available Balance: ₹{self.balance}")       
        

if __name__ == '__main__':
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__) + "\\tests" 
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_school_student_mgnt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Item))    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_calci))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_bank_Prabu_accounts))
        
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class_attributes_methods))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class_singleinheritance))
    

    # Run all tests in one go → single HTML report
    '''
    runner = HtmlTestRunner.HTMLTestRunner(
        output='example_dir',      # Folder for report
        report_name='combined_report',  # File name without extension
        combine_reports=True,      # <--- IMPORTANT for single file
        add_timestamp=False        # Optional: avoid timestamp in file name
    )
    '''
    runner = HTMLTestRunner(
        report_filepath="my_report.html",
        title="My unit test",
        description="This demonstrates the report output by HTMLTestRunner.",
        open_in_browser=True
    )
    
    runner.run(suite)
    
# style = """
    # .heading {
    # margin-top: 0ex;
    # margin-bottom: 1ex;
    # border-style:ridge;
    # color:white;
    # background-color:#999900;
    # background-color:#1E90FF;
    # font-weight:bold;
    # }
# """
# script = """
    # Your script
# """
""" 

#1. Import the module
#2. Create Object
#3. Create a new class
#4. Call the function     

# For test report  
#1. Testcase
#2. Test suite
#3. Test Runner
def suite():
    suite = unittest.TestSuite()
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Comments))
  
    runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Python Automation UnitTest Test report', report_name='report',
                        open_in_browser=True, description="Python UnitTest Automation", tested_by="Prakash Perumal",
                        add_traceback=False,script=script,style=style)
    runner.run(suite)

if __name__ == '__main__':
    suite()
"""