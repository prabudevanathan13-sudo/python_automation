# -------------------------------
# 1️⃣ Singleton Pattern (Logger)
# -------------------------------

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, message):
        print("LOG:", message)


# -------------------------------
# 2️⃣ Factory Pattern (Car Factory)
# -------------------------------

class Car:
    def drive(self):
        pass


class Sedan(Car):
    def drive(self):
        return "Sedan ride started"


class SUV(Car):
    def drive(self):
        return "SUV ride started"


class CarFactory:
    @staticmethod
    def create_car(car_type):
        if car_type == "sedan":
            return Sedan()
        elif car_type == "suv":
            return SUV()


# -------------------------------
# 3️⃣ Strategy Pattern (Payment)
# -------------------------------

class PaymentStrategy:
    def pay(self, amount):
        pass


class CreditCard(PaymentStrategy):
    def pay(self, amount):
        return f"Paid {amount} using Credit Card"


class UPI(PaymentStrategy):
    def pay(self, amount):
        return f"Paid {amount} using UPI"


# -------------------------------
# 4️⃣ Observer Pattern (Notification)
# -------------------------------

class User:
    def update(self, message):
        print("Notification:", message)


class Ride:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, user):
        self.subscribers.append(user)

    def notify(self, message):
        for user in self.subscribers:
            user.update(message)


# -------------------------------
# 🚀 Main System
# -------------------------------

# Logger (Singleton)
logger = Logger()

# Create car using Factory
car = CarFactory.create_car("sedan")
logger.log(car.drive())

# Setup ride and users (Observer)
ride = Ride()
user1 = User()
user2 = User()

ride.subscribe(user1)
ride.subscribe(user2)

# Payment using Strategy
payment_method = CreditCard()
amount = 500

print(payment_method.pay(amount))

# Notify users
ride.notify("Your ride has been completed!")

logger.log("Ride completed successfully.")
