from django.urls import path

from . import views

urlpatterns = [
        path('task/<str:uuid>/', views.task, name='task'),
        #path('project/', views.projectlist, name='projectlist'),
        path('project/<str:fullname>/', views.project, name='project'),
]
