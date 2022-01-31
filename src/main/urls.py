from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('profiles/<str:slug>/', views.UserDetailView.as_view(),
         name='profile_detail'),
    path('profile/offer/', views.ExecutorOfferFormView.as_view(),
         name='executor_offer'),
    path('profile/delete-offer', views.delete_offer, name='delete_offer'),
    path('profile/delete-project', views.delete_project, name='delete_project'),
    path('workers/', views.ExecutorOfferListView.as_view(), name='offer_list'),
    path('project/', views.ProjectFormView.as_view(),
         name='project'),

]
