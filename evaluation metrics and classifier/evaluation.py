# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 18:52:09 2022

@author: Janet
"""

# Evaluate 
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
import seaborn as sns
import matplotlib.pyplot as plt
from bert_score import score

df_test = pd.read_csv('df_test.csv')

tmp = df_test

#BERTscore
Pb, Rb, Fb = score([str(i) for i in tmp['Actual Text'].tolist()], [str(i) for i in tmp['Generated Text'].tolist()], lang='en')
print("Precision: "+str(Pb))
print("Recall: "+str(Rb))
print("Fbert: "+str(Fb))
print("Mean Precision: "+str(torch.mean(Pb)))
print("Mean Recall: "+str(torch.mean(Rb[~torch.isnan(Rb)])))
print("Mean Fbert: "+str(torch.mean(Fb)))
for epoch in [10,20]:
  Pb, Rb, Fb = score([str(i) for i in tmp['Actual Text'].tolist()], [str(i) for i in tmp[f'Generated Text {epoch}'].tolist()], lang='en')
  print("Epoch" + str(epoch))
  print("Precision: "+str(Pb))
  print("Recall: "+str(Rb))
  print("Fbert: "+str(Fb))
  print("Mean Precision: "+str(torch.mean(Pb)))
  print("Mean Recall: "+str(torch.mean(Rb[~torch.isnan(Rb)])))
  print("Mean Fbert: "+str(torch.mean(Fb)))
  

# ROUGE
# importing the native rouge library
from rouge_score import rouge_scorer
# a list of the hypothesis documents
hyp = [str(i) for i in tmp['Actual Text'].tolist()]
# a list of the references documents
ref = [str(i) for i in tmp['Generated Text'].tolist()]
for ind in ['1','2','L']:
  print("Rouge"+ind)
  scorer = rouge_scorer.RougeScorer(['rouge'+ind])
  results = {'precision': [], 'recall': [], 'fmeasure': []}
  for (h, r) in zip(hyp, ref):
      score = scorer.score(h, r)
      precision, recall, fmeasure = score['rouge'+ind]
      results['precision'].append(precision)
      results['recall'].append(recall)
      results['fmeasure'].append(fmeasure)
  print("results['precision']"+ str(np.around(np.mean(results['precision'])*100,2)))
  print("results['recall']"+ str(np.around(np.mean(results['recall'])*100,2)))
  print("results['fmeasure']"+ str(np.around(np.mean(results['fmeasure'])*100,2)))

for epoch in [10,20]:
  print("epoch" +str(epoch))
  # a list of the hypothesis documents
  hyp = [str(i) for i in tmp['Actual Text'].tolist()]
  # a list of the references documents
  ref = [str(i) for i in tmp[f'Generated Text {epoch}'].tolist()]
  for ind in ['1','2','L']:
    print("Rouge"+ind)
    scorer = rouge_scorer.RougeScorer(['rouge'+ind])
    results = {'precision': [], 'recall': [], 'fmeasure': []}
    for (h, r) in zip(hyp, ref):
        score = scorer.score(h, r)
        precision, recall, fmeasure = score['rouge'+ind]
        results['precision'].append(precision)
        results['recall'].append(recall)
        results['fmeasure'].append(fmeasure)
    print("results['precision']"+ str(np.around(np.mean(results['precision'])*100,2)))
    print("results['recall']"+ str(np.around(np.mean(results['recall'])*100,2)))
    print("results['fmeasure']"+ str(np.around(np.mean(results['fmeasure'])*100,2)))