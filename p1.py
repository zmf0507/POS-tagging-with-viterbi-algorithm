
import pickle

viterbi= {}

def initialisebackTrackMatrix(words):
	tagSet = ["start"] + list(tagFreq) + ["end"]

	for tag in tagSet:
		backTracking[tag] = {}
	for tag in tagSet:
		for word in words:			
			backTracking[tag][word] = " "

def initialiseViterbiMatrix(words):
	tagSet = ["start"] + list(tagFreq) + ["end"]

	for tag in tagSet:
		viterbi[tag] = {}
	for tag in tagSet:
		for word in words:			
			viterbi[tag][word] = 0 	

def loadFromPickle(pickleFile):
	file = open(pickleFile,'rb')
	pickleData = pickle.load(file)
	file.close()
	return pickleData

def getAllStartTagsFreq():
	freqSum = 0
	for tag in startTagFreq:
		freqSum+=startTagFreq[tag]
	return freqSum

def getAllEndTagsFreq():
	freqSum = 0
	for tag in endTagFreq:
		freqSum+=endTagFreq[tag]
	return freqSum		

def getEndStateMaxProbability(word):
	tagSet = list(tagFreq)
	max = 0
	maxTag = " "
	for i,tag in enumerate(tagSet):
		prob = viterbi[tag][word]*endProbability(tag)
		if(max < prob):
			max = prob
			maxTag = tag
	return max,maxTag		

def startProbability(tag):
	if(tag in startTagFreq):
		freq = startTagFreq[tag]
		allTagsFreq = getAllStartTagsFreq()	
		return (float(freq))/(float(allTagsFreq))
	else :	
		return 0

def endProbability(tag):
	if(tag in endTagFreq):
		freq = endTagFreq[tag]
		allTagsFreq = getAllEndTagsFreq()	
		return float(freq)/float(allTagsFreq)
	else :		
		return 0	
		
def observationProbability(tag, word):
	if(word in wordTagFreq[tag]):
		freq = wordTagFreq[tag][word]
		prob = float(freq+1)/float(tagFreq[tag]+1)
	else:
		prob = float(1)/float(tagFreq[tag]+1)
	return prob

def transitionProbability(tagi, tagj):
	if(tagj in bigramTagFreq[tagi]):
		prob = float(bigramTagFreq[tagi][tagj])/float(tagFreq[tagi])
	else:
		prob = 0	
	return prob


def viterbiAlgo(words, tags):
	N = len(tags) +2
	T = len(words)
	# print("f")
	# viterbi= {}
	tagSequence = []
	tagSet = list(tags)

	for j,tag in enumerate(tagSet):
		viterbi[tag][words[0]] = startProbability(tag)*observationProbability(tag, words[0])
		backTracking[tagSet[j]][words[0]] = "start"
	# slicedWords = words[1:]

	for t, word in enumerate(words):
		if(t>0):
			for j,tag in enumerate(tagSet):
				max = 0
				maxTag = " "
				prevTagSet = tagSet
				for i, prevTag in enumerate(prevTagSet):
					prob = viterbi[prevTagSet[i]][words[t-1]]*transitionProbability(prevTagSet[i],tagSet[j])
					if(max < prob):
						max = prob
						maxTag = prevTagSet[i]		
				viterbi[tagSet[j]][words[t]]=max*observationProbability(tagSet[j], words[t])	 
				backTracking[tagSet[j]][words[t]] = maxTag
	
	viterbi["end"][words[-1]], maxTag = getEndStateMaxProbability(words[-1])
	
	backTracking["end"][words[-1]] = maxTag			
	return maxTag
				


def getTagsCount():
	tags = loadFromPickle("tagFreq")
	return len(tags)		


startTagFreq = loadFromPickle("startTagFreq")
endTagFreq = loadFromPickle("endTagFreq")
bigramTagFreq = loadFromPickle("bigramTagFreq")
tagFreq = loadFromPickle("tagFreq")
wordTagFreq = loadFromPickle("wordTagFreq")

inputFile = open("decodingHMM.txt", "r")
input = inputFile.read()
sentences = input.split("\n\n")
for s in sentences:
	words = s.split('\n')
	viterbi = {}
	backTracking = {}
	initialisebackTrackMatrix(words)
	initialiseViterbiMatrix(words)
	maxTag = viterbiAlgo(words, tagFreq)
	# print(maxTag)
	tagSequence = []
	tagSequence.append(maxTag)

	newWords = words[::-1]
	for i,word in enumerate(newWords):
			maxTag = backTracking[maxTag][word]
			tagSequence.append(maxTag)

	# print(viterbi["end"][words[-1]])	
	# print(backTracking["end"][words[-1]])
	tagSequence = tagSequence[::-1]
	tagSequence = tagSequence[1:-1]
	for i,tag in enumerate(tagSequence):
		print(words[i],"	", tag)
	print(".	.")	
	print("-----------------")	
