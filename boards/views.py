from django.shortcuts import render, redirect

from .forms import BoardForm
from .models import *

# Create your views here.


def board_main(request):
    meeting_list = Meeting.objects.order_by('created_at')
    meeting_status_list = MeetingStatus.objects.all()
    content = {
        'meeting_list' : meeting_list,
        'meeting_status_list' : meeting_status_list,
        'request': request,
    }
    return render(request, 'boards/board_main.html', content)


def board_write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            print(meeting)
            meeting.user_id = request.user
            meeting.status = MeetingStatus.objects.get(status_number=0)
            meeting.total_amount = 0
            meeting.participant_count = 1
            meeting.save()

            # Meeting 저장 후 Participation 인스턴스 생성
            participation = Participation(meeting=meeting, user=request.user)
            participation.save()

            return redirect('boards:main')
    else:
        form = BoardForm()
    routeInfo = RouteInfo.objects.all()
    return render(request, 'boards/board_write.html',
                  {'form': form, 'routeInfo': routeInfo})