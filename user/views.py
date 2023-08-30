# from Diary.settings import MEDIA_ROOT
from django.contrib.auth import login, logout
# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Content
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

        # Check if password meets the requirements
        if len(password) < 6 or not any(char.isdigit() for char in password) or not any(
                char.isalpha() for char in password):
            return Response(status=400, data=dict(message="비밀번호는 영어와 숫자 조합으로 6자 이상이어야 합니다."))

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
        user = request.user
        try:
            content = Content.objects.get(user=user)
        except Content.DoesNotExist:
            content = None

        context = {
            'user': user,
            'content': content,
        }

        user = User.objects.filter(id=id).first()
        # user = authenticate(request, username=id, password=password)

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        request.session['loginCheck'] = True
        request.session['id'] = user.id

        login(request, user)
        # Check if user and partner's nickname both exist in content
        content_exists = Content.objects.filter(user=user).exists()

        if content_exists:
            return Response(status=200, data=dict(message='로그인에 성공했습니다.', redirect_to_main=True))
        else:
            return Response(status=200, data=dict(message='로그인에 성공했습니다.', redirect_to_main=False))


class MyPage(APIView):

    def get(self, request):
        return render(request, "user/mypage.html")

    def post(self, request):
        new_password = request.data.get('new_password', None)
        user = request.user
        request.session['password'] = user.password

        if not user.is_authenticated:
            return Response(data=dict(message="로그인이 필요합니다."), status=status.HTTP_401_UNAUTHORIZED)

        if new_password is None:
            return Response(data=dict(message="새로운 비밀번호를 입력해주세요."), status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 6 or not any(char.isdigit() for char in new_password) or not any(
                char.isalpha() for char in new_password):
            return Response(status=400, data=dict(message="비밀번호는 영어와 숫자 조합으로 6자 이상이어야 합니다."))

        # 비밀번호 변경 로직
        user.password = make_password(new_password)
        user.save()
        # 비밀번호가 변경되었으므로 로그아웃 처리 후 로그인 페이지로 리다이렉션
        logout(request)  # Django의 logout 함수를 사용하여 로그아웃 처리

        return Response(data=dict(message="비밀번호가 성공적으로 변경되었습니다."), status=status.HTTP_200_OK)


class ConnectPartner(APIView):
    def post(self, request):
        user = request.user
        try:
            content = Content.objects.get(user=user)
        except Content.DoesNotExist:
            content = None

        if not user.is_authenticated:
            return Response(data=dict(message="로그인이 필요합니다."), status=401)

        new_start_date = request.data.get('new_start_date', None)
        input_partner_nickname = request.data.get('input_partner_nickname', None)

        if new_start_date is None or input_partner_nickname is None:
            return Response(data=dict(message="날짜와 상대방 닉네임을 모두 입력하세요."), status=400)

        # 세션에 partner_nickname과 start_date 저장
        request.session['partner_nickname'] = content.partner_nickname
        request.session['start_date'] = str(content.start_date)  # date 객체를 문자열로 변환

        # DB에서 읽어온 partner_nickname와 입력한 닉네임 비교
        if content.partner_nickname != input_partner_nickname:
            return Response(data=dict(message="상대방의 닉네임이 일치하지 않습니다."), status=400)

        content.start_date = new_start_date
        content.save()

        return Response(data=dict(message="연인 연결 시작일이 변경되었습니다."), status=200)


class CoupleEnd(LoginRequiredMixin, APIView):
    def get(self, request):
        return render(request, "user/unregister.html")

    def post(self, request):
        # 사용자 정보 초기화 또는 삭제 작업 수행
        user = request.user
        try:
            content = Content.objects.get(user=user)
        except Content.DoesNotExist:
            content = None

        # 사용자의 데이터 삭제 또는 초기화 작업 수행
        content.delete()  # 또는 원하는 로직에 맞게 사용자 데이터 삭제
        return redirect('main2')  # main3에 해당하는 URL 패턴 이름으로 변경


class MyPage2(APIView):
    def get(self, request):
        return render(request, "user/mypage2.html")

    def post(self, request):
        return render(request, "user/mypage2.html")


class MyPageMain(APIView):

    def get(self, request):
        return render(request, "user/mypageMain.html")

    def post(self, request):
        current_password = request.data.get('current_password', None)
        user = request.user

        if current_password is None:
            return Response(data=dict(message="현재 비밀번호를 입력해주세요."), status=status.HTTP_400_BAD_REQUEST)

        if current_password.strip() == "":
            return Response(data=dict(message="현재 비밀번호를 입력해주세요."), status=status.HTTP_400_BAD_REQUEST)

        if not check_password(current_password, user.password):
            return Response(data=dict(message="비밀번호가 일치하지 않습니다."), status=status.HTTP_400_BAD_REQUEST)

        request.session['password'] = user.password

        return Response(data=dict(message="비밀번호가 확인되었습니다."), status=status.HTTP_200_OK)


class UnRegister(LoginRequiredMixin, APIView):
    def get(self, request):
        return render(request, "user/unregister.html")

    def post(self, request):
        # 사용자 정보 초기화 또는 삭제 작업 수행
        user = request.user

        # 사용자의 데이터 삭제 또는 초기화 작업 수행
        user.delete()  # 또는 원하는 로직에 맞게 사용자 데이터 삭제

        # 로그아웃 처리
        logout(request)

        # main3 페이지로 리다이렉트
        return redirect('main3')  # main3에 해당하는 URL 패턴 이름으로 변경
