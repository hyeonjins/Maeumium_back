# from Diary.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login
# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework import status
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
        #user = authenticate(request, username=id, password=password)

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        request.session['loginCheck'] = True
        request.session['id'] = user.id

        login(request, user)

        return Response(status=200, data=dict(message='로그인에 성공했습니다.'))


class MyPage(APIView):

    def get(self, request):
        return render(request, "user/mypage.html")

    def post(self, request):
        new_password = request.data.get('new_password', None)
        user = request.user

        if not user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        if new_password is None:
            return Response({"message": "새로운 비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 변경 로직
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)


class MyPage2(APIView):
    def get(self, request):
        return render(request, "user/mypage2.html")

    def post(self, request):
        return render(request, "user/mypage2.html")


class MyPageMain(APIView):
    def get(self, request):
        return render(request, "user/mypageMain.html")

    def post(self, request):
        nickname = request.user.nickname  # 로그인한 사용자의 닉네임
        current_password = request.data.get('password', None)  # 현재 비밀번호 입력값

        if current_password is None:
            return Response({"message": "현재 비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(nickname=nickname).first()

        if user is None:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 입력한 비밀번호와 저장된 비밀번호 일치 여부 확인
        if not check_password(current_password, user.password):
            return Response({"message": "닉네임 또는 비밀번호가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 닉네임과 비밀번호가 일치하는 경우 성공 응답 반환
        return Response({"success": True}, status=status.HTTP_200_OK)


class UnRegister(APIView):
    def get(self, request):
        return render(request, "user/unregister.html")

    def post(self, request):
        return render(request, "user/unregister.html")
