from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.models import make_password

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입
        phone = request.data.get('phone', None)
        username = request.data.get('username', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(phone=phone,
                            username=username,
                            name=name,
                            password=make_password(password),
                            )

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['username'] = username
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))