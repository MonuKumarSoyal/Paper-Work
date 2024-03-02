import torch
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import numpy as np  # added
from scipy.spatial.distance import cosine 
from sentence_transformers import SentenceTransformer 
import re
import os
import pandas as pd

import sys

sys.path.insert(0, "Alignment_of_files/Paper_work/sentence_sim")
from LaBSEalign import align


class CustomImageDataset(Dataset):
    def __init__(self, src_dir, tgt_dir, folder_index):
        self.src_dir = src_dir
        self.tgt_dir = tgt_dir
        self.folder_index = folder_index
   
    
    def __getitem__(self):
        src_files = os.listdir(self.src_dir)
        total_src_files = len(src_files)
        print(f"Number of files in the source folder is: {total_src_files}")

        tgt_files = os.listdir(self.tgt_dir)
        total_tgt_files = len(tgt_files)
        print(f"Number of files in the target folder is: {total_tgt_files}")

        print(" ============================================= ")
        sum_avg = 0
        common_files = 0
        for i in range(total_src_files):
            for j in range(total_tgt_files):
                # print(src_files[i], "and", tgt_files[j])
                if(src_files[i] == tgt_files[j]):
                    common_files += 1
                    break
        print(f"Number of common files are: {common_files}")


        output_file_index = 0
        for i in range(total_src_files):
            for j in range(total_tgt_files):
                if(src_files[i] == tgt_files[j]):
                    print(f"File number =====> {output_file_index + 1}")
                    src_file_path = self.src_dir + src_files[i]
                    tgt_file_path = self.tgt_dir + tgt_files[j]
                    print(f"source file: {src_files[i]} and target file: {tgt_files[j]}")
                    src_file_to_read = open(src_file_path, 'r', encoding='utf-8').read()
                    tgt_file_to_read = open(tgt_file_path, 'r', encoding='utf-8').read()
                    aligner = align(src_file_to_read, tgt_file_to_read, is_split=True, len_penalty=False)
                    aligner.align_sents()
                    sum_avg += aligner.print_sents(src_files[i][:-4], folder_index = self.folder_index)
                    output_file_index += 1
                    break


        # avg_similarity = sum_avg/index
        avg_similarity = sum_avg/output_file_index
        print(f"The average similarity score is: {avg_similarity}")
        # return src_list, tgt_list


src_dir = "Alignment_of_files/Paper_work/seven_lan/renamed_english/"
# tgt_dir = "Alignment_of_files/Paper_work/seven_lan/renamed_hindi/"
tgt_dirs_list = ["Alignment_of_files/Paper_work/seven_lan/renamed_assamese/",
                 "Alignment_of_files/Paper_work/seven_lan/renamed_bengali/",
                 "Alignment_of_files/Paper_work/seven_lan/renamed_malayalam/",
                 "Alignment_of_files/Paper_work/seven_lan/renamed_manipuri/",
                 "Alignment_of_files/Paper_work/seven_lan/renamed_urdu/"
                 ]

for i in range(len(tgt_dirs_list)):
    tgt_dir = tgt_dirs_list[i]
    print(f"***** {tgt_dir[48:]} *****")
    obj = CustomImageDataset(src_dir, tgt_dir, i)

    obj.__getitem__() # call it while giving input as files



