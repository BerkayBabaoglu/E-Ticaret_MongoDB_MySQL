from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'home'), #anasayfa icin index.html yonlendirmesi , http://127.0.0.1:8000/
    path('header.html', views.header),
    path('slider.html', views.slider),
    path('content.html', views.content),
    path('footer.html', views.footer),
    path('clothing/',views.clothing, name = 'clothing'),
    path('accessories/',views.accessories, name = 'accessories'),
    path('cart/',views.cart, name = 'cart'),
    path('about/',views.about, name = 'about'),
    path('contact/', views.contact, name='contact'),
]
