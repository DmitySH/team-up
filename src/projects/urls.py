from django.urls import path

from . import views

urlpatterns = [
    path('profile/delete-project', views.delete_project,
         name='delete_project'),
    path('project/delete-slot/<int:pk>', views.delete_slot,
         name='delete_slot'),
    path('project/', views.ProjectFormView.as_view(),
         name='project_form'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<str:title>/invite/<str:profile>/<int:slot_pk>/',
         views.invite_profile,
         name='slot_invite'),
    path('projects/<str:title>/apply/<str:profile>/<int:slot_pk>/',
         views.apply_for_slot,
         name='slot_apply'),
    path('projects/<str:title>/applies/<int:slot_pk>/',
         views.AppliedProfiles.as_view(),
         name='applied_profiles'),
    path('projects/<str:title>/apply/decline/<str:profile>/<int:slot_pk>/',
         views.decline_apply,
         name='decline_apply'),
    path('projects/<str:title>/invite/<str:profile>/',
         views.ProjectInvitesView.as_view(),
         name='project_invite'),
    path('projects/<str:slug>/', views.ProjectDetailView.as_view(),
         name='project_detail'),
    path('projects/<str:slug>/<int:pk>', views.WorkerSlotFormView.as_view(),
         name='worker_slot_form'),
]