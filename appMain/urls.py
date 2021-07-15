from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('CBR.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'^files/', include('db_file_storage.urls')),

]

