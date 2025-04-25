from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from .models import User  # MySQL'deki tabloya bağladığın model

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

        # Rolü sabit olarak 'customer' atıyoruz
        user = User.objects.create_user(email=email, username=username, password=password, role='customer')
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('signin')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'supplier':
                return redirect('supplier_dashboard')
            else:
                return redirect('customer_home')
        else:
            messages.error(request, 'Giriş başarısız. Bilgileri kontrol edin.')
            return redirect('signin')
    return render(request, 'index.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('signin')
