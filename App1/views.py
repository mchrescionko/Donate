from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import UpdateView, ListView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.core.mail import EmailMessage

from .tokens import *


from .models import *

class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        institutionsNumber = Institution.objects.all().count()
        Fundations = Institution.objects.filter(type=1)
        Organizations = Institution.objects.filter(type=2)
        Collections = Institution.objects.filter(type=3)
        bags = 0
        for donation in donations:
            bags = bags + int(donation.quantity)



        return render(request, 'App1/index.html', {"bags":bags,
                                                   "institutionsNumber":institutionsNumber,
                                                   "Fundations":Fundations,
                                                   "Organizations":Organizations,
                                                   "Collections":Collections})

class AddDonationView(View):
    def get(self, request):
        if request.user.id is not None:
            categories = Category.objects.all()
            institutions = Institution.objects.all()

            return render(request, 'App1/form.html', {"categories":categories,
                                                      "institutions":institutions})
        else:
            return render(request, 'App1/login.html')

    def post(self, request):
        bags = request.POST.get("bags")
        organization = request.POST.get("organization")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        data = request.POST.get("data")
        time = request.POST.get("time")
        more_info = request.POST.get("more_info")

        Donation.objects.create(city=city, zip_code = postcode, pick_up_date=data, pick_up_time=time, pick_up_comment=more_info, quantity=bags, institution=organization, address=address, phone_number=phone )

        return render(request, 'App1/index.html')



class LoginView(View):
    def get(self, request):
        return render(request, 'App1/login.html')

    def post(self, request):

        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return redirect("register")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):
    def get(self, request):
        return render(request, 'App1/register.html')

    def post(self, request):
        user_name = request.POST.get("name")
        user_surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2 and user_name != "" and user_surname != "" and email != "" and password != "":
            user = User.objects.create_user(is_active=False, username=email, password=password, first_name=user_name, last_name=user_surname, email=email)

            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = f"{current_site}/activate/{uid}/{token}"
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email = email

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')



class Activate(View):
    def get(self, request, uid, token):

        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)
            return render(request,'App1/index.html')

        else:
            return HttpResponse('Activation link is invalid!')

class Profile(View):
    def get(self, request):
        user = request.user
        id = request.user.id
        donations = Donation.objects.filter(user_id=id)
        return render(request,'App1/profile.html', {"user":user, "donations":donations})

class ChangePasswordView(View):
    def get(self, request):
        return render(request, "App1/changePassword.html")

    def post(self, request):
        oldpassword = request.POST.get("oldpassword")
        user = authenticate(username=request.user.email, password=oldpassword)

        if user is  None:
            return render(request, "App1/changePassword.html", {"user":user, "info":"Podałeś błędne hasło"})
        else:

            newpassword1 = request.POST.get("newpassword1")
            newpassword2 = request.POST.get("newpassword2")
            if newpassword1 == newpassword2 and newpassword2 != "":
                u = User.objects.get(id=request.user.id)
                u.set_password(newpassword2)
                u.save()
                return render(request, "App1/changePassword.html", {"user": user, "info": "Hasło zmienione"})
            else:
                return render(request, "App1/changePassword.html", {"user": user, "info": "Podaj dwa takie same hasła, hasło musi zawierać znaki"})

class ResetPasswordView(View):
    def get(self, request):
        return render(request, "App1/resetPassword.html")

    def post(self, request):
        email = request.POST.get("email")
        if len(User.objects.filter(email=email)) == 1:
            username = User.objects.get(email=email).username
            id = User.objects.get(email=email).id
            User.objects.get(id=id)
            token = uuid.uuid4()
            User.objects.update(tokenResetPassword=token)

            mail_subject = 'New password'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(token))
            activation_link = f"{current_site}/password/{uid}/{id}"
            message = "Hello {0},\n {1}".format(username, activation_link)
            to_email = email

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "App1/resetPassword.html", {"info":"Wysłano email"})
        else:
            return render(request, "App1/resetPassword.html", {"info":"Nie ma takiego emaila"})

class ActivateResetPasswordView(View):
    def get(self, request, uid, id):

        uid = force_text(urlsafe_base64_decode(uid))
        if len(User.objects.filter(tokenResetPassword=uid, id=id)) == 1:
            return render(request,'App1/newPassword.html')

        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request, id, uid):
        newpassword1 = request.POST.get("newpassword1")
        newpassword2 = request.POST.get("newpassword2")
        if newpassword1 == newpassword2 and newpassword2 != "":
            u = User.objects.get(id=id)
            u.set_password(newpassword2)
            u.save()
            return redirect("login")
        else:
            return render(request, "App1/newPassword.html",
                          { "info": "Podaj dwa takie same hasła, hasło musi zawierać znaki"})
