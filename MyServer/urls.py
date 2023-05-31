# from django.conf.urls import url,include
from django.urls import include,path
from django.contrib import admin
from MyServer import views
urlpatterns = [

    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path("Register/", views.RegisterView.as_view()),
    path('imagecode/', views.ImageCodeView.as_view()),
    path('message/', views.MessageView.as_view()),
    path('credential/', views.CredentialView.as_view()),
    # path('LoginWithPhone/', views.LoginWithPhoneView.as_view()),
    # path('LoginWithPasswords/', views.LoginWithPasswordsView.as_view()),
]