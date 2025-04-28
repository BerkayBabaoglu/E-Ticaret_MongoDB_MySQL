from django.contrib import admin
from .models import User

@admin.register(User) #user modelini admin panelinde gorunur hale getirir ve asagidaki sinifi yonet
class UserAdmin(admin.ModelAdmin): #User modelinin admin panelinde nasil gorunecegini ve nasil yonetilecegini burada belirleriz
    list_display = ('email', 'role', 'is_active')
    list_filter = ('role',)
    search_fields = ('email',)