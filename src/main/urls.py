from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('profiles/<str:slug>/', views.UserDetailView.as_view(),
         name='profile_detail'),
]
