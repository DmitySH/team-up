from django.urls import path

from src.accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-change/', views.MyPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', views.MyPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('profiles/<str:slug>/edit/', views.UserEditView.as_view(),
         name='edit_profile'),
]
