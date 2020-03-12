import numpy as np
import matplotlib.pyplot as plt

import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import Solve.ReadData.Phase1 as Phase1


def EqulideanProcessing(Output_path_Prefix, Data_path_Prefix):
    CWD = os.getcwd()

    #transComplete = trans2.Translate(Output_path_Prefix, Data_path_Prefix)
    # if transComplete == False:
    #    time.sleep(2)

    AllCorpus, InputQueryData, OriginalInputData = Phase1.Phase1(
        Output_path_Prefix, Data_path_Prefix)
    print(">>>>", len(AllCorpus))

    #SW= StopWords.loadStopWords()
    #AllCorpus = StopWords.RemoveStopWords(AllCorpus, SW)

    # Convert a collection of raw documents to a matrix of TF-IDF features
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 1), norm='l2')

    # Learn vocabulary and idf, return term-document matrix.
    tfidf_matrix = tfidf_vectorizer.fit_transform(AllCorpus)

    print(len(tfidf_vectorizer.vocabulary_))

    def Find_Max_Simi(tdata):
        tfidf_testing = tfidf_vectorizer.transform(tdata)
        output = euclidean_distances(tfidf_matrix, tfidf_testing)

        FinalIndex = -1
        MinDis = 9999

        index = 1
        for i in output:
            for j in i:
                if j <= MinDis:
                    MinDis = j
                    FinalIndex = index
            #print("DocNum CS:",index,":",j)
                index += 1

        return FinalIndex, MinDis

    Acc = 0
    Dindex = -1
    maxsim = -1
    tlist = []
    LNo = 1
    totDoc = len(InputQueryData)
    AllSimiScores = []
    AllOUTPUTData = []
    file_euclidean_output = open(
        CWD+"/"+Output_path_Prefix+"/EuclideanOutput.txt", "w+", encoding='utf-8')
    #file_simi_score = open(CWD+"/Output/EquSimi.txt", "w+", encoding='utf-8')
    file_line_mapping_simi = open(
        CWD+"/"+Output_path_Prefix+"/EquSimi.txt", "w+", encoding='utf-8')

    print("\n------------Euclidean Distance---------------")
    print("LangOne Sent: --> Corpus Sent (Similarty Score)")
    print("----------------------------------------------\n")
    print("Total Number of Features: ", len(
        tfidf_vectorizer.get_feature_names()), "\n")

    X = []
    Y = []
    for Tdoc in InputQueryData:
        tlist.append(Tdoc.strip('\n'))
        newDindex, newmaxsim = Find_Max_Simi(tlist)

        # print(LNo-1)
        PunjSent = OriginalInputData[LNo-1]
        SD = AllCorpus[newDindex-1]
        Sent = str(LNo)+": "+SD+"\n"+PunjSent+"\n\n"
        file_euclidean_output.write(
            str(newDindex)+": "+SD+"\n"+str(LNo)+": "+PunjSent+"\n\n")
        file_line_mapping_simi.write(
            str(newDindex)+","+str(LNo)+","+str(newmaxsim)+"\n")
        # file_simi_score.write(str(newmaxsim)+"\n")
        Y.append(newDindex)
        X.append(LNo)
        AllSimiScores.append(newmaxsim)
        AllOUTPUTData.append(str(newmaxsim)+"@"+str(newDindex) +
                             ":"+SD.strip()+"\n"+str(LNo)+":"+PunjSent.strip()+"\n\n")
        print("Sent Num:", LNo, "-->", newDindex,
              "(Simi:", round(newmaxsim, 3), ")")
        if LNo == newDindex:
            Acc += 1
        tlist.clear()
        LNo += 1

    file_euclidean_output.close()
    file_line_mapping_simi.close()
    print("\n")
    print("Source Sen:", len(AllCorpus))
    print("Target Sen:", len(InputQueryData), "\n")
    ThresholdVal = sum(AllSimiScores)/len(AllSimiScores)

    f1 = open(CWD+"/"+Output_path_Prefix+"/EquSimi.txt", "r", encoding='utf-8')
    f = open(CWD+"/"+Output_path_Prefix+"/EquSimiTh.txt", "w+", encoding='utf-8')
    Data = f1.readlines()
    for i in Data:
        if float(str(i).split(',')[2])<=ThresholdVal:
            f.write(str(i))
    f.close()
    f1.close()

    file_euclidean_output = open(
        CWD+"/"+Output_path_Prefix+"/EuclideanOutputThreshold.txt", "w+", encoding='utf-8')
    print("Threshold Value:", ThresholdVal)
    print("Writing Sentences Greated Then Threadold...")
    THcount = 0
    for Sent in AllOUTPUTData:
        score = Sent.split('@')[0]
        if float(score) <= ThresholdVal:
            file_euclidean_output.write(Sent.split('@')[1])
            THcount += 1
    print("Total Refined Sentences:", THcount)
    print("Completed, Press Enter")

    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(X, Y)
    ax.grid(True)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_position('zero')
    ax.set_yticks(np.arange(min(Y), max(Y), 2))
    ax.set_xticks(np.arange(min(X), max(X), 2))
    
