from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


#--------------------------- Category ------------------------
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

#--------------------------- Product ------------------------
class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity}"

#--------------------------- ExpenseCategory ------------------------
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    



#--------------------------- Income Category ------------------------
class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

#--------------------------- Supplier ------------------------
class Supplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

#--------------------------- Customer ------------------------
class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# ----------------   System Settings   ----------------
class SystemSettings(models.Model):
    company_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    vat = models.PositiveIntegerField()
    token_or_table = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    
    def __str__(self):
        return self.company_name
    
class Fund(models.Model):
    FUND_TYPE_CHOICES = (
        ('Bank', 'Bank'),
        ('Other', 'Other'),)
    fund_name = models.CharField(max_length=150)
    fund_type = models.CharField(max_length=10, choices=FUND_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fund_name
    
    
class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
    

class OtherIncome(models.Model):
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
    
    
class SupplierPayment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supplier.name} - {self.amount}"
    
    
class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"
    

class FundTransfer(models.Model):
    from_fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='transfer_from')
    to_fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='transfer_to')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_fund} → {self.to_fund} ({self.amount})"

    
class Order(models.Model):
    table = models.CharField(max_length=50)
    order_type = models.CharField(max_length=20, choices=[('heaving','Heaving'),('parcel','Parcel')])
    discount = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    fund = models.CharField(max_length=20, choices=[('cash','Cash'),('bkash','Bkash')])
    paid_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending / completed

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    

    
    
class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20,
        choices=[
            ('Received', 'Received'),
            ('Pending', 'Pending'),
            ('Ordered', 'Ordered'),
        ],
        default='Received')

    @property
    def subtotal(self):
        return sum(item.total() for item in self.items.all())

    @property
    def grand_total(self):
        return self.subtotal - self.discount + self.service_charge

    def update_total_amount(self):
        self.total_amount = self.grand_total
        self.save()


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total(self):
        return self.quantity * self.purchase_price
    
    
class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='returns')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    return_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Return {self.product.name} ({self.quantity})"