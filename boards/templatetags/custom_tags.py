from django import template
from boards.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def button_text(context, meeting_id):
    request = context['request']
    user = request.user
    # 현재 로그인된 사용자가 해당 meeting_id에 대한 Participation 객체에 속해 있는지 확인
    is_participant = Participation.objects.filter(meeting=meeting_id, user=user).exists()
    return is_participant

