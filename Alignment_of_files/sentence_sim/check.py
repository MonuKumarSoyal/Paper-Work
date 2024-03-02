import os
from LaBSEalign import align
import pandas as pd
# from eval import * 

src_dir = 'sentence_sim/src'
tgt_dir = 'sentence_sim/tgt'
#gold_dir = 'text+berg/gold'
test_alignments = []
#src_file = os.path.join(src_dir, file).replace("\\","/")
#tgt_file = os.path.join(tgt_dir, file).replace("\\","/")

# src = open('sentence_sim/src/Mann Ki Baat, January 2022.txt', 'r', encoding='utf-8').read()
# tgt = open('sentence_sim/tgt/मन की बात, जनवरी 2022.txt', 'r', encoding='utf-8').read()

dataset = pd.read_excel("hin_eng_split.xlsx", encoding='utf-8')

# src = open('hin_eng_split.xlsx', 'r', encoding='utf-8').read()
# tgt = open('sentence_sim/tgt/मन की बात, जनवरी 2022.txt', 'r', encoding='utf-8').read()

print(dataset[0].head())

#print("Start aligning {} to {}".format(src_file, tgt_file))
# aligner = align(src, tgt, is_split=True, len_penalty=False)
# aligner.align_sents()
# aligner.print_sents()
# test_alignments.append(aligner.result)