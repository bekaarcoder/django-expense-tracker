from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls', namespace='home')),
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls', namespace='expenses')),
    path('income/', include('income.urls', namespace='income')),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('preferences/', include('preferences.urls', namespace='preferences'))
]
