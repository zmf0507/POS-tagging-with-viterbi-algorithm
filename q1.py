
import pickle

bigramTagFreq = {}
tagFreq = {}
wordTagFreq = {}
startTagFreq = {}
endTagFreq = {}


def loadFromPickle(pickleFile):
	file = open(pickleFile,'rb')
	pickleData = pickle.load(file)
	file.close()
	return pickleData

def saveInPickle(data, pickleFile):
	file = open(pickleFile,"wb")
	pickle.dump(data,file)
	file.close()


def countTag(tag):
	if(tag in tagFreq):
			tagFreq[tag]+=1
	else:
			tagFreq[tag] = 0

def countStateBigram(currentTag, previousTag):
	if(previousTag != "" or currentTag != ""):
		if(previousTag not in bigramTagFreq):
			bigramTagFreq[previousTag] = {}
		if(currentTag not in bigramTagFreq[previousTag]):
			bigramTagFreq[previousTag][currentTag] = 0
		bigramTagFreq[previousTag][currentTag] += 1	

def countStateObservation(word, tag):
		if(tag != ""):
			if(tag not in wordTagFreq):
				wordTagFreq[tag] = {}
			if(word not in wordTagFreq[tag]):
				wordTagFreq[tag][word] = 0
			wordTagFreq[tag][word] += 1	

def countStartTag(currentTag, previousTag):
	if(previousTag == "."):
		if(currentTag in startTagFreq):
			startTagFreq[currentTag]+=1
		else:
			startTagFreq[currentTag] = 0

def countEndTag(currentTag, previousTag):
	if(currentTag == "."):
		if(previousTag in endTagFreq):
			endTagFreq[previousTag]+=1
		else:
			endTagFreq[previousTag] = 0			


previousTag = "."
file = open('TrainingsetHMM.txt','r')
lines = file.read()
lines = lines.split("\n")
for line in lines:

	if(line!=""):
		lineList = line.split("\t")
		currentWord =  lineList[0]
		currentTag = lineList[1]
		countTag(currentTag)
		countStateBigram(currentTag, previousTag)
		countStateObservation(currentWord, currentTag)
		countStartTag(currentTag, previousTag)
		countEndTag(currentTag, previousTag)
		previousTag = currentTag

	# if()
	# print(lineList)


# print(list(tagFreq))
# print(len(list(tagFreq)))
# print(bigramTagFreq["PRP"]["MD"])
print(wordTagFreq["NN"]["i"])
# print(startTagFreq)
# print(endTagFreq)

saveInPickle(tagFreq, "tagFreq")
saveInPickle(bigramTagFreq, "bigramTagFreq")
saveInPickle(wordTagFreq, "wordTagFreq")
saveInPickle(startTagFreq, "startTagFreq")
saveInPickle(endTagFreq, "endTagFreq")