'''
Project for B-659.
Author: Chaitanya Bilgikar (cbilgika@indiana.edu)
'''

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
	ranking = _filename[0]
	for line in _fileDescriptor:
		#print st.tag(line.split())
		print re.match('(\w\s\w+)(\s+.*)', line)

'''
Open each file in the directory and pass the name and file descriptor to getFileDetails
'''
def this_is_it(files):
	for eachFile in files:
		fullFilePath = mainDirectory + '/' + eachFile
		f = open(fullFilePath)
		getFileDetails(eachFile,f)

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



