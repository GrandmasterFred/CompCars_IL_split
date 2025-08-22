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

import re

def contains_valid_year(s):
    match = re.search(r"\b(19[0-9]{2}|20[0-9]{2}|2100)\b", s)
    return match.group(0) if match else None


def save_list_to_txt(data_list, file_path):
    """
    Saves a list of elements to a text file, one element per line.

    :param data_list: List of elements to save
    :param file_path: Path to the output .txt file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data_list:
                f.write(str(item) + '\n')
        print(f"List saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")


# goes through each of the vehicles provided in a cluster, and then finds the corresponding from the list, when it is taken from the list, it will be removed from the list to saev comp memory for later searches 
def sep_list_by_chunk(chunk, lst):
    """
    takes a dict of vehicles, iterates over them, find their count, and then takes them out from the list. 

    returns original list with extracted remoed, and extracted list
    """

    # this is the set of values that will be crossed checked against 
    req_values = set()

    for key, item in chunk.items():
        #this one iterates over the vehicles, and we are just extracting out the set i guess, makes it easier 
        # remember, the ones we encoded starts from 0-280, but the corresponding folder for compcars goes from 1-281
        target = int(item['count']) + 1 # from 0-281-1-281
        req_values.add(target)
    
    # this will go through the list, and then take items from it. will also create a new list that essentially loses the items that were taken from it 
    new_lst = []
    extracted_lst = []
    for item in lst:
        # they are encoded like 1/f39352d495ba11.jpg, so we split usin /
        watching_target = int(item.split(r'/')[0])   # should get the first value 
        # then we see if it exists inside the set or not 
        if watching_target in req_values:
            extracted_lst.append(item)
        else:
            new_lst.append(item)

    return new_lst, extracted_lst

import os 

def generate_chunked_list(output_folder_name, tasks, lst, name):
    """
    when given a list with multiple dicts, for each dict, generate a chunked list and save it  
    """

    # iterates over the whole list 
    for idx,  item in enumerate(tasks):
        # generate temporary target folder based on task
        curr_target_folder = os.path.join(str(output_folder_name), f'{str(output_folder_name)}_{str(idx)}')
        os.makedirs(name=curr_target_folder,exist_ok=True)

        # getting the current list based on the gievn list. The given list will be modified to remoev the extracted entries 
        lst, chunk_lst = sep_list_by_chunk(
            chunk=item, lst=lst
        )

        # we then save the list to a file inside that folder, simple 
        curr_save_file_path = os.path.join(curr_target_folder, f'{name}_{idx}.txt')
        save_list_to_txt(data_list=chunk_lst, file_path=curr_save_file_path)

def split_dict_by_year(data, n_chunks):
    # 1. Sort items by 'year'
    sorted_items = sorted(data.items(), key=lambda x: contains_valid_year(x[1]['release_date']))
    
    # 2. Compute chunk sizes
    total_items = len(sorted_items)
    base_chunk_size = total_items // n_chunks
    remainder = total_items % n_chunks
    
    # 3. Build chunks
    chunks = []
    start = 0
    for i in range(n_chunks):
        if i == 0:  # first chunk gets the remainder
            size = base_chunk_size + remainder
        else:
            size = base_chunk_size
        chunk_items = sorted_items[start:start + size]
        chunks.append(dict(chunk_items))
        start += size
    
    return chunks

def read_file_return_list(target):
    lst = []
    try:
        with open(target) as file:
            for line in file:
                lst.append(line.rstrip())
    except Exception as e:
        print(f'error of {e}')
    return lst