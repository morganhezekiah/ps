
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self,email, password):
        if not email:
            raise ValueError("Please enter an email")

        if not password:
            raise ValueError("Please enter a password")

        
        email = self.normalize_email(email)
        user = self.model(email=email,password=make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email, password)
        user.is_active=True
        user.is_super=True
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    slug = models.TextField(null=False, blank=False, unique=True)
    is_super = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD="email"
    PASSWORD_FIELD="password"
    REQUIRED_FIELDS = ['password']


    def has_perm(self, obj):
        return True

    def has_module_perms(self, obj):
        return True

    def equals(self,  object):
        return self.id == object.id
    
    object = UserManager()





