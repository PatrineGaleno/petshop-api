from django.db import models
from django.utils.translation import gettext as _


class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'categories'
        ordering = ['-id']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories') 


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    current_quantity = models.IntegerField(default=0)
    category = models.ForeignKey('sales.Category', on_delete=models.RESTRICT)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'products'
        ordering = ['-id']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')   


class Sale(models.Model):
    PAYMENT_FORM_CHOICES = (
        ('P', _('PIX')),
        ('C', _('Card'))
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('P', _('Pending')),
        ('C', _('Confirmed')),
    )
    
    customer = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    product = models.ForeignKey('sales.Product', on_delete=models.RESTRICT)
    bought_quantity = models.IntegerField()
    payment_form = models.CharField(max_length=1, choices=PAYMENT_FORM_CHOICES)
    price_on_sale = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.customer} - {self.product} - {self.bought_quantity}'
    
    class Meta:
        db_table = 'sales'
        ordering = ['-id']
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')   
