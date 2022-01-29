from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('profiles/<str:slug>/', views.UserDetailView.as_view(),
         name='profile_detail'),
    path('profile/offer/', views.ExecutorOfferView.as_view(),
         name='executor_offer'),
    path('profile/delete-offer', views.delete_offer, name='delete_offer')
]
