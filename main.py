from datetime import date, timedelta
import json
import os
import requests

keys = os.environ.get('WAKATIME_API_KEYS')

if keys:
    keys = keys.split(",")

BASE_URL = 'https://wakatime.com/api/v1/users/current'
yesterday = date.today() - timedelta(days=1)
formatted_date = yesterday.strftime('%d-%m-%Y')
combined_stats = {}

def make_request(endpoint: str, params: dict):
    headers = {
        'Content-Type': 'application/json'
    }
    request = requests.get(
        BASE_URL + endpoint,
        params=params,
        headers=headers,
        timeout=3000,
    )

    return request.json()


# Get User Details
def get_user_details(key):
    params = {
        "api_key": key
    }
    user_details = make_request('', params)
    return user_details

# Get User Stats
def get_user_stats(key):
    endpoint = '/summaries'
    params = {
        "api_key": key,
        "start": formatted_date,
        "end": formatted_date
    }
    user_stats = make_request(endpoint, params)
    return user_stats

for key in keys:
    user_details = get_user_details(key)
    stats = get_user_stats(key)

    username = user_details.get('data').get('username')
    stats = stats.get('data')

    print(f"adding stats for {username}")

    combined_stats.update({
        username: stats
    })

file = open(os.path.join('logs', f'{formatted_date}.json'), mode='w+')
file.write(json.dumps(combined_stats, indent=2))
file.close()
