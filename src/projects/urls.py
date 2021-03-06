from django.urls import path

from . import views
from .views import ProjectDetailAPIView
from ..base.services import add_prefix_to_urls

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
    path('projects/<str:slug>/<int:pk>/', views.WorkerSlotFormView.as_view(),
         name='worker_slot_form'),
    path('projects/<int:slot_id>/clear/', views.clear_worker_slot,
         name='worker_slot_clear'),
    path('projects/<int:slot_id>/leave/', views.leave_worker_slot,
         name='worker_slot_leave'),
    path('projects/<str:title>/analyze/', views.AnalyzeTeam.as_view(),
         name='analyze_team'),
]

# API urls.
api_urlpatterns = [
    path('get-project/<str:title>/', ProjectDetailAPIView.as_view()),
    path('update-project/',
         views.ProjectUpdateAPIView.as_view()),
    path('delete-project/',
         views.ProjectDeleteAPIView.as_view()),
    path('update-worker-slot/',
         views.WorkerSlotUpdateAPIView.as_view()),
    path('delete-worker-slot/<int:slot_id>/',
         views.WorkerSlotDeleteAPIView.as_view()),
    path('get-projects/',
         views.ProjectListAPIView.as_view()),
    path('invite-profile/<str:username>/<int:slot_id>/',
         views.InviteAPIView.as_view()),
    path('apply-slot/<int:slot_id>/',
         views.ApplyAPIView.as_view()),
    path('get-slot-applies/<int:slot_id>/',
         views.SlotAppliesAPIView.as_view()),
    path('decline-apply-slot/<str:username>/<int:slot_id>/',
         views.DeclineApplyAPIView.as_view()),
    path('get-current-projects/',
         views.CurrentProjectsListAPIView.as_view()),
    path('clear-slot/<int:slot_id>/',
         views.ClearSlotAPIView.as_view()),
    path('leave-slot/<int:slot_id>/',
         views.LeaveSlotAPIView.as_view()),
]

api_urlpatterns = add_prefix_to_urls(api_urlpatterns)

urlpatterns += api_urlpatterns
