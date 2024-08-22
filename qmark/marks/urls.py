from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from qmark import settings

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('home', HomeView.as_view(), name='home'),
    path('rooms', RoomsView.as_view(), name='rooms'),
    path('room/<slug>/', RoomView.as_view(), name='post_detail'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('things', ThingsView.as_view(), name='things'),
    path('thing/<slug>/', ThingDetailView.as_view(), name='thing_detail'),
    path('add', AddView.as_view(), name='add'),
	path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
]
