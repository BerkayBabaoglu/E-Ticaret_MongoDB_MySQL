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

from .permissions import IsCustomer, IsSupplier, IsAdmin
from HibritDB.mongodb import get_mongodb_collection
from HibritDB.mongodb_models import Cart, Product
import json
from bson import ObjectId

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
            return redirect('index')
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
    if not request.user.is_authenticated:
        return redirect('customer_login')
    if request.user.role != 'customer':
        messages.error(request, "Bu sayfaya sadece müşteriler erişebilir.")
        return redirect('customer_login')
    
    # MongoDB'den tüm ürünleri çek
    product_model = Product()
    products = product_model.get_all_products()
    
    # MongoDB ObjectId'leri string'e çevir
    for product in products:
        product['id'] = str(product['_id'])
    
    return render(request, 'customer_home.html', {
        'products': products
    })

def supplier_home(request):
    if not request.user.is_authenticated:
        return redirect('supplier_login')
    if request.user.role != 'supplier':
        messages.error(request, "Bu sayfaya sadece tedarikçiler erişebilir.")
        return redirect('supplier_login')
    return render(request, 'supplier_home.html')

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
    if request.user.is_authenticated and request.user.role == 'customer':
        cart = Cart()
        cart_items = cart.get_cart_items(request.user.id)
        total = cart.get_cart_total(request.user.id)
        
        # Debug için cart_items'ı kontrol et
        print("Cart Items:", cart_items)
        print("Total:", total)
        
        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total': total
        })
    return redirect('login')

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

@api_view(['GET'])
@permission_classes([IsCustomer])
def customer_only_view(request):
    return Response({"message": "Bu endpoint'e sadece müşteriler erişebilir."})

@api_view(['GET'])
@permission_classes([IsSupplier])
def supplier_only_view(request):
    return Response({"message": "Bu endpoint'e sadece tedarikçiler erişebilir."})

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_only_view(request):
    return Response({"message": "Bu endpoint'e sadece adminler erişebilir."})

@api_view(['GET'])
@permission_classes([IsCustomer | IsSupplier])
def customer_supplier_view(request):
    return Response({"message": "Bu endpoint'e hem müşteriler hem de tedarikçiler erişebilir."})

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password').strip()

        try:
            user = User.objects.get(username=username)
            if user.role != 'customer':
                messages.error(request, "Bu sayfaya sadece müşteriler giriş yapabilir.")
                return redirect('customer_login')

            if user.check_password(password):
                login(request, user)
                messages.success(request, "Başarıyla giriş yaptınız.")
                return redirect('customer_home')
            else:
                messages.error(request, "Kullanıcı adı veya şifre yanlış.")
        except User.DoesNotExist:
            messages.error(request, "Bu kullanıcı adı ile kayıtlı bir hesap bulunamadı.")

    return render(request, 'customer_login.html')

def supplier_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password').strip()

        try:
            user = User.objects.get(username=username)
            if user.role != 'supplier':
                messages.error(request, "Bu sayfaya sadece tedarikçiler giriş yapabilir.")
                return redirect('supplier_login')

            if user.check_password(password):
                login(request, user)
                messages.success(request, "Başarıyla giriş yaptınız.")
                return redirect('supplier_home')
            else:
                messages.error(request, "Kullanıcı adı veya şifre yanlış.")
        except User.DoesNotExist:
            messages.error(request, "Bu kullanıcı adı ile kayıtlı bir hesap bulunamadı.")

    return render(request, 'supplier_login.html')

def customer_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kayıtlı.')
            return redirect('customer_signup')

        user = User.objects.create_user(email=email, username=username, password=password, role='customer')
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('customer_login')

    return render(request, 'customer_signup.html')

def supplier_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kayıtlı.')
            return redirect('supplier_signup')

        user = User.objects.create_user(email=email, username=username, password=password, role='supplier')
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('supplier_login')

    return render(request, 'supplier_signup.html')

def urun_ekle(request):
    if not request.user.is_authenticated or request.user.role != 'supplier':
        messages.error(request, "Bu sayfaya sadece tedarikçiler erişebilir.")
        return redirect('supplier_login')
    if request.method == 'POST':
        print("POST isteği geldi!")  # DEBUG
        print(request.POST)           # DEBUG
        name = request.POST.get('urun_adi')
        price = request.POST.get('fiyat')
        if not name or not price:
            messages.error(request, "Tüm alanları doldurun.")
            return render(request, 'urun_ekle.html')
        product_data = {
            'name': name,
            'price': float(price),
            'supplier_id': request.user.id
        }
        collection = get_mongodb_collection('products')
        result = collection.insert_one(product_data)
        print("MongoDB Insert Result:", result.inserted_id)  # DEBUG
        messages.success(request, "Ürün başarıyla eklendi!")
        return redirect('supplier_home')
    return render(request, 'urun_ekle.html')

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCustomer])
def add_to_cart(request):
    try:
        data = request.data
        cart = Cart()
        cart.add_to_cart(
            user_id=request.user.id,
            product_id=data['product_id'],
            product_name=data['product_name'],
            price=float(data['price']),
            quantity=data.get('quantity', 1)
        )
        return Response({'message': 'Ürün sepete eklendi'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCustomer])
def get_cart(request):
    try:
        cart = Cart()
        cart_items = cart.get_cart_items(request.user.id)
        total = cart.get_cart_total(request.user.id)
        return Response({
            'items': cart_items,
            'total': total
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsCustomer])
def remove_from_cart(request, product_id):
    try:
        cart = Cart()
        cart.remove_from_cart(request.user.id, product_id)
        return Response({'message': 'Ürün sepetten kaldırıldı'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsCustomer])
def update_cart_item(request, product_id):
    try:
        data = json.loads(request.body)
        cart = Cart()
        cart.update_cart_item_quantity(request.user.id, product_id, data['quantity'])
        return Response({'message': 'Sepet güncellendi'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

Cart().cart_collection.delete_many({"price": {"$type": "string"}})
