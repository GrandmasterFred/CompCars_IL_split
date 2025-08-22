"""
this file reads the .mat file, and prints it out to a human readable format. Saves it to a .csv file for easy edits 
"""


import scipy.io as sio

from sp_functions import save_dict_to_json, load_dict_from_json

DATA = r'CompCarsData\sv_make_model_name.mat'
TARGET_SAVE = r'compcars_summary.json'

data = sio.loadmat(DATA)
print(data.keys())

storage_dict = {}
count = 0

for item in data['sv_make_model_name']:
    temp_dict = {
        'make': str(item[0][0]),
        'model': str(item[1][0]),
        'tag': int(item[2][0][0]),       # this is the internal compcars tag
        'year': 0,                  # encoded as 2020 for example, integer 
        'month': 0                  # encoded as 1~12, for the 12 months of the year 
    }
    print(f'{str(item[0][0])} {str(item[1][0])}')
    storage_dict[str(count)] = temp_dict
    count += 1

save_dict_to_json(data=storage_dict, filename=TARGET_SAVE)

# example load 
# storage_dict = load_dict_from_json(filename=TARGET_SAVE)

print(f'end of file')