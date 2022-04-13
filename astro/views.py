import json
from datetime import datetime, timedelta

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from astro.admin import Prev30
from astro.models import Astronomer
from django.contrib.auth import authenticate, login, logout

home_carousels = [{
    'images': {
        'pc': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/im1.jpg?raw=true',
        'mob': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/im1m.jpg?raw=true'
    },
    'caption_title': 'We are Astro Club,VNIT',
    'caption': 'Are you one of those Space buffs? Wanna hone you amateur skills in Astronomy? Look no'
               ' further you have reached your destination! Welcome to Astro Club VNIT!'
}, {
    'images': {
        'pc': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/im2.jpg?raw=true',
        'mob': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/im2m.jpg?raw=true'
    },
    'caption_title': 'Sky is the limit',
    'caption': 'Have a look at this beautiful image🤩, capturing the Star trails, taken by our club '
               'member Ojas Sharma.'
},
    {
        'images': {
            'pc': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/im4.jpg?raw=true',
            'mob': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/im4m.jpg?raw=true'
        },
        'caption_title': '',
        'caption': 'Astronomy Club of VNIT, Ashlesha invites you to gaze upon the heavens and beyond and see'
                   ' the unfolding of the cosmic miracle.'
    }
]


def home(request):
    carousel = {
        'image': '',
        'caption_title': '',
        'caption_info': ''
    }

    context = {
        'carousels': home_carousels
    }
    context['carousels'][0]['active'] = 'active'
    return render(request, 'index.html', context)


def about(request):
    carousel = {
        'image': '',
        'caption_title': '',
        'caption_info': ''
    }
    context = {
        'carousels': [
            {
                'image': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/about%201.jpg?raw=true',
                'caption_title': '',
                'caption_info': ''
            },
            {
                'image': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/about%202.jpg?raw=true',
                'caption_title': '',
                'caption_info': ''
            }
            ,
            {
                'image': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/about%203.jpg?raw=true',
                'caption_title': '',
                'caption_info': ''
            }
            ,
            {
                'image': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/about%204.jpg?raw=true',
                'caption_title': '',
                'caption_info': ''
            }
            ,
            {
                'image': 'https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/about%205.jpg?raw=true',
                'caption_title': '',
                'caption_info': ''
            }
        ]
    }
    context['carousels'][0]['active'] = 'active'
    return render(request, 'about.html', context)


def events(request):
    event = {
        'title': '',
        'description': '',  # can use basic html here
        'main_link_desc': '',
        'main_link': '',  # write if any else blank
        'additional links': [

        ]  # has  dicts of format {'description' : '','link_addr' :''}

    }
    context = {
        'events': [],

    }

    if len(context['events']) != 0:
        context['events'][0]['active'] = 'active'
        return render(request, 'events.html', context)
    else:
        return render(request, 'noevents.html')


def other_sources(request):
    context = {

    }
    return render(request, 'otherSources.html', context)


def apod(request):
    api_url = 'https://api.nasa.gov/planetary/apod'
    my_key = 'gE4OwsHm4NSF3efofSsGRvxcJeT3abrR05xk3Usd'
    context = {
        'prev_30': [],  # array of objects of the form img_info
        'active': '',

    }

    if len(Prev30.objects.all()) == 0 or len(
            Prev30.objects.all().filter(date=(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))) == 0:
        todays_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        date_month_before = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        print(date_month_before, todays_date)
        response = requests.get(f'{api_url}?start_date={date_month_before}&end_date={todays_date}&api_key={my_key}')
        context['prev_30'] = json.loads(response.text)[::-1]
        print(type(context['prev_30']))
        print(context['prev_30'])
        for obj in Prev30.objects.all():
            obj.delete()
        for i in context['prev_30']:
            entry = Prev30()
            print(i)
            entry.url = i['url']
            entry.date = i['date']
            entry.title = i['title']
            entry.explanation = i['explanation']
            entry.save()

    else:
        todays_date = datetime.today() - timedelta(days=1)
        for day_back in range(0, 29):
            try:
                entry = Prev30.objects.all().filter(date=(todays_date - timedelta(day_back)).strftime('%Y-%m-%d'))[0]
                new_context_data = dict()
                new_context_data['url'] = entry.url
                new_context_data['date'] = entry.date
                new_context_data['title'] = entry.title
                new_context_data['explanation'] = entry.explanation
                context['prev_30'].append(new_context_data)
            except:
                print('not found for today')
    context['prev_30'][0]['active'] = 'active'
    return render(request, 'apod.html', context)


def articles(request):
    context = {
        "articles": [],

    }
    article1 = {
        "id": 1,
        "link": "/article/1",
        "drive_link": "https://drive.google.com/u/0/uc?id=1NY32LkuJgIDEJYgko3z5GzzQ-B7mOfhx&export=download",
        "title": "STELLAR CLASSIFICATION",
        "summary": '''&emsp;Stellar classification is the classification of stars according to their size,
temperature and spectral characteristics. According to the much used MorganKeenan table, the classification of stars has evolved into seven different classes or
groups. This system was created by Annie Jump Cannon, an American
Astronomer. Cannon developed this system on the basis of Balmer spectral lines,
later characterization according to size and temperature were approached. The
seven groups are O, B, A, F, G, K and M.''' + '<br/><br/>' + '''&emsp;Stars classified in the 'O' group are the most massive and hottest, with
temperatures exceeding 30,000°C, while those in the 'M' group are the smallest
and coolest, with temperatures less than 3,000°C.
A star with a really high temperature is a Blue star while those quite the smallest
ones are Red stars. Hence colour of the star is dependent on its Size and
Temperature. This is similar to what we observe with the black bodies at very high
temperatures. Usually most blue stars are very hot and are therefore classed as
'O' stars, while the coolest are red stars, and are classified into the 'M' class.''',
        "cover_image": "https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/hr-diagram-credit-nso.png?raw=true",
        "images": [
            "https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/Stellar%20Classification%20Coverpage.jfif?raw=true",
            "https://raw.githubusercontent.com/Darshan110801/VNIT-Astronomy-Club-Website/master/static/images/800px-Morgan-Keenan_spectral_classification.png",
            "https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/hr-diagram-credit-nso.png?raw=true",

        ],
        "date": "July 27, 2021"

    }

    article2 = {
        "id": 2,
        "link": "/article/2",
        "drive_link": "https://drive.google.com/uc?id=1yjc4bRBqszeq8TFGKQuYxzeUobqgZkac&export=download",
        "title": "JAMES WEBB TELESCOPE (JWST)",
        "summary": '''The James Webb telescope (JWST) is all-ready to launch on the momentous day of 18th December 2021 on Ariane 5 rocket from French Guiana, NASA collaborated with ESA and CSA to develop this complex telescope, which is the successor of the Hubble space telescope. The project was eventually started from 1996 and in 2002 the Next Generation Space Telescope (NGST) was renamed to JWST to give tribute to James Edwin Webb who was an American government official, who served as undersecretary of state (1949-1952). He was also the second appointed administrator of NASA ( 14th Feb 1961-7th Oct 1968 ). This telescope will start it’s functioning after six months of the launch and the engineers behind the whole project are Northrop Grumman engineers, they all are very excited for the launch as they have given all their efforts to build this revolutionary telescope.
''',
        "cover_image": "https://github.com/Darshan110801/VNIT-Astronomy-Club-Website/blob/master/static/images/telescope.jpg?raw=true",
        "images": [

        ],
        "date": "October 20, 2021"

    }
    context['articles'].append(article2)
    context['articles'].append(article1)
    return render(request, "articles.html", context)


def article(request, num):
    articles_table = {
        1: "Article1.html",
        2: "Article2.html",

    }
    return render(request, articles_table[num])


def astronomers(request):
    context_ = {
        "astronomers": [

        ]
    }
    for astronomer in Astronomer.objects.all():
        context_['astronomers'].append({
            'name': astronomer.name,
            'image_link': astronomer.image_link,
            'yob': astronomer.yob,
            'yod': astronomer.yod,
            'books': astronomer.books,
            'summary': astronomer.summary,
            'wiki_link': astronomer.wiki_link,
            'active': ''
        })
    context_['astronomers'][0]['active'] = 'active'
    return render(request, 'astronomers.html', context=context_)


@login_required(login_url='/members/login_member')
def member_home(request):
    if not request.user.is_authenticated:
        return redirect('/members/login_member')
    else:
        return render(request, 'member_privileges/member_index.html', context={'carousels': home_carousels})


def login_member(request):
    if request.user.is_authenticated:
        print(request.user.username, request.user.password)
        return redirect('/members/member_home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/members/member_home')
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('/members/login_member')
    return render(request, 'authenticate/login.html')


@login_required(login_url='/members/login_member')
def logout_member(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/members/login_member')
def astronomer_crud_add(request):
    if request.method == "POST":
        name_ = request.POST.get('name')
        image_link_ = request.POST.get('image_link')
        yob_ = request.POST.get('yob')
        yod_ = request.POST.get('yod')
        books_ = request.POST.get('books')
        summary_ = request.POST.get('summary')
        wiki_link_ = request.POST.get('wiki_link')
        new_astronomer = Astronomer(name=name_, image_link=image_link_, yob=yob_, yod=yod_, books=books_,
                                    summary=summary_, wiki_link=wiki_link_)
        new_astronomer.save()
        return redirect('/members/astronomer_crud')

    return render(request, "member_privileges/astronomer_crud.html")


@login_required(login_url='/members/login_member')
def astronomer_crud_remove(request):
    if request.method =="POST":
        name=request.POST.get('name')
        is_there = Astronomer.objects.filter(name=name).exists()
        if is_there:
            astronomer = Astronomer.objects.filter(name=name)[0]
            astronomer.delete()
            messages.success(request,"Data pertaining to the astronomer "+name+" is deleted successfully.")
            return redirect('/members/astronomer_crud/remove')
        else:
            return redirect('/members/astronomer_crud/remove')
    return render(request, 'member_privileges/astronomer_crud_remove.html')
