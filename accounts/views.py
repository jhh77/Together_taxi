

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Member
from boards.models import *
from django.shortcuts import render, redirect
from accounts.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage


def index(request): #루트 페이지
    participate_count = 0
    if request.user.is_authenticated:
        # 모임 참여 횟수 구하기(모집 완료된 것만 카운트 + 내가 쓴 글도 카운트)
        meetings = Participation.objects.filter(user=request.user)
        for meeting in meetings:
            meeting_detail = Meeting.objects.get(id=meeting.meeting_id)
            # print(meeting_detail.status.status_number >= 1)
            if meeting_detail.status.status_number >= 1:
                participate_count += 1

        # 모임 개설 횟수 구하기
        open_meeting_list = Meeting.objects.filter(user_id=request.user)
        meeting_open_count = len(open_meeting_list)

        # 정산 내역 가져오기
        now = timezone.now()
        five_days_ago = now - timedelta(days=5) #5일치
        settle_list = SettleUp.objects.filter(user=request.user, created_at__gte=five_days_ago)
        settle_list = settle_list.order_by('-created_at')
        context = {
            'participate_count': participate_count,
            'meeting_open_count': meeting_open_count,
            'settle_list': settle_list,
        }
        return render(request, 'accounts/home.html', context)
    else:
        return render(request, 'accounts/login.html')


# 정산 내역 체크 - DB에 저장
def settle_check(request, settle_id):
    settle = SettleUp.objects.get(id=settle_id)
    if settle.is_check:
        settle.is_check = False
    else:
        settle.is_check = True
    settle.save()
    return redirect('/')


#회원가입
def signUp(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            user_id = form.cleaned_data.get('user_id')
            password = form.cleaned_data.get('password1')
            print(f"user_id: {user_id}, password: {password}")
            user = authenticate(username=user_id, password=password)
            if user is not None:
                # login(request, user)
                return redirect('accounts:signUpComplete')
            else:
                print("Authentication failed")
    else:
        form = SignupForm()
    return render(request, 'accounts/signUp.html', {'form':form})


# 회원 탈퇴
def user_delete(request):
    if request.method == 'POST':
        if 'check' in request.POST:
            print('체크함...')
    return render(request, 'accounts/user_delete.html')


#아이디 중복검사
def check_id(request):
    user_id = request.POST.get('user_id')
    is_taken = Member.objects.filter(user_id=user_id).exists() #아이디값이 존재하는지
    return JsonResponse({'is_taken': is_taken}) #결과 전송(json으로)


# 회원가입 완료 페이지
def signUpComplete(request):
    return render(request, 'accounts/signUpComplete.html')


# 마이페이지
def user_page(request):
    return render(request, 'accounts/myPage.html')


# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# 계좌 변경
def account_change(request):
    user = Member.objects.get(user_id=request.user)
    if request.method == 'POST':
        bank = request.POST['bank']
        account_no = request.POST['account_no']

        # 계좌번호 숫자만 입력했는지 검사
        if not account_no.isdigit():
            error = '계좌는 숫자로만 입력해주세요.'
            return render(request, 'accounts/account_change.html', {'user': user, 'error': error})

        # 계좌번호 중복 검사
        if Member.objects.filter(account_no=account_no).exists():
            error = '이미 등록된 계좌입니다. 다시 입력해 주세요.'
            return render(request, 'accounts/account_change.html', {'user': user, 'error': error})

        # 변경
        user.bank = bank
        user.account_no = account_no
        user.save()
        print("성공!")
        return redirect('accounts:account_change')
    context = {
        'user': user,
    }
    return render(request, 'accounts/account_change.html', context)

# 닉네임 변경
def nickname_change(request):
    user = Member.objects.get(user_id=request.user)
    if request.method == 'POST':
        nickname = request.POST['nickname']
        user.nickname = nickname
        user.save()
        return redirect('accounts:nickname_change')
    return render(request, 'accounts/nickname_change.html', {'user': user})


# 내가 쓴 모임 (모임 작성 아이디가 유저 아이디와 같은 것들)
def user_write_board(request):
    meeting_list = Meeting.objects.filter(user_id=request.user).order_by('-created_at')
    return render(request, 'boards/user_write_board.html',
                  {'meeting_list': meeting_list})


# 내가 참여한 모임
def user_participate_board(request):
    meeting_id_list = Participation.objects.filter(user=request.user).values_list('meeting', flat=True) # 모임 객체 가져오기

    # 해당 모임들 중에서 사용자가 생성자가 아닌 모임만 필터링
    meeting_list = Meeting.objects.filter(id__in=meeting_id_list).exclude(user_id=request.user).order_by('-created_at')

    return render(request, 'boards/user_participate_board.html',
                  {'meeting_list': meeting_list})


# 메일 발송
def send_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_validation = email[email.find('@') + 1:]

        # 학교 이메일인지 검사
        if email_validation != 'student.hywoman.ac.kr':
            error = '학교 이메일 주소를 입력해 주세요.'
            return render(request, 'accounts/send_email.html', {'error': error})

        url = 'http://localhost:8000/accounts/signUp/'
        email_message = EmailMessage(
            '함께나리 회원가입',  # 이메일 제목
            f'<h2>안녕하세요. 함께나리입니다.</h2><p>회원가입을 완료하려면 아래를 클릭해 주세요!</p><a href="{url}">클릭</a>',  # 이메일 본문
            'johh0588@naver.com',  # 발신자 이메일 주소
            [email],  # 수신자 이메일 리스트
            headers={'Reply-To': '함께나리@naver.com'}  # 별칭 이메일 주소로 회신받고 싶을 때
        )
        email_message.content_subtype = 'html'
        email_message.send()
        return redirect('accounts:send_email_done')

    return render(request, 'accounts/send_email.html')


# 메일 발송 완료
def send_email_done(request):
    return render(request, 'accounts/send_mail_complete.html')