from django.urls import path

from authentication.views import Login, LoginRequiredTest

urlpatterns = [
    path('login', Login.as_view()),
    path('loginrequiredtest', LoginRequiredTest.as_view())
]
