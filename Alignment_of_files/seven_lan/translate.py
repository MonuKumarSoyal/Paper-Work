import pandas as pd
import os
from googletrans import Translator
translator = Translator()

input_folder = "seven_lan/Bengali copy/"
all_files = os.listdir(input_folder)
size = len(all_files)
hindi_sentences = list()

output_folder_path = "All_data_translate_files/"

previous_line = 0
for i in range(size):
  hindi_translation = translator.translate(all_files[i], src="bn", dest="en").text
  # print(hindi_translation)
  hindi_sentences.append(hindi_translation)
  print("translation -->", i)

print(hindi_sentences)