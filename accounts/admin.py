from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'nickname', 'bank', 'account_no', 'is_active', 'is_admin'
    ]
