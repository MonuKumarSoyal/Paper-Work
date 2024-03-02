import os
import shutil

input_folder = "mal/"
output_folder = "new_mal/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


all_files = os.listdir(input_folder)

size = len(all_files)


year_dict = {
    "2016": "2016",
    "2017": "2017",
    "2018": "2018",
    "2019": "2019",
    "2020": "2020",
    "2021": "2021",
    "2022": "2022",
    "2023": "2023",
    "২০১৬": "2016",
    "২০১৭": "2017",
    "২০১৮": "2018",
    "২০১৯": "2019",
    "২০২০": "2020",
    "২০২১": "2021",
    "২০২২": "2022",
    "২০২৩": "2023"
}

for i in range(size):
    check = 0
    for key in year_dict:
        if key in all_files[i]:
            new_path = output_folder + all_files[i] + key + ".txt"
            old_path = input_folder + all_files[i]
            shutil.move(old_path, new_path)
            check = 1
            break
    if(not check):
        print(f"{all_files[i]} is not moved")