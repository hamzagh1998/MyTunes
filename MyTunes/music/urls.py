from django.urls import path
from . import views

app_name = "music"

urlpatterns = [
    path('user_profile/<int:id>', views.user_profile, name='user_profile'),
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('add_new_song/<int:id>/', views.songFormView, name='add_new_song'),
    path('song_detail/<int:id>', views.songUpdateView, name='song_detail'),
    path('delete_song/<int:id>', views.deleteSongView, name='delete_song'),
    path('favorite_song/<int:id>', views.songFavorite, name='favorite_song'),
    path('play/<int:id>/', views.play, name='play'),
    path('add_new_album/', views.albumFormView, name='add_new_album'),
    path('delete_album/<int:id>/', views.deleteAlbumView, name='delete_album'),
    path('favorite_album/<slug:slug>/', views.albumFvorite, name='favorite_album'),
    path('album_detail/<slug:slug>/', views.albumDetail, name='album_detail'),
    path('update_album/<slug:slug>/', views.albumUpdateView, name='update_album'),

]
