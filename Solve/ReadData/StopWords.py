def loadStopWords():
    """ Funtion will read stopword file and return list of stopwords \n 
            \n Return [" "," ", . .]"""
    StopWords=[]
    #reading Stopwords from file
    with open("StopWords.en","r") as sourceDoc:
        StopWords = sourceDoc.readlines()    

    #cleaing data
    templist=[]
    for word in StopWords:
        templist.append(word.replace('\n','',1))

    StopWords=templist
    del templist
    return StopWords


def RemoveStopWords(docs,StopWords):
    NewList=[]
    """ remove stop from all docs  \n Accept [ [], [] ]   Return [ [],[] ]"""
    for doc in docs:
        l = doc.split()
        for sw in StopWords:
            for w in l:
                if w == sw:
                    l.remove(sw)
        doc = " ".join(l)
        NewList.append(doc)
    return NewList