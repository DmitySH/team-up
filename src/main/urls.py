from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('profiles/<str:slug>/', views.UserDetailView.as_view(),
         name='profile_detail'),
    path('profiles/<str:slug>/edit/', views.UserEditView.as_view(),
         name='edit_profile'),
    path('profile/belbintest/', views.BelbinTestFormView.as_view(),
         name='belbin_test'),
    path('profile/mbtitest/', views.MBTITestFormView.as_view(),
         name='mbti_test'),
    path('profile/lsqtest/', views.LSQTestFormView.as_view(),
         name='lsq_test'),

]
