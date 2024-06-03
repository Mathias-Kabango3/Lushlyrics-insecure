from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
import json
# import cardupdate



f = open('card.json', 'r')
CONTAINER = json.load(f)

@login_required
def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


@login_required
def playlist(request):
    cur_user = User.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})

@login_required
def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})



@login_required
def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])

def register(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      email = request.POST.get('email')
      password_conf = request.POST.get('confirm-password')

      if password == password_conf:
         if User.objects.filter(username=username).exists():
            messages.error(request,'User already exists.')
            return render(request,'signup.html')
         elif User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists.')
         else:
            try:
              user = User.objects.create(username=username,email=email)
              user.set_password(password)
              user.save();
              login(request,user)
              return redirect(default)
            except IntegrityError:
               messages.error(request,'There was an error creating the user')
      else:
         messages.error(request,'Password did not match.')
   return render(request,'signup.html')


def loguser(request):
   if request.method == 'POST':
      username_or_email= request.POST.get('username')
      password = request.POST.get('password')

      if User.objects.filter(email=username_or_email).exists():
         username= User.objects.filter(email=username_or_email)
         user = authenticate(username=username[0],password=password)
         
         if user is not None:
            login(request,user)
            return redirect(default)
         else:
            messages.error(request,'Wrong password or email.')
      elif User.objects.filter(username=username_or_email).exists():
         username = username_or_email
         user = authenticate(request,username=username,password=password)
         
         if user is not None:
            login(request,user)
            return redirect(default)
         else:
            messages.error(request,'Wrong password or email.')   
   return render(request,'login.html')
@login_required
def logout_user(request):
   logout(request)
   return redirect('login')

class MyPasswordResetView(PasswordResetView):
    
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'  

   