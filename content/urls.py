from django.urls import path

from .views import MyDiary, CoupleDiary, Main, Main2, Main3

urlpatterns = [
    path('main/', Main.as_view(), name='main2'),
    path('main2/', Main2.as_view(), name='main2'),
    path('main3/', Main3.as_view(), name='main3'),
    path('mydiary', MyDiary.as_view(), name='mydiary'),
    path('couplediary', CoupleDiary.as_view(), name='couplediary'),
]
