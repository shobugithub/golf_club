from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from golf.form import EmailForm, LoginForm, RegisterForm
from golf.forms import News_letter, Become_member
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Contact_us, Events, User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from golf.tokens import account_activation_token
from django.contrib.auth import logout
from django.core.mail import send_mail, EmailMessage
# Create your views here.

def index_page(request):
    form = News_letter()
    become_member = Become_member()
    events = Events.objects.all()

    if request.method == "POST":
        form = News_letter(request.POST)
        become_member = Become_member(request.POST)
        if form.is_valid():
            form.save()

        if become_member.is_valid():
            full_name = become_member.cleaned_data['full_name']
            email = become_member.cleaned_data['email_address']
            comments = become_member.cleaned_data['comments']

            Contact_us.objects.create(
                full_name=full_name,
                email_address=email,
                comments=comments
            )
    context = {
        'form':form,
        'events': events
    }
    return render(request, 'golf/index.html', context)

def event_listing(request):
    events = Events.objects.all()
    contex = {
        'events':events
    }
    return render(request, 'golf/event-listing.html', contex)

def event_detail(request, pk):
    event = Events.objects.get(id=pk)
    context = {
        'event': event
    }
    return render(request, 'golf/event-detail.html', context)


class LoginPage(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'golf/auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

        return render(request, 'golf/auth/login.html', {'form': form})
    


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'golf/auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()

            current_site = get_current_site(request)
            subject = 'Verify your email'
            message = render_to_string('golf/auth/email/activation.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = 'html'
            email.send()

            return redirect('verify_email_done')

        return render(request, 'golf/auth/register.html', {'form': form})



class LogoutPage(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

    def post(self, request):
        return render(request, 'golf/auth/logout.html')


def sending_email(request):
    sent = False

    if request.method == 'POST':
        form = EmailForm(request.POST)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        to = request.POST.get('to')
        send_mail(subject, message, from_email, [to])
        sent = True

    return render(request, 'golf/blog/sending-email.html', {'form': form, 'sent': sent})



def verify_email_done(request):
    return render(request, 'golf/blog/auth/email/verify-email-done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('verify_email_complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'golf/blog/auth/email/verify-email-confirm.html')


def verify_email_complete(request):
    return render(request, 'golf/blog/auth/email/verify-email-complete.html')

