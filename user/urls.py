from django.urls import path

from .views import Join, Login, CheckDuplicate

urlpatterns = [
    path('join', Join.as_view(), name='join'),
    path('check_duplicate', CheckDuplicate.as_view(), name='check_duplicate'),
    path('login', Login.as_view(), name='login'),

]
