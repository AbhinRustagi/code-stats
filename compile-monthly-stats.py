import json
import os
from datetime import date

today = date.today()
current_year = today.year
current_month = today.month
previous_month = current_month - 1 if current_month > 1 else 12
current_year = current_year if previous_month < 12 else current_year - 1
str_previous_month = f'0{previous_month}' if previous_month < 10 else str(previous_month)

folder_path = os.path.join("logs", str(current_year), str_previous_month)
is_valid_path = os.path.exists(folder_path)


def add_time(prev_data, new_data):
    total_hours = prev_data.get('hours') + new_data.get('hours')
    total_minutes = prev_data.get('minutes') + new_data.get('minutes')
    total_seconds = prev_data.get('total_seconds') + new_data.get('total_seconds')

    seconds = None

    if prev_data.get('seconds') and new_data.get('seconds'):
        prev_seconds = prev_data.get('seconds')
        new_seconds = new_data.get('seconds')
        total = prev_seconds + new_seconds

        if total >= 60:
            remainder = total % 60
            quotient = total // 60
            seconds = remainder
            total_minutes += quotient

    if total_minutes >= 60:
        remainder = total_minutes % 60
        quotient = total_minutes // 60
        total_minutes = remainder
        total_hours += quotient
    
    if not seconds:
        digital = f"{total_hours}:{f'0{total_minutes}' if total_minutes < 10 else total_minutes}"
    else:
        digital = f"{total_hours}:{f'0{total_minutes}' if total_minutes < 10 else total_minutes}:{f'0{seconds}' if seconds < 10 else seconds}"

    minutes_percentage = total_minutes / 60
    decimal = total_hours + minutes_percentage
    text = f'{total_hours} hrs {total_minutes} mins'

    return {
        "decimal": decimal,
        "digital": digital,
        "hours": total_hours,
        "minutes": total_minutes,
        "text": text,
        "seconds": seconds,
        "total_seconds": total_seconds,
    }

def add_data(metric_type, prev_data, new_data, grand_total=None):
    if metric_type == 'grand_total':
        return add_time(prev_data, new_data)
    
    elif metric_type in ['languages', 'editors']:

        combined_data = {}
        grand_total_seconds = grand_total.get('total_seconds')

        for item in prev_data + new_data:
            name = item.get('name')
            item_value = item

            if not combined_data.get(name):
                percent = (item_value.get('total_seconds') * 100) / grand_total_seconds
                combined_data[name] = {
                    **item_value,
                    "percent": percent
                }
            else:
                prev = combined_data.get(name)
                cumulative = add_time(prev, item_value)

                percent = (item_value.get('total_seconds') * 100) / grand_total_seconds
                cumulative.update({
                    "percent": percent
                })

                combined_data[name] = cumulative


        return list(combined_data.values())
    elif metric_type == 'range':
        return prev_data
    else:
        return {}


def compile_monthly_stats():
    monthly_aggregate = {}
    files_list = os.listdir(folder_path)
    
    for json_file in files_list:
        file = open(os.path.join(folder_path, json_file), mode='r')
        content = file.read()
        content = dict(json.loads(content))
        required_keys = ['grand_total', 'languages', 'range', 'editors']

        date = json_file.replace(".json", "")
        file_data = {}

        for _, value in content.items():
            if isinstance(value, list):
                data = value[0]
            elif isinstance(value, dict):
                data = value
            else:
                continue

            for item_key in required_keys:
                prev_value = file_data.get(item_key)
                grand_total = file_data.get('grand_total')

                if not prev_value:
                    file_data.update({
                        item_key: data.get(item_key)
                    })
                else:
                    compiled_values = add_data(item_key, prev_value, data.get(item_key), grand_total)
                    file_data.update({
                        item_key: compiled_values
                    })

        monthly_aggregate.update({
            date: file_data
        })

    return monthly_aggregate

def save_monthly_stats():
    data = compile_monthly_stats()
    filename = f'monthly_aggregate-{str_previous_month}-{current_year}.json'
    file = open(os.path.join(folder_path, filename), "w+")
    file.write(json.dumps(data, indent=2))
    file.close()



save_monthly_stats()
