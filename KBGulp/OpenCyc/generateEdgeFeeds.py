from RoboBrainClient.RoboBrainAPI import RoboBrainAPI
import json
import re
import glob
import pprint
import threading
import Queue

RoboAPIUserName = 'Robot Learning Member'
RoboAPIPass = 'mYBW7C9rcsu9A3te2EeQSj5E'
S3KEY = 'AKIAJZIFU5A3XG5W2VFA'
S3SECRET = 'tsuJKDeMOtIpVJmv8jrOo5EC04iSIU/zXB8Y40a/'

URL = "http://test.robobrain.me:3000/api/feeds/"
#Please change your user name
userHandle = 'hcaseyal'

# Login to API
rC = RoboBrainAPI(RoboAPIUserName ,RoboAPIPass,S3KEY,S3SECRET,userHandle)

#Get the text friendly version of the predicate
def getPredicate(pred):
	if pred == 'is_type_of':
		return 'is a type of'
	elif pred == 'is_hyponym_of':
		return 'is an example of'
	elif pred == 'same_synset':
		return 'is a synonym of'
	elif pred == 'has_description':
		return ':'

def addFeedToApi(q):
	while True:
		rC.addFeed(q.get());
		q.task_done()

#Populate feeds
#apiLock = threading.Lock()
count = 0;
A = glob.glob('*.txt')
Dicti = {}

for f in A:
	F = json.load(open(f,'r'))
	for D in F:
		typeT  = 'OpenCyc'
		text = '#'+D['Subject']+' '+getPredicate(D['Pred'])+' #'+D['Object']+'.'
		#split desc into every word, each is a keyword
		keywords = [D['subUri']] + D['subDesc'].split() + [D['objUri']]  + D['objDesc'].split()
		source_text = 'OpenCyc'
		source_url = 'http://sw.opencyc.org'
		mediamap = []
		mediaShow = []
		mediatype = []
		graphStructure = [D['Pred']+": #0 ->#1"]
		media = []
		data = {'feedtype':typeT,'text':text,'media':media,'mediatype':mediatype,'graphStructure':graphStructure,'mediashow':mediaShow,'keywords':keywords,'mediamap':mediamap,'source_text':source_text,'source_url':source_url}
		rC.addFeed(data);
		#pprint.pprint(data)
		count = count+1;

#Push Everything
print(count);
rC.push2Brain(URL)
