from __future__ import division
from sklearn import svm
import os.path
import numpy
import nltk
import re
mainDirectory = './nyu/PROJECTS/Epicurious/DATA/ingredients'
instr_directory = './nyu_instr/PROJECTS/Epicurious/DATA/instructions'

'''
This is where we would reach each line of the file and then run a regex match on it to get all the words before
the first tab. (these are the names of the ingredients. Some of them may have adjectives like fresh, peeled,cut etc.
	Not sure what to do about them yet.)
'''
_featureSet=[]
def getFileDetails(_filename,_fileDescriptor):
	stemmer = nltk.stem.porter.PorterStemmer()
	rankingRegexMatch = re.match('([0-9](?:\_)[0-9]?)', _filename)
	
	if len(rankingRegexMatch.group(0)) == 2:
		ranking = float(rankingRegexMatch.group(0)[0])
	else:
		ranking = float(rankingRegexMatch.group(0)[0]+'.'+rankingRegexMatch.group(0)[2])
	
	_keywords = []
	_features={}
	ingre=""
	lines=[]
	for line in _fileDescriptor:
		#print line
		lines.append(line)
		eachColumn = line.split("\t")
		checkOneword = eachColumn[0].split(" ")
		#print len(checkOneword[0]),len(eachColumn[0])
		if(len(checkOneword[0])== len(eachColumn[0])):
			ingre=eachColumn[0]
			ingre=ingre.lower()
			ingre = stemmer.stem_word(ingre)
			
		else:
			newSentence = "I have "+eachColumn[0]
			text=nltk.word_tokenize(newSentence)
			taggedIngredient = nltk.pos_tag(text)
			#print taggedIngredient
			for i in range(len(taggedIngredient)):
				"""
				Stemming and getting rid of brackets
				"""
				a=""
				b = taggedIngredient[i][0].lower()
				if i !=0:
					a = taggedIngredient[i-1][0].lower()
					a=re.sub(r'[^\w]', '', a)
					a = stemmer.stem_word(a)
					x =['larg','small','mediu']
					for z in x:
						if z in a:
							a='';

					
				
				b=re.sub(r'[^\w]', '', b)
			
				b = stemmer.stem_word(b)

				if taggedIngredient[i][1] =="NNS" and taggedIngredient[i-1][1] =="NN":

					ingre= a+b
					#print ingre
				elif taggedIngredient[i-1][1] =="JJ" and taggedIngredient[i][1] =="NN":
					ingre= a+b
					#print ingre
				elif taggedIngredient[i-1][1] =="VBN" and taggedIngredient[i][1] =="NN":
					ingre= a+b
				elif taggedIngredient[i-1][1] =="VBN" and taggedIngredient[i][1] =="NNS":
					ingre= a+b
				elif taggedIngredient[i-1][1] =="JJ" and taggedIngredient[i][1] =="NNS":
					ingre= a+b
				elif taggedIngredient[i-1][1] =="JJS" and taggedIngredient[i][1] =="NN":
					ingre= a+b
				elif taggedIngredient[i-1][1] =="JJS" and taggedIngredient[i][1] =="NNS":
					ingre= a+b				
				elif taggedIngredient[i-1][1] =="NN" and taggedIngredient[i-1][1] =="NN":
					ingre= a+b
				elif  taggedIngredient[i][1] =="NN":
			
					ingre= b
				elif  taggedIngredient[i][1] =="NNS":
					ingre= b
				
			#print ingre
		
		
		#print ingre
		
		_features[ingre]=1
		if ingre not in _featureSet and ingre !='':
			_featureSet.append(ingre)
			
		
	#print _features,len(_features)
	
		
		

	return [_features,ranking]

'''
Open each file in the directory and pass the name and file descriptor to getFileDetails
'''
def this_is_it(files):
    _allKeywords = []
    _allRankings = []
    ingredient = open('ingredients.txt', 'w')
    rating = open('ratings.txt','w')
    i=0
    flag =0
    for eachFile in files:
        fullFilePath = mainDirectory + '/' + eachFile
        f = open(fullFilePath)
        XandYForThisFile = getFileDetails(eachFile,f)
	
        _allKeywords.append(XandYForThisFile[0])
        _allRankings.append(XandYForThisFile[1])
	"""
	if flag == 0 :
	
            for eachIngredient in XandYForThisFile[0]:
                ingredient.write(str(eachIngredient))
                ingredient.write("\t")
                        
            if(len(XandYForThisFile[0])==0):
                ingredient.write("null\t")
            ingredient.write("\n")
            rating.write(str(XandYForThisFile[1]))
            rating.write("\n")
            flag=1

        elif flag == 1:
            flag=2
        else :
            flag=0
	"""
	print i
	ingredient.write(str(XandYForThisFile[0]))
	i=i+1
	if i == 100:
		break;
	
        
    ingredient.close()
    rating.close()
    	#_allKeywords = numpy.asarray(_allKeywords,dtype=object)
    	#_allRankings = numpy.asarray(_allRankings)
	#svm_learning(_allKeywords,_allRankings)
	#return _allKeywords, _allRankings


def read_instructions_from_file(_filename,_fileDescriptor):
	stemmer = nltk.stem.porter.PorterStemmer()
	for line in _fileDescriptor:
		if(line):
			tokens = nltk.word_tokenize(line)
			tag_array = nltk.pos_tag(tokens)
			for (word,tag) in tag_array:
				if(tag == 'VBN' or tag == 'VBG' or tag == 'VB'):
					print word,tag,stemmer.stem(word)
		

def for_instructions(files):
	for eachFile in files:
		fullFilePath = instr_directory + '/' + eachFile
		f = open(fullFilePath)
		read_instructions_from_file(eachFile,f)

def svm_learning(x,y):
	clf = svm.SVC()
	clf.fit(x,y)


def print_files( x, dir_path , files ):
	x(files)
'''
code starts here
'''
def parse():
        #os.path.walk(mainDirectory, print_files, this_is_it)
        os.path.walk(instr_directory,print_files,for_instructions)
        #return _allKeywords, _allRankings

def main():
	parse()
if __name__ == '__main__':
	main()
