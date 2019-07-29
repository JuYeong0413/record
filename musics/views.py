from django.shortcuts import render, redirect, get_object_or_404
from .models import Music
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup

# Create your views here.
# 노래 메인 페이지
def main(request):
    music_list = Music.objects.all().order_by('-id')
    paginator = Paginator(music_list, 10)
    page = request.GET.get('page')
    musics = paginator.get_page(page)
    return render(request, 'musics/main.html', {'musics': musics})
   

# 노래 게시글 상세보기
def show(request, music_id):
    music = get_object_or_404(Music, id=music_id) 
    return render(request, 'musics/show.html', {'music': music})


# 노래 게시글 작성 페이지
def new(request):
    return render(request, 'musics/new.html')


# 노래 게시글 작성
def create(request):
    user = request.user
    if request.method =="POST":
        title = request.POST.get('title')
        singer = request.POST.get('singer')

        music = Music()
        music.writer = user
        music.title = title
        music.singer = singer

        # crawling genre and lyrics
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'} # 튕기는 현상이 있어서 header 추가
        melon = requests.get('https://www.melon.com/search/song/index.htm?q={}+{}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form'.format(singer, title), headers = header)
        melon_html = melon.text
        melon_parse = BeautifulSoup(melon_html, 'html.parser')
        detail = melon_parse.find(class_='btn_icon_detail')

        if detail is None:
            return redirect('musics:main') # 곡 정보가 없을 경우 처리 필요함

        song_link = detail['href'].split(';')
        song_number = song_link[1].split("'")[1]

        song = requests.get('https://www.melon.com/song/detail.htm?songId={}'.format(song_number), headers = header)
        song_html = song.text
        song_parse = BeautifulSoup(song_html, 'html.parser')
        genre = str(song_parse.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)'))
        genre = genre.replace('[<dd>', '').replace('</dd>]', '')
        if '&amp;' in genre:
            genre = genre.replace('&amp;', '&')

        lyrics = str(song_parse.find(id='d_video_summary'))
        lyrics = lyrics.replace('<div class="lyric" id="d_video_summary"><!-- height:auto; 로 변경시, 확장됨 -->','').replace('</div>','').strip()
        lyrics = lyrics.replace('<br/>', '\n')

        music.genre = genre
        music.lyrics = lyrics

        # crawling video from youtube
        # youtube_music = requests.get('https://music.youtube.com/search?q={}+{}'.format(singer, title))
        # youtube_music_html = youtube_music.text
        # youtube_music_parse = Beautifulsoup(youtube_music_html, 'html.parser')
        # play_button = youtube_music_parse.find(id='play_button')

        # if play_button is None:
        #     return redirect('musics:main') # 동영상 찾을 수 없는 경우 처리 필요함
        
        
        music.link = request.POST.get('link')
        music.save()

    return redirect('musics:main')


# 노래 게시글 수정
def update(request, music_id):
    if request.method == "POST":
        music = get_object_or_404(Music, pk=music_id)
        music.title = request.POST.get('title')
        music.singer = request.POST.get('singer')
        music.link = request.POST.get('link')
        music.save()

    return redirect('musics:show', music_id)


# 노래 게시글 삭제
def delete(request, music_id):
    get_object_or_404(Music, pk=music_id).delete()
    return redirect('musics:main')


# 노래 게시글 수정 페이지
def edit(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    return render(request, 'musics/edit.html', {'music': music})


# 노래 검색
def search(request):
    option = request.GET.get('option')
    query = request.GET.get('query')

    if option == "title":
        search_result = Music.objects.filter(title__contains=query)
    else:
        search_result = Music.objects.filter(singer__contains=query)

    return render(request,'musics/search.html', {'search_result': search_result})