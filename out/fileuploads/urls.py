
from django.contrib import admin
from django.urls import path

from document import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('beta/',views.beta, name = 'beta'),
    path('admin/', admin.site.urls),
    path('stripped/', views.stripped),
    #path('upload/',views.upload,name = 'upload')

]
