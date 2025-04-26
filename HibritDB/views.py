from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import TokenSerializer, ChangePasswordSerializer

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kayıtlı.')
            return redirect('signup')

        user = User.objects.create_user(email=email, username=username, password=password, role='customer')
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password').strip()  # Şifreyi temizle (başında/sonunda boşluk varsa)

        try:
            user = User.objects.get(username=username)
            print(f"Kullanıcı bulundu: {user.username}")
            print(f"Kullanıcı email: {user.email}")
            print(f"Kullanıcı rolü: {user.role}")
            print(f"Kullanıcı aktif mi: {user.is_active}")
        except User.DoesNotExist:
            messages.error(request, "Bu kullanıcı adı ile kayıtlı bir hesap bulunamadı.")
            return redirect('signin')

        # Debugging: Şifre kontrolü
        print(f"Girilen şifre: {password}")
        print(f"Veritabanındaki hash'lenmiş şifre: {user.password}")
        is_correct = check_password(password, user.password)
        print(f"Şifre doğru mu: {is_correct}")

        if is_correct:
            login(request, user)
            messages.success(request, "Başarıyla giriş yaptınız.")
            return redirect('customer_home')
        else:
            messages.error(request, "Kullanıcı adı veya şifre yanlış.")
            return redirect('signin')

    return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('index')

def change_password_html(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirildi!')
            return redirect('customer_home')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        # Eski şifreyi kontrol et
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": ["Eski şifre yanlış."]}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Yeni şifreyi ayarla
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        # Oturumu güncelle
        update_session_auth_hash(request, request.user)
        
        return Response(
            {"message": "Şifre başarıyla değiştirildi."},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def customer_home(request):
    return render(request, 'customer_home.html')

@api_view(['POST'])
def protected_view(request):
    return Response({"message": "Bu endpoint'e JWT ile erişildi!"})

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

@api_view(['POST'])
def obtain_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
