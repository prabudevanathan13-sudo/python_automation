class product:
    def __init__(self):
        self.prod={}
    def add_product(self, p_id,name,price):
        self.prod[p_id]={
            "name": name,
            "price": price
            
        }
        print("product added sucessfully")
    
    def update_product(self, p_id, newprice):
        if p_id in self.prod:
            self.prod[p_id]["price"]=newprice
            print("updated newprice")
            
    def del_product(self,p_id):
        if p_id in self.prod:
            del self.prod[p_id]
            print("product deleted sucessfully")
    
    
    def display(self):
        print("++++++++++++++++++++++++")
        for product_id,data in self.prod.items():
            print(f"pid :{product_id}, name : {data["name"]},price: {data["price"]}")
            
p1=product()
p1.add_product(101,"suji",100)
p1.add_product(102,"raj",300)
p1.add_product(103,"ma",200)
p1.add_product(104,"rma",500)
p1.update_product(101,750)
p1.del_product(104)

p1.display()

        
