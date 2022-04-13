"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from astro import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homePage'),
    path('home', views.home, name='nextHomePage'),
    path('about', views.about, name="aboutPage"),
    path('events', views.events, name="eventsPage"),
    path('otherSources', views.other_sources, name="otherSourcesPage"),
    path('apod', views.apod, name='apod'),
    path("articles", views.articles, name="articles"),
    path("article/<int:num>", views.article, name="article"),
    path("great_astronomers", views.astronomers, name="great astronomers"),


    path("members/", include('django.contrib.auth.urls'), name="login_things"),
    path('members/login_member',views.login_member,name="login_member"),
    path("members/member_home", views.member_home, name="member_home"),
    path("members/logout_member", views.logout_member, name="logout"),
    path("members/astronomer_crud",views.astronomer_crud_add,name="astronomer_crud_add"),
    path('members/astronomer_crud/remove',views.astronomer_crud_remove,name="astronomer_crud_remove")

]
