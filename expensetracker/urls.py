from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls', namespace='expenses')),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('preferences/', include('preferences.urls', namespace='preferences'))
]
