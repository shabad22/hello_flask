import os
from pathlib import Path
from Solve.ReadData.Tokenization import CreateSentences
import Solve.ReadData.trans2 as translate
import time
#from ReadData.Tokenization import CreateSentences
#from Tokenization import CreateSentences
# tempStatement for eng sentence tokenize
import nltk
#import re
from nltk.tokenize import sent_tokenize
def EngTokenize(PATH):
    strData = ''
    with open(PATH, 'r', encoding='utf-8') as f:
        data = f.read()
        #data = re.sub(r'\n','',data)
        data = data.replace('\n',' ')
        #print(data)
    f.close()
    TokenizeData=sent_tokenize(data)
    f=open(PATH, 'w',encoding='utf-8')
    for Sent in TokenizeData:
        f.writelines(Sent+'\n')
        #print(Sent)
    f.close()
# tempStatement for eng sentence tokenize

def CleanningData(PATH):
    #print("CleanningData()>>>>>>>>>>>>>++++++++>>>>>>>>>>>>>>>>>>",PATH)
    CreateSentences(PATH)

def TranslateSentences(Data_path_Prefix):
    transComplete = translate.Translate(Data_path_Prefix)
    if transComplete == False:
        time.sleep(2)


def Phase1(Output_path_Prefix, Data_path_Prefix):
    CWD = os.getcwd()
    AllCorpus = []

    source = []
    data = ""
    print(CWD+Data_path_Prefix+"/LangOne.en")

    INPUTCORPUS = None
    if os.path.exists(CWD+Data_path_Prefix+"/NGCourpus.en"):
        INPUTCORPUS = CWD+Data_path_Prefix+"/NGCourpus.en"
    elif os.path.exists(CWD+Data_path_Prefix+"/LangOne.en"):
        INPUTCORPUS = CWD+Data_path_Prefix+"/EngText.en"
    else:
        INPUTCORPUS = CWD+Data_path_Prefix+"/EngText.en"

    INPUTQUERY = None
    if os.path.exists(CWD+Data_path_Prefix+"/NGQuery.pa"):
        INPUTQUERY = CWD+Data_path_Prefix+"/NGQuery.pa"
    elif os.path.exists(CWD+Data_path_Prefix+"/PunjText.pa"):
        INPUTQUERY = CWD+Data_path_Prefix+"/PunjText.pa"

    CleanningData(INPUTQUERY)

# tempStatement for eng sentence tokenize
    EngTokenize(INPUTCORPUS)
  # tempStatement for eng sentence tokenize

    TranslateSentences(Data_path_Prefix)

    # reading data from file
    print(">>>>>>>>>>>>:", INPUTCORPUS)
    with open(INPUTCORPUS, "r", encoding='utf-8') as sourceDoc:
        CourpusData = sourceDoc.readlines()
        print(">>>>>>>", len(CourpusData))

    with open(CWD+Data_path_Prefix+"/LangOne.en", "r", encoding='utf-8') as sourceDoc:
        InputQueryData = sourceDoc.readlines()

    with open(INPUTQUERY, "r", encoding='utf-8') as sourceDoc:
        OriginalInputData = sourceDoc.readlines()

    # removing unwanted chars from converting into string and storing in list obj
    for d in CourpusData:
        d = d.lower()
        temp = "".join(d.split('\n'))  # conveting list to string
        if temp.strip() != '':
            AllCorpus.append(temp)

    tempTdata = []
    for d in InputQueryData:
        d = d.lower()
        temp = "".join(d.split('\n'))  # conveting list to string
        tempTdata.append(temp)

    InputQueryData.clear()
    InputQueryData = tempTdata

    tempTdata = []
    for d in OriginalInputData:
        d = d.lower()
        temp = "".join(d.split('\n'))  # conveting list to string
        tempTdata.append(temp)

    OriginalInputData = tempTdata
    # needed OriginalInputData
    del tempTdata

        
    return AllCorpus, InputQueryData, OriginalInputData


#Phase1()
