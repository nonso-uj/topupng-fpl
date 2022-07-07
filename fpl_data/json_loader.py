import requests, os, json
pwd = os.path.dirname(__file__)

def get_data():
    print('running json_loader...')
    url = "https://v3.football.api-sports.io/fixtures"

    querystring = {
        'league':'10',
        'season':'2021',
        'date':'2022-07-07',
    }


    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "895f0f2907cd027276b3a15febe3929d"
        }

    response = requests.request('GET', url, headers=headers, params=querystring)


    with open(pwd + '/json_data/fpl_data.txt', 'w') as j:
        j.write(response.text)





def scores_data():
    with open(pwd + '/json_data/fpl_data.txt','r') as f:
        raw_str = f.read()
    data = json.loads(raw_str)
    return data



