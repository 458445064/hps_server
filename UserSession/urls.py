# from django.conf.urls import url,include
from django.urls import include,path
from django.contrib import admin
from UserSession import views
urlpatterns = [

    path('speakerlist/', views.SpeakerListView.as_view()),
    path('images/<uuid:image_id>/', views.ImageView.as_view(), name='image-view'),
    path('virtualpresonlist/', views.VirtualPersonListView.as_view()),
    path('backgroundlist/', views.BackGroundListView.as_view()),
    path('frontgroundlist/', views.FrontGroundListView.as_view()),
    path('displayvideo/', views.DisplayVideoView.as_view()),
    path('uploadAudio/', views.UploadVideoAudioView.as_view()),
    path('downloadAudio/', views.DownloadAudioView.as_view()),

]