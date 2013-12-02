'''
Project for B-659.
Author: Chaitanya Bilgikar (cbilgika@indiana.edu)
'''
from __future__ import division
from sklearn import svm
import os.path
import numpy

import re

'''
The stanford-postagger was included to see how it tags the words and to see if it would help in getting just the names
of the ingredients. Turns out its pointless.
'''
#from nltk.tag.stanford import POSTagger
mainDirectory = './nyu/PROJECTS/Epicurious/DATA/ingredients'
#st = POSTagger('/usr/share/stanford-postagger/models/english-bidirectional-distsim.tagger','/usr/share/stanford-postagger/stanford-postagger.jar')

'''
This is where we would reach each line of the file and then run a regex match on it to get all the words before
the first tab. (these are the names of the ingredients. Some of them may have adjectives like fresh, peeled,cut etc.
	Not sure what to do about them yet.)
'''
def getFileDetails(_filename,_fileDescriptor):
	rankingRegexMatch = re.match('([0-9](?:\_)[0-9]?)', _filename)
	
	if len(rankingRegexMatch.group(0)) == 2:
		ranking = float(rankingRegexMatch.group(0)[0])
	else:
		ranking = float(rankingRegexMatch.group(0)[0]+'.'+rankingRegexMatch.group(0)[2])
	
	_keywords = []
	for line in _fileDescriptor:
		m = re.match('(\w+\s*\w*)(?=\t[0-9])', line)
		if m:
			_keywords.append(m.group(0))

	return [_keywords,ranking]

'''
Open each file in the directory and pass the name and file descriptor to getFileDetails
'''
def this_is_it(files):
	_allKeywords = []
	_allRankings = []
	for eachFile in files:
		fullFilePath = mainDirectory + '/' + eachFile
		f = open(fullFilePath)
		XandYForThisFile = getFileDetails(eachFile,f)
		_allKeywords.append(XandYForThisFile[0])
		_allRankings.append(XandYForThisFile[1])
	_allKeywords = numpy.asarray(_allKeywords,dtype=object)
	_allRankings = numpy.asarray(_allRankings)
	svm_learning(_allKeywords,_allRankings)



def svm_learning(x,y):
	clf = svm.SVC()
	clf.fit(x,y)
'''
This just prints the directory path and then calls the callback x on files
'''
def print_files( x, dir_path , files ):
	print dir_path
	x(files)
'''
code starts here
'''
os.path.walk(mainDirectory, print_files, this_is_it)