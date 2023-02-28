from datetime import date, timedelta
import json
import os
import requests

keys = os.environ.get('WAKATIME_API_KEYS')

if keys:
    keys = keys.split(",")

BASE_URL = 'https://wakatime.com/api/v1/users/current'
yesterday = date.today() - timedelta(days=1)
formatted_date = yesterday.strftime('%m-%d-%Y')

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

def combine_user_summaries():
    summaries = {}
    for key in keys:
        user_details = get_user_details(key)
        stats = get_user_stats(key)

        username = user_details.get('data').get('username')
        stats = stats.get('data')

        print(f"adding stats for {username}")

        summaries.update({
            username: stats
        })
    return summaries


def create_or_update_file(stats_obj: dict):
    # Check if folder exists
    month = formatted_date.split("-")[0]
    year = formatted_date.split("-")[2]
    folder_path = os.path.join('logs', year, month)
    is_valid_path = os.path.exists(folder_path)

    if not is_valid_path:
        os.mkdir(folder_path)

    file = open(os.path.join(folder_path, f'{formatted_date}.json'), mode='w+')
    file.write(json.dumps(stats_obj, indent=2))
    file.close()

combined_stats = combine_user_summaries()
create_or_update_file(combined_stats)
