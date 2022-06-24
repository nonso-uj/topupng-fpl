from django.shortcuts import render, redirect, get_object_or_404
from .models import Prediction, fplUser, Token
from .forms import UserRegForm, PredictionForm, TokenForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
import json
import os
# import .json_data/fpl_data.txt
# Create your views here.

pwd = os.path.dirname(__file__)




def scores_view(request):
    user = fplUser.objects.get(user=request.user)
    predictions = Prediction.objects.filter(user=user)
    fixtures = []
    # logo name score vs score name logo
    
    with open(pwd + '/json_data/fpl_data.txt','r') as f:
        raw_str = f.read()
    games = json.loads(raw_str)
    for game in games['response']:
        fixtures.append({
            'fixture_id' :game['fixture']['id'],
            'home_logo' :game['teams']['home']['logo'],
            'home_name' :game['teams']['home']['name'],
            'home_goals' :game['goals']['home'],
            'away_logo' :game['teams']['away']['logo'],
            'away_name' :game['teams']['away']['name'],
            'away_goals' :game['goals']['away']
        })

    # print(fixtures[0]['home_name'])

    # for fixture in fixtures:
    #     print(fixture["home_name"])
    fixtures = fixtures[-20:]
    context = {
        'fixtures': fixtures,
        'predictions': predictions
    }
    return render(request, 'home.html', context)





def predictor_view(request, pk):
    form = PredictionForm()
    fixture = []


    with open(pwd + '/json_data/fpl_data.txt','r') as f:
        raw_str = f.read()
    games = json.loads(raw_str)
    for game in games['response']:
        if game['fixture']['id'] == pk:
            fixture.append({
                'fixture_id' :game['fixture']['id'],
                'home_logo' :game['teams']['home']['logo'],
                'home_name' :game['teams']['home']['name'],
                'away_logo' :game['teams']['away']['logo'],
                'away_name' :game['teams']['away']['name'],
            })

    if request.method == 'POST':
        print('here 1')
        user = fplUser.objects.get(user=request.user)
        try:
            print('here 2')
            predicted = Prediction.objects.get(user = user, fixture_id=pk)
            if predicted:
                print('here 3')
                # add already predicted message later
                return redirect('predicted')
        except ObjectDoesNotExist:
            form = PredictionForm(request.POST)
            print('here 4')
            if form.is_valid():
                print('here 5')
                token = Token.objects.filter(user__exact=user ,used__exact=False).first()
                if token == None:
                # if user.counter == 0:
                    print('here 6')
                    return redirect('no tokens')
                # elif user.counter > 0:
                else:
                    print('here 7')
                    # token = Token.objects.filter(used__exact=False).first()
                    # token = token[0]
                    token.used = True
                    token.save()
                    # user.counter -= 1
                    # user.save()
                print('here 8')
                home_name = request.POST.get('home_name')
                away_name = request.POST.get('away_name')
                prediction = form.save(commit=False)
                prediction.user = user
                prediction.fixture_id = pk
                prediction.home_name = home_name
                prediction.away_name = away_name
                prediction.token = token
                prediction.is_active = True
                print('here 9')
                prediction.save()
                return redirect('home')

    context = {
        'form': form,
        'fixture': fixture
    }
    return render(request, 'predict.html', context)







def transaction_id_view(request):
    form = TokenForm()

    if request.method == 'POST':
        form = TokenForm(request.POST)
        token = request.POST.get('t_id')
        try:
            token = Token.objects.get(t_id=token)
            if token:
                # add func to tell user used already
                return redirect('already used')
        except ObjectDoesNotExist:
            if form.is_valid():
                token = form.save(commit=False)
                user = fplUser.objects.get(user=request.user)
                user.counter += 1
                user.save()
                token.user = user
                token.save()
                return redirect('tid')
    
    context = {
        'form': form
    }
    return render(request, 't_id.html', context)





def reg_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            fplUser.objects.create(user=user)
            return redirect('login')
    
    context = {
        'form': form
    }
    return render(request, 'user-reg.html', context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {}
    return render(request, 'login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')