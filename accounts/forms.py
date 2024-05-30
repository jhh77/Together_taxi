from .models import Member
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField


#유저 생성 폼
class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = ['user_id', 'nickname', 'bank', 'account_no']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 다릅니다. 다시 확인해주세요.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_account_no(self): #계좌번호 방지 함수
        account_no = self.cleaned_data.get('account_no')
        if account_no:
            qs = Member.objects.filter(account_no=account_no)
            if qs.exists():
                raise forms.ValidationError('이미 등록된 계좌입니다. 다시 입력해주세요.')
            return account_no

#유저 수정 폼
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = ['user_id', 'nickname', 'bank', 'account_no']

    def clean_password(self):
        return self.initial["password"]