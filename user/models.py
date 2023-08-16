from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    """
        유저 아이디 -> 화면 표기 이름
        유저 이름 -> 실제 사용자 이름
        유저 이메일 -> 회원가입시 사용하는 아이디
        유저 비밀번호
        유저 폰번호

    """

    username = None
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True, default="example@example.com")
    nickname = models.CharField(max_length=24, default="default_nickname")

    USERNAME_FIELD = 'id'

    def __str__(self):
        return self.id

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pass

    class Meta:
        db_table = "User"
