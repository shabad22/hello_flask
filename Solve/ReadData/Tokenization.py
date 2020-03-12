import re
import os


def CreateSentences(PATH):
    # print("CreateSentences()>>>>>>>>>>>>>>>>>>>>>>>>",PATH)
    with open(PATH, "r", encoding='utf-8') as sourceDoc:
        Ptext = sourceDoc.read()

    Ptext = re.sub("[?]", " ? END", Ptext)
    Ptext = re.sub("[।] [\"]", "। END", Ptext)
    Ptext = re.sub("[।]", "। END", Ptext)
    Ptext = re.sub("[|]", "| END", Ptext)
    Ptext = re.sub("[\n]", " END", Ptext)
    Ptext = re.sub("\r\n", " END", Ptext)
    Sen = re.split("END", Ptext)

    CreateNewFile(Sen, PATH)

    print("Tokenization Completed")


def CreateNewFile(ListSen, PATH):
    CWD = os.getcwd()
    print("CreateNewFile()>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", len(ListSen))

    of = open(PATH, 'w', encoding='utf-8')
    of.truncate()

    LineCount = 0
    for line in ListSen:
        if len(line.strip()) > 1:
            print("LINECOUNT->", LineCount)
            line = WordToken(line)
            of.write(line.strip()+"\n")
            LineCount += 1
        if LineCount >= 13:
            break
       
    of.close()


def WordToken(line):
    line = re.sub(r"(')(\w+)(')", r" \1 \2 \3 ", line)
    line = re.sub(r'[.?!]$', ' .', line)
    line = re.sub(r'[)]', ' ) ', line)
    line = re.sub(r'[(]', ' ( ', line)
    line = re.sub(r'["]', ' " ', line)
    line = re.sub(r'[“]', ' “ ', line)
    line = re.sub(r'[!]', ' ! ', line)
    line = re.sub(r',[^\d\w]', ' , ', line)
    line = re.sub(r'[,]', ' , ', line)
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'[-]', ' - ', line)

    return line
