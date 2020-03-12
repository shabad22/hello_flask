import codecs
import requests
from googletrans import Translator
from google.cloud import translate
import os.path
import time
import sys


def Translate2():
    client = translate.Client()
    text = u'Hello, world!'
    target = 'en'

    translation = translate_client.translate(text, target_language=target)
    
    print(u'Translation: {}'.format(translation['translatedText']))


def Translate():
    CWD = os.getcwd()
    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.in',
    ])

    INPUTFILE = None
    OUTPUTFILE = CWD+"/Data/LangOne.en"

    if os.path.exists(OUTPUTFILE) == True:
        print("\033[1;31m \nTranslated File is Already Present", OUTPUTFILE)
        time.sleep(1)
        print("Press Enter")
        return False

    if os.path.exists(CWD+"/Data/NGQuery.pa"):
        INPUTFILE = CWD+"/Data/NGQuery.pa"
    elif os.path.exists("./Data/PunjText.pa"):
        INPUTFILE = CWD+"/Data/PunjText.pa"

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
                print(translation.text)
                d.write('\n')
            print("Translated", count)
            NewInputSent.append(line)
            count = count+1
        except Exception as e:
            # pass
            print("Error at Line:", count, e)
            #count += 1
    print('done: ', count)

    f.close()
    d.close()

    d = codecs.open(INPUTFILE, mode="w", encoding="utf8")
    d.writelines(NewInputSent)
    d.close()
