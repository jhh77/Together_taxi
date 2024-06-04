from django.contrib import admin
from .models import *

# Register your models here.


class MeetingStatusAdmin(admin.ModelAdmin):
    list_display = ['status_number', 'button_text']


class RouteInfoAdmin(admin.ModelAdmin):
    list_display = ['route_id', 'value']


class MeetingAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'meeting_content', 'status', 'route', 'total_amount', 'participant_count', 'created_at']


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'user', 'content']


class SettleUpAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'user', 'amount', 'is_check', 'created_at']


admin.site.register(MeetingStatus, MeetingStatusAdmin)
admin.site.register(RouteInfo, RouteInfoAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SettleUp, SettleUpAdmin)