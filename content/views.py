from datetime import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Content
from user.models import User


class Main(APIView):
    def get(self, request):
        user = request.user  # 현재 로그인한 사용자
        try:
            content = Content.objects.get(user=user)
        except Content.DoesNotExist:
            content = None
        now = datetime.now()

        context = {
            'user': user,
            'content': content,
            'now': now,
        }

        return render(request, "content/main.html", context)

    def post(self, request):
        return render(request, 'content/main.html')


class Main2(APIView):
    def get(self, request):
        return render(request, "content/main2.html")

    def post(self, request):
        nickname = request.POST.get('nickname')
        date = request.POST.get('date')
        user = request.user  # 로그인한 사용자

        if not user.is_authenticated:
            return Response(status=200, data=dict(message="로그인이 필요합니다."))

        if not nickname or not date:
            return Response(status=400, data=dict(message="닉네임과 날짜를 모두 입력하세요."))

        # Check if user already submitted
        existing_content = Content.objects.filter(user=user)
        if existing_content.exists():
            return Response(status=400, data=dict(message="이미 제출한 사용자입니다."))

        # Get partner's nickname from user table
        try:
            partner_user = User.objects.exclude(id=user.id).get(nickname=nickname)
        except User.DoesNotExist:
            return Response(status=400, data=dict(message="존재하지 않는 닉네임입니다."))

        # Content 모델에 데이터 저장
        content = Content.objects.create(
            user=user,
            partner_nickname=partner_user.nickname,
            start_date=date
        )

        return Response(status=200, data=dict(message="데이터가 성공적으로 저장되었습니다."))


class Main3(APIView):
    def get(self, request):
        return render(request, "content/main3.html")

    def post(self, request):
        return render(request, 'content/main3.html')


# Create your views here.
class MyDiary(APIView):
    def get(self, request):
        return render(request, "content/mydiary.html")

    def post(self, request):
        return render(request, "content/mydiary.html")


class CoupleDiary(APIView):
    def get(self, request):
        return render(request, "content/couplediary.html")

    def post(self, request):
        return render(request, "content/couplediary.html")
