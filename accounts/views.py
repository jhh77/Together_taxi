from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Member


def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


def sign_up(request):
    return render(request, 'accounts/signUp.html')


def login(request):
    return render(request, 'accounts/login.html')


def check_id(request):
    user_id = request.POST.get('user_id')
    is_taken = Member.objects.filter(user_id=user_id).exists() #아이디값이 존재하는지
    return JsonResponse({'is_taken': is_taken}) #결과 전송(json으로)