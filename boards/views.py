from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import BoardForm, CommentForm
from .models import *

# Create your views here.

#게시판 메인
def board_main(request):
    meeting_list = Meeting.objects.order_by('-created_at')
    meeting_status_list = MeetingStatus.objects.all()
    content = {
        'meeting_list': meeting_list,
        'meeting_status_list': meeting_status_list,
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

    from_page = request.GET.get('from')
    if from_page:
        request.session['from_page'] = from_page

    if request.session.get('from_page') == 'my_posts':
        back_url = '/accounts/user-write-board/'
    elif request.session.get('from_page') == 'main_posts':
        back_url = '/boards/'
    else:
        back_url = '/accounts/user-participate-board/'

    context = {
        'meeting': meeting,
        'meeting_status_list': meeting_status_list,
        'participant': participant,
        'request': request,
        'comments': comments,
        'back_url': back_url,
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


# 모임 참여하기
def board_participate(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if meeting.participant_count == 4:
        return redirect(request.META.get('HTTP_REFERER', 'default_route'))
    participation = Participation(meeting=meeting, user=request.user)
    participation.save()

    meeting.participant_count += 1
    meeting.save()
    return redirect(request.META.get('HTTP_REFERER', 'default_route'))


# 모임 참여취소하기
def board_participate_delete(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    Participation.objects.filter(meeting=meeting, user=request.user).delete()
    meeting.participant_count -= 1
    meeting.save()
    return redirect(request.META.get('HTTP_REFERER', 'default_route'))


# 모집 종료하기
def board_gather_done(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.status = MeetingStatus.objects.get(status_number=1)
    meeting.save()
    return redirect(request.META.get('HTTP_REFERER', 'default_route'))


# 정산하기
def board_settle(request, meeting_id):
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, id=meeting_id)
        total_amount = int(request.POST['total_amount'])
        if total_amount <= 0:
            return redirect('boards:detail', meeting_id=meeting.id)
        meeting.status = MeetingStatus.objects.get(status_number=2)
        meeting.total_amount = total_amount
        meeting.save()
        participation = Participation.objects.filter(meeting=meeting)
        # print(meeting.user_id) # 모임 개설자 id
        for participant in participation:
            if meeting.user_id != participant.user:
                print(meeting.user_id, participant.user, 'false!')
                amount = meeting.total_amount // meeting.participant_count
                SettleUp.objects.create(
                    meeting=meeting,
                    user=participant.user,
                    bank=meeting.user_id.bank,
                    account_no=meeting.user_id.account_no,
                    amount=amount
                )
            # print(participant.user_id) # 모임의 모든 참여자 id(반복)
        return redirect('boards:detail', meeting_id=meeting.id)


# 완료하기
def board_meeting_complete(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.status = MeetingStatus.objects.get(status_number=3)
    meeting.save()
    return redirect('boards:detail', meeting_id=meeting.id)