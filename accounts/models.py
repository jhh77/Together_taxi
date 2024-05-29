from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, user_id, nickname, bank, account_no, password=None):
        if not user_id:
            raise ValueError('아이디는 필수 입력입니다.')

        if not nickname:
            raise ValueError('닉네임은 필수 입력입니다.')

        if not bank:
            raise ValueError('은행명은 필수 입력입니다.')

        if not account_no:
            raise ValueError('계좌번호는 필수 입력입니다.')

        user = self.model(
            user_id=user_id,
            nickname=nickname,
            bank=bank,
            account_no=account_no
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, nickname, bank, account_no, password=None):
        user = self.create_user(
            user_id=user_id,
            nickname=nickname,
            bank=bank,
            account_no=account_no,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    user_id = models.CharField(primary_key=True,max_length=15, null=False, blank=False, unique=True)
    nickname = models.CharField(null=False, max_length=8, blank=False)
    bank = models.CharField(null=False, max_length=20, blank=False)
    account_no = models.CharField(max_length=20, unique=True, blank=False)

    # 추가 필드 정의
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['nickname', 'bank', 'account_no']

    def __str__(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


