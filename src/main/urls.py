from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('profiles/<str:slug>/', views.UserDetailView.as_view(),
         name='profile_detail'),
    path('profiles/<str:slug>/edit/', views.UserEditView.as_view(),
         name='edit_profile'),

    path('register/', views.UserFormView.as_view(), name='register'),

]
