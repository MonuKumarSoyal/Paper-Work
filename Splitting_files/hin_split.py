# inltk is to split the hindi files
import inltk
# setup('hi')
from indicnlp.tokenize import sentence_tokenize
import os


input_folder = "Splitting_files/Hindi_new/"
output_folder = "Splitting_files/Hindi_output/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

hindi_all_files = os.listdir(input_folder)
no_of_files = len(hindi_all_files)
print(no_of_files)

for file in hindi_all_files:
    hindi_file = input_folder + file
    hin_ptr = open(hindi_file, "r")
    hindi_content = hin_ptr.read()

    # splitting the content on sentence level
    hindi_sen = sentence_tokenize.sentence_split(hindi_content, lang='hi')
    size1 = len(hindi_sen)
    print(size1)


    #  writing the sentence in a  file
    hin_output_file = output_folder + file
    file_1 = open(hin_output_file, 'w')
    for j in range(size1):
        sen = hindi_sen[j].strip()
        if(sen == '।'or sen == "\n"):
            pass
        else:
            file_1.write(sen + "\n")

    hin_ptr.close()
    file_1.close()



