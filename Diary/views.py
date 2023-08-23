from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "Diary/write.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, 'Diary/write.html')


class EmotionsView(APIView):
    def get(self, request):
        return render(request, "Diary/emotions.html")


