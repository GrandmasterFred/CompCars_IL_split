"""
this file splits compcars into tasks based on the year each of the models has been released. 

This draws on the .json file, and each vehicle's date of release/production

and with those production dates, it will sort out how many there are, and then also make it so that 

also, i should re-tag them with the proper info that i forgot to carry over from the original data 
"""

# this section sets the number of tasks that is needed

# this section gets the number of unique years there are, and see if they are divisible or not 

# loads in the .json file 

TARGET_SAVE = r'car_release_dates_wiki_final.json'
SPLITS_SAVE = r'car_tasks_IL.json'
TASKS_SAVE = r'car_tasks_IL_5_task'

INPUT_TRAIN_LIST = r'CompCarsData\train_surveillance.txt'
INPUT_TEST_LIST = r'CompCarsData\test_surveillance.txt'

NUMBER_TASKS = 5

from sp_functions import load_dict_from_json, contains_valid_year, save_dict_to_json, split_dict_by_year, read_file_return_list, generate_chunked_list

data = load_dict_from_json(filename=TARGET_SAVE)

# iterate through each of the items, and check for the numbber of uniques based on year 

result = split_dict_by_year(data=data, n_chunks=NUMBER_TASKS)

save_dict_to_json(data=result, filename=SPLITS_SAVE)

for idx, chunk in enumerate(result, start=1):
    print(f"Chunk {idx} ({len(chunk)} items):")


# this section now then uses those spilts, and then makes them into tasks

# it first loads in both train and test.txt, and then we start grabbing items from it, and then chucking it into a resulting list 

train_list = read_file_return_list(target=INPUT_TRAIN_LIST)
test_list = read_file_return_list(target=INPUT_TEST_LIST)

print(len(train_list))
print(len(test_list))
print(f'{len(train_list) + len(test_list)}')


generate_chunked_list(
    output_folder_name=TASKS_SAVE,
    tasks=result,
    lst=train_list,
    name='TRAIN'
)

generate_chunked_list(
    output_folder_name=TASKS_SAVE,
    tasks=result,
    lst=test_list,
    name='TEST'
)