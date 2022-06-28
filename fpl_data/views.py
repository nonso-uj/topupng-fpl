from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Prediction, Token
from accounts.models import Referral
from .forms import PredictionForm, TokenForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json, os, schedule, time
from .json_loader import scores_data, get_data


from accounts.models import fplUser
# Create your views here.



@login_required(login_url='login')
def admin_dash(request):
    if not request.user.is_superuser:
        messages.warning(request, 'Access Denied')
        return redirect('home')
    return render(request, 'admin-dash.html')


# AUTOMATES API CALLS
def scores_update(request):
    schedule.every(5).seconds.until('09:00').do(get_data)

    x = 0
    while True:
        schedule.run_pending()
        print('running scores func...')
        print(x)
        x += 1
        if x == 2:
            break
        time.sleep(5)
    messages.success(request, 'Updates started successfully')
    return redirect('admin-dash')



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
    messages.success(request, 'Points awarded successfully')
    return redirect('admin-dash')
    





# HOME VIEW FUNC
# AUTOMATE ADDING SCORES WITHOUT RELOAD WITH AJAX
# make more efficient, always going through all users, bad performance
@login_required(login_url='login')
def home_view(request):
    user = fplUser.objects.get(user=request.user)
    referrals = Referral.objects.all()
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
        u_dct[u] = p_ttl
        p_ttl = 0


    ndict = {}
    nlst = sorted(u_dct, key=u_dct.get, reverse=True)
    for w in nlst:
        ndict[w] = u_dct[w]


    dct = {}
    for r in referrals:
        # u = r.referrer
        if r in dct:
            dct[r] += 1
        else:
            dct[r] = 1


    rdct = {}
    rlst = sorted(dct, key=dct.get, reverse=True)
    for w in rlst:
        rdct[w] = dct[w]
    




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
        'users': ndict,
        'referrals': rdct
    }
    return render(request, 'home.html', context)







# add decoretor for tokens so you cant enter without tokens
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
                messages.success(request, 'You can only predict a game once')
                return redirect('home')
        except ObjectDoesNotExist:
            form = PredictionForm(request.POST)
            if form.is_valid():
                token = Token.objects.filter(user__exact=user,used__exact=False).first()
                if token == None:
                    messages.success(request, 'Please add more transaction ids from Topup.ng to continue predicting')
                    return redirect('home')
                else:
                    token.used = True
                    token.save()
                home_name = request.POST.get('home_name')
                home_logo = request.POST.get('home_logo')
                away_name = request.POST.get('away_name')
                away_logo = request.POST.get('away_logo')
                prediction = form.save(commit=False)
                prediction.user = user
                prediction.fixture_id = pk
                prediction.home_name = home_name
                prediction.home_logo = home_logo
                prediction.away_name = away_name
                prediction.away_logo = away_logo
                prediction.token = token
                prediction.is_active = True
                prediction.save()
                messages.success(request, 'Your prediction has been added successfully')
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
                messages.success(request, 'This Transaction id has been used already, please check your spelling or try another')
                return redirect('tid')
        except ObjectDoesNotExist:
            if form.is_valid():
                token = form.save(commit=False)
                user = fplUser.objects.get(user=request.user)
                token.user = user
                token.save()
                messages.success(request, 'YourTransaction id was added successfully')
                return redirect('home')
    
    context = {
        'form': form
    }
    return render(request, 't_id.html', context)

