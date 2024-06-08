

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



def index(request): #루트 페이지
    participate_count = 0
    if request.user.is_authenticated:
        # 모임 참여 횟수 구하기
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
        five_days_ago = now - timedelta(days=5)
        settle_list = SettleUp.objects.filter(user=request.user, created_at__gte=five_days_ago)
        context = {
            'participate_count': participate_count,
            'meeting_open_count': meeting_open_count,
            'settle_list': settle_list,
        }
        return render(request, 'accounts/home.html', context)
    else:
        return render(request, 'accounts/login.html')


# 정산 내역 체크
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
            # nickname = form.cleaned_data.get('nickname')
            # bank = form.cleaned_data.get('bank')
            # account_no = form.cleaned_data.get('account_no')
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


def check_id(request): #아이디 중복검사
    user_id = request.POST.get('user_id')
    is_taken = Member.objects.filter(user_id=user_id).exists() #아이디값이 존재하는지
    return JsonResponse({'is_taken': is_taken}) #결과 전송(json으로)

#회원가입 완료 페이지로 이동?
def signUpComplete(request):
    return render(request, 'accounts/signUpComplete.html')


#마이페이지
def user_page(request):
    return render(request, 'accounts/myPage.html')


#로그아웃
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# 계좌 변경
def account_change(request):
    user = Member.objects.get(user_id=request.user)
    if request.method == 'POST':
        bank = request.POST['bank']
        account_no = request.POST['account_no']
        if not account_no.isdigit():
            error = '계좌번호는 숫자로만 입력해주세요.'
            return render(request, 'accounts/account_change.html', {'error': error})
    context = {
        'user': user,
    }
    return render(request, 'accounts/account_change.html', context)