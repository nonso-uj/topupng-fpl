from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, response
from .forms import PredictionForm, TokenForm
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json, os, schedule, time
from .json_loader import scores_data, get_data
from django.urls import reverse


from .models import Prediction, Token
from accounts.models import fplUser
# from accounts.models import Referral
# Create your views here.



@login_required(login_url='login')
def admin_dash(request):
    if not request.user.is_superuser:
        messages.warning(request, 'Access Denied')
        return redirect('home')
    
    users = fplUser.objects.all()
    fusers = users.order_by('-total_points')
    rusers = users.order_by('-total_referrals')

    context = {
        'fusers': fusers,
        'rusers': rusers
    }
    return render(request, 'admin-dash.html', context)











# puts json in dictionary for frontend
def get_scores(request):
    if request.method == 'GET':
        
        fixtures = []
        games = scores_data()

        for game in games['response']:
            if game['goals']['home'] == None or game['goals']['away'] == None:
                game['goals']['home'] = '0'
                game['goals']['away'] = '0'
            fixtures.append({
                'fixture_id' :game['fixture']['id'],
                'home_logo' :game['teams']['home']['logo'],
                'home_name' :game['teams']['home']['name'],
                'home_goals' :game['goals']['home'],
                'away_logo' :game['teams']['away']['logo'],
                'away_name' :game['teams']['away']['name'],
                'away_goals' :game['goals']['away'],
                'link': reverse('predict', args=[game['fixture']['id']])
            })

        fixtures = fixtures[-20:]
        # predictions = serializers.serialize('json', list(predictions))
        return JsonResponse({'fixtures':list(fixtures)})
        # , 'predictions':predictions})




def get_predicts(request):
    if request.method == 'GET':
        user = fplUser.objects.get(user=request.user)
        predictions = Prediction.objects.filter(user=user)

        return JsonResponse({'predictions':list(predictions.values())})




def user_predictions(request, pk):
    if request.method == 'GET':
        user = fplUser.objects.get(id=pk)
        predictions = Prediction.objects.filter(user=user).order_by('-date_created')

        return JsonResponse({'predictions':list(predictions.values())})






# AUTOMATES API CALLS WITH AJAX AND USE FORM TO PASS IN TIME
def scores_update(request):
    if request.method == 'GET':
        schedule.clear()
        messages.success(request, 'Updates stopped successfully THIS TIME')
        return redirect('admin-dash')
    if request.method == 'POST':
        until = request.POST.get('until')
        print(until)
        schedule.every(10).seconds.until(until).do(get_data)

        x = 0
        while True:
            schedule.run_pending()
            print('running scores func...')
            print(x)
            x += 1
            if x == 20:
                break
            time.sleep(11)
        # messages.success(request, 'Updates started successfully')
        # return redirect('admin-dash')
        return JsonResponse({'result':'Updates started successfully'})
    schedule.clear()
    messages.success(request, 'Updates stopped successfully')
    return redirect('admin-dash')
    # return JsonResponse({'result':'Something went wrong'})


def stop_calls(request):
    schedule.clear()
    messages.success(request, 'Updates stopped successfully')
    return redirect('admin-dash')



def points_view(request):
    if not request.user.is_superuser:
        messages.warning(request, 'Access Denied')
        return redirect('home')
    predictions = Prediction.objects.filter(is_active__exact=True)
    games = scores_data()
    games = games['response'][-20:]
    
    for game in games:
        if game['goals']['home'] == None or game['goals']['away'] == None:
                game['goals']['home'] = '0'
                game['goals']['away'] = '0'
    
    # awards points to predictions
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
                        np.is_active = False
                        np.save()

    # updates total scores
    users = fplUser.objects.all()
    u_dct = {}
    p_ttl = 0
    for u in users:
        ps = Prediction.objects.filter(user=u)
        for p in ps:
            np = Prediction.objects.get(id=p.id)
            p_ttl += np.points
        u.total_points = p_ttl
        # updates total referrals
        u.get_referred_num()
        u.save()
        p_ttl = 0

    messages.success(request, 'Points awarded successfully')
    return redirect('admin-dash')
    





# HOME VIEW FUNC
# AUTOMATE ADDING SCORES WITHOUT RELOAD WITH  done
# make more efficient, always going through all users, bad performance done
# @login_required(login_url='login')
def home_view(request):
    form = TokenForm()

    predictions = []
    if request.user.is_authenticated:
        user = fplUser.objects.get(user=request.user)
        predictions = Prediction.objects.filter(user=user)

    users = fplUser.objects.all()
    fusers = users.order_by('-total_points')
    rusers = users.order_by('-total_referrals')

    fixtures = []
    games = scores_data()
    for game in games['response']:
            if game['goals']['home'] == None or game['goals']['away'] == None:
                game['goals']['home'] = '0'
                game['goals']['away'] = '0'

            fixtures.append({
                'fixture_id' :game['fixture']['id'],
                'home_logo' :game['teams']['home']['logo'],
                'home_name' :game['teams']['home']['name'],
                'home_goals' :game['goals']['home'],
                'away_logo' :game['teams']['away']['logo'],
                'away_name' :game['teams']['away']['name'],
                'away_goals' :game['goals']['away'],
                'link': reverse('predict', args=[game['fixture']['id']])
            })

    context = {
        'predictions': predictions,
        'fusers': fusers,
        'rusers': rusers,
        'form': form,
        'fixtures': fixtures
    }
    return render(request, 'home.html', context)



# USE AJAX TO GET TOTAL SCORES MAYBE


# add decorator for tokens so you cant enter without tokens
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
                'link': reverse('predict', args=[game['fixture']['id']])
            })

    if request.method == 'POST':
        user = fplUser.objects.get(user=request.user)
        try:
            predicted = Prediction.objects.get(user = user, fixture_id=pk)
            if predicted:
                # messages.success(request, 'You can only predict a game once')
                # return redirect('home')
                return JsonResponse({'result':'You can only predict a game once', 'class':'danger'})
        except ObjectDoesNotExist:
            form = PredictionForm(request.POST)
            if form.is_valid():
                token = Token.objects.filter(user__exact=user,used__exact=False).first()
                if token == None:
                    # messages.success(request, 'Please add more transaction ids from Topup.ng to continue predicting')
                    # return redirect('home')

                    return JsonResponse({'result':'Please add more transaction ids from Topup.ng to continue predicting', 'class':'danger'})
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
                # messages.success(request, 'Your prediction has been added successfully')
                # return redirect('home')
                
                return JsonResponse({'result':'Your prediction has been added successfully', 'class':'success'})
            else:
                return JsonResponse({'result':'Invalid Form', 'class':'danger'})


    context = {
        'form': form,
        'fixture': fixture
    }
    return JsonResponse({'fixture': list(fixture)})
    # return HttpResponse(form)
    # return render(request, 'predict.html', context)







def transaction_id_view(request):
    form = TokenForm()

    if request.method == 'POST':
        form = TokenForm(request.POST)
        token = request.POST.get('t_id')
        try:
            token = Token.objects.get(t_id=token)
            if token:
                # messages.success(request, 'This Transaction id has been used already, please check your spelling or try another')
                return JsonResponse({'result':'used'})
        except ObjectDoesNotExist:
            if form.is_valid():
                token = form.save(commit=False)
                user = fplUser.objects.get(user=request.user)
                token.user = user
                token.save()
                return JsonResponse({'result':'success'})
            else:
                return JsonResponse({'result':'error'})
        return JsonResponse({'result':'error'})

