import os
class file_oper:
    def file_create(self):
        with open("data.txt",'x')as f:
            print(f.write("file created sucessfully"))
            
        
        
    def check_file_avaiablity(self):
        if os.path.exists("data.txt"):
            print("file exist")
        else:
            print("file not found")
    
            
        
    def write_file(self,text):
        with open("data.txt","w") as f:
            f.write(text+"\n")
    def read_file(self):
        with open("data.txt","r") as f:
            print(f.read())

    def read_line_by_line(self):
        with open ("data.txt","r") as f:
            for line in f:
                print(line.strip())
    def read_lines(self):
        with open("data.txt","r")as f:
            print(f.readlines())
    def file_delete(self):
        os.remove("data.txt")
            
f1=file_oper()
f1.file_create()
f1.check_file_avaiablity()
f1.write_file("india is my countryi love it very much")
f1.read_file()
f1.read_line_by_line()
f1.read_lines()#print line in list
f1.file_delete()

    
