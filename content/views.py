from django.shortcuts import render
from rest_framework.views import APIView


def MyDiaryView(APIView):
    return render(request, 'content/mydiary.html')


def CoupleDiaryView(APIView):
    return render(request, 'content/couplediary.html')
