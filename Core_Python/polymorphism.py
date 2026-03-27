#Payemnt System Example

class Payment:
    def pay(self, amount):
        return f"Paying {amount}"
    
class CreditCard(Payment):
    def pay(self, amount):
        return f"Paid {amount} using credit card"

class UPI(Payment):
    def pay(self, amount):
        return f"Paid ₹{amount} using UPI"

class Cash(Payment):
    def pay(self, amount):
        return f"Paid ₹{amount} in Cash"

class PayPal(Payment):
    def pay(self, amount):
        return f"Paid {amount} through Paypal"

def process_payment(payment_method, amount):
    print(payment_method.pay(amount))

p1 = CreditCard()
p2 = UPI()
p3 = Cash()
p4  = PayPal()

process_payment(p1, 1000)
process_payment(p2, 500)
process_payment(p3, 200)
process_payment(p4, 2000)