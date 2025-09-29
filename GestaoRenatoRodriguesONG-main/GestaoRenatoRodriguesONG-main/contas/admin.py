from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdminPersonalizado(UserAdmin): # Renomeado
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )

admin.site.register(Usuario, UsuarioAdminPersonalizado) 
