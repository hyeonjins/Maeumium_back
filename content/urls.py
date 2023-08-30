from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import MyDiary, CoupleDiary, Main, Main2, Main3, Write, Emotions

urlpatterns = [
    path('main/', Main.as_view(), name='main'),
    path('main2/', Main2.as_view(), name='main2'),
    path('main3/', Main3.as_view(), name='main3'),
    path('write/', Write.as_view(), name='write'),
    path('emotions/', Emotions.as_view(), name='emotions'),
    path('mydiary', MyDiary.as_view(), name='mydiary'),
    path('couplediary', CoupleDiary.as_view(), name='couplediary'),
]
