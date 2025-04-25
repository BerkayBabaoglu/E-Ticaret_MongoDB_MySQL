from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('header.html', views.header),
    path('slider.html', views.slider),
    path('content.html', views.content),
    path('footer.html', views.footer),
    path('clothing/', views.clothing, name='clothing'),
    path('accessories/', views.accessories, name='accessories'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),

    # Ekstra: login ve register aliasları
    path('login/', views.signin, name='login'),
    path('register/', views.signup, name='register'),

    # Django built-in password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
    path('customer-home/', views.customer_home, name='customer_home'),
]
