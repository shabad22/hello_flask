import math
import os
import signal
import subprocess
import sys
import Solve.ReadData.Phase1 as Phase1
from start import downloadnltk
 
downloadnltk()  
    
sys.path.insert(0, "./Solve/ReadData/")
sys.path.insert(0, "./Solve/")


#global Variables
Output_path_Prefix=""
Data_path_Prefix=""

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
    global Output_path_Prefix
    global Data_path_Prefix
    import Solve.EuclideanDistance_eng_eng as eudis
    eudis.EqulideanProcessing(Output_path_Prefix, Data_path_Prefix)
    

def Cosine():
    global Output_path_Prefix
    global Data_path_Prefix
    import Solve.CosineSimi_eng_eng as Cosdis
    Cosdis.CosineProcessing(Output_path_Prefix, Data_path_Prefix)


# def Hamming():
#     global Output_path_Prefix
#     global Data_path_Prefix
#     import Solve.HammingDistance2 as Hamdis
#     Hamdis.HammingProessing(Output_path_Prefix, Data_path_Prefix)



def Jaccard():
    global Output_path_Prefix
    global Data_path_Prefix
    import Solve.jaccardDistance as JacDis
    JacDis.JaccrdProcessing(Output_path_Prefix, Data_path_Prefix)


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

Finaloutput=""
def GenerateFinalOutput(LISTMAPPING):
    global Finaloutput
    Finaloutput = ""
    global Output_path_Prefix
    global Data_path_Prefix
    CWD = os.getcwd()

    AllCorpus, InputQueryData, OriginalInputData = Phase1.Phase1(Output_path_Prefix, Data_path_Prefix)
    File_Output = open(CWD+Output_path_Prefix+"/FinalOutput.txt", "w", encoding='utf-8')
    for MAP in LISTMAPPING:
        EngSent = AllCorpus[MAP[0]-1]
        PunjSent = OriginalInputData[MAP[1]-1]
        File_Output.write(str(MAP[0])+":"+EngSent+"\n"+str(MAP[1])+" "+PunjSent+"\n\n")
        Finaloutput+=str(MAP[0])+":"+EngSent+"\n"+str(MAP[1])+" "+PunjSent+"\n\n"
    File_Output.close()
    return len(AllCorpus), len(InputQueryData)


def ComlipreAll(Output_path_Pre, Data_path_Pre):
    CWD = os.getcwd()
    global Output_path_Prefix
    global Data_path_Prefix
    Output_path_Prefix = Output_path_Pre
    Data_path_Prefix = Data_path_Pre

    Euclidean()
    Cosine()
    #Hamming()
    Jaccard()

    EquData = open(CWD+Output_path_Prefix+"/EquSimi.txt", 'r').read()
    CosData = open(CWD+Output_path_Prefix+"/CosSimi.txt", 'r').read()
   # HamData = open(CWD+Output_path_Prefix+"/HamSimi.txt", 'r').read()
    JaccData = open(CWD+Output_path_Prefix+"/JaccSimi.txt", 'r').read()

    DataList = []
    DataList.append([x for x in EquData.split('\n') if x != "" and x != None])
    DataList.append([x for x in CosData.split('\n') if x != "" and x != None])
    #DataList.append([x for x in HamData.split('\n') if x != "" and x != None])
    DataList.append([x for x in JaccData.split('\n') if x != "" and x != None])

    EquDataList=[]
    CosDataList=[]
    JaccDataList=[]
    EquDataList.append([x for x in EquData.split('\n') if x != "" and x != None])
    CosDataList.append([x for x in CosData.split('\n') if x != "" and x != None])
    #DataList.append([x for x in HamData.split('\n') if x != "" and x != None])
    JaccDataList.append([x for x in JaccData.split('\n') if x != "" and x != None])
    

    def RefineSent(List):
        Target=[]
        for i in List[0]:
            Target.append(list((int(i.split(',')[0]),int(i.split(',')[1]))))
        return Target
    EquDataSet =RefineSent(EquDataList)
    CosDataSet = RefineSent(CosDataList)
    JaccDataSet = RefineSent(JaccDataList)
    FinalIndex2 = []
    #print(EquDataSet)  
    FinalINDEXs = []
    for i in range(0,len(EquDataSet)):
        Target = []
        if str(EquDataSet[i]).split(',')[0].replace('[','')==str(CosDataSet[i]).split(',')[0].replace('[','') and str(EquDataSet[i]).split(',')[0].replace('[','')==str(JaccDataSet[i]).split(',')[0].replace('[',''):
            Target.append(int(str(EquDataSet[i]).split(',')[0].replace('[','')))
            Target.append(int(str(EquDataSet[i]).split(',')[1].replace(']','')))
        if len(Target) != 0:
            FinalINDEXs.append(Target)

    print('Refined Sentences:',len(FinalINDEXs))
    


    of = open("ALLVlues", 'w')
    # FinalINDEXs = []
    LISTval = DataList[0]
    print("==============",len(LISTval))
    for i in range(len(LISTval)):
        TargetSenIdx = []
        for k in range(len(DataList)):
            if DataList[k][i].split(',')[0] != "":
                TargetSenIdx.append(int(DataList[k][i].split(',')[0]))
        of.write(str(TargetSenIdx)+"\n")
    #     if len(TargetSenIdx) != 0:
    #         CorpusIDX = GETFinalIDx(TargetSenIdx)
    #         print(CorpusIDX)
    #         PunjIDX= int(DataList[k][i].split(',')[1])
    #         print(PunjIDX)
    #         FinalINDEXs.append([CorpusIDX, PunjIDX])
    
    # print(FinalINDEXs)

    AllCorpusCount, PunjCorpusCount = GenerateFinalOutput(FinalINDEXs)
    of.close()
    print("Process Completed...................Done")
    global Finaloutput
    return Finaloutput, AllCorpusCount, PunjCorpusCount
