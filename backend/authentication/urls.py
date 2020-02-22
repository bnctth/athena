from django.urls import path

from authentication.views import Login, LoginRequiredTest, RenewToken

urlpatterns = [
    path('login', Login.as_view()),
    path('renew',RenewToken.as_view()),
    path('loginrequiredtest', LoginRequiredTest.as_view())
]
