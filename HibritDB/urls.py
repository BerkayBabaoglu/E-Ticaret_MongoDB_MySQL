from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
#http isteklerini uygun view fonksiyonlarina yonlendiren URL desenlerini icerir.
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
    path('customer/login/', views.customer_login, name='customer_login'),
    path('supplier/login/', views.supplier_login, name='supplier_login'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('supplier/signup/', views.supplier_signup, name='supplier_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password_html, name='change_password_html'),
    path('customer-home/', views.customer_home, name='customer_home'),
    path('supplier-home/', views.supplier_home, name='supplier_home'),

    # API endpoints
    path('api/change-password/', views.change_password, name='change_password_api'),
    path('api/token/', views.obtain_token, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', views.protected_view, name='protected'),
    
    # Rol bazlı endpoint'ler
    path('api/customer-only/', views.customer_only_view, name='customer_only'),
    path('api/supplier-only/', views.supplier_only_view, name='supplier_only'),
    path('api/admin-only/', views.admin_only_view, name='admin_only'),
    path('api/customer-supplier/', views.customer_supplier_view, name='customer_supplier'),

    # Şifre sıfırlama
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('urun-ekle/', views.urun_ekle, name='urun_ekle'),

    # Cart endpoints
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/', views.get_cart, name='get_cart'),
    path('api/cart/remove/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/update/<str:product_id>/', views.update_cart_item, name='update_cart_item'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
]
