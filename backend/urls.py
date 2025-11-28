from django.contrib import admin
from django.urls import path, include # <--- Import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls')), # <--- Link the apps URLs
]