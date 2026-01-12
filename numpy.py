import numpy as np

marks = np.array([78, 85, 90, 66, 45, 88, 92])

total = marks.sum()
average = marks.mean()
highest = marks.max()
lowest = marks.min()

pass_count = np.sum(marks >= 50)
fail_count = np.sum(marks < 50)

print("Total Marks:", total)
print("Average Marks:", average)
print("Highest:", highest)
print("Lowest:", lowest)
print("Passed Students:", pass_count)
print("Failed Students:", fail_count)

print("========emp_salary===========")

salaries = np.array([25000, 30000, 28000, 40000, 35000])

avg_salary = salaries.mean()
high_salary = salaries.max()
low_salary = salaries.min()

above_avg = salaries[salaries > avg_salary]

print("Average Salary:", avg_salary)
print("Highest Salary:", high_salary)
print("Lowest Salary:", low_salary)
print("Above Average Salaries:", above_avg)
print("========Banl emi=============")


emi = np.array([8500, 8500, 9000, 9000, 9500, 9500])

print("Total EMI Paid:", emi.sum())
print("Average EMI:", emi.mean())
print("Highest EMI:", emi.max())


print("========temperature monituring =============")

temperature = np.array([30, 32, 35, 33, 36, 38, 34])

avg_temp = temperature.mean()
high_temp_days = temperature[temperature > 35]

print("Average Temperature:", avg_temp)
print("High Temperature Days:", high_temp_days)

