from django.urls import path

from . import views
from ..base.services import add_prefix_to_urls

urlpatterns = [
    path('profile/belbintest/', views.BelbinTestFormView.as_view(),
         name='belbin_test'),
    path('profile/mbtitest/', views.MBTITestFormView.as_view(),
         name='mbti_test'),
    path('profile/lsqtest/', views.LSQTestFormView.as_view(),
         name='lsq_test'),
]

# API urls.
api_urlpatterns = [
    path('process-belbin/', views.BelbinProcessAPIView.as_view()),
    path('process-mbti/', views.MBTIProcessAPIView.as_view()),
    path('process-lsq/', views.LSQProcessAPIView.as_view()),
]

api_urlpatterns = add_prefix_to_urls(api_urlpatterns)

urlpatterns += api_urlpatterns
