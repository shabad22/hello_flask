import sys
import time

print("\n\033[1;37m")
try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
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
    templist = []
    token = sent.split(' ')
    while len(token) > 0:
        ii = 0
        for ii in range(limit):
            if ii > len(token):
                # if len(token) == 1:
                #    temp = token.pop(0)
                #    templist.append(temp)
                break
            temp = token.pop(0)
            templist.append(temp)

        outstring = " ".join(templist)
        if len(token) == 1:
            outstring += " "+token.pop(0)
            # print(templist)
        if len(outstring) != 0:
            of.write(outstring+"\n")
            tot += 1
            #print("Total Phrases:", tot)
        templist = []

print("")
print("\033[1;32m", outputFile, "file contain Total Phrases:", tot)
