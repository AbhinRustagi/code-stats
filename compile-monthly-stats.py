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

for json_file in files_list[:1]:
    file = open(os.path.join(folder_path, json_file), mode='r')
    content = file.read()
    content = dict(json.loads(content))
    required_keys = ['grand_total', 'languages', 'range', 'editors']
    
    file_data = {}

    for key in content.keys():
        value: dict = content[key][0]
        
        for item_key in value.keys():
            pass
