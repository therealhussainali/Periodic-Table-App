import json

def get_element_data():
    with open('elements.json') as f:
        elements = json.load(f)
    return elements
