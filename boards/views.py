from django.shortcuts import render, redirect, get_object_or_404

from .forms import BoardForm, CommentForm
from .models import *

# Create your views here.

#게시판 메인
def board_main(request):
    meeting_list = Meeting.objects.order_by('created_at')
    meeting_status_list = MeetingStatus.objects.all()
    content = {
        'meeting_list' : meeting_list,
        'meeting_status_list' : meeting_status_list,
        'request': request,
    }
    return render(request, 'boards/board_main.html', content)


#게시판 글쓰기
def board_write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
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


#게시글 상세보기 & 댓글 쓰기
#댓글 쓰기 추가하기 전 코드
# def board_detail(request, meeting_id):
#     meeting = Meeting.objects.get(id=meeting_id)
#     participant = Participation.objects.filter(meeting=meeting_id)
#     meeting_status_list = MeetingStatus.objects.all()
#     context = {
#         'meeting': meeting,
#         'meeting_status_list': meeting_status_list,
#         'participant': participant,
#         'request' : request,
#     }
#     return render(request, 'boards/board_detail.html', context)

def board_detail(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.meeting = meeting
            comment.user = request.user
            comment.save()
            return redirect('boards:detail', meeting_id=meeting_id)
    else:
        form = CommentForm()
    participant = Participation.objects.filter(meeting=meeting_id)
    meeting_status_list = MeetingStatus.objects.all()
    comments = meeting.comments.all()
    context = {
        'meeting': meeting,
        'meeting_status_list': meeting_status_list,
        'participant': participant,
        'request' : request,
        'comments': comments,
    }
    return render(request, 'boards/board_detail.html', context)


# 게시글 수정하기
def board_edit(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id) # 해당 모임 데이터 가져오기
    routeInfo = RouteInfo.objects.all() # 경로 정보 데이터 가져오기

    if request.method == 'POST': # POST로 접근 시(=폼 제출 시)
        route_id = request.POST.get('route')  # 사용자가 선택한 경로의 ID 가져오기
        route_instance = get_object_or_404(RouteInfo, route_id=route_id)  # 해당 ID에 맞는 RouteInfo 인스턴스 가져오기
        meeting.route = route_instance # 값 변경
        meeting.meeting_content = request.POST['meeting_content'] # 값 변경
        meeting.save()
        return redirect('boards:detail', meeting_id=meeting_id)
    else:
        form = BoardForm()
        return render(request, 'boards/board_edit.html',
                      {'meeting': meeting, 'routeInfo': routeInfo})


# 게시글 삭제하기
def board_delete(request, meeting_id):
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, id=meeting_id)
        meeting.delete()
        return redirect('boards:main')
    else:
        return render(request, 'boards/board_main.html')


# 댓글 삭제하기
def comment_delete(request, meeting_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return redirect('boards:detail', meeting_id=meeting_id)
