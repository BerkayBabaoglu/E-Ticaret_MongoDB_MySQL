from pathlib import Path #dosya ve klasor yollarini kolay yonetmek icin
import os #os ile klasor yollarini yonetmek icin, isletim sistemi fonksiyonlarini yonetmek icin
import pymysql #MySQL veritabani

BASE_DIR = Path(__file__).resolve().parent.parent #projenin ana dizinini (manage.py oldugu yeri) belirler.

SECRET_KEY = 'django-insecure-i@f7rfy^!(*g18%^ab%z7b-ymebk(ph5u^-$i8x(3!crteje*&' #Django'nun guvenlik anahatari

DEBUG = True

ALLOWED_HOSTS = []


# Application definition (
INSTALLED_APPS = [ #djangonun yuklu uygulamalari
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HibritDB',
    'rest_framework', #api gelistirmek icin
    'rest_framework_simplejwt', #token bazli (JWT) kimlij dogrulama icin
]

REST_FRAMEWORK = { #apilerde kullanici dogrulamada session ve JWT token sistemini kullanir.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [ #istek ve cevaplar arasındaki isleyen katmanlar
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HibritDB.urls' #ana url ayarlarinin bulundugu dosya

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], #templates klasorunu gormesi icin
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'HibritDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

pymysql.install_as_MySQLdb()

DATABASES = { #mysql database bilgileri
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# MongoDB ayarlari
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DB = 'hibritdb_mongodb'

AUTH_USER_MODEL = 'HibritDB.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#eposta ayarlari (smtp(gmail)) uzerinden epost agonderiyor
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#statik dosyalar (css,js) icin yol ayarlari
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), #static klasoru online

]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
