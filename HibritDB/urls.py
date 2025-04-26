from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML sayfaları
    path('', views.index, name='index'),
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

    # Auth işlemleri
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.signin, name='login'),
    path('register/', views.signup, name='register'),
    path('change_password/', views.change_password_html, name='change_password_html'),
    path('customer-home/', views.customer_home, name='customer_home'),

    # API endpoints
    path('api/change-password/', views.change_password, name='change_password_api'),
    path('api/token/', views.obtain_token, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', views.protected_view, name='protected'),

    # Şifre sıfırlama
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
