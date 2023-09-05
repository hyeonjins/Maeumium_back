import base64
import os
import re
from collections import Counter
from datetime import datetime

import numpy as np
from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from gensim.summarization import summarize
from konlpy.tag import Okt
from rest_framework.response import Response
from rest_framework.views import APIView
from wordcloud import WordCloud

from content.forms import DiaryForm
from content.models import Content, Diary
from user.models import User


class Main(APIView):
    def get(self, request):
        user = request.user  # 현재 로그인한 사용자
        try:
            content = Content.objects.get(user=user)
        except Content.DoesNotExist:
            content = None

        # 현재 날짜
        current_date = datetime.now().date()

        # 저장된 start_date (예: content.start_date)와의 날짜 차이 계산
        days_passed = (current_date - content.start_date).days + 1
        context = {
            'user': user,
            'content': content,
            'now': now,
            'days_passed': days_passed,
        }

        return render(request, "content/main.html", context)

    def post(self, request):
        return render(request, 'content/main.html')


class Main2(APIView):
    def get(self, request):
        return render(request, "content/main2.html")

    def post(self, request):
        nickname = request.POST.get('nickname')
        date = request.POST.get('date')
        user = request.user  # 로그인한 사용자

        if not user.is_authenticated:
            return Response(status=200, data=dict(message="로그인이 필요합니다."))

        if not nickname or not date:
            return Response(status=400, data=dict(message="닉네임과 날짜를 모두 입력하세요."))

        # Check if user already submitted
        existing_content = Content.objects.filter(user=user)
        if existing_content.exists():
            return Response(status=400, data=dict(message="이미 제출한 사용자입니다."))

        # Get partner's nickname from user table
        try:
            partner_user = User.objects.exclude(id=user.id).get(nickname=nickname)
        except User.DoesNotExist:
            return Response(status=400, data=dict(message="존재하지 않는 닉네임입니다."))

        # Content 모델에 데이터 저장
        content = Content.objects.create(
            user=user,
            partner_nickname=partner_user.nickname,
            start_date=date
        )

        return Response(status=200, data=dict(message="데이터가 성공적으로 저장되었습니다."))


class Main3(APIView):
    def get(self, request):
        return render(request, "content/main3.html")

    def post(self, request):
        return render(request, 'content/main3.html')


class Write(APIView):
    def get(self, request):
        form = DiaryForm()
        context = {'form': form}
        return render(request, 'content/write.html', context)

    def post(self, request):
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user

            if 'thumbnail' in request.FILES:
                uploaded_thumbnail = request.FILES['thumbnail']
                fs = FileSystemStorage()
                uploaded_thumbnail_url = fs.save('thumbnails/' + uploaded_thumbnail.name, uploaded_thumbnail)
                diary.thumbnail = uploaded_thumbnail_url  # 저장할 때 전체 경로가 아닌 파일명만 저장하도록 변경

            diary.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})


def clean_text(text):
    """
    한글, 영문, 숫자만 남기고 제거
    """
    text = text.replace(".", " ").strip()
    text = text.replace("·", " ").strip()
    pattern = '[^ ㄱ-ㅣ가-힣|0-9|a-zA-Z]+'
    text = re.sub(pattern=pattern, repl='', string=text)

    # print("clean_text:", text)
    return text


def tokenize(text):
    # 불용어 처리
    cleaned_text = clean_text(text)

    # Okt 형태소 분석기를 사용하여 텍스트 데이터를 전처리
    okt = Okt()
    words = okt.pos(cleaned_text, stem=True, norm=True)
    nouns = [word for word, pos in words if pos in ['Noun', 'Adjective']]
    tokenized_text = ' '.join(nouns)

    # print("tokenize:", tokenized_text)
    return tokenized_text


def filtering(tokenized_text):
    # 전처리된 텍스트를 공백을 기준으로 단어로 나눔
    words = tokenized_text.split()

    # 단어 빈도 계산
    word_counts = Counter(words)

    # 빈도를 내림차순으로 정렬
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # 누적 빈도와 전체 단어 수 초기화
    cumulative_count = 0
    total_word_count = len(words)

    # 누적 빈도가 전체 단어 수의 70% 이상이 될 때까지 단어 선택
    filtered_words = []
    for word, count in sorted_word_counts:
        if cumulative_count / total_word_count >= 0.7:
            break
        filtered_words.append(word)
        cumulative_count += count

    print("filtering:", filtered_words)
    return filtered_words


def generate_wordcloud(text_data, diary_id):
    # 마스크 이미지 열기
    mask_image_path = 'static/image/heart.png'
    font_path = 'static/fonts/강원교육모두 Bold.ttf'
    mask_image = Image.open(mask_image_path)
    mask_array = np.array(mask_image)

    # WordCloud 생성
    wordcloud = WordCloud(
        font_path=font_path,
        width=400,
        height=400,
        background_color='white',
        max_font_size=150,
        relative_scaling=0.5,
        random_state=23,
        colormap='spring',
        mask=mask_array,
        prefer_horizontal=True
    )

    # 텍스트 데이터를 이용하여 WordCloud 생성
    wordcloud.generate(text_data)

    # 워드 클라우드 이미지를 파일로 저장
    image_filename = f'wordcloud_{diary_id}.png'  # 일기별로 다른 파일 이름 사용
    image_path = os.path.join(settings.MEDIA_ROOT, 'wordcloud', image_filename)
    wordcloud.to_file(image_path)

    return image_path


def summary(text):
    # 다이어리 엔트리를 문서로 결합

    for diary_text in text:
        print(diary_text)
        # 문서 요약
        summary_text = summarize(diary_text, ratio=0.2)
        print("summary", summary_text)
    return summary_text


# APIView 클래스 정의
class Emotions(APIView):
    def get(self, request):
        diaries = Diary.objects.filter(user=request.user)
        wordcloud_images = []
        summaries = []

        for diary in diaries:
            # 텍스트 데이터 추출
            text_data = diary.content

            # 전처리 함수를 사용하여 텍스트 데이터 전처리
            tokenized_text = tokenize(text_data)

            # 필터링 함수를 사용하여 필터링된 단어 추출
            filtered_words = filtering(tokenized_text)

            # 필터링된 단어를 공백으로 구분하여 문자열로 변환하여 WordCloud 생성
            wordcloud_text = ' '.join(filtered_words)

            # 워드 클라우드 이미지 생성
            wordcloud_image_path = generate_wordcloud(wordcloud_text, diary.id)
            # 이미지를 Base64로 인코딩
            with open(wordcloud_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            wordcloud_images.append({
                'diary_id': diary.id,
                'wordcloud_image_base64': encoded_string
            })

            # 요약 함수 호출
            summary_text = summary(text_data)
            summaries.append(summary_text)

        context = {
            'diaries': diaries,
            'wordcloud_images': wordcloud_images,
            'summaries': summaries
        }

        return render(request, "content/emotions.html", context)


# Create your views here.
class MyDiary(APIView):
    def get(self, request):
        diaries = Diary.objects.filter(user=request.user)
        context = {'diaries': diaries}
        return render(request, "content/mydiary.html", context)


class CoupleDiary(APIView):
    def get(self, request):
        if request.user.is_authenticated:  # 로그인한 사용자인지 확인
            user = request.user  # 현재 로그인한 사용자

            # 사용자와 연관된 Content 객체 가져오기
            try:
                content = Content.objects.get(user=user)
                lover_nickname = content.partner_nickname

                # 연인의 다이어리 목록 가져오기
                if lover_nickname:
                    lover_diaries = Diary.objects.filter(user__nickname=lover_nickname)
                else:
                    lover_diaries = []

                context = {
                    'lover_diaries': lover_diaries
                }

                return render(request, "content/couplediary.html", context)
            except Content.DoesNotExist:
                # Content 객체가 없는 경우에 대한 처리
                # 사용자에게 메시지를 보여주거나 다른 처리를 추가하세요.
                pass
        else:
            # 로그인하지 않은 사용자에게 메시지를 보여주거나 로그인 페이지로 리다이렉션하세요.
            return redirect('login')  # login은 실제 로그인 URL에 해당하는 부분으로 변경해야 합니다.
