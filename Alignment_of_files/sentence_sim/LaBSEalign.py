from encoder import *
from utils import *
#from bertalign import model
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from corelib import *
import torch
import xlsxwriter
import torch.nn.functional as similar

from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
import sys
import os

embedding_model = SentenceTransformer("johngiorgi/declutr-small")



model = SentenceTransformer('sentence-transformers/LaBSE')

class align:
    def __init__(self,
                 src,
                 tgt,
                 max_align=5,
                 top_k=3,
                 win=5,
                 skip=-0.1,
                 margin=True,
                 len_penalty=False,
                 is_split=False,
                 ):
        self.max_align = max_align
        self.top_k = top_k
        self.win = win
        self.skip = skip
        self.margin = margin
        self.len_penalty = len_penalty

        src = clean_text(src)
        tgt = clean_text(tgt)
        src_lang = 'en'
        tgt_lang = 'hi'
        if is_split:
            src_sents = src.splitlines()
            tgt_sents = tgt.splitlines()
        else:
            src_sents = split_sents(src, src_lang)
            tgt_sents = split_sents(tgt, tgt_lang)

        src_num = len(src_sents)
        tgt_num = len(tgt_sents)

        print("Source language: {}, Number of sentences: {}".format(src_lang, src_num))
        print("Target language: {}, Number of sentences: {}".format(tgt_lang, tgt_num))
        src_vecs = model.encode(src_sents)
        tgt_vecs = model.encode(tgt_sents)
        src_vecs = torch.from_numpy(src_vecs).unsqueeze(0)
        tgt_vecs = torch.from_numpy(tgt_vecs).unsqueeze(0)
        src_vecs1 = src_vecs.detach().numpy()
        tgt_vecs1 = tgt_vecs.detach().numpy()
        src_vecs = np.tile(src_vecs1, (4, 1, 1))
        tgt_vecs = np.tile(tgt_vecs1, (4, 1, 1))

        char_count_src=[]
        char_count_tgt=[]
        for sentence_src, sentence_tgt  in zip(src_sents, tgt_sents):
            char_count1 = len(sentence_src)
            char_count2 = len(sentence_tgt)
            char_count_src.append(char_count1)
            char_count_tgt.append(char_count2)

        char_ratio = sum(char_count_src) / sum(char_count_tgt)

        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.src_sents = src_sents
        self.tgt_sents = tgt_sents
        self.src_num = src_num
        self.tgt_num = tgt_num
        self.src_lens = char_count_src
        self.tgt_lens = char_count_tgt
        self.char_ratio = char_ratio
        self.src_vecs = src_vecs
        self.tgt_vecs = tgt_vecs

    def align_sents(self):

        print("Performing first-step alignment ...")
        D, I = find_top_k_sents(
            self.src_vecs[0, :], self.tgt_vecs[0, :], k=self.top_k)
        first_alignment_types = get_alignment_types(2)  # 0-1, 1-0, 1-1
        first_w, first_path = find_first_search_path(
            self.src_num, self.tgt_num)
        first_pointers = first_pass_align(
            self.src_num, self.tgt_num, first_w, first_path, first_alignment_types, D, I)
        first_alignment = first_back_track(
            self.src_num, self.tgt_num, first_pointers, first_path, first_alignment_types)

        print("Performing second-step alignment ...")
        second_alignment_types = get_alignment_types(self.max_align)
        
        second_w, second_path = find_second_search_path(
            first_alignment, self.win, self.src_num, self.tgt_num)
        second_pointers = second_pass_align(self.src_vecs, self.tgt_vecs, self.src_lens, self.tgt_lens,
                                            second_w, second_path, second_alignment_types,
                                            self.char_ratio, self.skip, margin=self.margin, len_penalty=self.len_penalty)
        second_alignment = second_back_track(
            self.src_num, self.tgt_num, second_pointers, second_path, second_alignment_types)
        # print(second_alignment)
        # self.print_second_alignment(second_alignment)
        print("Finished! Successfully aligning {} {} sentences to {} {} sentences\n".format(
            self.src_num, self.src_lang, self.tgt_num, self.tgt_lang))
        self.result = second_alignment
        
    def print_second_alignment(self, second_alignment):
        file = open("compare_eng/numeric_alignment.txt", 'w')
        size = len(second_alignment)
        for i in range(size):
            file.write(str(second_alignment[i][0]) + ":" + str(second_alignment[i][1]) + "\n")
            
        file.close()
        

    def print_sents(self, index = 0, folder_index = 0, row = 0):

        # output_folder = "Alignment_of_files/Paper_work/Eng-Hindi/"
        output_folder_list = ["Alignment_of_files/Paper_work/Eng-Assamese/",
                              "Alignment_of_files/Paper_work/Eng-Bengali/",
                              "Alignment_of_files/Paper_work/Eng-Malayalam/",
                              "Alignment_of_files/Paper_work/Eng-Manipuri/",
                              "Alignment_of_files/Paper_work/Eng-Urdu/"                           
                              ]
        output_folder = output_folder_list[folder_index]
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_name =  output_folder + index + ".xlsx"
        output_file = xlsxwriter.Workbook(file_name)
        worksheet = output_file.add_worksheet()
        sum_similarity = 0
        sent_count = 0
        
        for bead in (self.result):
            texts = []
            first_line = str(bead[0])
            second_line = str(bead[1])
            texts.append(first_line)
            texts.append(second_line)
            embeddings = embedding_model.encode(texts)

            semantic_sim = 1 - cosine(embeddings[0], embeddings[1])
            sum_similarity += semantic_sim
            sent_count+=1
            
            src_line = self._get_line(bead[0], self.src_sents)
            tgt_line = self._get_line(bead[1], self.tgt_sents)
            worksheet.write(row, 0, src_line)
            worksheet.write(row, 1, tgt_line)
            # worksheet.write(row, 2, semantic_sim)
            row+=1
        output_file.close()
        
        avg_similarity = sum_similarity/sent_count
        return avg_similarity

    @staticmethod
    def _get_line(bead, lines):
        line = ''
        if len(bead) > 0:
            line = ' '.join(lines[bead[0]:bead[-1]+1])
        return line
