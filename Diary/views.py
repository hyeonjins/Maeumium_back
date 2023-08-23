from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        return render(request, "Diary/write.html")

    def post(self, request):
        return render(request, 'Diary/write.html')


class EmotionsView(APIView):
    def get(self, request):
        return render(request, "Diary/emotions.html")

"""
class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = "login"  # 로그인 페이지 URL 설정
    redirect_field_name = 'next'  # 리다이렉트할 URL 파라미터 이름 설정


class Main(APIView):

    def get(self, request):
        nickname = request.GET.get('user.nickname')  # 쿼리 매개변수로부터 nickname 값 받아오기
        context = {'user': request.user, 'nickname': nickname}
        return render(request, "Diary/main.html", context)

    def post(self, request):
        return render(request, 'Diary/main.html')


"""
