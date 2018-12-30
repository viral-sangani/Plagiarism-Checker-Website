from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webpages.urls')),
    path('teacher/', include('teacher.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]
