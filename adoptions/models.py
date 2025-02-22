from django.db import models
from django.utils.translation import gettext as _


class Species(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'species'
        ordering = ['-id']
        verbose_name = _('Species')
        verbose_name_plural = _('Species')   


class Pet(models.Model):
    STATUS_CHOICES = (
        ('A', _('Available')),
        ('T', _('Tramit')),
        ('C', _('Chosen')),
    )
    
    name = models.CharField(max_length=200)
    species = models.ForeignKey('adoptions.Species', on_delete=models.RESTRICT)
    race = models.CharField(max_length=200) 
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'pets'
        ordering = ['-id']
        verbose_name = _('Pet')
        verbose_name_plural = _('Pets') 
        

class Adoption(models.Model):
    STATUS_CHOICES = (
        ('P', _('Pending')),
        ('A', _('Approved')),
        ('R', _('Refused'))
    )
    
    pet = models.ForeignKey('adoptions.Pet', on_delete=models.RESTRICT)
    customer = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    solicitation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f'{self.pet} - {self.customer} - {self.status}'

    class Meta:
        db_table = 'adoptions'
        ordering = ['-id']
        verbose_name = _('Adoption')
        verbose_name_plural = _('Adoptions') 
