from django.urls import path

from .views import Join, Login, CheckDuplicate, MyPage, MyPage2, MyPageMain, UnRegister

urlpatterns = [
    path('join', Join.as_view(), name='join'),
    path('check_duplicate', CheckDuplicate.as_view(), name='check_duplicate'),
    path('login', Login.as_view(), name='login'),
    path('mypage', MyPage.as_view(), name='mypage'),
    path('mypage2', MyPage2.as_view(), name='mypage2'),
    path('mypageMain', MyPageMain.as_view(), name='mypageMain'),
    path('unregister', UnRegister.as_view(), name='unregister'),

]
