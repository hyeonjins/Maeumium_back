from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView

from content.forms import DiaryForm
from content.models import Content, Diary
from user.models import User


class Main(APIView):
    def get(self, request):
        user = request.user  # 현재 로그인한 사용자
        try:
            content = Content.objects.get(user=user)
        except Content.DoesNotExist:
            content = None

        # 현재 날짜
        current_date = datetime.now().date()

        # 저장된 start_date (예: content.start_date)와의 날짜 차이 계산
        days_passed = (current_date - content.start_date).days + 1
        context = {
            'user': user,
            'content': content,
            'now': now,
            'days_passed': days_passed,
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


class Write(APIView):
    def get(self, request):
        form = DiaryForm()
        context = {'form': form}
        return render(request, 'content/write.html', context)

    def post(self, request):
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user

            if 'thumbnail' in request.FILES:
                uploaded_thumbnail = request.FILES['thumbnail']
                fs = FileSystemStorage()
                uploaded_thumbnail_url = fs.save('thumbnails/' + uploaded_thumbnail.name, uploaded_thumbnail)
                diary.thumbnail = uploaded_thumbnail_url  # 저장할 때 전체 경로가 아닌 파일명만 저장하도록 변경

            diary.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})


class Emotions(APIView):
    def get(self, request):
        return render(request, "content/emotions.html")


# Create your views here.
class MyDiary(APIView):
    def get(self, request):
        diaries = Diary.objects.filter(user=request.user)
        context = {'diaries': diaries}
        return render(request, "content/mydiary.html", context)


class CoupleDiary(APIView):
    def get(self, request):
        if request.user.is_authenticated:  # 로그인한 사용자인지 확인
            user = request.user  # 현재 로그인한 사용자

            # 사용자와 연관된 Content 객체 가져오기
            try:
                content = Content.objects.get(user=user)
                lover_nickname = content.partner_nickname

                # 연인의 다이어리 목록 가져오기
                if lover_nickname:
                    lover_diaries = Diary.objects.filter(user__nickname=lover_nickname)
                else:
                    lover_diaries = []

                context = {
                    'lover_diaries': lover_diaries
                }

                return render(request, "content/couplediary.html", context)
            except Content.DoesNotExist:
                # Content 객체가 없는 경우에 대한 처리
                # 사용자에게 메시지를 보여주거나 다른 처리를 추가하세요.
                pass
        else:
            # 로그인하지 않은 사용자에게 메시지를 보여주거나 로그인 페이지로 리다이렉션하세요.
            return redirect('login')  # login은 실제 로그인 URL에 해당하는 부분으로 변경해야 합니다.
