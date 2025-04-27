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
    ROLE_CHOICES = (
        ('customer', 'Müşteri'),
        ('supplier', 'Tedarikçi'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    musteri_mi = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.role == "customer":
            self.musteri_mi = True
        else:
            self.musteri_mi = False
        super().save(*args, **kwargs)
