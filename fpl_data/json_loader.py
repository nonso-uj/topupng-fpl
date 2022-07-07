from pytz import timezone
import requests, schedule, time, os, json
from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

pwd = os.path.dirname(__file__)



class StartSchedule:

    def __init__(self):
        self.count = 0
        self.ender = 0

    def starter(self, request):
        if request.method == 'GET':
            print('got here2')
            schedule.clear()
            self.ender = 1
            messages.success(request, 'Updates stopped successfully THIS TIME')
            return redirect('admin-dash')

        if request.method == 'POST':
            print('got here3')
            self.ender = 0
            interval = int(request.POST.get('interval'))
            print(interval)
            # interval has to be under 30s
            schedule.every(interval).seconds.until("23:59").do(self.get_data, request)

            while True:
                schedule.run_pending()
                print('running scores func...')
                print(self.count)
                if self.count == 2 or self.ender == 1:
                    schedule.clear()
                    break
                time.sleep(1)
            messages.success(request, 'Scores done')
            return redirect('admin-dash')
            # return JsonResponse({'result':'Updates started successfully'})
        # schedule.clear()
        messages.success(request, 'Updates stopped successfully')
        return redirect('admin-dash')
        # return JsonResponse({'result':'Something went wrong'})






    def get_data(self, request):
        print('running json_loader...')
        league = request.POST.get('league')
        fixture_date = request.POST.get('date')
        if fixture_date == '' or None:
            fixture_date = date.today()
        url = "https://v3.football.api-sports.io/fixtures"

        querystring = {
            'league':league,
            'season':'2022',
            'date': fixture_date,
        }


        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': "895f0f2907cd027276b3a15febe3929d"
            }

        response = requests.request('GET', url, headers=headers, params=querystring)

        json_data = json.loads(response.text)

        with open(pwd + '/json_data/fpl_data.json', 'w') as j:
            json.dump(json_data, j, indent=4)

        self.count += 1
        




def scores_data():
    with open(pwd + '/json_data/fpl_data.txt','r') as f:
        raw_str = f.read()
    data = json.loads(raw_str)
    return data



