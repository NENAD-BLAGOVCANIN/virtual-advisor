from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_staff = True
        user.is_superuser = True
        return user

class User(AbstractBaseUser):

    ADMIN_ROLE = "admin"
    CUSTOMER_ROLE = 'customer'

    APPLICATION_ACCESS_STATUS_PENDING = 'pending'
    APPLICATION_ACCESS_STATUS_ALLOWED = 'allowed'
    APPLICATION_ACCESS_STATUS_DECLINED = 'declined'

    email = models.EmailField(max_length=60, unique=True, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, null=True)
    application_access = models.CharField(max_length=50, default=APPLICATION_ACCESS_STATUS_PENDING)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "user"


class Translation(BaseModel):

    phrase = models.CharField(max_length=2900)
    language = models.CharField(max_length=20, default="ba")
    translation = models.CharField(max_length=2900)

    REQUIRED_FIELDS = [phrase, translation]


    def __str__(self):
        return self.translation
    
    class Meta:
        db_table = "translation"