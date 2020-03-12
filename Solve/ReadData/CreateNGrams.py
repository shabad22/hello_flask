import sys
# usage
# python3 CreateNGrams.py InputFileName OutputFileName

#pylint: disable=E1101
# reading data from file
print("\n\033[1;37m")

inputFile = None
outputFile = None

try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
except:
    print("\nInput File Command is Not Correct")
    sys.exit()

with open(inputFile, "r", encoding='utf-8') as sourceDoc:
    data = sourceDoc.readlines()


def CreateNGram(tokens, limit):
    tempLimit = limit
    ngram = ""
    i = 0
    j = 0
    NewNgram = []
    for i in range(len(tokens)-1):
        for j in range(i, limit):
            ngram += tokens[j] + " "
            if j == limit-1:
                NewNgram.append(ngram.strip())
                limit += tempLimit
                ngram = ""
                break
            elif (j == len(tokens)-1):
                NewNgram.append(ngram.strip())
                ngram = ""
                break
            elif len(ngram.strip().split()) == tempLimit:
                NewNgram.append(ngram.strip())
                ngram = ""
                break

    return NewNgram


print("Creating Phrases...")
of = open(outputFile, "w+", encoding='utf-8')
totalNgram = 0
for line in data:
    tokens = line.split()
    ngram = CreateNGram(tokens, 20)
    totalNgram += len(ngram)
    for line in ngram:
        of.write(line+"\n")

print("Total Phrases:", totalNgram)
print("\n\033[1;32m output is saved in ", outputFile)
