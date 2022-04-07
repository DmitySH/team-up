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

# API urls.
urlpatterns += [
    path('process-belbin/', views.BelbinProcessAPIView.as_view()),
    path('process-mbti/', views.MBTIProcessAPIView.as_view()),
    path('process-lsq/', views.LSQProcessAPIView.as_view()),
]
