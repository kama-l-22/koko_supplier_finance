from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
user_tags = (("Client","Client"),("Supplier","Supplier"),("Bank","Bank"))
c_st = (("GOOD","GOOD"),("BAD",'BAD'))
gen = (("MALE","MALE"),("FEMALE","FEMALE"),("OTHERS",'OTHERS'))
class Kouser(AbstractUser):
    Phone = models.BigIntegerField(null=True,blank=True)
    Is_bank = models.BooleanField(default=False)
    Is_client = models.BooleanField(default=False)
    Is_supplier = models.BooleanField(default=False)
    DoB = models.DateField(null=True,blank=True)
    Gender = models.CharField(choices=gen,max_length=50,null=True,blank=True)


class Kosupplier(models.Model):
    Username = models.OneToOneField(Kouser,on_delete=models.CASCADE)
    User_type = models.CharField(max_length=20,choices=user_tags,default='Supplier')
    Address = models.CharField(max_length=100)
    Supplier_id = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.Supplier_id

class Koclient(models.Model):
    Username = models.OneToOneField(Kouser,on_delete=models.CASCADE)
    User_type = models.CharField(max_length=20,choices=user_tags,default='Client')
    Address = models.CharField(max_length=100)
    Client_id = models.CharField(max_length=10)
    Client_Status = models.CharField(max_length=10,choices=c_st)  

    def __str__(self) -> str:
        return self.Client_id

class Requested_Invoice(models.Model):
    defa = models.CharField(max_length=5,default='defa')
    Requested_by = models.CharField(max_length=50)
    Supplier_code = models.CharField(max_length=10)
    Invoice_number = models.CharField(max_length=100)
    Invoice_date = models.DateField(default=timezone.now)
    Invoice_amount = models.CharField(max_length=100,null=True,blank=True)
    Currency = models.CharField(max_length=50,default='INR')


class Verified_Invoice(models.Model):
    Verified_by = models.CharField(max_length=50)
    Requested_by = models.CharField(max_length=50)
    Supplier_code = models.CharField(max_length=10)
    Invoice_number = models.CharField(max_length=100)
    Invoice_date = models.DateField(default=timezone.now)
    Invoice_amount = models.CharField(max_length=100,null=True,blank=True)
    Currency = models.CharField(max_length=50,default='INR')

        
class Approved_Invoice(models.Model):
    Requested_by = models.CharField(max_length=100)
    Supplier_code = models.CharField(max_length=10)
    Invoice_number = models.CharField(max_length=100)
    Invoice_date = models.DateField(default=timezone.now)
    Invoice_amount = models.CharField(max_length=100,null=True,blank=True)
    Currency = models.CharField(max_length=50,default='INR')
    Approved_by = models.CharField(max_length=100)
   


class Denied(models.Model):
       Invoice_number = models.CharField(max_length=100)
       Denied_by = models.CharField(max_length=100)