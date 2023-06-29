from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    """
        유저 닉네임 -> 화면 표기 이름
        유저 이름 -> 실제 사용자 이름
        유저 이메일 -> 회원가입시 사용하는 아이디
        유저 비밀번호
        유저 폰번호

    """

    username= models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    phone = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    class Meta:
        db_table = "User"