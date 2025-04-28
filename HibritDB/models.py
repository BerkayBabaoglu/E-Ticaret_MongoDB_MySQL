from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager): #BaseUserManager -> kullanici olustururken kullanacagin yonetici sinifi.
    def create_user(self, email, username, password=None, role="customer"):
        if not email:
            raise ValueError("Kullanıcı email adresi gereklidir.")
        if not username:
            raise ValueError("Kullanıcı adı gerekli.")
        user = self.model( #construction
            email=self.normalize_email(email), #buyuk harfleri kucuk yapmak icin normalize yaptik.
            username=username,
            role=role
        )
        user.set_password(password) #hashleyip veritabanina gonderiyoruz.
        user.save(using=self._db) #database'e kaydet
        return user

    def create_superuser(self, email, username, password=None): #admin kullanici olusturur.
        return self.create_user(email, username, password, role="admin")
#ozellestirilmis kullanici modeli
class User(AbstractBaseUser): #AbstractBaseUser->kendi kullanici modelini yazmak icin djangonun sundugu temel kullanici sinifi.
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.IntegerField(default=1)
    musteri_mi = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=32, null=True, blank=True)
    reset_password_token_created = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username' #sisteme giris yaparken username kullanilir.
    REQUIRED_FIELDS = ['email'] #superuser olustururken email zorunlu olsun diye.

    objects = UserManager()

    class Meta: #django bu tabloyu olusturmaz ya da migrate etmez, cunku bu tablo zaten hazir bir sekilde veritabanimda var.
        managed = False
        db_table = 'users' #kullanilacak tablo adi

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == "customer":
            self.musteri_mi = 1 #eger rolu customer ise musteri_mi = 1
        else:
            self.musteri_mi = None
        super().save(*args, **kwargs) #veritabanina kaydedilir.
