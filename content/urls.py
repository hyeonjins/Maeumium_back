from django.urls import path
from . import views

urlpatterns = [
    # 기존 URL 패턴들...
    path('mydiary/', MyDiaryView.as_view()),
    path('couplediary/', CoupleDiaryView.as_view()),
]
