#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final Project"""
__author__="Mirna Salem"

import csv
from nltk.tokenize import word_tokenize
import math

def readFiles():
    #Read file and tokenize sentences
    count = 0 
    symptoms_text = []
    vax_names = []
    with open("dataset.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            if count >= 1:
                vax_names.append(lines[0])
                symptoms_text.append(lines[1])
            count += 1
    
    #Tokenize words
    tokens = []        
    for doc in symptoms_text:
        tokens.append(word_tokenize(doc.lower()))
    
    #Map each word to unique ID using a dictionary
    dct = {}
    for l in tokens:
        for w in l:
            dct[w] = 0
          
    count = 0 
    for key in dct:
        dct[key] = count
        count += 1
    
    #Create bag of words
    corpus = []
    for w in tokens:
        temp = []
        for key in dct:
            if key in w:
                temp.append((dct[key], w.count(key)))
            else:
                temp.append((dct[key], 0))
        corpus.append(temp)
    
    return corpus, dct, tokens,vax_names

def tfidf(corpus,dct,tokens):
    N = len(corpus)
    tfidf_corpus = []
    for w in tokens:
        temp = []
        for key in dct:
            if key in w:
                temp.append((dct[key], round((1 + math.log2(w.count(key))) * math.log2(N/df(key,tokens)),2)))
            else:
                temp.append((dct[key], 0))
                
        tfidf_corpus.append(temp)
    
    return(tfidf_corpus)

def df(key,tokens):
    count = 0
    for i in tokens:
        if key in i:
            count +=1
    return count
    
def find_similarity(doc1,doc2):
    sum_of_products = 0
    doc1_sq_sum = 0
    doc2_sq_sum = 0
    for x,y in zip(doc1,doc2):
        sum_of_products += (x[1] * y[1])
        doc1_sq_sum += x[1] ** 2
        doc2_sq_sum += y[1] ** 2
    
    result = sum_of_products / (math.sqrt(doc1_sq_sum) * math.sqrt(doc2_sq_sum))
    
    return result

def main():
    corpus,dct,tokens,vax_names = readFiles()
    tfidf_corpus = tfidf(corpus,dct,tokens)
    
    for i in range(0, len(tfidf_corpus)):
        if i >= len(tfidf_corpus) - 1:
            break
        max_value = -99
        highest_sim1, highest_sim2 = None, None
        for j in range(i+1,len(tfidf_corpus)):
            result = find_similarity(tfidf_corpus[i],tfidf_corpus[j])
            if result > max_value:
                max_value = result
                highest_sim1, highest_sim2 = i,j
        
        print('Vaccine 1:',vax_names[highest_sim1])
        print('Vaccine 2:', vax_names[highest_sim2])
        print('They have a similarity of', max_value,'\n')
    
    
if __name__ == "__main__":
    main()
