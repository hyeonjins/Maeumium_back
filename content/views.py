from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


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
