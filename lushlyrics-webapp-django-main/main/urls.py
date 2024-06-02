from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path('register/',views.register,name='register'),
    path('login/',views.loguser,name='login'),
    path('logout/',views.logout_user,name='logout')
]