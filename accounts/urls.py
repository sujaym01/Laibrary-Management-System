# from django.urls import path
# from .views import UserRegistrationView, UserLoginView, UserLogoutView,UserLibraryAccountUpdateView
 
# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='register'),
#     path('login/', UserLoginView.as_view(), name='login'),
#     path('logout/', UserLogoutView.as_view(), name='logout'),
#     path('profile/', UserLibraryAccountUpdateView.as_view(), name='profile')
# ]

from django.urls import path
# from . views import *
# from .import views
from . views import (UserRegistrationView, UserLoginView, UserLogoutView, 
            UserProfileUpdateView, UserProfileView,
            password_change,UserPasswordChangeView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    # path('password_change/', password_change, name='password_change'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change')
    # path('password_change/', views.password_change, name='password_change'),
]