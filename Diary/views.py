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


class Main(APIView):

    def get(self, request):
        context = {'user': request.user}
        return render(request, "Diary/main.html", context)

    def post(self, request):
        return render(request, 'Diary/main.html')


class Main2(APIView):
    def get(self, request):
        return render(request, "Diary/main2.html")

    def post(self, request):
        return render(request, 'Diary/main2.html')


class Main3(APIView):
    def get(self, request):
        return render(request, "Diary/main3.html")

    def post(self, request):
        return render(request, 'Diary/main3.html')
