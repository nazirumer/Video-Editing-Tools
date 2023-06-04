
from . import views
from django.urls import path


urlpatterns = [
    
    path("", views.index, name = 'index'),
    path('preview', views.preview, name='preview'),
    path('templates', views.templates, name='templates'),
    path('output', views.output, name='output'),
]
