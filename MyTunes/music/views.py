from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Album, Song
from .forms import AlbumForm, SongForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def index(request):
    albums = Album.objects.all()
    if request.POST:
        if request.POST.get('favorite') == "True":
            print(request.POST.get('favorite'), request.user.id)
            albums = Album.objects.filter(is_favorite=request.POST.get('favorite'), user=request.user.id)

    # Search
    if request.GET:
        print(getQuerySet(request.GET.get('user_search', '')))
        albums = getQuerySet(request.GET.get('user_search', ''))
        return render(request, 'index.html', {'albums':albums})

    return render(request, 'index.html', {'albums':albums})

def getQuerySet(query=None):
    query_set = []
    for q in query.split(" "): # Convert it to list
        posts = Album.objects.filter(Q(title__icontains=q)|
                                    Q(date_created__icontains=q)|
                                    Q(artist__icontains=q)|
                                    Q(genre__icontains=q)).distinct()
        for post in posts:
            query_set.append(post)

    return list(set(query_set))

def user_profile(request, id):
    if not request.user.is_authenticated:
        return redirect('music:login')

    albums = Album.objects.filter(user=id)
    if albums:
        if albums[0].user != request.user:
            return HttpResponse('You are not allowed to see this page!')

    if request.POST:
        if request.POST.get('favorite') == 'True':
            albums = Album.objects.filter(user=id, is_favorite=True)

    return render(request, 'user_profile.html', {'albums':albums})

def registerView(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save(commit=True)
            return redirect('music:login')

    return render(request, 'register.html', {'form':form})

def loginView(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index')

    return render(request, 'login.html', {'form':form})

@login_required(login_url="music:login")
def logoutView(request):
    logout(request)
    return redirect('music:login')

def albumFormView(request):
    if not request.user.is_authenticated:
        return redirect('index')

    form = AlbumForm()
    if request.POST:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = AlbumForm()
            return redirect('index')

    return render(request, 'album_form.html', {'form':form})

def albumUpdateView(request, slug):
    if not request.user.is_authenticated:
        return redirect('music:login')

    album = get_object_or_404(Album, slug=slug)
    if album.user != request.user:
        return HttpResponse('You are not the author of this album!')

    form = AlbumForm(initial={'artist':album.artist,'title':album.title,
                              'genre':album.genre, 'image':album.image,
                              'discription':album.discription, 'is_favorite':album.is_favorite,
                              'is_public':album.is_public})
    if request.POST:
        form = AlbumForm(request.POST or None, request.FILES or None, instance=album)
        form.save(commit=True)
        return redirect('index')

    return render(request, 'update_album.html', {'form':form})

def deleteAlbumView(request, id):

    if not request.user.is_authenticated:
        return redirect('music:login')

    album = get_object_or_404(Album, id=id)
    if album.user != request.user:
        return HttpResponse('You are not the author of this album!')

    album.delete()
    return redirect('index')

def albumDetail(request, slug):

    album = get_object_or_404(Album, slug=slug)
    songs = Song.objects.filter(album=album)
    if album.is_public == 'private' and album.user != request.user:
        return HttpResponse('You are not allwed to see this album!')

    if request.POST:
        if request.POST.get('favorite') == "True":
            songs = Song.objects.filter(is_favorite=True, album=album)

    return render(request, 'album_detail.html', {'album':album, 'songs':songs})

def songFormView(request, id):
    if not request.user.is_authenticated:
        return redirect('music:login')

    album = get_object_or_404(Album, id=id)

    if request.user != album.user:
        return HttpResponse('You are not the author of this album!')

    form = SongForm()
    if request.POST:
        form = SongForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.album = album
            obj.save()
            form = SongForm()
            return redirect('music:album_detail', album.slug)

    return render(request, 'song_form.html', {'form':form, 'album':album})

def songUpdateView(request, id):
    if not request.user.is_authenticated:
        return redirect('music:login')

    song = get_object_or_404(Song, id=id)
    if song.album.user != request.user:
        return HttpResponse('You are not the author of this song!')

    form = SongForm(initial={'title':song.title, 'song_file':song.song_file, 'is_favorite':song.is_favorite})
    if request.POST:
        form = SongForm(request.POST or None, request.FILES or None, instance=song)
        form.save(commit=True)
        return redirect('music:album_detail', song.album.slug)

    return render(request, 'update_song.html', {'form':form, 'song':song})

def deleteSongView(request, id):

    if not request.user.is_authenticated:
        return redirect('music:login')

    song = get_object_or_404(Song, id=id)
    if song.album.user != request.user:
        return HttpResponse('You are not the author of this song!')

    song.delete()
    return redirect('music:album_detail', song.album.slug)

def albumFvorite(request, slug):
    if not request.user.is_authenticated:
        return redirect('music:login')

    album = get_object_or_404(Album, slug=slug)
    if album.user != request.user:
        return HttpResponse('You are not the author of this album!')

    if album.is_favorite == True:
        album.is_favorite = False
    else:
        album.is_favorite = True
    album.save()
    return redirect('index')

def songFavorite(request, id):
    if not request.user.is_authenticated:
        return redirect('music:login')

    song = get_object_or_404(Song, id=id)
    if song.album.user != request.user:
        return HttpResponse('You are not the author of this song!')
    if song.is_favorite == True:
        song.is_favorite = False
    else:
        song.is_favorite = True
    song.save()
    return redirect('music:album_detail', song.album.slug)

def play(request, id):

    song = get_object_or_404(Song, id=id)

    if not song.album.is_public:
        return HttpResponse('This song belong to a private album!')

    return render(request, 'play.html', {'song':song})
