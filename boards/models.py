from django.db import models
from django.conf import settings
# Create your models here.


# 모임 상태 정보 테이블
class MeetingStatus(models.Model):
    status_number = models.IntegerField(primary_key=True, null=False)
    button_text = models.CharField(max_length=10)

    def __str__(self):
        return self.button_text


# 모임 경로 정보 테이블
class RouteInfo(models.Model):
    route_id = models.IntegerField(primary_key=True, null=False)
    value = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.value


# 모임 테이블
class Meeting(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_meetings')
    meeting_content = models.TextField(null=False, blank=False)
    status = models.ForeignKey(MeetingStatus, on_delete=models.CASCADE)
    route = models.ForeignKey(RouteInfo, on_delete=models.CASCADE, null=False, blank=False)
    total_amount = models.IntegerField(null=False, default=0)
    participant_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


#모임 참여 테이블
class Participation(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='group')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


#댓글 테이블
class Comment(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)


#모임 정산 테이블
class SettleUp(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='settle')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    is_check = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


