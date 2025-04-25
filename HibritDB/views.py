from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from .models import User  # MySQL'deki tabloya bağladığın model

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    return render(request, 'index.html')

def header(request):
    return render(request, 'header.html')

def slider(request):
    return render(request, 'slider.html')

def content(request):
    return render(request, 'content.html')

def footer(request):
    return render(request, 'footer.html')

def clothing(request):
    return render(request, 'clothing.html')

def accessories(request):
    return render(request, 'accessories.html')

def cart(request):
    return render(request, 'cart.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kayıtlı.')
            return redirect('signup')

        # Şifreyi düz metin olarak kaydediyoruz
        user = User.objects.create_user(email=email, username=username, password=password, role='customer')
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Bu username ile kayıtlı bir hesap bulunamadı.")
            return redirect('signin')

        # Düz metin şifre karşılaştırması yapıyoruz
        if password == user.password:  # Şifreyi düz metin olarak karşılaştırıyoruz
            login(request, user)
            messages.success(request, "Başarıyla giriş yaptınız.")
            return redirect('customer_home')  # Başarıyla giriş yaptıktan sonra index sayfasına yönlendir
        else:
            messages.error(request, "E-posta veya şifre yanlış.")
            return redirect('signin')

    return render(request, 'signin.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('index')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Kullanıcının oturumunu güncelle
            return redirect('customer_home')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

def customer_home(request):
    # your view logic here
    return render(request, 'customer_home.html')