# from Diary.settings import MEDIA_ROOT


# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        id = request.data.get('id')
        nickname = request.data.get('nickname')
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        date = request.data.get('date')

        user = User.objects.create(
            name=name,
            email=email,
            id=id,
            password=make_password(password),
            nickname=nickname,
            date=date,
        )
        # You can also add extra fields like gender to the user instance

        return Response(status=200, data=dict(message="회원가입 성공했습니다. 로그인 해주세요."))


class CheckDuplicate(APIView):
    def get(self, request):
        nickname = request.query_params.get('nickname', None)
        id = request.query_params.get('id', None)

        response_data = {}

        if nickname:
            if User.objects.filter(nickname=nickname).exists():
                return Response(status=400, data=dict(message='이미 사용 중인 닉네임입니다.'))
            return Response(status=200, data=dict(message='사용 가능한 닉네임입니다.'))
        if id:
            if User.objects.filter(id=id).exists():
                return Response(status=400, data=dict(message='이미 사용 중인 아이디입니다.'))
            return Response(status=200, data=dict(message='사용 가능한 아이디입니다.'))


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        id = request.data.get('id', None)
        password = request.data.get('password', None)

        if id is None:
            return Response(status=500, data=dict(message='아이디를 입력해주세요'))

        if password is None:
            return Response(status=500, data=dict(message='비밀번호를 입력해주세요'))

        user = User.objects.filter(id=id).first()

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        request.session['loginCheck'] = True
        request.session['id'] = user.id

        return Response(status=200, data=dict(message='로그인에 성공했습니다.'))
