import functions
import numpy as np
import string
import os

if not os.path.exists('./data/engWordDict.npy'):
	print('First model needs to be trained')
	choice = str(input('Do you want to train? Y:N\n'))
	
	if(choice == 'Y'):
		functions.train()
	else:
		print('Good Bye')
		raise
	

# loading dictionaries and model
	engDict = np.load('./data/engWordDict.npy').item()
	print('English Dictionary loaded')
	fnDict = np.load('./data/fnWordDict.npy').item()
	print('Dutch dictionary loaded')

	probDutToEng = np.load('./data/IBM_Model_dut_to_eng.npy')
	print('Dutch to English model loaded')

	probEngToDut = np.load('./data/IBM_Model_eng_to_dut.npy')
	print('English to Dutch model loaded')


# creating a mapping of all eng to foreign language
maxIds = probDutToEng.argmax(axis=1)
mappingDutToEng = dict()
for i in fnDict:
    mappingDutToEng[i] = maxIds[fnDict[i]]
print('Mapping from dutch to english created')

maxIds = probEngToDut.argmax(axis=1)
mappingEngToDut = dict()
for i in engDict:
    mappingEngToDut[i] = maxIds[engDict[i]]
print('Mapping from english to dutch created')


# function to translate Dutch sentence to English
def translateDutToEng(st):
	st = functions.processSentence(st)
	tk = st.split()
	ans = ""
	for t in tk:
		try:
			ans += functions.getItem(engDict,mappingDutToEng[t]) + " "
		except:
			print('Key Error',t)
			continue
	ans = ans.strip()
	return ans
# function to translate English sentence to Dutch
def translateEngToDut(st):
	st = functions.processSentence(st)
	tk = st.split()
	ans = ""
	for t in tk:
		try:	
			ans += functions.getItem(fnDict,mappingEngToDut[t]) + " "
		except:
			print('Key Error')
			continue
	ans = ans.strip()
	return ans


# driver starts from here
print()
print()
print("------Namaste!!-------")
print("Welcome to Aapka apna Google Trasnslate for Dutch and English")

cnt = 0
sumJacCoeff = 0
sumCosCoeff = 0

while(True):
	print()
	print()
	print('Please select an option and enter the corresponding number')
	print('1. Translate the document')
	print('2. Calculate Jaccard Coefficient and Cosine Similarity of the Document')
	print('3. Show the average of Jaccard Coefficient and Cosine Similarity')
	print('9. To exit')

	choice = int(input())

	if(choice == 1): # translating document

		path = input('Please specify the path of file to be translated relative to this directory\n')
		lang = int(input('Please tell the language of the document\n1. English\n2. Dutch\n'))
		
		# read file and their sentences
		try:
			fi = open(path)
		except:
			print("File not found at specified location")
			continue
		data = fi.readlines()
	
		res = list()		

		if(lang == 1):
			for st in data:
				#print(translateEngToDut(st))
				res.append(translateEngToDut(st))
		elif(lang == 2):
				#print(translateDutToEng(st))
			for st in data:
				res.append(translateDutToEng(st))
		else:
			print('Invalid choice')
		
		with open('result.txt', 'w') as f:
			f.writelines("%s\n" % it for it in res)
		
		print('Please check result file for translation')
		print()

	elif(choice == 2): # printing Jaccard Coefficient and Cosine Similarity
		cnt += 1
		
		pathFn = input('Please specify the path of foreign file to be translated relative to this directory\n')
		try:
			fiFn = open(pathFn)
		except:
			print("File not found at specified location")
			continue
		lang = int(input('Please tell the language of the file to be translated\n1. English\n2. Dutch\n'))
		pathEn = input('Please specify the path of original translated file relative to this directory\n')
		try:
			fiEn = open(pathEn)
		except:
			print("File not found at specified location")
			continue
		
	
		dataFn = fiFn.readlines()
		resFn = ""
		if(lang == 1):
			for st in dataFn:
				#print(translateEngToDut(st))
				resFn += translateEngToDut(st)
				resFn += " "
		elif(lang == 2):
				#print(translateDutToEng(st))
			for st in dataFn:
				resFn += translateDutToEng(st)
				resFn += " "
		else:
			print('Invalid choice')

		dataEn = fiEn.read()
		dataEn = dataEn.translate({ord('\n'):' '})
		resEn = functions.processSentence(dataEn)
		
		jac = functions.jaccCoeff(resEn,resFn)
		print('Jaccard Coefficient: ', jac)
		sumJacCoeff += jac 
		
		cos = functions.cosDistance(resEn,resFn)
		print('Cosine similarity: ', cos)
		sumCosCoeff += cos
		
		print()
		print(resFn)
		print()
		print(resEn)		

	elif(choice == 3): # printing average Jaccard Coefficient and Cosine Similarity
		print('Till now Jaccard Coefficient and Cosine Similarity have been calculated for '+str(cnt)+' documents.')
		print('Average Jaccard Coefficient: ' + str(sumJacCoeff/cnt))	
		print('Average Cosine Similarity: ' + str(sumCosCoeff/cnt))		

	elif(choice == 9):
		print('Thank You')
		print('Bye')
		break
	
	else:

		print('Invalid Choice')
