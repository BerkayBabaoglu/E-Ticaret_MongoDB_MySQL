from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role="customer"):
        if not email:
            raise ValueError("Kullanıcı email adresi gereklidir.")
        if not username:
            raise ValueError("Kullanıcı adı gerekli.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        return self.create_user(email, username, password, role="admin")

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.IntegerField(default=1)
    musteri_mi = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=32, null=True, blank=True)
    reset_password_token_created = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == "customer":
            self.musteri_mi = 1
        else:
            self.musteri_mi = None
        super().save(*args, **kwargs)
