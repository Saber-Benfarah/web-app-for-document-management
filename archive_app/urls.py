from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('consultation/', views.consultation, name='consultation'),
    path('parametrage/', views.archive_config, name='archive_config'),
    path('add/', views.add_line, name='add_line'),
    path('edit/<int:id>/', views.edit_line, name='edit_line'),
    path('users/', views.create_user, name='create_user'),
    path('users/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('logout/', views.logout_view, name='logout'),
]
urlpatterns += [
    path('users/list/', views.list_users, name='list_users'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('archive/delete/<int:id>/', views.delete_line, name='delete_line'),
]
