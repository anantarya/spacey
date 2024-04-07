from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# Create your models here.

class Employee(AbstractUser):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_groups',  # Use a unique related_name for Employee groups
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    # Specify related_name for user_permissions relationship
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_user_permissions',  # Use a unique related_name for Employee user_permissions
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    def __str__ (self):
        return self.name
    
    
    
class Product(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length = 500)
    quantity = models.CharField(max_length = 10, default=0)
    unit_price = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'Products'

    
    def __str__(self):
        return self.product_name

        
class Customer(models.Model):
    name = models.CharField(max_length = 300)
    email = models.EmailField(max_length = 300)
    number = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100, default='Cash')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.customer} - {self.product}"