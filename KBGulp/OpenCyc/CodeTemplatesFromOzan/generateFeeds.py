from RoboBrainClient.RoboBrainAPI import RoboBrainAPI
import json

import re
import glob
import pprint


RoboAPIUserName = 'RobotLearningMember'
RoboAPIPass = 'mYBW7C9rcsu9A3te2EeQSj5E'
S3KEY = 'AKIAJZIFU5A3XG5W2VFA'
S3SECRET = 'tsuJKDeMOtIpVJmv8jrOo5EC04iSIU/zXB8Y40a/'

URL = "http://test.robobrain.me:3000/api/feeds/"



POSES = ['','Standing','Sitting','Standing','Sitting','Standing','Sitting']

# Login to API
rC = RoboBrainAPI(RoboAPIUserName,RoboAPIPass,'AKIAJZIFU5A3XG5W2VFA','tsuJKDeMOtIpVJmv8jrOo5EC04iSIU/zXB8Y40a/','ozanSener')


#Populate feeds
A = glob.glob('*.jpg')
for f in A:
	#bName = f[0:-15]
	bName = f.split('_')[0]
	typeT  = 'Object Affordance'
	media1 = './images/'+bName+'_.jpg'
	fiel = f.split('_')
	heatID = int(fiel[1])
	pID = int(fiel[2][0:-4])
	text = 'The position of a #'+POSES[pID]+' human while using a #'+bName+' is distributed as #$heatmap_'+str(heatID)+'.' #subject predicate object
	keywords = ['Human','Affordance','Object',bName,POSES[pID]] #opencyc node description
	source_text = 'Hallucinating Humans'
	source_url = 'http://pr.cs.cornell.edu/hallucinatinghumans/' #opencyc url
	mediamap = ['#1','#0#1#2']
	mediaShow = ['True','True']
	mediatype = ['Image','Image']
	graphStructure = ["#spatially_distributed_as: #1 ->#2","#spatially_distributed_as: #0 ->#2","can_use: #0 ->#1"] #subject and object
	media = [media1,f]
	data = {'feedtype':typeT,'text':text,'media':media,'mediatype':mediatype,'graphStructure':graphStructure,'mediashow':mediaShow,'keywords':keywords,'mediamap':mediamap,'source_text':source_text,'source_url':source_url}
	pprint.pprint(data)
	#Add Feed to the API
	rC.addFeed(data)
#Push Everything
rC.push2Brain(URL)
