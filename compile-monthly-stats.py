from datetime import date
import json, os

today = date.today()
current_year = today.year
current_month = today.month
previous_month = current_month - 1 if current_month > 1 else 12
current_year = current_year if previous_month < 12 else current_year - 1

str_previous_month = f'0{previous_month}' if previous_month < 10 else str(previous_month)

folder_path = os.path.join("logs", str(current_year), str_previous_month)
is_valid_path = os.path.exists(folder_path)

files_list = os.listdir(folder_path)

monthly_aggregate = {}

def add_data(type, prev_data, new_data):
    if type == 'grand_total':
        return {}
    elif type == 'languages':
        return {}
    elif type == 'editors':
        return {}
    elif type == 'range':
        return prev_data
    else:
        return {}

for json_file in files_list:
    file = open(os.path.join(folder_path, json_file), mode='r')
    content = file.read()
    content = dict(json.loads(content))
    required_keys = ['grand_total', 'languages', 'range', 'editors']
    
    date = json_file.replace(".json", "")
    file_data = {}

    for key, value in content.items():
        data = value[0]
        
        for item_key in required_keys:
            prev_value = file_data.get(item_key)

            if not prev_value:
                file_data.update({
                    item_key: data.get(item_key)
                })
            else:
                compiled_values = add_data(item_key, prev_value, data.get(item_key))
                file_data.update({
                    item_key: compiled_values
                })

    monthly_aggregate.update({
        date: file_data
    })

filename = f'monthly_aggregate-{str_previous_month}-{current_year}.json'
file = open(os.path.join("logs", str(current_year), str_previous_month, filename), "w+")
file.write(json.dumps(monthly_aggregate, indent=2))
file.close()
