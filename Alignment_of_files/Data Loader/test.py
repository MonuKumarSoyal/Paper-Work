import sys
import os
sys.path.insert(0, "/home/user/Documents/MonuKumarSoyal/Machine_Learning_Internship/split")

from eng_hin_splitter_together import Spiltter

index = 0
hindi_file = "split/dec_hindi_input.txt"
english_file = "split/dec_eng_input.txt"
hindi_output = "H/H"+str(index)+".txt"
english_output = "E/E"+str(index)+".txt"
split_obj = Spiltter(hindi_file, english_file, hindi_output, english_output)
split_obj.preprocess_hin()
split_obj.preprocess_eng()
split_obj.split_hin()
split_obj.split_eng()
split_obj.print_hin()
split_obj.print_eng()
split_obj.output_file.close()