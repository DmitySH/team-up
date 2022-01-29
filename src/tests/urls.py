from django.urls import path
from . import views

urlpatterns = [
    path('profile/belbintest/', views.BelbinTestFormView.as_view(),
         name='belbin_test'),
    path('profile/mbtitest/', views.MBTITestFormView.as_view(),
         name='mbti_test'),
    path('profile/lsqtest/', views.LSQTestFormView.as_view(),
         name='lsq_test'),
]