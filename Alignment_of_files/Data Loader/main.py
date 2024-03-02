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

sys.path.insert(0, "sentence_sim")
from LaBSEalign import align

sys.path.insert(0, "split")
from eng_hin_splitter_together import Spiltter



class CustomImageDataset(Dataset):
    def __init__(self, src_dir, tgt_dir):
        self.src_dir = src_dir
        self.tgt_dir = tgt_dir
        self.src_files_list = os.listdir(self.src_dir)
        self.tgt_files_list = os.listdir(self.tgt_dir)

    def __len__(self):
        return len(self.src_files_list), len(self.tgt_files_list)

    def split(self, hindi_file, english_file, hindi_output_file, english_output_file, file_format):
        split_obj = Spiltter(hindi_file, english_file, hindi_output_file, english_output_file, file_format)
        split_obj.preprocess_hin()
        split_obj.preprocess_eng()
        # split_obj.split_hin()
        # split_obj.split_eng()
        split_obj.print_hin()
        split_obj.print_eng()
        # split_obj.output_file.close()
    
    
    def __getitem__(self):
        src_path = []
        tgt_path = []
        src_list = []  # this is used when we want to store all files contents in one file
        tgt_list = []  # this is used when we want to store all files contents in one file

        row = 0

        for i in self.src_files_list:
            src_path.append(os.path.join(self.src_dir, i))
        for i in self.tgt_files_list:
            tgt_path.append(os.path.join(self.tgt_dir, i))
        
        src_path.sort()
        tgt_path.sort()

        
        index = 0
        for file1, file2 in zip(src_path, tgt_path):
            hindi_output = "train_test_val_hin/H"+str(index)+".txt"
            english_output = "train_test_val_eng/E"+str(index)+".txt"
            self.split(file2, file1, hindi_output, english_output, file_format=True)
            index += 1
            
            with open(file1, 'r') as src_file:
                src_list = src_list + src_file.readlines()
            with open(file2, 'r') as tgt_file:
                tgt_list = tgt_list + tgt_file.readlines()

        print(f"The value of index is: {index}")
        sum_avg = 0
        
        # instead of 5 we have to put index variable to get the alignment and similarity score of all the files but to 
        # conda's size i am giving 5 files so that we don't get error on run.
        var = 5
        for i in range(0, index):
            read_english = "train_test_val_eng/E"+str(i)+".txt"  
            read_hindi = "train_test_val_hin/H"+str(i)+".txt"
            # read_english = "preprocess/preprocessed_english.txt"
            # read_hindi = "preprocess/preprocessed_hindi.txt"
            src_file_to_read = open(read_english, 'r', encoding='utf-8').read()
            tgt_file_to_read = open(read_hindi, 'r', encoding='utf-8').read()
            aligner = align(src_file_to_read, tgt_file_to_read, is_split=True, len_penalty=False)
            
            aligner.align_sents()            
            sum_avg += aligner.print_sents(i)

        # avg_similarity = sum_avg/index
        avg_similarity = sum_avg/index
        print(f"The average similarity score is: {avg_similarity}")
        return src_list, tgt_list
    
    def prepare_data(self, input_file):
        file = pd.ExcelFile(input_file)
        sheet_name = file.sheet_names
        # input_sheets = [i for i in sheet_name if ("Final" or "final")  in i]
        input_sheets = sheet_name

        index = 0
        src_list = []
        tgt_list = []
        
        print(f"Total number of sheets to read are: {len(input_sheets)}")
        for sheet in input_sheets:
            input_df = file.parse(sheet) # sheet is the name of a particular sheet of the input excel file
            
            # first column of the excel file should be hindi and second column should be english
            hin_sents = [input_df.iloc[i, 0] for i in range(len(input_df)) if pd.notnull(input_df.iloc[i, 0])]
            eng_sents = [input_df.iloc[i, 1] for i in range(len(input_df)) if pd.notnull(input_df.iloc[i, 1])]
            hindi_output = "Gold/H"+str(index)+".txt"
            english_output = "Gold/E"+str(index)+".txt"
            file_format = False
            self.split(hin_sents, eng_sents, hindi_output, english_output, file_format)
            index+=1
            src_list = src_list + eng_sents
            tgt_list = tgt_list + hin_sents
            
        return src_list, tgt_list, index
    
    def MKB_Align(self, input_file):
        src_list = []  # this is used when we want to store all files contents in one file
        tgt_list = []  # this is used when we want to store all files contents in one file

        
        src_list, tgt_list, index = self.prepare_data(input_file)
        sum_avg = 0
        
        # instead of 5 we have to put index variable to get the alignment and similarity score of all the files but due to
        # conda's size i am giving 5 files so that we don't get error on run.
        for i in range(0, index):
            read_english = "Gold/E"+str(i)+".txt"  
            read_hindi = "Gold/H"+str(i)+".txt"
            src_file_to_read = open(read_english, 'r', encoding='utf-8').read()
            tgt_file_to_read = open(read_hindi, 'r', encoding='utf-8').read()
            aligner = align(src_file_to_read, tgt_file_to_read, is_split=True, len_penalty=False)
            aligner.align_sents()            
            sum_avg += aligner.print_sents(i)

        # avg_similarity = sum_avg/index
        avg_similarity = sum_avg/index
        print(f"The average similarity score is: {avg_similarity}")        
        return src_list, tgt_list

# src_dir = "./Entire_data/eng"
# tgt_dir = "./Entire_data/hin"

src_dir = "MMT_english"
tgt_dir = "MMT_hindi"

input_file = "compare_eng/Golden.xlsx"


obj = CustomImageDataset(src_dir, tgt_dir)
# src_len, tgt_len = obj.__len__() # call it while giving input as files
src_list, tgt_list = obj.__getitem__() # call it while giving input as files

# print(f"Number of files in the source directory is: {src_len}")
# print(f"Number of files in the target directory is: {tgt_len}")

# src_list, tgt_list = obj.MKB_Align(input_file)


