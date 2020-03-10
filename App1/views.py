from django.shortcuts import render
import datetime
import re
import pdb
# Create your views here.
from django.http import HttpResponse, JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

        return render(request, 'App1/index.html', {"bags": bags,
                                                   "institutionsNumber": institutionsNumber,
                                                   "Fundations": Fundations,
                                                   "Organizations": Organizations,
                                                   "Collections": Collections})


@method_decorator(csrf_exempt, name='dispatch')
class AddDonationView(View):
    def get(self, request):
        if request.user.id is not None:
            categories = Category.objects.all()
            institutions = Institution.objects.all()

            return render(request, 'App1/form.html', {"categories": categories,
                                                      "institutions": institutions})
        else:
            return render(request, 'App1/login.html')

    def post(self, request):

        quantity = request.POST.get("quantity")


        categories2 = request.POST.get("categories2").split()


        institution = int(request.POST.get("institution"))
        institution = Institution.objects.get(pk=institution)
        address = request.POST.get("city")
        phone_number = int(request.POST.get("phone_number"))
        city = request.POST.get("city")
        zip_code = request.POST.get("zip_code")
        pick_up_date = request.POST.get("pick_up_date")
        pick_up_date = datetime.datetime.strptime(pick_up_date, "%Y-%m-%d").date()

        pick_up_time = request.POST.get("pick_up_time")
        pick_up_time = datetime.datetime.strptime(pick_up_time, "%H:%M").time()
        # pdb.set_trace()

        pick_up_comment = request.POST.get("pick_up_comment")
        # pdb.set_trace()

        user = request.user.id

        Donation.objects.create(quantity=quantity, institution=institution,
                                address=address, phone_number=phone_number, city=city,
                                zip_code=zip_code, pick_up_date=pick_up_date,
                                pick_up_time=pick_up_time, pick_up_comment= pick_up_comment, is_taken = False, user = request.user)

        return render(request, 'App1/login.html')


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
        specialCharacters = ['$', '#', '@', '!', '*']

        if password == password2 and user_name != "" and user_surname != "" and email != "" and password != "":
            if len(list(password2)) < 8:
                return render(request, 'App1/register.html', {"info": "Hasło jest zbyt krótkie"})
            elif not re.search(r"[\d]+", password2):
                return render(request, 'App1/register.html', {"info": "Upewnij się, że Twoje hasło zawiera cyfrę"})
            elif re.search(r"[A-Z]+", password2) is None:
                return render(request, 'App1/register.html',
                              {"info": "Upewnij się, że Twoje hasło zawiera wielką literę"})
            elif not re.search(r"[?!@#$%^&*~]+", password2):
                return render(request, 'App1/register.html',
                              {"info": "Upewnij się, że Twoje hasło zawiera znak specjalny"})

            user = User.objects.create_user(is_active=False, username=email, password=password, first_name=user_name,
                                            last_name=user_surname, email=email)

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
        else:
            return render(request, 'App1/register.html', {"info": "Wypełnij wszystkie pola"})


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
            return render(request, 'App1/index.html')

        else:
            return HttpResponse('Activation link is invalid!')


class Profile(View):
    def get(self, request):
        user = request.user
        id = request.user.id
        donations = Donation.objects.filter(user_id=id).order_by('-is_taken')
        return render(request, 'App1/profile.html', {"user": user, "donations": donations})

    def post(self, request):
        id = request.POST.get("button")
        taken = Donation.objects.get(id=id).is_taken
        Donation.objects.filter(id=id).update(pick_up_date=datetime.date.today().isoformat())
        Donation.objects.filter(id=id).update(pick_up_time=datetime.time())
        if taken == True:
            Donation.objects.filter(id=id).update(is_taken=False)
        else:
            Donation.objects.filter(id=id).update(is_taken=True)
        return redirect("profile")


class ChangePasswordView(View):
    def get(self, request):
        return render(request, "App1/changePassword.html")

    def post(self, request):
        oldpassword = request.POST.get("oldpassword")
        user = authenticate(username=request.user.email, password=oldpassword)

        if user is None:
            return render(request, "App1/changePassword.html", {"user": user, "info": "Podałeś błędne hasło"})
        else:

            newpassword1 = request.POST.get("newpassword1")
            newpassword2 = request.POST.get("newpassword2")
            if newpassword1 == newpassword2 and newpassword2 != "":
                u = User.objects.get(id=request.user.id)
                u.set_password(newpassword2)
                u.save()
                return render(request, "App1/changePassword.html", {"user": user, "info": "Hasło zmienione"})
            else:
                return render(request, "App1/changePassword.html",
                              {"user": user, "info": "Podaj dwa takie same hasła, hasło musi zawierać znaki"})


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

            return render(request, "App1/resetPassword.html", {"info": "Wysłano email"})
        else:
            return render(request, "App1/resetPassword.html", {"info": "Nie ma takiego emaila"})


class ActivateResetPasswordView(View):
    def get(self, request, uid, id):

        uid = force_text(urlsafe_base64_decode(uid))
        if len(User.objects.filter(tokenResetPassword=uid, id=id)) == 1:
            return render(request, 'App1/newPassword.html')

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
                          {"info": "Podaj dwa takie same hasła, hasło musi zawierać znaki"})


class EditProfileView(View):
    def get(self, request):
        user = request.user
        return render(request, "App1/editProfile.html", {"user": user})

    def post(self, request):
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if len(User.objects.filter(email=email)) == 1:
            return render(request, "App1/editProfile.html", {"info": "podany email już istnieje"})
        u = request.user
        if first_name is not None and first_name != "":
            u.first_name = first_name
        if last_name is not None and last_name != "":
            u.last_name = last_name
        if email is not None and email != "":
            u.email = email
        u.save()
        return render(request, "App1/editProfile.html", {"info": "Dane zmienione"})


class sendEmailView(View):
    def post(self, request):
        message = request.POST.get("message")
        first_name = request.POST.get("namee")
        last_name = request.POST.get("surname")

        mail_subject = 'Wiadomość od użytkownika'

        message = f"{first_name} {last_name} {message}"
        emails = User.objects.filter(is_superuser=True)
        for element in emails:
            emailadress = element.email
            email = EmailMessage(mail_subject, message, to=[emailadress])
            email.send()
        return render(request, "App1/index.html")

class ConfirmationView(View):
    def get(self, request):
        return render(request, "App1/form-confirmation.html")

@method_decorator(csrf_exempt, name='dispatch')
class SummaryDonationView(View):
    def post(self, request):
        Summ_quantity = request.POST.get("quantity")
        pdb.set_trace()
        Summ_categories2 = request.POST.get("categories2").split()

        # Summ_institution = int(request.POST.get("institution"))
        # Summ_institution = Institution.objects.get(pk=institution)
        # Summ_address = request.POST.get("city")
        # Summ_phone_number = int(request.POST.get("phone_number"))
        # Summ_city = request.POST.get("city")
        # Summ_zip_code = request.POST.get("zip_code")
        # Summ_pick_up_date = request.POST.get("pick_up_date")
        # Summ_pick_up_date = datetime.datetime.strptime(pick_up_date, "%Y-%m-%d").date()
        #
        # Summ_pick_up_time = request.POST.get("pick_up_time")
        # Summ_pick_up_time = datetime.datetime.strptime(pick_up_time, "%H:%M").time()
        # # pdb.set_trace()
        #
        # Summ_pick_up_comment = request.POST.get("pick_up_comment")
        # # pdb.set_trace()
        return JsonResponse({'Summ_quantity': Summ_quantity,
                             'Summ_categories2': Summ_categories2,
                             'foo': 'bar',
                             'foo': 'bar',
                             'foo': 'bar',
                             'foo': 'bar',
                             'foo': 'bar',
                             'foo': 'bar',
                             'foo': 'bar',
                             'foo': 'bar',
                             })
