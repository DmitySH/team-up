from django.urls import path
from djoser.views import UserViewSet, TokenCreateView

urlpatterns = [
    path('users/', UserViewSet.as_view({'post': 'create'})),
    path('token/login/', TokenCreateView.as_view()),
]
