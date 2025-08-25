This repo provides a method to split the Comprehensive Cars surveillance dataset ([link](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/)) into Incremental Learning applications, since there are no publically available methods to do so at the time of writing (25th August 2025). 

This repo contributes a standardized method to divide vehicles into incremental learning tasks based on the date of when the vehicles were released. 

The dates for when those vehicles were released were scraped from wikipedia, and its contents double checked and verified. Vehicles that are not logged on wikipedia were manually searched for and logged, with only a few exceptions wherein the data for the vehicles denoted in Comprehensive Cars were not available online. In this case, a (modifiable) placeholder date was placed in. 

To obtain the desired number of splits, CompCars_IL_split.py should be ran with the NUMBER_TASKS variable modified to suit the number of tasks needed. The script then divides up the vehicles based on year, and places any remainer into the first task. The train/test split is based on Comprehensive Cars' own train/test split. 

To modify the placeholder year, compcars_fill_in_gaps.py should be ran with the PLACEHOLDER_RELEASE_DATE varaible modified. 

The process of which the data was created was:
1. car_release_dates_wiki3.json, where web data was scraped
2. car_release_dates_wiki3_MANUAL_EDIT.json, where missing information was filled in
3. car_release_dates_wiki3_MANUAL_EDIT_CHECK.json, where another pass at the information was manually verified
4. car_release_dates_wiki_final.json, where vehicles without any found date is automatically filled in with their placeholder values


This final file car_release_dates_wiki_final.json encodes each vehicle model as a key inside a dictionary. Each key provides a release date, as well as its corresponding source if available. 

Running CompCars_IL_split.py provides each task with its own separate folder, with it going:
```
root_folder
  task_0
    train_set.txt
    test_set.txt
  task_1
    ...
```
where each train/test_set.txt is a list of image locations corresponding to the splits, for example: 
```
9/8472696bba54c4.jpg
9/61b62f87073b5d.jpg
9/e7dccbc630d2c4.jpg
9/747c1dd9e07a16.jpg
9/f7d061dfc2f433.jpg
9/9d916c83fa38f4.jpg
9/c993d4a6309836.jpg
9/4027e66cf0970e.jpg
9/1bfae5a8c1f4d2.jpg
9/fa934a680b5916.jpg
```
