"""
URL configuration for taskproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('task/', views.tasks, name='task'),
    path('logout/', views.signout, name='logout'),
    path('task/create/', views.create_task, name='task_create'),
    path('task/<int:task_id>/', views.task_details, name='task_details'),
    path('task/<int:task_id>/completed', views.complete_task, name='task_completed'),
    path('task/<int:task_id>/undocompleted', views.undo_complete_task, name='undo_complete_task'),
    path('task/<int:task_id>/delete', views.delete_task, name='delete_task'),
]

