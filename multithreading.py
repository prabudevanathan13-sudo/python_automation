import time
start_time=time.time()
def task1():
    print("task1 started:")
    time.sleep(2)
    print("task1 completed:")

def task2():
    print("task2 started:")
    time.sleep(3)
    print("task2 completed:")

def task3():
    print("task3 started:")
    time.sleep(5)
    print("task3 completed:")
task1()
task2()
task3()
end_time=time.time()
print(f"execution time: {end_time-start_time}")
print("execution completed sucesfully")
