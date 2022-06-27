from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import fplUser, Referral
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def referral_code_gen():
    User = get_user_model()
    random_number = User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

    while fplUser.objects.filter(referral_code=random_number):
        random_number = User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    return random_number


def referral_func(refer, fpl_user):
    try:
        print(fpl_user, refer)
        referrer = fplUser.objects.get(referral_code=refer)
        referral = Referral.objects.create(referrer = referrer, referred = fpl_user)
        referral.code = refer
        # referral.
        # referral.
        referral.save()
        # return redirect('login')
    except ObjectDoesNotExist:
        return HttpResponse('<h1>Wheres your referral code bitch</h1>')



def reg_view(request):
    User = get_user_model()
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False
            user.save()
            fpl_user = fplUser.objects.create(user=user)
            fpl_user.referral_code = referral_code_gen()
            fpl_user.save()
            refer = request.POST.get('referral')
            if refer is not None:
                referral_func(refer, fpl_user)
            print('lol')
            
                    # pass
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your account'
            # # make better template
            # message = render_to_string('active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.id)),
            #     'token': account_activation_token.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # # add company email
            # send_mail(mail_subject, message, 'nonso.udonne@gmail.com', [to_email])
            # return HttpResponse('<h1>Please confirm your email</h1>')

            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'user-reg.html', context)





def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # add template and message to 
        return HttpResponse('Thanks for email confirmation')
    else:
        return HttpResponse('Invalid Activation link')







def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {}
    return render(request, 'login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')