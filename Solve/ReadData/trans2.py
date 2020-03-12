import codecs
import requests
from googletrans import Translator
import os.path
import time
import sys


def Translate(Data_path_Prefix):
    CWD = os.getcwd()
    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.in',
    ])

    INPUTFILE = None
    OUTPUTFILE = CWD+Data_path_Prefix+"/LangOne.en"

    if os.path.exists(OUTPUTFILE) == True:
        print("\033[1;31m \nTranslated File is Already Present", OUTPUTFILE)
        time.sleep(1)
        #print("Press Enter")
        return False

    if os.path.exists(CWD+Data_path_Prefix+"/NGQuery.pa"):
        INPUTFILE = CWD+Data_path_Prefix+"/NGQuery.pa"
    elif os.path.exists(CWD+Data_path_Prefix+"/PunjText.pa"):
        INPUTFILE = CWD+Data_path_Prefix+"/PunjText.pa"

    f = codecs.open(INPUTFILE,  mode="r", encoding="utf8")
    d = codecs.open(OUTPUTFILE, mode="w", encoding="utf8")

    # engLines=engFileRead.readlines()
    NewInputSent = []

    count = 1

    for line in f:
        try:
            translations = translator.translate([line], src='pa', dest='en')
            # print(translations)
            for translation in translations:
                d.write(translation.text)
                #print(translation.text)
                d.write('\n')
            print("Translated", count)
            NewInputSent.append(line)
            count = count+1
        except Exception as e:
            #pass
            print("Error at Line:", count,e)
            #count += 1
    print('done: ', count)

    f.close()
    d.close()

    print("INPUTFILE========>",len(NewInputSent))
    d = codecs.open(INPUTFILE, mode="w", encoding="utf8")
    d.writelines(NewInputSent)
    d.close()