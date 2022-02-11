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
]
