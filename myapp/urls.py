from django.urls import path
from .views import UserRegisterView, UserLoginView,BloggerUserRegisterView,MakeleView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('blogger', BloggerUserRegisterView.as_view(), name='blogger'),
    path('makale', MakeleView.as_view(), name='blogger'),
]
