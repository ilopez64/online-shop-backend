# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    """Helps Django work with out custom user model"""
    def create_user(self,email,first_name,last_name,password=None):
        """Creates a new user object"""
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, first_name, last_name,password):
        """Creates and saves a new superuser with given details"""
        user = self.create_user(email,first_name,last_name,password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self.db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # User inside our system

    #account_id = models.CharField(primary_key=True, max_length=9)
    email = models.EmailField(max_length=255,unique=True) # unique=True
    #password_hash = models.CharField(max_digits=255,  blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        """ Used to get a users full name"""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return self.full_name.strip()

    def get_short_name(self):
        """Used to get a users short name"""
        return self.first_name

    def __str__(self):
        """Django uses this when it needs to convert the obj to a str"""
        return self.email

    class Meta:
        #managed = False
        db_table = 'User'


class Discount(models.Model):
    #discount_id = models.CharField(primary_key=True, max_length=8)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    percent_off = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        #managed = False
        db_table = 'discount'


class Item(models.Model):
    #item_id = models.CharField(primary_key=True, max_length=8)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE,blank=True, null=True)
    item_type = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    item_length = models.CharField(max_length=20)
    year_released = models.IntegerField()
    creator = models.CharField(max_length=60)
    genre = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        #managed = False
        db_table = 'item'


class Purchase(models.Model):
    #invoice_id = models.CharField(primary_key=True, max_length=8)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)

    class Meta:
        #managed = False
        db_table = 'purchase'


class PurchasedItem(models.Model):
    item_id = models.ForeignKey(Item,on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Purchase,on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'purchased_item'
        unique_together = (('item_id', 'invoice_id'),)
