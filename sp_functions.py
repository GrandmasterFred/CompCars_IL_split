import json

def save_dict_to_json(data: dict, filename: str) -> None:
    """
    Saves a Python dictionary to a JSON file.
    
    Args:
        data (dict): The dictionary to save.
        filename (str): Path to the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_dict_from_json(filename: str) -> dict:
    """
    Loads a dictionary from a JSON file.
    
    Args:
        filename (str): Path to the JSON file.
        
    Returns:
        dict: The loaded dictionary.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
