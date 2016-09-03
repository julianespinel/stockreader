import inflection

def json_keys_to_lower_and_snake_case(json):
    if isinstance(json, list):
        return [json_keys_to_lower_and_snake_case(element) for element in json]
    elif isinstance(json, dict):
        return dict((inflection.underscore(key), json_keys_to_lower_and_snake_case(value)) for key, value in json.items())
    else:
        return json