

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Member
from django.shortcuts import render, redirect
from accounts.forms import SignupForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

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