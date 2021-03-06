"""Donate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from App1.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name = "index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name ="register"),
    path('addDonation/', AddDonationView.as_view(), name="add_donation"),
    path('activate/<str:uid>/<str:token>', Activate.as_view(), name='activate'),
    path('password/<str:uid>/<str:id>', ActivateResetPasswordView.as_view(), name='resetPassword'),
    path('profile/', Profile.as_view(), name='profile'),
    path('changePassword/', ChangePasswordView.as_view(), name='changePassword'),
    path('resetPassword/', ResetPasswordView.as_view(), name='activateResetPassword'),
    path('editProfile/', EditProfileView.as_view(), name='editProfile'),
    path('sendEmail/', sendEmailView.as_view(), name='sendEmail'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('summaryDonation/', SummaryDonationView.as_view(), name='summaryDonationn'),

]
