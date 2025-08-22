"""
this file will be used to fille in the gaps for the vehicles that do not have a searchable production/one the road day
"""

from sp_functions import load_dict_from_json, save_dict_to_json, contains_valid_year

# loading the modified wiki-scraped data

TARGET_SAVE = r'car_release_dates_wiki3_MANUAL_EDIT_CHECK.json'
RESULT_SAVE = r'car_release_dates_wiki_final.json'

PLACEHOLDER_RELEASE_DATE = "2000"

data = load_dict_from_json(filename=TARGET_SAVE)

# this section goes through each of the vehicle names, and finds the ones without any valid release date, and then replaces them with a set release date
item_count = 0
replacement_count = 0
for key, item in data.items():
    if not contains_valid_year(item['release_date']):
        print(f'{key} does not have a valid release date, it has {item["release_date"]}')
        item['release_date'] = PLACEHOLDER_RELEASE_DATE
        item['source'] = 'replacement'
        item['snippet'] = 'replacement'
        replacement_count += 1
    else:
        # getting the year itself i guess 
        year = contains_valid_year(item['release_date'])
    # adds in the item count, this is essentially the order they are in
    item['count'] = item_count
    item_count += 1


# then we save the data into a differnet .json file 
print(f'number of items replaced with placeholder is {replacement_count}')
save_dict_to_json(data=data, filename=RESULT_SAVE)
print(f'resulding file is saved to {RESULT_SAVE}')