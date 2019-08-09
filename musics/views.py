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

        # crawling genre and lyrics
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-gpu')
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if os.name == 'nt':
            driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
        else:
            driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

        driver.get('https://www.genie.co.kr/search/searchSong?query={}+{}'.format(singer, title))
        time.sleep(1)

        btn = driver.find_element_by_class_name("btn-info").click()
        if btn is None:
            return redirect('musics:main')
        time.sleep(1)

        genre = driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[3]/span[2]').text
        lyrics = driver.find_element_by_xpath('//*[@id="pLyrics"]/p').text

        music.genre = genre
        music.lyrics = lyrics

        # crawling video link
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('—disable-gpu')
        if os.name == 'nt':
            driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
        else:
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
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-gpu')
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")


        if os.name == 'nt':
            driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
        else:
            driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

        driver.get('https://www.genie.co.kr/search/searchSong?query={}+{}'.format(singer, title))
        time.sleep(1)

        btn = driver.find_element_by_class_name("btn-info").click()
        if btn is None:
            return redirect('musics:main')
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
