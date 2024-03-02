import os
import shutil

input_folder = "seven_lan/Malayalam (copy)/"
output_folder = "seven_lan/renamed_malayalam_new/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


all_files = os.listdir(input_folder)

size = len(all_files)

# print(all_files[0][-8:-4])

months_dict = {
    1: "ജനുവരി",
    2: "ഫെബ്രുവരി",
    3: "മാർച്ച്",
    4: "ഏപ്രിൽ",
    5: "മെയ്",
    6: "ജൂൺ",
    7: "ജൂലൈ",
    8: "ഓഗസ്റ്റ്",
    9: "സെപ്റ്റംബർ",
    10: "ഒക്ടോബർ",
    11: "നവംബർ",
    12: "ഡിസംബർ"    
}






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
no = 0
for i in range(size):
    check = 0
    for key in months_dict:
        if(months_dict[key] in all_files[i]):
            # past_year = all_files[i][0:4]
            # new_year = year_dict[past_year]
            # output_file = output_folder + str(key) + "_" + new_year + ".txt"
            output_file = output_folder + str(key) + "_" + all_files[i][-8:-4] + ".txt"
            input_file = input_folder + all_files[i]
            shutil.move(input_file, output_file)
            check = 1
            break
    if(not check):
        no+=1
        print(f"{all_files[i]} is not moved")

print(no)
