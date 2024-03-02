# nltk is to split the english files
import nltk 
from nltk.tokenize import sent_tokenize
import os


input_folder = "Splitting_files/English_new/"
output_folder = "Splitting_files/English_output/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

english_all_files = os.listdir(input_folder)
no_of_files = len(english_all_files)
print(no_of_files)

for file in english_all_files:
    english_file = input_folder + file
    print(english_file)
    eng_ptr = open(english_file, "r")
    english_content = eng_ptr.read()
    eng_ptr.close()
    eng_ptr = open(english_file, "r")
    sen_num = eng_ptr.readlines()
    total_sen = len(sen_num)
    print(f"Previous ---> {total_sen}")

    # splitting the content on sentence level
    english_sen = sent_tokenize(english_content)
    size1 = len(english_sen)
    # print(size1)

    score = 0
    #  writing the sentence in a  file
    eng_output_file = output_folder + file
    file_1 = open(eng_output_file, 'w')
    for j in range(size1):
        sen = english_sen[j].strip()
        if(sen == "." or sen == "\n"):
            pass
        else:
            score+=1
            file_1.write(sen + "\n")
    print(f"After ---> {score}")
    eng_ptr.close()
    file_1.close()