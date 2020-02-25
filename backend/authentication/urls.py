from django.urls import path

from authentication.authentication_views import Login, LoginRequiredTest, RenewToken, Logout
from authentication.user_views import LogoutEverywhereElse, LogoutByRTPK, GetRTPKs, ChangePassword

urlpatterns = [
    path('login', Login.as_view()),
    path('renew', RenewToken.as_view()),
    path('getrtpks', GetRTPKs.as_view()),
    path('logout', Logout.as_view()),
    path('logout/all', LogoutEverywhereElse.as_view()),
    path('logout/<int:pk>', LogoutByRTPK.as_view()),
    path('changepassword', ChangePassword.as_view()),
    path('loginrequiredtest', LoginRequiredTest.as_view())
]
