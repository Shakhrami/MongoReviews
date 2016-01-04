#?/usr/beqin/env python
from pymongo import MongoClient
import math

#Using cosine similarity, this will check to see how similar moview reviews are to
#each other. All the reviews are in a Mongo DB, and this just pulls a sample of six
#reviews, and a query, to match to each other. 

def makeIDFvector(cursor):
    unique = set()
    numOfDocsWithWord = {}
    for document in cursor:
        dic = document['review']
        for i in range(0, len(dic)):
            word = dic[i]['word']
            if(word in unique):
                numOfDocsWithWord[word] = numOfDocsWithWord[word] + 1
            else:
                unique.add(word)
                numOfDocsWithWord[word] = 1
    
    n = cursor.count()
    print("N = " + str(n))
    print("V = " + str(len(numOfDocsWithWord)))
    for word in numOfDocsWithWord:
        numOfDocsWithWord[word] = math.log(n/numOfDocsWithWord[word], 10)
      
    return numOfDocsWithWord

def makeTFvector(review, IDFvec):
    #ruturn a dictionary
    wordsInThisDoc = {}
    #make a dic of all words with count, then append words not in document that are in idf with value 0
    for i in range(0,len(review)):
        word = review[i]['word']
        wordsInThisDoc[word] = 1 + math.log(review[i]['count'], 10)
        
    for key in IDFvec:
        if(key not in wordsInThisDoc):
            wordsInThisDoc[key] = 0
    
    #make tf-idf weighted vector
    for key in wordsInThisDoc:
        wordsInThisDoc[key] = wordsInThisDoc[key] * IDFvec[key]
        
    return wordsInThisDoc
        
def cosSim(doc1, doc2):
    num = 0
    denom1 = 0
    denom2 = 0
    for key in doc1:
        num += doc1[key] * doc2[key]
        denom1 += doc1[key] * doc1[key]
        denom2 += doc2[key] * doc2[key]
    
    denom = math.sqrt(denom1) * math.sqrt(denom2)
    
    return num/denom
    
    

#Create a conecction
client = MongoClient()
db = client.cs336
collectionSplit =  db.unlabel_review_after_splitting

cursor = collectionSplit.find({}, {'id': 1, 'review': 1})
idfVector = makeIDFvector(cursor)


cursor2 = collectionSplit.find({}, {'id': 1, 'review': 1})

reviews = []
for document in cursor2[0:7]:
    reviews.append(document['review'])

rStar = makeTFvector(reviews[0], idfVector)
r1 = makeTFvector(reviews[1], idfVector)
r2 = makeTFvector(reviews[2], idfVector)
r3 = makeTFvector(reviews[3], idfVector)
r4 = makeTFvector(reviews[4], idfVector)
r5 = makeTFvector(reviews[5], idfVector)
r6 = makeTFvector(reviews[6], idfVector)
query = [{'count' : 1, 'word' : 'nurses'}, {'count':1, 'word' : 'women'}]
rQ = makeTFvector(query, idfVector)

print "cosSim(rStar, r1) = " + str(cosSim(rStar,r1))
print "cosSim(rStar, r2) = " + str(cosSim(rStar,r2))
print "cosSim(rStar, r3) = " + str(cosSim(rStar,r3))
print "cosSim(rStar, r4) = " + str(cosSim(rStar,r4))
print "cosSim(rStar, r5) = " + str(cosSim(rStar,r5))
print "cosSim(rStar, r6) = " + str(cosSim(rStar,r6))
print"**********************************************"
print "TF-IDF(nurses) = "  + str(rQ['nurses'])
print "TF-IDF(women) = " +  str(rQ['women'])
print "cosSim(rQ, rStar) = " + str(cosSim(rQ,rStar))
print "cosSim(rQ, r1) = " + str(cosSim(rQ,r1))
print "cosSim(rQ, r2) = " + str(cosSim(rQ,r2))
print "cosSim(rQ, r3) = " + str(cosSim(rQ,r3))
print "cosSim(rQ, r4) = " + str(cosSim(rQ,r4))
print "cosSim(rQ, r5) = " + str(cosSim(rQ,r5))
print "cosSim(rQ, r6) = " + str(cosSim(rQ,r6))

#Jason Schwartz aka JSON Schwartz
#CS336
#12/01/15









        
    