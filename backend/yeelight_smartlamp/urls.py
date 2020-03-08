from django.urls import path

from yeelight_smartlamp.views import Search, AddLamp

urlpatterns = [
    path('search', Search.as_view()),
    path('add', AddLamp.as_view()),
]
