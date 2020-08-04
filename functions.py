import numpy as np
import string 
import math
from collections import Counter

# function to remove punctuation and other symbols from document
def processSentence(st):
    inp = [ord(char) for char in string.punctuation]
    out = [None for i in inp]
    transTable = dict(zip(inp,out))

    st = st.translate(transTable)
    st = st.lower()    
    return st

# function to create a dictionary of all unique words in training set
def wordDict(listData):
    newData = list()
    wDict = {}
    cnt  = 0
    
    for it in listData:

        it = processSentence(it)
        tk = it.split()
        
        newIt = ""
        for t in tk:
            if t in wDict:
                newIt += t + " "
            else:
                wDict[t] = cnt
                cnt += 1
                newIt += t + " "
        newIt = newIt.strip()
        newData.append(newIt)
    
    return newData, wDict


# Implementation of IBM Model 1
def trainModel(engData,fnData,engDict,fnDict):
	engNum = len(engDict)
	fnNum = len(fnDict)

	prob = np.ones((fnNum,engNum),dtype='float64')/engNum

	for it in range(50):
		count = np.zeros((fnNum,engNum))

		total = np.zeros(fnNum)
		s_total = dict()

		for i in range(len(engData)):
			e = engData[i].split()
			for j in e:
			    ei = engDict[j]
			    s_total[j] = 0
			    f = fnData[i].split()
			    for k in f:
			        fi = fnDict[k]

			        s_total[j] += prob[fi,ei]

			for j in e:
			    ei = engDict[j]
			    f = fnData[i].split()
			    for k in f:
			        fi = fnDict[k]

			        count[fi,ei] += prob[fi,ei]/s_total[j]
			        total[fi] += prob[fi,ei]/s_total[j]
		
		prob = np.copy(count)
		total = np.reshape(total,(total.shape[0],1))
		prob = prob/total		
		
		print(it)
		
	prob = np.round(prob, decimals=3)
	print('Model Trained')

	return prob


def getItem(dc,val):
    for key,v in dc.items():
        if(val == v):
            return key
    print('value not in dict')
    return 'ERR'

# function to calculate jaccard coefficient
def jaccCoeff(ori,trans):
    
	tkOri = ori.split()
	tkTrans = trans.split()

	sOri = set(tkOri)
	sTrans = set(tkTrans)

	ans = len(sOri & sTrans)/len(sOri | sTrans)
	return ans


def textToVector(text):
	words = text.split()
	tp = Counter(words)
	for key,val in tp.items():
		tp[key] = 1+math.log10(val)
	return tp
	
# function to calculate cosine similarity
def cosDistance(ori, trans):

	v1 = textToVector(ori)
	v2 = textToVector(trans)

	common = set(v1.keys()) & set(v2.keys())  # return set with elements in intersection
	numerator = sum([v1[x] * v2[x] for x in common])

	sum1 = sum([v1[x] ** 2 for x in v1.keys()])
	sum2 = sum([v2[x] ** 2 for x in v2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if denominator:
		return float(numerator) / denominator
	else:
		return 0.0

# function to train models and create dictionaries
def train():
	f_en = open('./data/english.txt')
	engData = f_en.readlines()
	f_fn = open('./data/dutch.txt')
	fnData = f_fn.readlines()

	engData , engDict =  wordDict(engData)
	np.save("data/engWordDict",engDict)

	fnData , fnDict = wordDict(fnData)
	np.save("data/fnWordDict",fnDict)

	probDutToEng = trainModel(engData,fnData,engDict,fnDict)
	np.save('data/IBM_Model_dut_to_eng',probDutToEng)

	probEngToDut = train(fnData,engData,fnDict,engDict)
	np.save('data/IBM_Model_eng_to_dut',probEngToDut)
	
	print('model and dictionaries saved')
