from django.urls import path

from .views import MyDiary, CoupleDiary

urlpatterns = [
    path('mydiary', MyDiary.as_view(), name='mydiary'),
    path('couplediary', CoupleDiary.as_view(), name='couplediary'),
]
