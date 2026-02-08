from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import secrets

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, name=name, password=password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=100,blank=False,null=False)
    email=models.EmailField(unique=True,blank=False,null=False)
    password=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=20,blank=False,null=False,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"
    username=None
    objects=UserManager()

    REQUIRED_FIELDS=["name"]

    def set_password(self, raw_password):
        self.password=make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password,self.password)
    
    def generate_password_reset_token(self):
        reset_token = secrets.token_hex(32)  
        self.password_reset_token = reset_token
        self.password_reset_expires = timezone.now() + timezone.timedelta(hours=1)  # Token expires in 1 hour
        self.save()

    def reset_password(self, new_password):
        """Reset the password using a valid reset token and update the password."""
        self.set_password(new_password)
        self.password_reset_token = None  # Clear the reset token
        self.password_reset_expires = None  # Clear the expiration time
        self.save()

    def __str__(self):
        return self.name