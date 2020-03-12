import os
import time
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
from scipy.spatial import distance
from sklearn.feature_extraction.text import TfidfVectorizer
import Solve.ReadData.Phase1 as Phase1

#from ReadData import Phase1, StopWords, trans2


def JaccrdProcessing(Output_path_Prefix, Data_path_Prefix):
    CWD = os.getcwd()

    #transComplete = trans2.Translate(Output_path_Prefix, Data_path_Prefix)
    # if transComplete == False:
    #    time.sleep(2)

    AllCorpus, InputQueryData, OriginalInputData = Phase1.Phase1(
        Output_path_Prefix, Data_path_Prefix)

    #SW= StopWords.loadStopWords()
    #AllCorpus = StopWords.RemoveStopWords(AllCorpus, SW)

    # Convert a collection of raw documents to a matrix of TF-IDF features
    tfidf_vectorizer = TfidfVectorizer(norm=None)

    # Learn vocabulary and idf, return term-document matrix.
    tfidf_matrix = tfidf_vectorizer.fit_transform(AllCorpus)

    TrainList = []
    for i in range(tfidf_matrix.shape[0]):
        for l in tfidf_matrix[i, :].toarray():
            templist = []
            TrainList.append(l.tolist())
            # for n in l:
            #    templist.append(n)
            # TrainList.append(templist)

    def FindSimi(TDoc):
        tfidf_testing = tfidf_vectorizer.transform(TDoc)
        # VI=np.cov(tfidf_matrix.toarray())
        TestList = []
        for i in range(tfidf_testing.shape[0]):
            for l in tfidf_testing[i, :].toarray():
                #templist = []
                TestList.append(l.tolist())
                # for n in l:
                #    templist.append(n)
                # TestList.append(templist)

        DocIndex = -1
        Index = 1
        MinVal = 999
        for train in TrainList:
            output = distance.jaccard(TestList, train)
            if output <= MinVal:
                MinVal = output
                DocIndex = Index
            Index += 1
        return DocIndex, MinVal

    Acc = 0
    Dindex = -1
    maxsim = -1
    tlist = []
    LNo = 1
    totDoc = len(InputQueryData)
    AllSimiScores = []
    AllOUTPUTData = []
    X = []
    Y = []
    file_jaccard_output = open(
        CWD+"/"+Output_path_Prefix+"/JaccardOutput.txt", "w+", encoding='utf-8')
    #file_simi_score = open(CWD+"/Output/JaccSimi.txt", "w+", encoding='utf-8')
    file_line_mapping_simi = open(
        CWD+"/"+Output_path_Prefix+"/JaccSimi.txt", "w+", encoding='utf-8')

    print("\n-------------Jaccard Distance---------------")
    print("LangOne Sent: --> Corpus Sent (Similarty Score)")
    print("----------------------------------------------\n")
    print("Total Number of Features: ", len(
        tfidf_vectorizer.get_feature_names()), "\n")

    for Tdoc in InputQueryData:
        tlist.append(Tdoc.strip('\n'))
        newDindex, newmaxsim = FindSimi(tlist)
        PunjSent = OriginalInputData[LNo-1]
        SD = AllCorpus[newDindex-1]
        Sent = str(LNo)+": "+SD+"\n"+PunjSent+"\n\n"
        file_jaccard_output.write(
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

    file_jaccard_output.close()
    file_line_mapping_simi.close()
    print("\n")
    print("Source Sen:", len(AllCorpus))
    print("Target Sen:", len(InputQueryData), "\n")

    ThresholdVal = sum(AllSimiScores)/len(AllSimiScores)

    f1 = open(CWD+"/"+Output_path_Prefix+"/JaccSimi.txt", "r", encoding='utf-8')
    f = open(CWD+"/"+Output_path_Prefix+"/JaccSimiTh.txt", "w+", encoding='utf-8')
    Data = f1.readlines()
    for i in Data:
        if float(str(i).split(',')[2])<=ThresholdVal:
            f.write(str(i))
    f1.close()
    f.close()

    file_jaccard_output = open(
        CWD+"/"+Output_path_Prefix+"/JaccardOutputThreshold.txt", "w+", encoding='utf-8')
    print("Threshold Value:", ThresholdVal)
    print("Writing Sentences Greated Then Threadold...")
    THcount = 0
    for Sent in AllOUTPUTData:
        score = Sent.split('@')[0]
        if float(score) <= ThresholdVal:
            file_jaccard_output.write(Sent.split('@')[1])
            THcount += 1
    print("Total Refined Sentences:", THcount)
    print("Completed, Press Enter")

    """
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(X, Y)
    ax.grid(True)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_position('zero')
    ax.set_yticks(np.arange(min(Y), max(Y), 2))
    ax.set_xticks(np.arange(min(X), max(X), 2))
    #plt.show()
    """
