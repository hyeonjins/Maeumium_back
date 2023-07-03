from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입
        phone = request.data.get('phone')
        username = request.data.get('username')
        name = request.data.get('name')
        password = request.data.get('password')
        agree = request.data.get('agree') == 'true'
        gender = request.data.get('gender')

        if not agree:
            return Response(status=500, data=dict(message='서비스 이용약관 동의를 하지 않았습니다.'))
        if User.objects.filter(phone=phone).exists():
            return Response(status=500, data=dict(message='해당 핸드폰 번호가 존재합니다.'))
        if User.objects.filter(username=username).exists():
            return Response(status=500, data=dict(message='아이디 "' + username + '"이(가) 존재합니다.'))

        User.objects.create(phone=phone,
                            username=username,
                            name=name,
                            password=make_password(password),
                            agree=agree,
                            gender=gender,
                            )

        return Response(status=200, data=dict(message="회원가입 성공했습니다. 로그인 해주세요."))



class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None:
            return Response(status=500, data=dict(message='아이디를 입력해주세요'))

        if password is None:
            return Response(status=500, data=dict(message='비밀번호를 입력해주세요'))

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        request.session['loginCheck'] = True
        request.session['username'] = user.username


        return Response(status=200, data=dict(message='로그인에 성공했습니다.'))
