from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-change/', views.MyPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', views.MyPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('profiles/<str:slug>/', views.UserDetailView.as_view(),
         name='profile_detail'),
    path('profile/edit/', views.UserEditView.as_view(),
         name='edit_profile'),
    path('profile/invitations/', views.InvitationsView.as_view(),
         name='invitations'),
    path('profile/invitations/accept/<int:slot>/', views.accept_invite,
         name='accept_invite'),
    path('profile/invitations/decline/<int:slot>/', views.decline_invite,
         name='decline_invite'),
    path('profile/invitations/retract/<int:slot>/', views.retract_invite,
         name='retract_invite'),
    path('profile/offer/', views.ExecutorOfferFormView.as_view(),
         name='executor_offer'),
    path('profile/delete-offer', views.delete_offer, name='delete_offer'),
    path('workers/', views.ExecutorOfferListView.as_view(), name='offer_list'),
]

# API urls.
urlpatterns += [
    path('get-profile/<str:slug>/', views.ProfileDetailAPIView.as_view()),
    path('edit-profile/', views.ProfileUpdateAPIView.as_view()),
    path('update-executor-offer/',
         views.ExecutorOfferUpdateAPIView.as_view()),
    path('delete-executor-offer/',
         views.ExecutorOfferDeleteAPIView.as_view()),
    path('change-password/',
         views.ChangePasswordView.as_view()),
    path('get-executor-offers/',
         views.ExecutorOfferListAPIView.as_view()),
    path('get_invited_slots/',
         views.InvitedWorkerSlotListAPIView.as_view()),
    path('accept_invite/<int:slot_id>/',
         views.AcceptInviteAPIView.as_view()),
]
