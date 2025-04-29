import json

def load_json():
    with open('json_to_csv_converter/sample.json') as file:
        data = json.load(file)

    return data

def flatten_dict(data, exterior_key=''):
    flat_dict = {}
    for key, value in data.items():
        if exterior_key:
            new_key = exterior_key + "_" + key
        else:
            new_key = key
        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value, new_key))
        else:
            flat_dict[new_key] = value

    return flat_dict



print(flatten_dict(load_json()))