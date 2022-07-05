from django.shortcuts import render, redirect
from django.http import HttpResponse
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
from django.contrib import messages
from django.urls import reverse

from .models import fplUser
User = get_user_model()
# Create your views here.




def referrer_num(request, refer):
    try:
        referrer = User.objects.get(phone=refer)
        referrer = fplUser.objects.get(user=referrer)
        return referrer
    except ObjectDoesNotExist:
        messages.info(request, 'Referrers phone number incorrect or does not exist')
        # return redirect('reg')





def reg_view(request):
    User = get_user_model()
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            fpl_user = fplUser.objects.create(user=user)
            refer = request.POST.get('referrer')
            if refer is not None and refer != '':
                print(refer)
                referrer = referrer_num(request, refer)
                if referrer is not None:
                    print(referrer)
                    fpl_user.referrer = referrer
            fpl_user.save()

            # SEND MAIL PART
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            # make better template
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # add company email
            send_mail(mail_subject, message, 'nonso.udonne@gmail.com', [to_email])

            messages.info(request, 'Account registration successfull, Please confirm your email to Login')
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
        if user.fpluser.referrer is not None:
            user.fpluser.refer_valid = True
        user.save()
        # add login redirect and message to 
        login_link = reverse('login')
        return HttpResponse(f'<h1>Thanks for email confirmation</h1><p> Click {login_link} to go back</p>')
    else:
        return HttpResponse('Invalid Activation link')






# if user not active, go confirm your email
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Please confirm your email to Login')
            return redirect('login')


    context = {}
    return render(request, 'login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')
