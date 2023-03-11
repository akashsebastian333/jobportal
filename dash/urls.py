from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import serve
from django.conf.urls.static import static



urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('/joblistings', views.job_dashboard_view, name='dashboard'),
    path('/all', views.index, name='dashboard'),
    path('/edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('/search', views.search_jobs, name='search_jobs'),
    path('/jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('/submissions/', views.submissions, name='submissions'),
    path('/myapplications/', views.my_files, name='my_files'),
    path('/submissions/<int:submission_id>/download/', views.download_submission, name='download_submission'),
    path('/send_message/<int:submission_id>/', views.send_message, name='send_message'),
    path('/inbox', views.inbox, name='inbox'),
    path('/reply_message/<int:message_id>/', views.reply_message, name='reply_message'),
    path('/user_messages/<str:username>/', views.user_messages, name='user_messages'),
    #path('resumes/<path:path>', views.protected_serve, {'document_root': settings.STATICFILES_DIRS}),
    #path('/resumes/<int:pk>/download/', views.login_required(views.download_resume), name='download_resume'),

    # other URL patterns go here
]


