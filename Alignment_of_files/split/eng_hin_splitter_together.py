import re
import pandas as pd
import xlsxwriter

# input_file = pd.read_excel("input.xlsx")
# header = input_file.columns
# # print(header)

class Spiltter:
  def __init__(self, hin_file_name, 
               eng_file_name,
               hin_output_file = "hindi_split.txt", 
               eng_output_file = "english_split.txt",
               file_format = True,
               output_file_path = 'hin_eng_split.xlsx'):
    self.eng_input_file = eng_file_name
    self.hin_input_file = hin_file_name
    self.file_format = file_format
    self.eng_lines = []
    self.hin_lines = []
    self.english_sents = []
    self.hin_sents = []
    self.list_of_eng_conjunctions = []
    self.list_of_hin_conjunctions = []
    self.output_eng_list = []
    self.output_hin_list = []
    self.output_file_path = output_file_path
    self.hin_output_file = hin_output_file
    self.eng_output_file = eng_output_file
    self.output_file = xlsxwriter.Workbook(self.output_file_path)
    self.worksheet = self.output_file.add_worksheet()
    
  def preprocess_eng(self):
    if(self.file_format):
      with open(self.eng_input_file, "r") as source:
        self.eng_lines = source.readlines()
    else:
      self.eng_lines = self.eng_input_file
      
    self.english_sents = [line.strip() for line in self.eng_lines]
    # self.list_of_eng_conjunctions = [" and ", ". ", "; "]
    self.list_of_eng_conjunctions = [". "]
    
    for i in self.english_sents:
      # temp = i.split(delim)
      # temp = re.split('( and |\. |; )', i)
      temp = re.split('(\. )', i)
      self.output_eng_list.append(temp)
      
  def preprocess_hin(self):
    if(self.file_format):
      with open(self.hin_input_file , "r") as source:
        self.hin_lines = source.readlines()
    else:
      self.hin_lines = self.hin_input_file
    
    self.hin_sents = [line.strip() for line in self.hin_lines]
    # self.list_of_hin_conjunctions = [" और ", "। ", "; ", "।"]
    self.list_of_hin_conjunctions = ["। ", "।"]
    
    for i in self.hin_sents:
      # temp = i.split(delim)
      # temp = re.split('( और |। |; |।)', i)
      temp = re.split('(। |।)', i)
      # print(temp)
      self.output_hin_list.append(temp)
      
  def split_eng(self):
    sent = 0
    for lst in self.output_eng_list:                   # output_eng_list is list of list
      temp = lst.copy()                      # lst is the list containing phrases and conjunctions of a sentences(line)
      index = 0
      while(index!=len(temp)):
        if temp[index] in self.list_of_eng_conjunctions:
            pre_list = temp[index-1].split(" ")
            post_list = temp[index+1].split(" ")
            # temp.pop(index)
            # index-=1
            if(len(pre_list) >= 4 and len(post_list) >=4):
              temp.pop(index)
              index-=1
            else:
              temp[index-1] = temp[index-1] + temp[index] + temp[index+1]
              temp.pop(index)
              temp.pop(index)
              index-=2
        index+=1
      # print(temp)
      self.output_eng_list[sent] = temp
      sent+=1
      
  def split_hin(self):
    sent = 0
    for lst in self.output_hin_list:                   # output_hindi_list is list of list
      temp = lst.copy()                      # lst is the list containing phrases and conjunctions of a sentences(line)
      index = 0
      while(index!=len(temp)):
        if temp[index] in self.list_of_hin_conjunctions:
            pre_list = temp[index-1].split(" ")
            post_list = temp[index+1].split(" ")
            # temp.pop(index)
            # index-=1
            if(len(pre_list) >= 4 and len(post_list) >=4):
              temp.pop(index)
              index-=1
            else:
              temp[index-1] = temp[index-1] + temp[index] + temp[index+1]
              temp.pop(index)
              temp.pop(index)
              index-=2
        index+=1
      # print(temp)
      self.output_hin_list[sent] = temp
      sent+=1
  
  def print_eng(self):
    with open(self.eng_output_file, 'w') as f:
      for line in self.output_eng_list:
        for sent in line:
          if sent == "":
            pass
          else:
            sent = sent.strip()
            f.write(sent +"\n")    

  def print_hin(self):
    with open(self.hin_output_file, 'w') as f:
      for line in self.output_hin_list:
        for sent in line:
          if sent == "":
            pass
          else:
            sent = sent.strip()
            f.write(sent +"\n") 