from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Member


#관리자 페이지에서 해당 정보 보고 관리하기 위해 추가한 코드
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'nickname', 'bank', 'account_no', 'is_active', 'is_admin'
    ]
