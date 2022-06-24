from django.shortcuts import render, redirect, get_object_or_404
from .models import Prediction, fplUser, Token
from .forms import UserRegForm, PredictionForm, TokenForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json
import os
# Create your views here.

pwd = os.path.dirname(__file__)


def scores_data():
    with open(pwd + '/json_data/fpl_data.txt','r') as f:
        raw_str = f.read()
    data = json.loads(raw_str)
    return data


def points_view(request):
    predictions = Prediction.objects.filter(is_active__exact=True)
    # print(len(predictions))
    games = scores_data()
    games = games['response'][-20:]
    # print(len(games))
    fixtures = []

    for prediction in predictions:
        for game in games:
            if int(game['fixture']['id']) == int(prediction.fixture_id):
                if int(prediction.home_goals) == int(game['goals']['home']) and int(prediction.away_goals) == int(game['goals']['away']):
                    np = Prediction.objects.get(id=prediction.id, fixture_id=game['fixture']['id'])
                    if np.points == 3:
                        pass
                    else:
                        np.is_correct = True
                        np.points = 3
                        np.save()

    context = {
        'fixtures': fixtures
    }
    return render(request, 'points.html', context)








@login_required(login_url='login')
def home_view(request):
    user = fplUser.objects.get(user=request.user)
    users = fplUser.objects.all()
    predictions = Prediction.objects.filter(user=user)
    fixtures = []

    u_dct = {}
    p_ttl = 0
    for u in users:
        ps = Prediction.objects.filter(user=u)
        for p in ps:
            np = Prediction.objects.get(id=p.id)
            p_ttl += np.points
        u_dct[u.user.username] = p_ttl
        p_ttl = 0

    ndict = {}
    nlst = sorted(u_dct, key=u_dct.get, reverse=True)
    for w in nlst:
        ndict[w] = u_dct[w]


    games = scores_data()
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

    fixtures = fixtures[-20:]
    context = {
        'fixtures': fixtures,
        'predictions': predictions,
        'users': ndict
    }
    return render(request, 'home.html', context)



# add decoretor for tokens
def predictor_view(request, pk):
    form = PredictionForm()
    fixture = []

    games = scores_data()
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
        user = fplUser.objects.get(user=request.user)
        try:
            predicted = Prediction.objects.get(user = user, fixture_id=pk)
            if predicted:
                # add already predicted message later
                return redirect('predicted')
        except ObjectDoesNotExist:
            form = PredictionForm(request.POST)
            if form.is_valid():
                token = Token.objects.filter(user__exact=user ,used__exact=False).first()
                if token == None:
                    return redirect('no tokens')
                else:
                    token.used = True
                    token.save()
                home_name = request.POST.get('home_name')
                away_name = request.POST.get('away_name')
                prediction = form.save(commit=False)
                prediction.user = user
                prediction.fixture_id = pk
                prediction.home_name = home_name
                prediction.away_name = away_name
                prediction.token = token
                prediction.is_active = True
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