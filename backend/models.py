from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
import jwt
from datetime import date, datetime, timedelta
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import date


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth=None, password=None):
       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, date_of_birth=None, password=None):
  
        user = self.create_user(
            email,
            username = username,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user






class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
       
        return True



    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        
        return self.is_admin

class User(AbstractUser):
    phone = models.IntegerField(blank=True, null=True)
    is_branch = models.BooleanField(default=True)
    is_delivery = models.BooleanField(default=True)
    is_phone_status = models.BooleanField(default=False)
    date_of_birth = models.CharField(blank=True,null=True,max_length=200)
    is_admin = models.CharField(blank=True,null=True,max_length=200)

class Profile(models.Model):
    data = models.TextField(blank=True,null=True)
    link = models.TextField(blank=True,null=True)
    image = models.ImageField(default='Screenshot_5.png',blank=True, null=True)
    phone = models.IntegerField(blank=True,null=True)
    first_name = models.CharField(blank=True,null=True,max_length=200)
    last_name =  models.CharField(blank=True,null=True,max_length=200)
    username = models.CharField(blank=True,null=True,max_length=200)
    email = models.TextField(blank=True,null=True)






class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address_name = models.CharField(max_length=40)
    home = models.CharField(max_length=10)
    city = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class UserOtp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_otp')
    otp = models.CharField(max_length=6)
    rpt = models.IntegerField(default=3)
    date = models.DateTimeField(auto_now=True)


class UserVerify(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    token = models.CharField(max_length=400,blank=True,null=True)
    status = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return self.token

    def save(self,*args, **kwargs):
        self.token = ''
        if not self.token:
            self.token = self._create_verify_token()
        super().save(*args, **kwargs)

    def _create_verify_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            "id": self.id,
            "exp": int(dt.timestamp())
        },settings.SECRET_KEY,algorithm='HS256')
        return token