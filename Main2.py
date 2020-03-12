import math
import os
import signal
import subprocess
import sys

sys.path.insert(0, "./Solve/ReadData/")
sys.path.insert(0, "./Solve/")


def CreatePhrases():
    print("\033[1;32m")

    print("\n\n")
    print("[1] for Overlapping Phrases for Punjabi and Corpus")
    print("[2] for Continous Phrases for Punjabi and Corpus")

    ch = input()
    if ch == '1':
        subprocess.Popen(
            "python ./Solve/ReadData/CreateNGram3.py ./Data/PunjText.pa ./Data/NGQuery.pa 4", shell=True)
        subprocess.Popen(
            "python ./Solve/ReadData/CreateNGram3.py ./Data/EngText.en ./Data/NGCourpus.en 4", shell=True)
    elif ch == '2':
        subprocess.Popen(
            "python ./Solve/ReadData/CreateNGrams2.py ./Data/PunjText.pa ./Data/NGQuery.pa", shell=True)
        subprocess.Popen(
            "python ./Solve/ReadData/CreateNGrams2.py ./Data/EngText.en ./Data/NGCourpus.en", shell=True)
    else:
        print("\033[1;31m Wrong Choice")
        return


def Euclidean():
    import Solve.EuclideanDistance_eng_eng
    #subprocess.Popen("python ./Solve/ReadData/trans2.py", shell=True)
    # subprocess.Popen(
    #    "python ./Solve/EuclideanDistance_eng_eng.py", shell=True)


def Cosine():
    import Solve.CosineSimi_eng_eng
    #subprocess.Popen("python ./Solve/ReadData/trans2.py", shell=True)
    #subprocess.Popen("python ./Solve/CosineSimi_eng_eng.py", shell=True)


def Hamming():
    import Solve.HammingDistance2
    #subprocess.Popen("python ./Solve/ReadData/trans2.py", shell=True)
    #subprocess.Popen("python ./Solve/HammingDistance2.py", shell=True)


def Jaccard():
    import Solve.jaccardDistance
    #subprocess.Popen("python ./Solve/ReadData/trans2.py", shell=True)
    #subprocess.Popen("python ./Solve/jaccardDistance.py", shell=True)


def Softmax(Scores):
    output = []
    SUM = sum(Scores)
    for score in Scores:
        val = math.exp(score) / SUM
        output.append(val)

    return output


def GetMaxIndex(Scores):
    MAXVAL = Scores[0]
    Index = 0
    for i in range(1, len(Scores)):
        if Scores[i] > MAXVAL:
            MAXVAL = Scores[i]
            Index = i

    return Index


def GETFinalIDx(LIST):
    TempDict = {}
    for val in LIST:
        if val in TempDict:
            TempDict[val] += 1
        else:
            TempDict[val] = 1

    TempDict = sorted(TempDict.items(), key=lambda x: x[1], reverse=True)

    return list(TempDict)[0][0]


def GenerateFinalOutput(LISTMAPPING):
    import Phase1
    AllCorpus, InputQueryData, OriginalInputData = Phase1.Phase1()
    File_Output = open("./Output/FinalOutput.txt", "w+", encoding='utf-8')
    for MAP in LISTMAPPING:
        EngSent = AllCorpus[MAP[0]-1]
        PunjSent = OriginalInputData[MAP[1]-1]
        File_Output.write(str(MAP[0])+":"+EngSent+"\n"+str(MAP[1])+" "+PunjSent+"\n\n")
    File_Output.close()


def ComlipreAll():
    # Euclidean()
    # Cosine()
    # Hamming()
    # Jaccard()

    EquData = open("./Output/EquSimi.txt", 'r').read()
    CosData = open("./Output/CosSimi.txt", 'r').read()
    HamData = open("./Output/HamSimi.txt", 'r').read()
    JaccData = open("./Output/JaccSimi.txt", 'r').read()

    DataList = []
    DataList.append([x for x in EquData.split('\n') if x != "" or x != None])
    DataList.append([x for x in CosData.split('\n') if x != "" or x != None])
    DataList.append([x for x in HamData.split('\n') if x != "" or x != None])
    DataList.append([x for x in JaccData.split('\n') if x != "" or x != None])

    of = open("ALLVlues", 'w')
    FinalINDEXs = []
    LISTval = DataList[0]
    for i in range(len(LISTval)):
        TargetSenIdx = []
        for k in range(len(DataList)):
            if DataList[k][i].split(',')[0] != "":
                TargetSenIdx.append(int(DataList[k][i].split(',')[0]))
        of.write(str(TargetSenIdx)+"\n")
        if len(TargetSenIdx) != 0:
            CorpusIDX = GETFinalIDx(TargetSenIdx)
            PunjIDX= int(DataList[k][i].split(',')[1])
            FinalINDEXs.append([CorpusIDX, PunjIDX])
    GenerateFinalOutput(FinalINDEXs)
    of.close()


#ComlipreAll()


ch = -1

while True:
    print("\033[1;34m")

    print("\n--------------------------------")
    print("Compariable Corpus Creation Tool")
    print("--------------------------------\n")

    print("\nPress [1] Create Phrases")
    print("Press [2] for Euclidean Distance")
    print("Press [3] for Cosine Similarity ")
    print("Press [4] for Hamming Distance ")
    print("Press [5] for Jaccard Distance ")
    print("Press [0] for exit")
    ch = input("Choice:")

    if ch == '0':
        break
    if ch == '1':
        # subprocess.Popen('clear')
        CreatePhrases()
    if ch == '2':
        subprocess.Popen('clear')
        Euclidean()
    if ch == '3':
        subprocess.Popen('clear')
        Cosine()
    if ch == '4':
        subprocess.Popen('clear')
        Hamming()
    if ch == '5':
        subprocess.Popen('clear')
        Jaccard()
