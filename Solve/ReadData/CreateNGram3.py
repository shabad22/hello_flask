import sys
import time

print("\n\033[1;37m")

NgramCount = 3

try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    NgramCount = int(sys.argv[3])
except:
    print("\nInput File Command is Not Correct")
    sys.exit()

# inputFile="./Data/QueryData.pa"
# outputFile="./Data/NGQuery.pa"

with open(inputFile, "r", encoding='utf-8') as sourceDoc:
    CourpusData = sourceDoc.readlines()

of = open(outputFile, "w+", encoding='utf-8')

print("Creating Phrases for:", inputFile)
time.sleep(2)

limit = 3

AllCorpus = []
for d in CourpusData:
    d = d.lower()
    temp = "".join(d.split('\n'))  # conveting list to string
    AllCorpus.append(temp)

tot = 0
for sent in AllCorpus:
    text = sent.split(' ')

    if (len(text) <= NgramCount):
        outstring = " ".join(text)
        if len(outstring) != 0:
            of.write(outstring+"\n")
            tot += 1
        continue

    for i in range(len(text)-(NgramCount-1)):
        nextW = currW = i
        nextW += 1
        WW = ""
        for ii in range(i, NgramCount+i):
            WW += text[ii]+" "
        # print(WW.strip())
        #WW = text[i]+" "+text[nextW]
        # print(WW)
        outstring = "".join(WW)
        if len(outstring) != 0:
            of.write(outstring+"\n")
            tot += 1

print("")
print("\033[1;32m", outputFile, "file contain Total Phrases:", tot)
