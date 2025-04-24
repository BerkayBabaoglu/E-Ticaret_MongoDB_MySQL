from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), #anasayfa icin index.html yonlendirmesi , http://127.0.0.1:8000/
    path('header.html', views.header, name='header'),
    path('slider.html', views.slider, name='slider'),
    path('content.html', views.content, name='content'),
    path('footer.html', views.footer, name='footer'),
]
