from django.shortcuts import render, redirect, get_object_or_404
from .models import Music
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from playlists.models import Playlist
import pdb

# 노래 메인 페이지
def main(request):
    music_list = Music.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(music_list, 10)
    try:
        musics = paginator.get_page(page)
    except PageNotAnInteger:
        musics = paginator.page(1)
    except EmptyPage:
        musics = paginator.page(paginator.num_pages)

    return render(request, 'musics/main.html', {'musics': musics})
   

# 노래 게시글 상세보기
def show(request, music_id):
    music = get_object_or_404(Music, id=music_id) 
    return render(request, 'musics/show.html', {'music': music})


# 노래 게시글 작성 페이지
def new(request):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')
        
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

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-gpu')
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
        driver.get('https://www.genie.co.kr/search/searchSong?query={}+{}'.format(singer, title))
        time.sleep(1)


        driver.find_element_by_class_name("btn-info").click()
        time.sleep(1)

        genre = driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[3]/span[2]').text
        lyrics = driver.find_element_by_xpath('//*[@id="pLyrics"]/p').text

        music.genre = genre
        music.lyrics = lyrics

        # crawling video link

        driver.get('https://www.youtube.com/results?search_query={}+{}'.format(singer, title))
        time.sleep(2)

        video_title = driver.find_element_by_id('video-title')
        url = video_title.get_attribute('href')
            
        if url is None:
            video_title = driver.find_elements_by_id('video-title')[1]
            url = video_title.get_attribute('href')
        
        url = url.replace('watch?v=', 'embed/')

        driver.quit()
        
        
        music.link = url
        music.save()

    return redirect('musics:main')


# 노래 게시글 수정
def update(request, music_id):
    if request.method == "POST":
        music = get_object_or_404(Music, pk=music_id)
        title = request.POST.get('title')
        singer = request.POST.get('singer')

        # crawling genre and lyrics
        # header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        # melon = requests.get('https://www.melon.com/search/song/index.htm?q={}+{}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form'.format(singer, title), headers = header)
        # melon_html = melon.text
        # melon_parse = BeautifulSoup(melon_html, 'html.parser')
        # detail = melon_parse.find(class_='btn_icon_detail')

        

        # song_link = detail['href'].split(';')
        # song_number = song_link[1].split("'")[1]

        # song = requests.get('https://www.melon.com/song/detail.htm?songId={}'.format(song_number), headers = header)
        # song_html = song.text
        # song_parse = BeautifulSoup(song_html, 'html.parser')
        # genre = str(song_parse.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)'))
        # genre = genre.replace('[<dd>', '').replace('</dd>]', '')
        # if '&amp;' in genre:
        #     genre = genre.replace('&amp;', '&')

        # lyrics = str(song_parse.find(id='d_video_summary'))
        # lyrics = lyrics.replace('<div class="lyric" id="d_video_summary"><!-- height:auto; 로 변경시, 확장됨 -->','').replace('</div>','').strip()
        # lyrics = lyrics.replace('<br/>', '\n')

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-gpu')
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
        driver.get('https://www.genie.co.kr/search/searchSong?query={}+{}'.format(singer, title))
        time.sleep(1)


        driver.find_element_by_class_name("btn-info").click()
        time.sleep(1)

        genre = driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[3]/span[2]').text
        lyrics = driver.find_element_by_xpath('//*[@id="pLyrics"]/p').text

        music.genre = genre
        music.lyrics = lyrics
        

        # crawling video link

        
        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

        driver.get('https://www.youtube.com/results?search_query={}+{}'.format(singer, title))
        time.sleep(2)

        video_title = driver.find_element_by_id('video-title')
        url = video_title.get_attribute('href')

        if url is None:
            video_title = driver.find_elements_by_id('video-title')[1]
            url = video_title.get_attribute('href')

        url = url.replace('watch?v=', 'embed/')

        driver.quit()
        
        music.title = title
        music.singer = singer
        music.link = url
        music.save()

    return redirect('musics:show', music_id)


# 노래 게시글 삭제
def delete(request, music_id):
    get_object_or_404(Music, pk=music_id).delete()
    return redirect('musics:main')


# 노래 게시글 수정 페이지
def edit(request, music_id):
    user = request.user
    music = get_object_or_404(Music, pk=music_id)

    if user == music.writer:
        return render(request, 'musics/edit.html', {'music': music})
    else:
        return redirect('musics:show', music_id)


# 노래 검색
def search(request):
    option = request.GET.get('option')
    query = request.GET.get('query')

    if option == "title":
        search_list = Music.objects.filter(title__contains=query)
    else:
        search_list = Music.objects.filter(singer__contains=query)

    # page = request.GET.get('page', 1)
    paginator = Paginator(search_list, 10)
    
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        search_result = paginator.get_page(page)
    except PageNotAnInteger:
        search_result = paginator.page(1)
    except EmptyPage:
        search_result = paginator.page(paginator.num_pages)
    
    return render(request,'musics/search.html', {'search_result': search_result, 'search_list':search_list})


# 기존 플레이리스트 생성 플레이리스트 보여주기
def add(request):
    user = request.user
    playlist_list = Playlist.objects.filter(creator=user)
    paginator = Paginator(playlist_list, 10)
    page = request.GET.get('page')
    playlists = paginator.get_page(page)

    return render(request, 'musics/add.html', {'playlists':playlists, 'playlist_list':playlist_list})

# 기존 플레이리스트에 곡 추가
def add_music(request):
    if request.method == "POST":
        playlist_id = request.POST.get('playlist_id')
        music_id = request.POST.get('music_id')
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        music = Music.objects.get(pk=music_id)
        playlist.musics.add(music)
        
        return redirect('playlists:show', playlist_id)
